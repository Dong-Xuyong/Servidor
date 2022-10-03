import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get') as resp:
            print(resp.status)
            print(await resp.text())
            
    async with aiohttp.ClientSession('http://httpbin.org') as session:
        async with session.get('/get'):
            pass
        async with session.post('/post', data=b'data'):
            pass
        async with session.put('/put', data=b'data'):
            pass
        
asyncio.run(main())