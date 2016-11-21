import webapp2
from google.appengine.ext import ndb
import json
import db_models

#code structure based on CS 496 lecture materials

class Book(webapp2.RequestHandler):
	#add a new book
	def post(self):
		#setup for JSON respsonse
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.write("JSON format support only.")
			return
			
		add_book = db_models.Book()
		title = self.request.get('title', default_value=None)
		rating = self.request.get('rating', default_value=None)
		name = self.request.get('name', default_value=None)
		user = self.request.get('user', default_value=None)
		
		#required fields verification
		if title and rating and name and user:
			
			#verify rating is an int
			try:
				add_book.rating = int(rating)
			except:
				self.response.status = 400
				self.response.write("Book rating must be an integer value.\n")
				return
			#verify user exists
			try:
				d = db_models.User.get_by_id(int(user))
				if d:
					add_book.user = ndb.Key(db_models.User, int(user))
				else:
					self.response.status = 404
					self.response.write("user id not found. Please POST user to add ratings.\n")
					return
			except:
				self.response.status = 400
				self.response.write("user id must be a number.\n")
				return
			
			add_book.title = title
			add_book.name = name
			
			key = add_book.put()
			
			#add rating to user ratings list
			u = db_models.User.get_by_id(int(user))
			u.ratings.append(ndb.Key(db_models.Book, add_book.key.id()))
			u.put()
			
			out = add_book.to_dict()
			self.response.write("Book rating added to database.\n")
			return
		
		else:
			self.response.status = 400
			self.response.status_message = "Title, rating, and user all all required.\n"
			return
	
	#return book details
	def get(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.write("JSON format support only.")
			return
		else:
			name = self.request.get('name', default_value=None)
			d = db_models.Book.query(db_models.Book.name == name)
			keys = d.fetch(keys_only=False)
			results = { 'titles' : [x.title for x in keys],'ratings' : [x.rating for x in keys]}
			self.response.write(json.dumps(results))
			return
				
	#update rating
	def put(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.write("JSON format support only.")
			return
		
		if 'id' in kwargs:
			new_rating = ndb.Key(db_models.Book, int(kwargs['id'])).get()
			rating = self.request.get('rating', default_value=None)
			if rating:
				try:
					new_rating.rating = int(rating)
				except:
					self.response.status = 400
					self.response.write("Rating must be an integer value.\n")
					return
			new_rating.put()
			out = new_rating.to_dict()
			self.response.write("Book rating edited.\n")
			return
		else:
			self.response.status = 403
			self.response.write("Only rating for single Book can be changed.\n")
			return
			
	#delete Book		
	def delete(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.write("JSON format support only.")
			return
		if 'id' in kwargs:
			delete_book = ndb.Key(db_models.Book, int(kwargs['id'])).get()
			user = self.request.get('user', default_value=None)
			d = db_models.User.get_by_id(int(user))
			#if book rating exists for user, delete from user list
			if d.ratings:
				new_list = []
				for r in d.ratings:
					if r.id() != delete_book.key.id():
						new_list.append(r)
				d.ratings = new_list
				d.put()
			delete_book.key.delete()
			self.response.write("Book rating deleted.\n")
		else:
			self.response.status = 403
			self.response.write("Book ID does not exist.\n")
			return
			
	