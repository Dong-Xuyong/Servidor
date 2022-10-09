import asyncio
import time
import base64
from cryptography import fernet
from aiohttp import web
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import json
from multidict import MultiDict



class Handler:

    def __init__(self):
        pass

    
    async def handle(request):
        response_obj = { 'status' : 'success' }
        return web.Response(text=json.dumps(response_obj))

    async def new_user(request):
        try:
            session = await get_session(request)
            last_visit = session['last_visit'] if 'last_visit' in session else None
            text = 'Last visited: {}'.format(last_visit)
            ## happy path where name is set
            user = request.query['name']
            ## Process our new user
            print("Creating new user with name: " , user)

            response_obj = { 'status' : 'success' }
            ## return a success json response with status code 200 i.e. 'OK'
            return web.Response(text=json.dumps(response_obj), status=200)
        except Exception as e:
            ## Bad path where name is not set
            response_obj = { 'status' : 'failed', 'reason': str(e) }
            ## return failed with a status code of 500 i.e. 'Server Error'
            return web.Response(text=json.dumps(response_obj), status=500)

    async def all_handler(request):
        response_obj = { 'status' : 'success' }
        return web.Response(text=json.dumps(response_obj))
    

handler = Handler()
app = web.Application()
app.add_routes([web.get('/', handler.handle),
                web.post(r'/{name:\D+}', handler.new_user),
                web.route('*', '/path', handler.all_handler),
                ])



web.run_app(app)