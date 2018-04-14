import requests
from xml.etree import ElementTree
import webbrowser
import os

def first_page():
    url = 'http://api.digitalpodcast.com/v2r/search/'
    query = input("Enter search terms:\t")
    data = {'appid':'7df91a58d793790699ccedf7c3f660b2',
    'keywords':query}
    response = requests.get(url, params=data)
    if response.status_code != requests.codes.ok: 
        return "Something went wrong:\n{0}".format(response.text)
    root = ElementTree.fromstring(response.content)

    urls = []
    for child in filter(lambda x: x.attrib['type'] == 'link', root.iter('outline')):
        urls.append(child.attrib['url'])

    for i in range(len(urls)):
        print("{0}:     {1}".format(i+1, urls[i]))

    choice = input("Which do you want?\t")
    return urls[int(choice)-1]

def main():
    url = first_page()
    response = requests.get(url)
    root = ElementTree.fromstring(response.content)
    shows = []
    for item in root.iter('item'):
        show ={'url':item.find('enclosure').get('url'),
        'title':item.find('title').text}
        shows.append(show)
    shows = shows[:25]
    print("Here are the first 25 shows. ")
    for i in range(len(shows)):
        print("{0}:    {1}".format(i+1, shows[i]['title']))
    var = input("Which do you want to listen to?\t")
    os.startfile(shows[int(var)-1]['url'])
    # They are all RSS 2.0 NS-es !

if __name__ == '__main__':
    main()