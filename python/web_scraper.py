
# Web scraper using Python


import requests
import bs4


def ml_wiki():
    res = requests.get('https://en.wikipedia.org/wiki/Machine_learning')

    # print(res.text)

    soup = bs4.BeautifulSoup(res.text, "lxml")

    title = soup.select('title')
    print(title)
    print(''.center(50, '#'))

    # to select w.r.t class name, use .
    title2 = soup.select('.mw-headline')
    for i in title2:
        print(i.text)
    print(''.center(50, '#'))

    # to select w.r.t class name, use #
    title3 = soup.select('#t-whatlinkshere')
    print(title3)
    print(''.center(50, '#'))

    # to select w.r.t child tag, use >
    title4 = soup.select('h2 > span')
    print(title4)
    print(''.center(50, '#'))

    findall = soup.find_all("a", href=True)
    for link in findall:
        print(link['href'])
    print(''.center(50, '#'))


def raga_songs():
    raga_songs_map = {}

    res = requests.get('http://ragawisesongs.blogspot.com/')
    # print(res.text)
    soup = bs4.BeautifulSoup(res.text, "lxml")

    # # to select w.r.t child tag, use >
    # title4 = soup.select('h3 > a')
    # for i in title4:
    #     print(i.text)
    # print(''.center(50, '#'))

    raga_part = soup.select('.date-outer')[1]
    # print(raga_part)
    for part in raga_part.select('.date-posts'):
        for raga in part.select('h3 > a'):
            print(raga.text)
        for songs in part.find_all("div", {"dir": "ltr"}):
            print(songs)
        # print(part.div)


raga_songs()
