from configparser import ConfigParser
from urllib.parse import urlsplit
import requests
from apiclient.discovery import build
import httplib2
import socks


# import config options, put them in variables for future use
parser = ConfigParser()
parser.read('config.ini')
developperkey = parser.get('google', 'developperkey')
cx = parser.get('google', 'cx')
proxyurl = parser.get('proxy_settings', 'requests_proxy')

# hack for making proxy work in python3
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, 'localhost', 9000, )
socks.wrapmodule(httplib2)
httpproxy = httplib2.Http()


def search_google(search):
    service = build('customsearch', 'v1', developerKey=developperkey, http=httpproxy)
    res = service.cse().list(q=search, cx=cx, searchType='image').execute()
    return [l['link'] for l in res['items']]

# with open('data.txt', 'w') as outfile:
#     json.dump(res, outfile)
#
#
# with open('test.json') as data:
#     d = json.load(data)
#     # pprint.pprint(d['items'])
#
# links = [l['link'] for l in d['items']]
# pprint.pprint(links)


proxies = {"http": proxyurl, }


def save_images_from_link(links):
    for link in links:
        page = requests.get(link, proxies=proxies)
        scheme, netloc, path, query, fragment = urlsplit(link)
        with open(path.split('/')[-1], 'wb') as test:
            test.write(page.content)


toto= search_google('vegeta')
print(toto)