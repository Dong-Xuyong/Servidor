import requests
 
query = {'q': 'Forest', 'order': 'popular', 'min_width': '800', 'min_height': '600'}
req = requests.get('https://pixabay.com/en/photos/', params=query)
 
req.url
# returns 'https://pixabay.com/en/photos/?order=popular&amp;min_height=600&amp;q=Forest&amp;min_width=800'