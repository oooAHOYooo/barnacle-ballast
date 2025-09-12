"""
Database Models for Barnacle Films Inc.
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Import db from app to avoid circular imports
from app import db

class User(db.Model):
    """User model for role-based access"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='crew')  # director, cast, crew, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class CallSheet(db.Model):
    """Call sheet model for production scheduling"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    call_time = db.Column(db.String(20), nullable=False)
    wrap_time = db.Column(db.String(20), nullable=False)
    weather_contingency = db.Column(db.Text)
    cast_notes = db.Column(db.Text)
    crew_notes = db.Column(db.Text)
    special_notes = db.Column(db.Text)
    scenes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<CallSheet {self.title} - {self.date}>'

class BlogPost(db.Model):
    """Blog post model for public site content"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text)
    featured_image = db.Column(db.String(200))
    published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<BlogPost {self.title}>'

class Document(db.Model):
    """Document model for file uploads"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    filepath = db.Column(db.String(300), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)  # script, sides, dailies, photo, document
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(100))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<Document {self.title}>'

class Contact(db.Model):
    """Contact model for cast, crew, and vendor directory"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    emergency_contact = db.Column(db.Boolean, default=False)
    department = db.Column(db.String(50))  # cast, camera, sound, production, etc.
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Contact {self.name} - {self.role}>'

class Scene(db.Model):
    """Scene model for master scene breakdown"""
    id = db.Column(db.Integer, primary_key=True)
    scene_number = db.Column(db.Integer, nullable=False, unique=True)
    title = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    time_of_day = db.Column(db.String(50), nullable=False)  # DAY, NIGHT, DAWN, DUSK
    scene_type = db.Column(db.String(50), nullable=False)  # INT, EXT, INT/EXT
    description = db.Column(db.Text)
    characters = db.Column(db.Text)  # JSON string of character names
    estimated_duration = db.Column(db.String(20))  # e.g., "2-3 minutes"
    status = db.Column(db.String(20), default='planned')  # planned, shot, in_progress, completed
    call_sheet_id = db.Column(db.Integer, db.ForeignKey('call_sheet.id'), nullable=True)
    shot_count = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Scene {self.scene_number}: {self.title}>'

class Announcement(db.Model):
    """Announcement model for crew communications"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    target_audience = db.Column(db.String(50), default='all')  # all, cast, crew, specific department
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    created_by = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<Announcement {self.title}>'
