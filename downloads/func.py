import requests
import config

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'cookie': config.cookie,
    'referer': 'https://www.pixiv.net/'
}


def isAi(list):
    for i in list:
        if "AI" in i['tag']:
            return True
    return False


def getUser(j):
    l = []
    for i in j:
        l.append(j[i]['name'])
    if len(l) != 0:
        return ','.join(l)
    else:
        return 'Unknown'


def getTags(j):
    l = []
    for i in j:
        l.append(i['tag'])
    if len(l) != 0:
        return ','.join(l)
    else:
        return 'Unknown'


def getImgContent(url):
    r = requests.get(url, headers=headers)
    open('./runtime/{}'.format(url.split('/')[-1]), 'wb').write(r.content)
    return url.split('/')[-1]
