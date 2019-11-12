
import hashlib
import database
import hmac


secret = b'aasfafas'
def info(request):
    cookie = request.request.cookies.get('user')
    loginInfo = {'username':None, 'loggedin':False}
    if cookie:
        cookie = cookie.split(':')
        if len(cookie) == 2:
            if hmac.new(secret, cookie[0].encode('utf-8'), hashlib.sha256).hexdigest() == cookie[1]:
                loginInfo['username'] = cookie[0]
                loginInfo['loggedin'] = True

    return loginInfo


def set_login(request,username):
    if not(username):
        username = ""
    request.response.set_cookie('user',username+':'+hmac.new(secret, username.encode('utf-8'), hashlib.sha256).hexdigest())


def set_logout(request):
    request.response.delete_cookie('user')
    print('logging out')


