import requests
from bs4 import BeautifulSoup
from render import Renderer
import sys
UNREACHABLE_ITEMS = []
ITEMS_LIST = []
REACHABLE_ITEMS = []
MAIN_URL = sys.argv[1]

        





'''
DESCRIPTION:
    This function is tries to connect to the given resource url
PARAMS:
    - url: The url to connect to
RETURNS:
    None.
'''
def check_resource(url)-> None:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False




'''
DESCRIPTION:
    This function parses html that given as parameter,
    and extracts the resources and the hyper links as list
PARAMS:
    - html: The html to parse
RETURNS:
    None
'''

def parse_html(html)-> None:
    parser = BeautifulSoup(html,'lxml')
    _imagesList = []
    _styleList = []
    _jsList = []

    print('Fetching images...')

    imageList = parser.find_all('img')
    for image in imageList:
        _imagesList.append(image['src'])

    print(f'{len(_imagesList)} Image resources founded')

    print('Fetching Javascripts...')
    jsList = parser.find_all('script')
    for js in jsList:
        if js.has_attr('src'):
            _jsList.append(js['src'])
    print(f'{len(_jsList)} Javascript resources founded')

    print('Fetching Styles...')
    
    styleList = parser.find_all('link')
    for style in styleList:
        if style.has_attr('rel') and style['rel'][0] == 'stylesheet':
            _styleList.append(style['href'])

    print(f'{len(_styleList)} Stylesheet resources founded')

    print('Checking for images...')
    for image in _imagesList:
        control = check_resource(image)
        if control:
            print(image+' Founded')
            REACHABLE_ITEMS.append({'source': image,'type': 'image'})
        else:
            UNREACHABLE_ITEMS.append({'source':image,'type':'image'})
            print(image+' Not founded')

    print('Checking for javascript...')
    for js in _jsList:
        control = check_resource(js)
        if control:
            print(js+' Founded')
            REACHABLE_ITEMS.append({'source': js,'type': 'js'})
        else:
            UNREACHABLE_ITEMS.append({'source':js,'type':'js'})
            print(js+' Not founded')

    print('Checking for stylesheet...')
    for style in _styleList:
        control = check_resource(style)
        if control:
            print(style+' Founded')
            REACHABLE_ITEMS.append({'source': style,'type': 'style'})
        else:
            UNREACHABLE_ITEMS.append({'source':style,'type':'style'})
            print(style+' Not founded')

    output = Renderer(MAIN_URL,REACHABLE_ITEMS, UNREACHABLE_ITEMS)
    output.RenderOutput()


'''
DESCRIPTION:
    This function gets the html content of the given url address if it's possible.
PARAMS:
    - url: The url to crawl
RETURNS:
    String
'''
def get_html(url)-> str:
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return ''



html = get_html(MAIN_URL)
parse_html(html)