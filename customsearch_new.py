
import pprint

from apiclient.discovery import build



service = build("customsearch", "v1", developerKey="")

res = service.cse().list(q='vegeta', cx='',searchType='image').execute()
pprint.pprint(res)
for i in res['items']:
  pprint.pprint(i['link'])


