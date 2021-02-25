from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    favorites = db.relationship('Favorite', lazy=True) #los favoritos del usuario

    def __repr__(self):
        return '<User %r>' % self.name
    
    def passwordHider(self, passw):
        hiddenPass = ''
        for i in range(len(passw)):
            hiddenPass += '*'
        return hiddenPass
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "password": self.passwordHider(self.password),
            "favorites": list(map(lambda x: x.serialize(), self.favorites)) #los favoritos
            # do not serialize the password, its a security breach
        }

# Parent para el one to many
class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(50), nullable=False)
    diameter = db.Column(db.String(50), nullable=False)
    gravity = db.Column(db.String(50), nullable=False)
    population = db.Column(db.String(50), nullable=False)
    terrain = db.Column(db.String(50), nullable=False)
    children = db.relationship('Character', lazy=True) #los personajes

    def __repr__(self):
        return '<Planet %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "population": self.population,
            "terrain": self.terrain,
            "Characters": list(map(lambda x: x.serialize(), self.children)) #los personajes
            # do not serialize the password, its a security breach
        }

#Child para el one to many
class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    birth_year = db.Column(db.String(50), nullable=False)
    height = db.Column(db.String(50), nullable=False)
    mass = db.Column(db.String(50), nullable=False)
    hair_color = db.Column(db.String(50), nullable=False)
    eye_color = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))

    def __repr__(self):
        return '<Character %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "planet_id": self.planet_id
        }

class Favorite(db.Model):
    #__tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    character = db.relationship('Character', lazy=True) #los personajes favoritos
    planet = db.relationship('Planet', lazy=True) #los planetas favoritos

    def __repr__(self):
        return '<Favorite %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
            "character": self.character.serialize(), #los favoritos personajes
            "planet": self.planet.serialize() #los favoritos planetas
        }