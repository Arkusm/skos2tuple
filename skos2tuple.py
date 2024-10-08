import getopt
import json
import os
import pprint
import requests
import sys


vocab = []


def main(argv):
    
    url = None
    lang = None
    durl = "https://e-teachingorg.github.io/skos-vocabularies/example.org/w3i/index.json"
    # url = "https://skohub.io/dini-ag-kim/schulfaecher/heads/main/w3id.org/kim/schulfaecher/index.json"
    # url = "https://skohub.io/dini-ag-kim/educationalLevel/heads/main/w3id.org/kim/educationalLevel/index.json"
    # url = "https://skohub.io/dini-ag-kim/hochschulfaechersystematik/heads/master/w3id.org/kim/hochschulfaechersystematik/scheme.json"
   
    try:
        opts, args = getopt.getopt(argv,"hi:l:",["ifile=", "llang="])
    except getopt.GetoptError:
        print(f'{os.path.basename(__file__)} -i <URL> -l <language code>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print (f'{os.path.basename(__file__)} -i <URL> -l <language code>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            url = arg
            print('Set URL to:', url)
        elif opt in ("-l", "--llang"):
            lang = arg
            print('Set language to', lang)
    if not url:
        url = durl
        print('Try the default URL:', url)
    if not lang:
        lang = 'de'
        print('Try the default language:', lang)
        
        
    
    skos_dict = skos_api(url)    

    print()    
    if 'hasTopConcept' in skos_dict:
        for top in skos_dict['hasTopConcept']:
            title = None
            if 'prefLabel' in top:
                title = top['prefLabel'].get(
                    lang, f'title not available in language {lang}')
                tid = top.get('id', None)            
                tterm = [tid, title]
                print(tterm[1])
                vocab.append(tuple(tterm))      
                get_narrower(top, lang)
    
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


def get_narrower(layer, lang, n=0):
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
                get_narrower(narrower, lang, n+1)
   
if __name__ == "__main__":
    main(sys.argv[1:])
