import webapp2
from google.appengine.ext import ndb
import json
import db_models

#code structure based on CS 496 lecture materials

class User(webapp2.RequestHandler):
	def post(self):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.write("JSON format support only.")
			return
		
		add_user = db_models.User()
		username = self.request.get('username', default_value=None)
		
		if username:
			#check if name already exists
			d = db_models.User.query(db_models.User.username == username)
			match_u = d.fetch()
			if match_u:
				self.response.status = 400
				self.response.write("That username already exists.\n")
				return
			add_user.username = username
			
			key = add_user.put()
			out = add_user.to_dict()
			self.response.write(json.dumps(out))
			return
			
		else:
			self.response.status = 400
			self.response.write("Unique username is required.\n")
			return
