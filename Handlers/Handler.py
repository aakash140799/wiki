

import os
import jinja2
import webapp3
import hmac
import hashlib
import database


template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp3.RequestHandler):
    def write(self,*a,**param):
        self.response.write(*a,**param)

    def render_str(self,template,**param):
        t = jinja_env.get_template(template)
        return t.render(param)

    def render(self,template,**param):
        self.write(self.render_str(template,**param))

    def renderjson(self,pagedict):
        json_txt = json.dumps(pagedict)
        self.response.header['content-type'] = 'application/json charset=UTF-8'
        self.write(json_txt)

    def login(self,name,secret):
        secret = hmac.new(name.encode('utf-8'),secret.encode('utf-8'),hashlib.sha256).hexdigest()
        self.response.set_cookie('user_id',name+':'+secret)

    def logout(self):
        self.response.delete_cookie('user_id')

    def checklogin(self):
        secret = self.request.cookies.get('user_id')
        if secret and len(secret.split(':')) == 2:
            name,secret = secret.split(':')
            userInfo = database.fetchuser(name)
            if secret == hmac.new(name.encode('utf-8'),
                                  userInfo['secret'].encode('utf-8'),
                                  hashlib.sha256).hexdigest():
                return True
            else:
                self.logout()
        return False

    def name(self):
        cookie = self.request.cookies.get('user_id')
        if cookie and len(cookie.split(':'))==2:
            return cookie.split(':')[0]
