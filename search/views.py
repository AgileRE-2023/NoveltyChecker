import ast
from django.shortcuts import redirect, render
from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch
from elsapy.elsdoc import AbsDoc
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import nltk
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

from search.models import Manuscript

# nltk.download('stopwords')
# nltk.download('punkt')


def search(request):
    username = request.user.username
    if request.method == 'POST':
        query = request.POST.get('title')
        user_abstract = request.POST.get('abstract')
        
        

        if query == '' and user_abstract == '':
            return render(request, 'search/searchreport.html', {'error': 'Please fill all the fields'})
        else:
            print(query)
            scopus = SearchScopus(query)
            scopus.getScopusData(user_abstract)  
            scopus_id = scopus.dataId()
            scopus_title = scopus.dataTitle()
            scopus_abstract = scopus.dataAbstract()
            scopus_num_found = scopus.numFound()
            scopus_keyword_found = scopus.keywordFound()
            highest_similarity = scopus.highest_similarity_percentage()
            scopus_similarities = scopus.getAllSimilarity()
            scopus_message = scopus.message()  
            novelty_grade = scopus.noveltyGrade()
            api_response = scopus.getApi()
            
            # Print hasil ke konsol
            print("Scopus ID:", scopus_id)
            print("Title:", scopus_title)
            print("Abstract:", scopus_abstract)
            print("Number of results found:", scopus_num_found)
            print("Keyword found:", scopus_keyword_found)

            similarities = scopus.calculate_similarity_for_all(user_abstract)

            manuscript = Manuscript()
            manuscript.createManuscript(manuscript_title=query, manuscript_owner=request.user, manuscript_abstract=user_abstract, manuscript_api=api_response, novelty_score=novelty_grade, similarity_percentage=highest_similarity)
            manuscript.save()
            
            return render(request, 'search/searchreport.html', {'scopus_id': scopus_id, 'scopus_title': scopus_title, 'scopus_abstract': scopus_abstract, 'scopus_similarities': scopus_similarities, 'novelty_grade':novelty_grade, 'scopus_message':scopus_message, 'scopus_num_found': scopus_num_found, 'query': query, 'user_abstract': user_abstract, 'highest_similarity': highest_similarity, 'user': username, 'scopus_keyword_found': scopus_keyword_found, 'api_response': api_response, 'feedback_manuscript': manuscript})

    return render(request, 'search/searchpage.html', {'user': username})

def report(request):
    return render(request, 'search/searchreport.html')

def list(request):
    if request.method == 'POST':
        scopus_id = ast.literal_eval(request.POST.get('scopus_id'))
        scopus_title = ast.literal_eval(request.POST.get('scopus_title'))
        scopus_abstract = ast.literal_eval(request.POST.get('scopus_abstract'))
        scopus_num_found = request.POST.get('scopus_num_found')
        scopus_all = []
        scopus_similarities = ast.literal_eval(request.POST.get('scopus_similarities'))
    
        
        for i in range(min(10, len(scopus_id))):
            entry = {
                'scopus_id': scopus_id[i],
                'scopus_title': scopus_title[i],
                'scopus_similarities': scopus_similarities[i]
            }
            scopus_all.append(entry)

        return render(request, 'search/searchlist.html', {'scopus_all': scopus_all, 'scopus_num_found': scopus_num_found, 'scopus_similarities': scopus_similarities})
    
    elif request.method == 'GET':
        return render(request, 'search/searchlist.html')
    
