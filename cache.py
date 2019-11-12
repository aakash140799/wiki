
import memcache

cache = memcache.Client(['127.0.0.1:11211'], debug=True)
def fetchblog(title):
    title = title.replace(' ','_')
    blog = cache.get(title)
    if blog:
        blog['title'] = blog['title'].replace('_',' ')
    return blog


def insertblog(blog):
    blog['title'] = blog['title'].replace(' ','_')
    cache.set(blog['title'],blog)

def fetchuser(username):
    return cache.get(username)

def insertuser(userInfo):
    cache.set(userInfo['username'],userInfo)

def insertpage(page):
    cache.set(page['pageno'],page)
    
def fetchpage(pageno):
    return cache.get(pageno)

def resetpage(pageno):
    cache.delete(pageno)
