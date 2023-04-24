import requests
import re
import json
import os
import sys
from tqdm import trange

import func
import db

try:
    os.mkdir("./runtime")
    os.mkdir("./db")
except:
    pass


def getPixivImage(id):
    try:
        r = requests.get(
            'https://www.pixiv.net/artworks/{}'.format(id), headers=func.headers)

        s = re.findall(
            r'\<meta name="preload-data" id="meta-preload-data" content=\'(.*)\'', r.text)
        j = json.loads(s[0])

        info = j["illust"][str(id)]
        if not func.isAi(info['tags']['tags']):
            author = func.getUser(j['user'])
            tags = func.getTags(info['tags']['tags'])
            try:
                img = requests.get(
                    'https://www.pixiv.net/ajax/illust/{}/pages'.format(id), headers=func.headers)
                imgj = json.loads(img.text)
                if not imgj['error']:
                    n = 0
                    for i in imgj['body']:
                        n += 1
                        file = func.getImgContent(i['urls']['original'])
                        try:
                            os.mkdir('./db/{}'.format(id))
                        except:
                            pass
                        os.system(
                            'magick -quality 90 ./runtime/{} ./db/{}/{}.avif'.format(
                                file, id, n
                            )
                        )
                        os.remove('./runtime/{}'.format(file))

                    cur = db.conn.cursor()
                    cur.execute(
                        "INSERT INTO image (pid, name, author, tags, num) VALUES ({},'{}','{}','{}',{})".format(
                            id, info['title'], author, tags, n
                        )
                    )
                    db.conn.commit()
                else:
                    print('Get Image URL Error')
            except:
                print('Get Image URL Error')
        else:
            print("is AI")
    except KeyboardInterrupt:
        sys.exit()
    except:
        pass


def getNewId():
    pid = -1
    nr18 = requests.get(
        'https://www.pixiv.net/ajax/illust/new?lastId=0&limit=1&type=illust&r18=false', headers=func.headers
    )
    r18 = requests.get(
        'https://www.pixiv.net/ajax/illust/new?lastId=0&limit=1&type=illust&r18=true', headers=func.headers
    )
    nr18j = json.loads(nr18.text)
    r18j = json.loads(r18.text)
    if not nr18j['error'] and not r18j['error']:
        if nr18j['body']['illusts'][0]['id'] > r18j['body']['illusts'][0]['id']:
            pid = int(nr18j['body']['illusts'][0]['id'])
        else:
            pid = int(r18j['body']['illusts'][0]['id'])
    return pid


new = getNewId()
try:
    now = int(open('./now', 'r').read())
except:
    now = 100000000

print("Starting... {}->{}".format(now, new))

# getPixivImage(104847504)

for i in trange(now, new):
    getPixivImage(i)
    open('./now', 'w').write(str(i))
