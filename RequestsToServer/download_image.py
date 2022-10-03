import requests
req = requests.get('https://m.media-amazon.com/images/M/MV5BNGU1ZDJmMWUtYjkzZC00YmZlLWE3YjYtMmQ1MjFmNGM1MGZjXkEyXkFqcGdeQXVyMTk2OTAzNTI@._V1_FMjpg_UX1000_.jpg', stream=True)
req.raise_for_status()
with open('Forest.jpg', 'wb') as fd:
    for chunk in req.iter_content(chunk_size=50000):
        print('Received a Chunk')
fd.write(chunk)
