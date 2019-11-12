

import Handler
class logout(Handler.Handler):
    def get(self):
        self.logout()
        self.redirect('/')



