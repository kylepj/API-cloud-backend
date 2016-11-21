import webapp2
import book
import user

#code structure based on CS 496 lecture materials

app = webapp2.WSGIApplication([('/user', 'user.User'),('/book', 'book.Book')], debug=True)
app.router.add(webapp2.Route(r'/book/<id:[0-9]+><:/?>', 'book.Book'))
