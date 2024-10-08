import getopt
import json
import pprint
import requests
import sys


vocab = []
lang = 'de'


def main(argv):
    
    arg = None
    url = "https://e-teachingorg.github.io/skos-vocabularies/example.org/w3i/index.json"
    # url = "https://skohub.io/dini-ag-kim/schulfaecher/heads/main/w3id.org/kim/schulfaecher/index.json"
    # url = "https://skohub.io/dini-ag-kim/educationalLevel/heads/main/w3id.org/kim/educationalLevel/index.json"
    # url = "https://skohub.io/dini-ag-kim/hochschulfaechersystematik/heads/master/w3id.org/kim/hochschulfaechersystematik/scheme.json"
   
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile="])
    except getopt.GetoptError:
        print ('test.py -i <URL>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('skos2tuple.py -i <URL>')
            sys.exit()
        if opt in ("-i", "--ifile"):
            url = arg
            print('Try to get a Skos vocabulary from the following URL:', url)
    if not arg:
        print('Try the default URL:', url)
    
    skos_dict = skos_api(url)    

    print()    
    if 'hasTopConcept' in skos_dict:
        for top in skos_dict['hasTopConcept']:
            title = None
            if 'prefLabel' in top:
                title = top['prefLabel'].get(lang, None)
            tid = top.get('id', None)            
            tterm = [tid, title]
            print(tterm[1])
            vocab.append(tuple(tterm))      
            get_narrower(top)
    
    print()    
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(tuple(vocab))


def skos_api(url):
    sd = {}
    headers = {"content-type": "application/json"}
    request_string = url
    response = requests.get(request_string, headers=headers)
    if response.status_code == 200:
        sd = json.loads(response.text)
    return sd


def get_narrower(layer, n=0):
    num = '  ' * n
    if 'narrower' in layer: 
        for narrower in layer['narrower']:
            title = None
            if 'prefLabel' in narrower:
                title = narrower['prefLabel'].get(lang, None)
            id = narrower.get('id', None)
            if title:
                print(f'{num} -- {title}')        
                term = [id, title]
                vocab.append(tuple(term)) 
                get_narrower(narrower, n+1)
   
if __name__ == "__main__":
    main(sys.argv[1:])
