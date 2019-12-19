import random, datetime

#### PERSON CLASS
class Person():

	def __init__(self):
		self.reset()

	def reset(self):
		self.id = 0
		self.name = None
		self.age = 0
		self.sex = None
		self.created_at = None
		self.updated_at = None
		self.deleted_at = None

	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'age': self.age,
			'sex': self.sex,
			'created_at': self.created_at,
			'updated_at': self.updated_at,
			'deleted_at': self.deleted_at
		}

#### Class for save data temporelly
class Persons():

	persons = []

	def __init__(self):
		for i in range(15):
			person = Person()
			person.id = i
			person.name = "Person ke %d" % (i)
			person.age = random.randrange(1, 80)
			person.sex = random.choice(["male", "female"])
			self.persons.append(person.serialize())

	def get_list(self):
		return self.persons

	def add(self, person):
		person.created_at = str(datetime.datetime.now())
		self.persons.append(person.serialize())

	def get_one(self, id):
		for _, v in enumerate(self.persons):
			if int(v['id']) == int(id):
				return v
		return None

	def edit_one(self, id, name, age, sex):
		for k, v in enumerate(self.persons):
			if int(v['id']) == int(id):
				person = Person()
				person.id = id
				person.name = name if name != None else v['name'] 
				person.age = age if age != None else v['age']
				person.sex = sex if sex != None else v['sex']
				person.created_at = v['created_at']
				person.updated_at = str(datetime.datetime.now())
				person.deleted_at = v['deleted_at']
				self.persons[k] = person.serialize()
				return person
		return None
	
	def edit_one_obj(self, id, person_obj):
		for k, v in enumerate(self.persons):
			if int(v['id']) == int(person_obj.id):
				person_obj.id = v['id']
				self.persons[k] = person_obj.serialize()
				return person_obj
		return None

	def delete_one(self, id):
		for k, v in enumerate(self.persons):
			if int(v['id']) == int(id):
				person = Person()
				person = v
				person.deleted_at = str(datetime.datetime.now())
				self.persons[k] = person.serialize()
				return person
		return None
