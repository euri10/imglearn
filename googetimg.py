from apiclient.discovery import build
import httplib2
from oauth2client import file, client, tools

import argparse

CLIENT_SECRET = 'client_secret.json'
SCOPES = 'https://www.googleapis.com/auth/youtube'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

store = file.Storage('storage.json')
creds = store.get()
parser = argparse.ArgumentParser(parents=[tools.argparser])
flags = parser.parse_args()
proxy__user = ''
proxy_pass = ''
proxy_host = ''
httpProxy = httplib2.Http(
    proxy_info=httplib2.ProxyInfo(proxy_type=httplib2.socks.PROXY_TYPE_HTTP, proxy_host=proxy_host,
                                  proxy_port=8080, proxy_user=proxy__user,
                                  proxy_pass=proxy_pass))

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES, redirect_uri=REDIRECT_URI)
    # creds = tools.run_flow(flow,store,flags)
    authorize_url = flow.step1_get_authorize_url()
    print
    'Go to the following link in your browser: ' + authorize_url
    code = input('Enter verification code: ').strip()
    creds = flow.step2_exchange(code, http=httpProxy)
    store.put(creds)

creds.authorize(httpProxy)

myyt = build('youtube', 'v3', http=httpProxy)

mysearch = input('Enter what you want to search:').strip()

search_response = myyt.search().list(q=mysearch, part="id,snippet", maxResults=10).execute()
videos = []
channels = []
playlists = []
# Add each result to the appropriate list, and then display the lists of
# matching videos, channels, and playlists.
for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
        videos.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["videoId"]))
    elif search_result["id"]["kind"] == "youtube#channel":
        channels.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["channelId"]))
    elif search_result["id"]["kind"] == "youtube#playlist":
        playlists.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["playlistId"]))
print
"Videos:\n", "\n".join(videos), "\n"
print
"Channels:\n", "\n".join(channels), "\n"
print
"Playlists:\n", "\n".join(playlists), "\n"

