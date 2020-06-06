import requests
from xml.etree import ElementTree
import webbrowser
import sys, subprocess

OPENER = "open" if sys.platform == "darwin" else "xdg-open"

def first_page():
    url = 'http://api.digitalpodcast.com/v2r/search/'
    query = input("Enter search terms: ")
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


def pick(shows, start=0, end=25):
    page = shows[start:end]
    print(f"Shows between {start + 1} and {end}")
    for i in range(len(page)):
        print("{0}:    {1}".format(i+1, page[i]['title']))
    var = input("Which do you want to listen to?\t")
    if var.lower() not in ('n', 'p') and not (start < int(var) <= end):
        print(f"Choice {var} invalid. Must be n, p or above {start} and below {end}. Try again.\n")
        return pick(start, end, shows)
    return var


def main():
    url = first_page()
    response = requests.get(url)
    root = ElementTree.fromstring(response.content)
    shows = []
    for item in root.iter('item'):
        show ={'url':item.find('enclosure').get('url'),
        'title':item.find('title').text}
        shows.append(show)
    print("Press N for the next page, P for the previous.")
    start = 0
    end = 25
    var = pick(shows, start=start, end=end)
    while var.lower() in ('n', 'p'):
        if var.lower() == 'n':
            start += 25
            end += 25
            var = pick(shows, start=start, end=end)
        elif var.lower() == 'p':
            start = min(0, start - 25)
            end = min(25, end - 25)
            var = pick(shows, start=start, end=end)
    subprocess.call([OPENER, shows[int(var)-1]['url']])
    # They are all RSS 2.0 NS-es !


if __name__ == '__main__':
    main()
