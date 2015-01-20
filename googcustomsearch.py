import httplib2

__author__ = 'euri10'

from apiclient.discovery import build
import pprint

def main():
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.

    proxy__user = ''
    proxy_pass = ''
    proxy_host = ''
    httpProxy = httplib2.Http(
    proxy_info=httplib2.ProxyInfo(proxy_type=httplib2.socks.PROXY_TYPE_HTTP, proxy_host=proxy_host,
                                  proxy_port=8080, proxy_user=proxy__user,
                                  proxy_pass=proxy_pass))
    proxy_info=httplib2.ProxyInfo(proxy_type=httplib2.socks.PROXY_TYPE_HTTP, proxy_host='',
                                  proxy_port=8080, proxy_user=proxy__user,
                                  proxy_pass=proxy_pass))

  service = build("customsearch", "v1",
            developerKey="AIzaSyDRRpR3GS1F1_jKNNM9HCNd2wJQyPG3oN0",  http=httpProxy)

  res = service.cse().list(
      q='lectures',
      cx='017576662512468239146:omuauf_lfve',
    ).execute()
  pprint.pprint(res)

if __name__ == '__main__':
  main()


