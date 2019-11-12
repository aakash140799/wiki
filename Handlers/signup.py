

import Handler
import re
import random
import database
import webapp3
import string
import hashlib
emailre = '[a-zA-Z]{1,20}[0-9]{0,20}@[a-zA-Z0-9]{1,20}\.[a-zA-Z0-9\._]{1,20}'
class signup(Handler.Handler):
    def write_page(self,pagedict={}):
        self.render('signup.html',pagedict=pagedict)

    def get(self):
        if self.checklogin():
            self.redirect('/')
        else:
            self.write_page()


    def post(self):
        if self.checklogin():
            self.redirect('/')
        else:

            pagedict = {}
            pagedict['username'] = self.request.get('username')
            pagedict['password'] = self.request.get('password')
            pagedict['verify']   = self.request.get('verify')
            pagedict['email']    = self.request.get('email')
            pagedict['error']    = None

            if len(pagedict['username']) == 0 or len(pagedict['username']) > 20:
                pagedict['errusername'] = 'username should be 1 to 20 char long';pagedict['error']=True
            if database.fetchuser(pagedict['username']):
                pagedict['errusername'] = 'Username already exists';pagedict['error']=True
            if len(pagedict['password']) < 8 or len(pagedict['password']) > 30:
                pagedict['errpassword'] = 'password should be 8 to 30 char lon';pagedict['error']=True
            if pagedict['password'] != pagedict['verify']:
                pagedict['errverify'] = 'Passwords do not match';pagedict['error']=True
            matcher = re.compile(emailre)
            if pagedict['email'] and (matcher.match(pagedict['email']) is None or matcher.match(pagedict['email']).end() != len(pagedict['email'])):
                pagedict['erremail'] = 'Invalid email address';pagedict['error']=True

            if pagedict['error']:
                self.write_page(pagedict)
            else:
                secret = ''.join([random.choice(string.ascii_letters+string.digits) for n in range(32)])
                userInfo = {'username':pagedict['username'],
                            'password':hashlib.sha256((secret+pagedict['password']).encode('utf-8')).hexdigest(),
                            'email':pagedict['email'],
                            'secret':secret}
                
                if database.insertuser(userInfo):
                    self.login(userInfo['username'],userInfo['secret'])
                    self.redirect('/')
                else:
                    pagedict['errdb'] = 'database error'
                    self.write_page(pagedict)
