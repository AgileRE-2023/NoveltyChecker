from django.shortcuts import render
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

# nltk.download('stopwords')
# nltk.download('punkt')


def search(request):
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

            # Print hasil ke konsol
            print("Scopus ID:", scopus_id)
            print("Title:", scopus_title)
            print("Abstract:", scopus_abstract)
            print("Number of results found:", scopus_num_found)

            similarities = scopus.calculate_similarity_for_all(user_abstract) 

            return render(request, 'search/searchreport.html', {'scopus_id': scopus_id, 'scopus_title': scopus_title, 'scopus_abstract': scopus_abstract, 'similarities': similarities, 'scopus_num_found': scopus_num_found})

    return render(request, 'search/searchpage.html')

def report(request):
    return render(request, 'search/searchreport.html')

def list(request):
    return render(request, 'search/searchlist.html')

class SearchScopus():
    con_file = open("config.json")
    config = json.load(con_file)
    con_file.close()
    query = ''
    num_found = ''
    scopus_id = []
    scopus_title = []
    scopus_abstract = []
    scopus_doi = []

    client = ElsClient(config['apikey'])

    def __init__(self, query):
        self.query = query

    def getAbstract(self):
        for i in range(10):
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
            
            # # Debugging: Cetak nilai TF-IDF matrix
            # print("TF-IDF Matrix:")
            # print(tfidf_matrix.toarray())

            similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)

            # # Debugging: Cetak nilai similarity_matrix
            # print("Similarity Matrix:")
            # print(similarity_matrix)
            
            # Convert similarity to percentage
            similarity_percentage = similarity_matrix[0][1] * 100
            api_similarities.append(similarity_percentage)

        return api_similarities

    def calculate_novelty(self, num_searched_titles, avg_similarity):
        if 6000 <= num_searched_titles <= 10000000 or avg_similarity >= 12:
            return 1
        elif 100 <= num_searched_titles <= 6000 or avg_similarity >= 10:
            return 2
        elif 5 <= num_searched_titles <= 100 or avg_similarity >= 5:
            return 3
        elif num_searched_titles < 5 or avg_similarity>=3:
            return 4
        
        return None

    def getScopusData(self, user_abstract):
        doc_srch = ElsSearch(self.query, 'scopus')
        doc_srch.execute(self.client, get_all=False)
        self.num_found = doc_srch.tot_num_res

        # Pastikan jumlah hasil pencarian memadai
        num_results = min(10, self.num_found)
        for i in range(num_results):
            scp_clear = doc_srch.results[i]['dc:identifier'].replace('SCOPUS_ID:', '')
            self.scopus_title.append(doc_srch.results[i]['dc:title'])
            self.scopus_id.append(scp_clear)

        if num_results > 0:
            self.scopus_abstract = self.getAbstract()

            # Hitung nilai novelty
            avg_similarity = sum(self.calculate_similarity_for_all(user_abstract)) / len(self.scopus_id)
            novelty = self.calculate_novelty(self.num_found, avg_similarity)

            # Print nilai novelty
            print(self.num_found)
            print(f"Average Similarity: {avg_similarity:.2f}%")
            print(f"Novelty: {novelty}")

        # Print nilai similarity untuk setiap ID
        similarities = self.calculate_similarity_for_all(user_abstract)
        for idx, similarity in enumerate(similarities):
            if idx < len(self.scopus_id):  
                print(f"Scopus ID: {self.scopus_id[idx]}, Similarity: {similarity:.2f}%")
            else:
                print("Index out of range. Check the lengths of self.scopus_id and similarities.")

    def dataId(self):
        return self.scopus_id

    def dataTitle(self):
        return self.scopus_title

    def dataAbstract(self):
        return self.scopus_abstract

    def numFound(self):
        return self.num_found