class SearchScopus():
    con_file = open("config.json")
    config = json.load(con_file)
    con_file.close()
    query = ''
    keyword = ''
    num_found = ''
    keyword_found = ''
    scopus_id = []
    scopus_title = []
    scopus_abstract = []
    scopus_doi = []
    scopus_similarities = []
    novelty_grade = 0
    highest_similarity = 0
    scopus_message = ''
    api = ''

    client = ElsClient(config['apikey'])

    def __init__(self, query):
        self.query = query

    def getAbstract(self):
        for i in range(min(10, len(self.scopus_id))):
            scp_doc = AbsDoc(scp_id = self.scopus_id[i])
            if scp_doc.read(self.client):   
                self.scopus_abstract.append(scp_doc.data["coredata"]["dc:description"])
                # self.scopus_doi.append(scp_doc.data["coredata"]["prism:url"])
            else:
                print("Read document failed.")
        return self.scopus_abstract

    

    def calculate_similarity_for_all(self, user_abstract):
        if not self.scopus_abstract or not self.scopus_id:
            print("No abstract or ID available for similarity calculation.")
            return []
        stop_words = set(stopwords.words('english'))
        user_abstract_tokens = word_tokenize(user_abstract)

        user_abstract_filtered = [word.lower() for word in user_abstract_tokens if word.isalnum() and word.lower() not in stop_words]
        user_abstract_stemmed = [PorterStemmer().stem(word) for word in user_abstract_filtered]
        user_abstract_str = ' '.join(user_abstract_stemmed)
        # print(f"User Abstract filtered: {user_abstract_filtered}")
        # print(f"User Abstract: {user_abstract_stemmed}")
        

        api_similarities = []

        for idx, api_abstract in enumerate(self.scopus_abstract):
            api_abstract_tokens = word_tokenize(api_abstract)
            api_abstract_filtered = [word.lower() for word in api_abstract_tokens if word.isalnum() and word.lower() not in stop_words]
            api_abstract_stemmed = [PorterStemmer().stem(word) for word in api_abstract_filtered]
            api_abstract_str = ' '.join(api_abstract_stemmed)

            # # Debugging: Cetak isi dari user_abstract_str dan api_abstract_str
            # print(f"User Abstract: {user_abstract_str}")
            # print(f"API Abstract: {api_abstract_str}")

            # Calculate TF-IDF and cosine similarity
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform([user_abstract_str, api_abstract_str])
            similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
        

            similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
            
            # Convert similarity to percentage

            similarity_percentage = round(similarity_matrix[0][1] * 100, 1)
            self.scopus_similarities.append(similarity_percentage)
            # print(self.scopus_similarities)
            self.highest_similarity = self.highest_similarity_percentage()

        return self.scopus_similarities
    
    
    def highest_similarity_percentage(self):
        data = self.scopus_similarities
        highdata = data
        # highdata.sort(reverse=True)
        if len(highdata) > 0:
            self.highest_similarity = max(highdata)
        else:
            self.highest_similarity = 0       
        return self.highest_similarity

    
    
    def calculate_novelty(self, num_searched_titles, avg_similarity):
        
        if 6000 <= num_searched_titles or avg_similarity >= 12 or self.keyword_found > 10000000:
            self.novelty_grade = 1
            self.scopus_message = f"Nilai novelty 1 karena jurnal Anda memiliki {num_searched_titles} result found yang sama dan {self.keyword_found} keyword yang sama, terdapat similarity {self.highest_similarity}% yang sangat tinggi untuk jurnal baru."
        elif 100 <= num_searched_titles <= 6000 or avg_similarity >= 8 or self.keyword_found > 7000000:
            self.novelty_grade = 2
            self.scopus_message = f"Nilai novelty 2 karena jurnal Anda memiliki {num_searched_titles} result found yang sama dan {self.keyword_found} keyword yang sama, terdapat similarity {self.highest_similarity}% yang tinggi untuk jurnal baru."
        elif 5 <= num_searched_titles <= 100 or avg_similarity >= 5 or self.keyword_found > 5000000:
            self.novelty_grade = 3
            self.scopus_message = f"Nilai novelty 3 karena jurnal Anda memiliki {num_searched_titles} result found yang sama dan {self.keyword_found} keyword yang sama, terdapat similarity {self.highest_similarity}% yang cukup tinggi untuk jurnal baru."
        elif num_searched_titles < 5 or avg_similarity <= 3 or self.keyword_found < 1000000:
            self.novelty_grade = 4
            self.scopus_message = f"Nilai novelty 4 karena jurnal Anda memiliki {num_searched_titles} result found yang sama dan {self.keyword_found} keyword yang sama, terdapat similarity {self.highest_similarity}% yang rendah untuk jurnal baru."
        
        return self.novelty_grade, self.scopus_message

    
    
    def getScopusData(self, user_abstract):
        doc_srch = ElsSearch(self.query, 'scopus')
        doc_srch.execute(self.client, get_all=False)
        SearchScopus.extract_features(self)
        self.api = doc_srch.results
        self.num_found = doc_srch.tot_num_res
        key_srch = ElsSearch(self.keyword, 'scopus')
        key_srch.execute(self.client, get_all=False)
        self.keyword_found = key_srch.tot_num_res

        # Pastikan jumlah hasil pencarian memadai
        num_results = min(10, self.num_found)
        for i in range(num_results):
            scp_clear = doc_srch.results[i]['dc:identifier'].replace('SCOPUS_ID:', '')
            self.scopus_title.append(doc_srch.results[i]['dc:title'])
            self.scopus_id.append(scp_clear)
            
        self.scopus_abstract = []

        if num_results > 0:
            self.scopus_abstract = self.getAbstract()

            # Hitung nilai novelty
            similarity = self.calculate_similarity_for_all(user_abstract)
            avg_similarity = sum(similarity) / len(self.scopus_id)
            novelty = self.calculate_novelty(self.num_found, avg_similarity)

            # Print nilai novelty
            print(self.num_found)
            print(f"Average Similarity: {avg_similarity:.2f}%")
            print(f"Novelty: {novelty}")

        else:
            print("No results found.")
            self.novelty_grade = 4
            self.scopus_message = f"Nilai novelty 4 karena jurnal Anda tidak memiliki result found yang sama dan hanya memiliki {self.keyword_found} keyword yang sama"
       

    def extract_features(self):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(self.query)

        # Remove stop words from noun chunks
        noun_phrases = [' AND '.join(token.text for token in chunk if token.text.lower() not in STOP_WORDS) for chunk in doc.noun_chunks]
        filtered_noun_phrases = [' '.join(phrase.split(' AND ')) for phrase in noun_phrases]
        self.keyword = filtered_noun_phrases[0]
        
        
        return self.keyword


    def getAllSimilarity(self):
        print(self.scopus_similarities)
        return self.scopus_similarities
        
    def dataId(self):
        return self.scopus_id

    def dataTitle(self):
        return self.scopus_title

    def dataAbstract(self):
        return self.scopus_abstract

    def numFound(self):
        return self.num_found

    def noveltyGrade(self):
        return self.novelty_grade

    def keywordFound(self):
        return self.keyword_found
    
    def message(self):
        return self.scopus_message
    
    def getApi(self):
        return self.api