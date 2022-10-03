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


async def make_app():
    app = web.Application()
    # secret_key must be 32 url-safe base64-encoded bytes
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secret_key))
    app.add_routes([web.get('/', handler)])
    return app

async def do_login(request):
    data = await request.post()
    login = data['login']
    password = data['password']


async def store_mp3_handler(request):

    # WARNING: don't do that if you plan to receive large files!
    data = await request.post()

    mp3 = data['mp3']

    # .filename contains the name of the file in string format.
    filename = mp3.filename

    # .file contains the actual file data that needs to be stored somewhere.
    mp3_file = data['mp3'].file

    content = mp3_file.read()

    return web.Response(body=content,
                        headers=MultiDict(
                            {'CONTENT-DISPOSITION': mp3_file}))
    

async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws

raise web.HTTPFound('/redirect')

@aiohttp_jinja2.template('login.html')
async def login(request):

    if request.method == 'POST':
        form = await request.post()
        error = validate_login(form)
        if error:
            return {'error': error}
        else:
            # login form is valid
            location = request.app.router['index'].url_for()
            raise web.HTTPFound(location=location)

    return {}

app.router.add_get('/', index, name='index')
app.router.add_get('/login', login, name='login')
app.router.add_post('/login', login, name='login')

handler = Handler()
app = web.Application()
app.add_routes([web.get('/', handler.handle),
                web.post(r'/{name:\D+}', handler.new_user),
                web.route('*', '/path', handler.all_handler),
                web.get('/ws', websocket_handler)])



web.run_app(app)