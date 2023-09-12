from . import db

class Athlete(db.Model):
    __tablename__ = "athlete"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    country = db.Column(db.String(50))
    sex = db.Column(db.String(1), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'sex': self.sex
        }
