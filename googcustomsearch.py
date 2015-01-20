import requests
import pprint

url = ('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=barack%20obama')

request = requests.get(url)
pprint.pprint(request.json())
# Process the JSON string.

