# from app import db

# class Patient(db.Model):
#     __tablename__ = 'patients'
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(50), nullable=False)
#     last_name = db.Column(db.String(50), nullable=False)
#     date_of_birth = db.Column(db.Date, nullable=False)
#     caregiver_id = db.Column(db.Integer, db.ForeignKey('caregivers.id'))
#     image = db.Column(db.String(120))
# class Caregiver(db.Model):
#     __tablename__ = 'caregivers'
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(50), nullable=False)
#     last_name = db.Column(db.String(50), nullable=False)
#     phone_number = db.Column(db.String(15), nullable=False)
#     patients = db.relationship('Patient', back_populates='caregiver', lazy=True)