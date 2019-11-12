import os

import jinja2
import webapp3
from datetime import datetime
from paste import httpserver

import frontpage
import editpage
import blogpage
import signup
import login
import logout



def main():
    app = webapp3.WSGIApplication([('/',frontpage.front_page),
                                   ('/blog/(\w+)/?',blogpage.blogpage),
                                   ('/_edit/(\w+)/?',editpage.edit_page),
                                   ('/submit/?',editpage.edit_page),
                                   ('/signup/?',signup.signup),
                                   ('/login/?',login.login),
                                   ('/logout/?',logout.logout)], debug=True)
    httpserver.serve(app, host='127.0.0.1', port='8080')


    

if __name__ == "__main__":
    main()
