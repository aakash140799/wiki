
import Handler
import database
class front_page(Handler.Handler):
    def write_page(self,pagedict={}):
        pagedict.update(database.fetchpage(1))
        self.render('front_page.html',pagedict=pagedict)

        
    def get(self):
        pagedict = {}
        if self.checklogin():
            pagedict['username'] = self.name()
        self.write_page(pagedict)


