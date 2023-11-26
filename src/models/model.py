import pydantic
import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()

class BaseModel(pydantic.BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {
            db.Model: lambda m: m.to_dict() if hasattr(m, 'to_dict') else m.__dict__
        }
        SQLALCHEMY_DATABASE_URI = 'sqlite:///resumeCreator.db'  # Replace this with your actual database connection string
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=True)
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.Text, nullable=True)
    state = db.Column(db.Text, nullable=True)
    zip = db.Column(db.Text, nullable=True)
    country = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    resumes = db.relationship('Resume', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'name': self.name,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip': self.zip,
            'country': self.country,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'resumes': self.resumes
        }
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def get_id(self):
        return str(self.id)  # Assuming your ID is an integer or string

    @property
    def is_authenticated(self):
        # Check if the user is authenticated (e.g., if the user has valid credentials)
        return True  # Return True if the user is authenticated, otherwise False

    @property
    def is_active(self):
        # Check if the user account is active
        return True  # Return True if the user account is active, otherwise False

    @property
    def is_anonymous(self):
        # Check if the user is an anonymous user (not logged in)
        return False  # Return False as this user is not anonymous
    
class Resume(db.Model):
    __tablename__ = 'resumes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resume_name = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    sections = db.relationship('Section', backref='resume', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'resume_name': self.resume_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'sections': self.sections
        }
    
class Section(db.Model):
    __tablename__ = 'sections'
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    section_name = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    fields = db.relationship('Field', backref='section', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'resume_id': self.resume_id,
            'section_name': self.section_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'fields': self.fields
        }
    
class Field(db.Model):
    __tablename__ = 'fields'
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)
    field_name = db.Column(db.Text, nullable=False)
    field_value = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'section_id': self.section_id,
            'field_name': self.field_name,
            'field_value': self.field_value,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
class Education(db.Model):
    __tablename__ = 'educations'
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    education_name = db.Column(db.Text, nullable=False)
    education_start_date = db.Column(db.DateTime, nullable=False)
    education_end_date = db.Column(db.DateTime, nullable=False)
    education_location = db.Column(db.Text, nullable=False)
    education_description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'resume_id': self.resume_id,
            'education_name': self.education_name,
            'education_start_date': self.education_start_date,
            'education_end_date': self.education_end_date,
            'education_location': self.education_location,
            'education_description': self.education_description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
class Experience(db.Model):
    __tablename__ = 'experiences'
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    experience_name = db.Column(db.Text, nullable=False)
    experience_start_date = db.Column(db.DateTime, nullable=False)
    experience_end_date = db.Column(db.DateTime, nullable=False)
    experience_location = db.Column(db.Text, nullable=False)
    experience_description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'resume_id': self.resume_id,
            'experience_name': self.experience_name,
            'experience_start_date': self.experience_start_date,
            'experience_end_date': self.experience_end_date,
            'experience_location': self.experience_location,
            'experience_description': self.experience_description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    skill_name = db.Column(db.Text, nullable=False)
    skill_level = db.Column(db.Text, nullable=False)
    skill_description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'resume_id': self.resume_id,
            'skill_name': self.skill_name,
            'skill_level': self.skill_level,
            'skill_description': self.skill_description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

