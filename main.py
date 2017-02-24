import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Post(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class MainPage(Handler):
    def render_front(self, title="", content="", error=""):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")

        self.render("front.html", title=title, content=content, error=error, posts=posts)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")

        if title and content:
            a = Post(title = title, content = content)
            a.put()
            self.redirect("/")

        else:
            error = "We need both a title and some content."
            self.render_front(error = error, title = title, content = content)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
