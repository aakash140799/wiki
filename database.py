
import cache
import sqlite3
import datetime
db = sqlite3.connect('wikiblog.db', check_same_thread = False)
"""
db.execute(
                CREATE TABLE users(username string PRIMARY KEY,
                                   password string NOT NULL   ,
                                   email    string,
                                   secret   string);
          )

db.execute(
                CREATE TABLE blogs(title string PRIMARY KEY,
                                   author string NOT NULL,
                                   content string NOT NULL,
                                   submitted_date string,
                                   last_modified string,
                                   submission_no integer NOT NULL);
          )

"""

submission_no = int(db.execute("SELECT MAX(submission_no) from blogs").fetchone()[0])+1

userstuple = ('username', 'password', 'email', 'secret')
blogstuple = ('title', 'author', 'content', 'submitted_date', 'last_modified', 'submission_no')

insertuserstr = "INSERT INTO users VALUES(?,?,?,?);"
fetchuserstr = "SELECT * from users WHERE username == ?;"
insertblogstr = "INSERT INTO blogs VALUES(?,?,?,?,?,?);"
fetchblogstr = "SELECT * from blogs WHERE title == ?;"
updateblogstr = "UPDATE blogs SET content = ?, last_modified = ? WHERE title = ?"
fetchpagestr = "SELECT * from blogs WHERE submission_no <= ? AND submission_no >= ? ORDER BY submission_no DESC;"


def fetchblog(title):
    blog = cache.fetchblog(title)
    if not(blog):
        print('db blog hit')
        blog = db.execute(fetchblogstr,(title,)).fetchone()
        if blog:
            blog = {'title':blog[0],'author':blog[1],'content':blog[2],'submitted_date':blog[3],'last_modified':blog[4],'submission_no':blog[5],'cache_time':datetime.datetime.now()}
            cache.insertblog(blog)

    if blog:
        blog['query_time'] = (datetime.datetime.now()-blog['cache_time']).total_seconds()
        blog.pop('cache_time')
    
    return blog



def insertblog(blog):
    db.execute(insertblogstr,(blog['title'],blog['author'],blog['content'],datetime.datetime.now(),datetime.datetime.now(),submission_no))
    try:
        db.commit()
        submissionno = submissionno+1
        return True
    except:
        return False



def updateblog(blog):
    db.execute(updateblogstr,(blog['content'],datetime.datetime.now(),blog['title'],))
    try:
        db.commit()
        cache.insertblog(blog)
        return True
    except:
        return False

    
def fetchuser(username):
    userInfo = None
    if username:
        userInfo = cache.fetchuser(username)
        if not(userInfo):
            print('db user hit')
            userInfo = db.execute(fetchuserstr,(username,)).fetchone()
            if userInfo:
                userInfo = {'username':userInfo[0], 'password':userInfo[1], 'email':userInfo[2], 'secret':userInfo[3]}
                cache.insertuser(userInfo)

    return userInfo



def insertuser(userInfo):
    db.execute(insertuserstr,(userInfo['username'],userInfo['password'],userInfo['email'],userInfo['secret']))
    try:
        db.commit()
        return True
    except:
        return False


def fetchpage(pageno):
    page = cache.fetchpage(str(pageno))
    if page is None:
        print('db page hit')
        dbblogs = db.execute(fetchpagestr,(submission_no-((pageno-1)*10),submission_no-(pageno*10))).fetchall()
        if dbblogs:
            blogs = [{'title':dbblogs[i][0],'author':dbblogs[i][1],'content':dbblogs[i][2],'submitted_date':dbblogs[i][3],'last_modified':dbblogs[i][4],'submission_no':dbblogs[i][5]} for i in range(len(dbblogs))]
            page = {'blogs':blogs,'cache_time':datetime.datetime.now(),'pageno':str(pageno)}
            cache.insertpage(page)

    if page:
        page['query_time'] = (datetime.datetime.now()-page['cache_time']).total_seconds()
        page.pop('cache_time')
    return page

