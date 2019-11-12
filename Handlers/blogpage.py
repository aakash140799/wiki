
import Handler
import database
import webapp3

class blogpage(Handler.Handler):
    def write_page(self,pagedict={}):
        self.render('blogpage.html',pagedict=pagedict)

        
    def get(self,title=None):
        if title is None:
            self.redirect('/submit')
            return

        blog = database.fetchblog(title)
        if blog is None and self.checklogin():
            self.redirect('/_edit/'+str(title))
        elif blog is None and not(self.checklogin()):
            self.redirect('/login')
        elif blog is not None:
            pagedict = blog
            pagedict['username'] = self.name()
            print(pagedict)
            self.write_page(pagedict)


