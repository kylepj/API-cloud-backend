from google.appengine.ext import ndb

#code structure based on CS 496 lecture materials

#dict function to return key per lecture
class Model(ndb.Model):
	def to_dict(self):
		d = super(Model, self).to_dict()
		d['key'] = self.key.id()
		return d
		
class Book(Model):
	title = ndb.StringProperty(required=True)
	rating = ndb.IntegerProperty(required=True)
	name = ndb.StringProperty(required=True)
	user = ndb.KeyProperty(required=True)
	
class User(Model):
	username = ndb.StringProperty(required=True)
	ratings = ndb.KeyProperty(repeated=True)
	
	#key-value pairs for ratings keys list
	def to_dict(self):
		d = super(User, self).to_dict()
		d['ratings'] = [x.id() for x in d['ratings']]
		return d
		
		
		
