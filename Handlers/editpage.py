

import Handler
import datetime
import webapp3
import database


class edit_page(Handler.Handler):
    def write_page(self,pagedict={}):
        self.render('edit_page.html',pagedict=pagedict)


    def get(self,title='None'):
        if not(self.checklogin()):
            self.redirect('/login')
            return
        
        pagedict = {}
        if title != 'None' and title != '':
            blog = database.fetchblog(title)
            if blog is not None:
                pagedict.update(blog)
                pagedict['update'] = True
                
        pagedict['username'] = self.name()
        self.write_page(pagedict)



    def post(self,title=None):
        if not(self.checklogin()):
            self.redirect('/login')
            return

        pagedict = {'title':self.request.get('title'), 'author':self.name(), 'content': self.request.get('content'), 'error':None}
        if len(pagedict['title']) == 0 or len(pagedict['title']) > 100:
            pagedict['errtitle'] = 'title must be of length 1 to 100';pagedict['error'] = True
        if len(pagedict['content']) == 0 or len(pagedict['content']) > 1000000:
            pagedict['errcontent'] = 'content must be of non-empty length';pagedict['error'] = True
        
        
        if pagedict['error'] is not None:
            self.write_page(pagedict)
        else:
            blog = database.fetchblog(pagedict['title'])
            if blog is not None:
                if database.updateblog(pagedict):
                    self.redirect('/blog/'+pagedict['title'])
                else:
                    pagedict['dberror'] = 'database error'
                    self.write_page(pagedict)
            else:
                if database.insertblog(pagedict):
                    self.redirect('/blog/'+pagedict['title'])
                else:
                    pagedict['dberror'] = 'database error'
                    self.write_page(pagedict)

