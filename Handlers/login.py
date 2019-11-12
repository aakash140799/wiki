

import Handler
import database
import hashlib

class login(Handler.Handler):
    def write_page(self,pagedict={}):
        self.render("login.html", pagedict=pagedict)


    def get(self):
        if self.checklogin():
            self.redirect('/')
        else:
            self.write_page()



    def post(self):
        if self.checklogin():
            self.redirect('/')
        else:
            userInfo = {'username':self.request.get('username'),
                        'password':self.request.get('password')
                        }
            pagedict = {'error':None}
            
            """
            pagedict.update(userInfo)
            if userInfo['username'] == '':
                pagedict['error'] = 'Empty username'
            elif userInfo['password'] == '':
                pagedict['error'] = 'Empty password'"""
            dbuser = database.fetchuser(userInfo['username'])
            if dbuser is None or dbuser['password'] != hashlib.sha256((dbuser['secret']+userInfo['password']).encode('utf-8')).hexdigest():
                pagedict['error'] = 'Invalid username or password'

            
            if pagedict['error'] is not None:
                self.write_page (pagedict)
            else:    
                self.login(dbuser['username'],dbuser['secret'])
                self.redirect('/')
                    
