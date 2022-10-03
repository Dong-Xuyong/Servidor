import requests
 
url = 'http://some-domain.com/set/cookies/headers'
 
headers = {'user-agent': 'your-own-user-agent/0.0.1'}
cookies = {'visit-month': 'February'}
 
req = requests.get(url, headers=headers, cookies=cookies)


import requests
 
jar = requests.cookies.RequestsCookieJar()
jar.set('first_cookie', 'first', domain='httpbin.org', path='/cookies')
jar.set('second_cookie', 'second', domain='httpbin.org', path='/extra')
jar.set('third_cookie', 'third', domain='httpbin.org', path='/cookies')
 
url = 'http://httpbin.org/cookies'
req = requests.get(url, cookies=jar)
 
req.text
 
# returns '{ "cookies": { "first_cookie": "first", "third_cookie": "third" }}'