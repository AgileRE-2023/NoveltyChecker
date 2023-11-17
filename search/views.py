from django.shortcuts import render
from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch
from elsapy.elsdoc import AbsDoc
import ast
import json

# Create your views here.
def search(request):
    if request.method == 'POST':
        query = request.POST.get('title')
        abstract = request.POST.get('abstract')

        if query == '' and abstract == '':
            return render(request, 'search/searchreport.html', {'error':'Please fill all the fields'})
        else:
            # print(query)
            scopus = SearchScopus(query)
            scopus.getScopusData()
            scopus_id = scopus.dataId()
            scopus_title = scopus.dataTitle()
            scopus_abstract = scopus.dataAbstract()
            scopus_num_found = scopus.numFound()
            # scopus_doi = scopus.dataDoi()
            # print(scopus_id)
            # print(scopus_title)
            # print(scopus_abstract)
            # print(scopus_num_found)
            # print(scopus_doi)
            
            return render(request, 'search/searchreport.html', {'scopus_id':scopus_id, 'scopus_title':scopus_title, 'scopus_abstract':scopus_abstract, 'query':query, 'abstract': abstract})

    return render(request, 'search/searchpage.html')

def report(request):
    return render(request, 'search/searchreport.html')

def list(request):
    if request.method == 'POST':
        scopus_id = ast.literal_eval(request.POST.get('scopus_id'))
        scopus_title = ast.literal_eval(request.POST.get('scopus_title'))
        scopus_abstract = ast.literal_eval(request.POST.get('scopus_abstract'))
        scopus_all = []
        
        for i in range(len(scopus_id)):
            entry = {
                'scopus_id': scopus_id[i],
                'scopus_title': scopus_title[i],
                'scopus_abstract': scopus_abstract[i]
            }
            scopus_all.append(entry)

        return render(request, 'search/searchlist.html', {'scopus_all': scopus_all})

    elif request.method == 'GET':
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
        for i in range (10):
            scp_doc = AbsDoc(scp_id = self.scopus_id[i])
            if scp_doc.read(self.client):
                self.scopus_abstract.append(scp_doc.data["coredata"]["dc:description"])
                # self.scopus_doi.append(scp_doc.data["coredata"]["prism:url"])
            else:
                print ("Read document failed.")
        # print(self.scopus_doi)
        return self.scopus_abstract

    def getScopusData(self):
        doc_srch = ElsSearch(self.query,'scopus')
        doc_srch.execute(self.client, get_all = False)
        result = json.dumps(doc_srch.results, indent=4)
        # print(len(doc_srch.results))
        # print(result)
        self.num_found = doc_srch.tot_num_res
        for i in range(10):
            scp_clear = doc_srch.results[i]['dc:identifier'].replace('SCOPUS_ID:','')
            self.scopus_title.append(doc_srch.results[i]['dc:title'])
            self.scopus_id.append(scp_clear)
        SearchScopus.getAbstract(self);

    def dataId(self):
        return self.scopus_id
    
    def dataTitle(self):
        return self.scopus_title
    
    def dataAbstract(self):
        return self.scopus_abstract
    
    def numFound(self):
        return self.num_found