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
from django.http import JsonResponse
import subprocess
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
# def rerun_server(request):
#     subprocess.run(['python', 'manage.py', 'runserver'])
#     return JsonResponse({'status': 'success'})
    
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
    avg_similarity = 0.0
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

    
    
    def calculate_novelty(self):
        if 6000 <= self.num_found or self.avg_similarity >= 12 or self.keyword_found > 10000000:
            self.novelty_grade = 1
            if self.highest_similarity >= 70:
                self.scopus_message = f"seems like this journal has been published and indexed at scopus."
            
            elif 6000 <= self.num_found:
                self.scopus_message = f"Your journal, with {self.num_found} similar results and {self.keyword_found} identical keywords, exhibits an exceptionally high {self.highest_similarity}% similarity. Consider exploring new avenues to enhance its originality."

            elif self.avg_similarity >= 12:
                self.scopus_message = f"While your journal shares {self.num_found} results and {self.keyword_found} identical keywords, the extremely high {self.highest_similarity}% similarity suggests the need for unique perspectives to enhance its novelty."

            elif self.keyword_found > 10000000:
                self.scopus_message = f"Despite the {self.num_found} related results and {self.keyword_found} identical keywords, the remarkably high {self.highest_similarity}% similarity indicates the importance of introducing innovative elements for greater originality."

        elif 100 <= self.num_found <= 6000 or self.avg_similarity >= 8 or self.keyword_found > 7000000:
            self.novelty_grade = 2
            if self.highest_similarity >= 70:
                self.scopus_message = f"seems like this journal has been published and indexed at scopus."
            
            elif 100 <= self.num_found <= 6000:
                self.scopus_message = f"While your journal, featuring {self.num_found} similar results and {self.keyword_found} identical keywords, has a significant {self.highest_similarity}% similarity, consider introducing distinct elements to elevate its uniqueness."

            elif self.avg_similarity >= 8:
                self.scopus_message = f"With {self.num_found} matching results and {self.keyword_found} identical keywords, your journal demonstrates a notable {self.highest_similarity}% similarity. Consider incorporating diverse perspectives to enhance its originality."

            elif self.keyword_found > 7000000:
                self.scopus_message = f"Your journal, with {self.num_found} related results and {self.keyword_found} identical keywords, showcases a significant {self.highest_similarity}% similarity. Exploring new approaches could contribute to its uniqueness."

        elif 5 <= self.num_found <= 100 or self.avg_similarity >= 5 or self.keyword_found > 5000000:
            self.novelty_grade = 3
            if self.highest_similarity >= 70:
                self.scopus_message = f"seems like this journal has been published and indexed at scopus."
            
            elif 5 <= self.num_found <= 100:
                self.scopus_message = f"Kudos! Your journal, with {self.num_found} similar results and {self.keyword_found} identical keywords, displays a moderate {self.highest_similarity}% similarity. Exploring different angles can further enhance its novelty."

            elif self.avg_similarity >= 5:
                self.scopus_message = f"Good effort! Having {self.num_found} matching results and {self.keyword_found} identical keywords, your journal showcases a noteworthy {self.highest_similarity}% similarity. Consider introducing varied perspectives to increase its originality."

            elif self.keyword_found > 5000000:
                self.scopus_message = f"Excellent contribution! Your journal, with {self.num_found} related results and {self.keyword_found} identical keywords, presents a substantial {self.highest_similarity}% similarity. Incorporating diverse elements could further elevate its uniqueness."

        elif self.num_found < 5 or self.avg_similarity <= 3 or self.keyword_found < 1000000:
            self.novelty_grade = 4
            if self.highest_similarity >= 70:
                self.scopus_message = f"seems like this journal has been published and indexed at scopus."
            
            elif self.num_found < 5:
                self.scopus_message = f"Fantastic work! Your journal, featuring only {self.num_found} results and {self.keyword_found} identical keywords, indicates a low {self.highest_similarity}% similarity. This suggests a promising start towards creating a truly novel contribution."

            elif self.avg_similarity <= 3:
                self.scopus_message = f"Great start! With {self.num_found} matching results and {self.keyword_found} identical keywords, your journal shows a low {self.highest_similarity}% similarity. Keep exploring new avenues to further enhance its originality."

            elif self.keyword_found < 1000000:
                self.scopus_message = f"Start of something new! Your journal, with {self.num_found} related results and {self.keyword_found} identical keywords, displays a low {self.highest_similarity}% similarity. Every discovery opens doors to uncharted territories."

        return self.novelty_grade, self.scopus_message


    
    
    def getScopusData(self, user_abstract):
        self.scopus_id = []
        self.scopus_title = []
        self.scopus_abstract = []
        self.scopus_doi = []
        self.scopus_similarities = []
        self.avg_similarity = 0.0
        self.novelty_grade = 0
        self.highest_similarity = 0
        self.scopus_message = ''
        self.api = ''
        
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

            similarity = self.calculate_similarity_for_all(user_abstract)
            self.avg_similarity = sum(similarity) / len(self.scopus_id)
            novelty = self.calculate_novelty()

            self.scopus_similarities = similarity
            self.highest_similarity = self.highest_similarity_percentage()
            self.novelty_grade, self.scopus_message = novelty
            
            # Print nilai novelty
            print(self.num_found)
            print(f"Average Similarity: {self.avg_similarity:.2f}%")
            print(f"Novelty: {novelty}")

        else:
            print("No results found.")
            novelty = self.calculate_novelty()
       

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
