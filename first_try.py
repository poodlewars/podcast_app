import requests
from xml.etree import ElementTree

def first_page():
    url = 'http://api.digitalpodcast.com/v2r/search/'
    data = {'appid':'7df91a58d793790699ccedf7c3f660b2',
    'keywords':'rock and roll'}
    response = requests.get(url, params=data)
    if response.status_code != requests.codes.ok: 
        return "Something went wrong:\n{0}".format(response.text)
    root = ElementTree.fromstring(response.content)
    for child in filter(lambda x: x.attrib['type'] == 'link', root.iter('outline')):
        properties = child.attrib
        print(child.attrib['url'])
    return "done"

def main():
    url = 'http://www.americanheartbreak.com/rnrgeekwp/?feed=podcast'
    response = requests.get(url)
    print(response.text)
    root = ElementTree.fromstring(response.content)
    for neighbour in root.iter('item'):
        print(neighbour.attrib)
    #first_page()

if __name__ == '__main__':
    print(main())