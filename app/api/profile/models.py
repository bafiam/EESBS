
from appConfig import db, flask_bcrypt


class UserProfile(db.Model):

    __tablename__="profile"
     
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    till = db.Column(db.Integer,nullable=True)
    phone = db.Column(db.Integer, nullable=False)
    company_no = db.Column(db.String(255))
    about_me = db.Column(db.Text(),nullable=False)
    avatar_hash = db.Column(db.String(32))
    user_id = db.Column(db.Integer, db.ForeignKey('user.public_id'), unique=True)
    users=db.relationship('User', backref='profiles', uselist=False)

    def __repr__(self):
        return "<UserProfile '{}'>".format(self.name)
