import webapp2
import os
import jinja2
from gcloud import datastore 
import datastore_abstraction as dal

template_dir=os.path.join(os.path.dirname(__file__),'templates')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)
    def render_str(self,template,**params):
        t=jinja_env.get_template(template)
        return t.render(params)
    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

class NewPostPage(Handler):
    def get(self):
        self.render("new_post.html")
    def post(self):
        subject=self.request.get('subject')
        content=self.request.get('content')
        if subject and content:
            blog_entry=dal.add_new_post(subject,content)
            self.redirect("/blog/%d" % blog_entry.id)
        else:
            error='content cannot be empty'
            self.render("new_post.html",error)

class BlogPage(Handler):
    def get(self):
        posts=dal.get_list_of_blog_posts()
        self.render("blog.html",posts=posts)

class SignupPage(Handler):
    def get(self):
        self.render("signup.html")
    def post(self):
        name=self.request.get('username')
        password=self.request.get('password')
        verified_password=self.request.get('verified_password')
        email=self.request.get('email')
        if name!='' and password!='':
            if password==verified_password:
                dal.add_user(name,password,email)
                self.response.headers.add_header('Set-Cookie', 'user='+name+'; Path=/')
                self.redirect("/blog/welcome")
            else:
                error="Your password didn't match"
                self.render("signup.html", error = error)
           

class PermaLink(Handler):
    def get(self, id):
        post = dal.get_post(long(id))
        self.render("blog_entry.html", post = post)

class WelcomePage(Handler):
    def get(self):
        name=self.request.cookies.get('user')
        if name!='':
            self.render("welcome.html", name = name)
        else:
            self.redirect("/blog/signup")

class LogInPage(Handler):
    def get(self):
        self.render("login.html")
    def post(self):
        name=self.request.get('username')
        password=self.request.get('password')
        if name!='' and password!='':
            user=dal.get_user(name,password)
            if len(user) == 1:
                name=user[0]['name']
                self.response.headers.add_header('Set-Cookie', 'user='+name+'; Path=/')
                self.redirect("/blog/welcome")
            else:
                error = "Invalid login"
                self.render("login.html", error = error)

class LogOutPage(Handler):
    def get(self):
        self.render("login.html")
        self.response.headers.add_header('Set-Cookie', 'user=''; Path=/')
        self.redirect("/blog/signup")
               
app = webapp2.WSGIApplication([
    ('/blog', BlogPage),
    ('/blog/newpost',NewPostPage),
    ('/blog/signup',SignupPage),
    ('/blog/welcome',WelcomePage),
    ('/blog/login',LogInPage),
    ('/blog/logout',LogOutPage),
    ('/blog/(\d+)', PermaLink)
], debug=True)


def main():
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    main()