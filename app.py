#!/usr/bin/env python3
"""
Barnacle Ballast Inc. - Main Flask Application
Production Management System for Independent Filmmaking
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import json
from config import config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config['development'])

# Initialize database
db = SQLAlchemy(app)

# Define models here to avoid circular imports
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

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

# Import forms
from forms import ContactForm, CrewLoginForm, CallSheetForm, BlogPostForm

# Import utilities
from utils import allowed_file, get_weather_data, format_countdown

# Routes for Public Site
@app.route('/')
def index():
    """Homepage with hero section and latest blog posts"""
    recent_posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).limit(3).all()
    return render_template('public/index.html', posts=recent_posts)

@app.route('/about')
def about():
    """About page with studio mission and director bio"""
    return render_template('public/about.html')

@app.route('/projects')
def projects():
    """Projects showcase page"""
    return render_template('public/projects.html')

@app.route('/blog')
def blog():
    """Blog listing page"""
    posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).all()
    return render_template('public/blog.html', posts=posts)

@app.route('/blog/<int:post_id>')
def blog_post(post_id):
    """Individual blog post page"""
    post = BlogPost.query.get_or_404(post_id)
    return render_template('public/post.html', post=post)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact form page"""
    form = ContactForm()
    if form.validate_on_submit():
        # Here you would typically save to database or send email
        flash('Thank you for your message! We\'ll get back to you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('public/contact.html', form=form)

# Crew Portal Routes
@app.route('/crew/login', methods=['GET', 'POST'])
def crew_login():
    """Crew portal login"""
    if session.get('crew_logged_in'):
        return redirect(url_for('crew_dashboard'))
    
    form = CrewLoginForm()
    if form.validate_on_submit():
        if form.password.data == app.config['CREW_PASSWORD']:
            session['crew_logged_in'] = True
            session.permanent = True
            flash('Welcome to the crew portal!', 'success')
            return redirect(url_for('crew_dashboard'))
        else:
            flash('Invalid password. Please try again.', 'error')
    
    return render_template('crew/login.html', form=form)

@app.route('/crew/logout')
def crew_logout():
    """Crew portal logout"""
    session.pop('crew_logged_in', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('crew_login'))

@app.route('/crew/dashboard')
def crew_dashboard():
    """Crew dashboard with today's overview"""
    if not session.get('crew_logged_in'):
        return redirect(url_for('crew_login'))
    
    # Get today's call sheet
    today = datetime.now().date()
    todays_call_sheet = CallSheet.query.filter_by(date=today).first()
    
    # Get weather data
    weather = get_weather_data()
    
    # Get recent announcements
    recent_posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).limit(3).all()
    
    return render_template('crew/dashboard.html', 
                         call_sheet=todays_call_sheet, 
                         weather=weather,
                         posts=recent_posts)

@app.route('/crew/callsheets')
def crew_callsheets():
    """Call sheets management"""
    if not session.get('crew_logged_in'):
        return redirect(url_for('crew_login'))
    
    call_sheets = CallSheet.query.order_by(CallSheet.date.desc()).all()
    return render_template('crew/callsheets.html', call_sheets=call_sheets)

@app.route('/crew/callsheets/<int:sheet_id>')
def crew_callsheet_detail(sheet_id):
    """Individual call sheet view"""
    if not session.get('crew_logged_in'):
        return redirect(url_for('crew_login'))
    
    call_sheet = CallSheet.query.get_or_404(sheet_id)
    return render_template('crew/callsheet_detail.html', call_sheet=call_sheet)

@app.route('/crew/scripts')
def crew_scripts():
    """Scripts and sides page"""
    if not session.get('crew_logged_in'):
        return redirect(url_for('crew_login'))
    
    scripts = Document.query.filter_by(document_type='script').order_by(Document.created_at.desc()).all()
    sides = Document.query.filter_by(document_type='sides').order_by(Document.created_at.desc()).all()
    
    return render_template('crew/scripts.html', scripts=scripts, sides=sides)

@app.route('/crew/storyboards')
def crew_storyboards():
    """Crew storyboards page"""
    if not session.get('crew_logged_in'):
        return redirect(url_for('crew_login'))
    
    # Get storyboards and visual references from database
    storyboards = Document.query.filter(
        (Document.document_type == 'document') & 
        (Document.title.contains('Storyboard'))
    ).order_by(Document.created_at.desc()).all()
    
    visual_refs = Document.query.filter(
        (Document.document_type == 'photo') | 
        (Document.document_type == 'document')
    ).filter(
        (Document.title.contains('Location')) |
        (Document.title.contains('Character')) |
        (Document.title.contains('Reference'))
    ).order_by(Document.created_at.desc()).all()
    
    return render_template('crew/storyboards.html', storyboards=storyboards, visual_refs=visual_refs)

@app.route('/crew/schedule')
def crew_schedule():
    """Production schedule calendar"""
    if not session.get('crew_logged_in'):
        return redirect(url_for('crew_login'))
    
    call_sheets = CallSheet.query.order_by(CallSheet.date).all()
    today = datetime.now().date()
    return render_template('crew/schedule.html', call_sheets=call_sheets, today=today)

@app.route('/crew/dailies')
def crew_dailies():
    """Daily footage review"""
    if not session.get('crew_logged_in'):
        return redirect(url_for('crew_login'))
    
    dailies = Document.query.filter_by(document_type='dailies').order_by(Document.created_at.desc()).all()
    return render_template('crew/dailies.html', dailies=dailies)

@app.route('/crew/gallery')
def crew_gallery():
    """Photo gallery"""
    if not session.get('crew_logged_in'):
        return redirect(url_for('crew_login'))
    
    photos = Document.query.filter_by(document_type='photo').order_by(Document.created_at.desc()).all()
    return render_template('crew/gallery.html', photos=photos)

@app.route('/crew/contacts')
def crew_contacts():
    """Contact directory"""
    if not session.get('crew_logged_in'):
        return redirect(url_for('crew_login'))
    
    contacts = Contact.query.order_by(Contact.name).all()
    return render_template('crew/contacts.html', contacts=contacts)

@app.route('/crew/documents')
def crew_documents():
    """Document management"""
    if not session.get('crew_logged_in'):
        return redirect(url_for('crew_login'))
    
    documents = Document.query.order_by(Document.created_at.desc()).all()
    return render_template('crew/documents.html', documents=documents)

# API Routes
@app.route('/api/weather')
def api_weather():
    """Weather API endpoint"""
    weather = get_weather_data()
    return jsonify(weather)

@app.route('/api/countdown')
def api_countdown():
    """Countdown to next shoot API"""
    next_shoot = CallSheet.query.filter(CallSheet.date >= datetime.now().date()).order_by(CallSheet.date).first()
    if next_shoot:
        return jsonify({
            'target_date': next_shoot.date.isoformat(),
            'countdown': format_countdown(next_shoot.date)
        })
    return jsonify({'countdown': 'No upcoming shoots'})

# File upload handling
@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads"""
    if not session.get('crew_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Create document record
        doc = Document(
            filename=filename,
            filepath=filepath,
            document_type=request.form.get('type', 'document'),
            title=request.form.get('title', filename)
        )
        db.session.add(doc)
        db.session.commit()
        
        return jsonify({'success': True, 'filename': filename})
    
    return jsonify({'error': 'Invalid file type'}), 400

# Error handlers
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon/favicon.ico')

@app.route('/view/<int:doc_id>')
def view_document(doc_id):
    """View document in PDF viewer"""
    if not session.get('crew_logged_in'):
        return redirect(url_for('crew_login'))
    
    document = Document.query.get_or_404(doc_id)
    return render_template('crew/document_viewer.html', document=document)

@app.route('/download/<int:doc_id>')
def download_document(doc_id):
    """Download document file"""
    if not session.get('crew_logged_in'):
        return redirect(url_for('crew_login'))
    
    document = Document.query.get_or_404(doc_id)
    return send_file(f'static/{document.filepath}', as_attachment=True, download_name=document.filename)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

# Initialize database
def create_tables():
    """Create database tables and initial data"""
    with app.app_context():
        db.create_all()
        
        # Create initial call sheet for September 21st
        if not CallSheet.query.filter_by(date=datetime(2025, 9, 21).date()).first():
            call_sheet = CallSheet(
                title="Creatures in the Tall Grass - Equipment Test",
                date=datetime(2025, 9, 21).date(),
                location="Bole's Residency",
                call_time="1:00 PM",
                wrap_time="5:00 PM",
                weather_contingency="Indoor/Outdoor options available",
                cast_notes="Mac (Father), Dallas (Son) - Character chemistry tests",
                crew_notes="Director, Camera Op, Script Supervisor",
                special_notes="RED KOMODO vs BMPCC4K comparison",
                scenes="Equipment tests and character chemistry"
            )
            db.session.add(call_sheet)
            db.session.commit()

        # Create sample scripts and storyboards
        if not Document.query.filter_by(document_type='script').first():
            # Main Script
            main_script = Document(
                title="BARNACLE - Main Script",
                filename="barnacle_main_script.pdf",
                document_type='script',
                filepath='documents/scripts/barnacle_main_script.pdf',
                description='Complete feature script - A Father. A Son. A Marsh That Remembers Everything.',
                created_by='Director'
            )
            db.session.add(main_script)

            # Shooting Script
            shooting_script = Document(
                title="BARNACLE - Shooting Script v2.1",
                filename="barnacle_shooting_script_v2.1.pdf",
                document_type='script',
                filepath='documents/scripts/barnacle_shooting_script_v2.1.pdf',
                description='Revised shooting script with scene numbers and technical notes',
                created_by='Director'
            )
            db.session.add(shooting_script)

            # Sides for September 21st
            sides_921 = Document(
                title="Sides - September 21st",
                filename="sides_sept_21.pdf",
                document_type='sides',
                filepath='documents/sides/sides_sept_21.pdf',
                description='Daily sides for equipment test day - Mac and Dallas scenes',
                created_by='Script Supervisor'
            )
            db.session.add(sides_921)

            # Storyboards
            storyboard_1 = Document(
                title="BARNACLE - Storyboards Part 1",
                filename="barnacle_storyboards_part1.pdf",
                document_type='document',
                filepath='documents/storyboards/barnacle_storyboards_part1.pdf',
                description='Visual storyboards for opening sequences and marsh scenes',
                created_by='Director'
            )
            db.session.add(storyboard_1)

            storyboard_2 = Document(
                title="BARNACLE - Storyboards Part 2",
                filename="barnacle_storyboards_part2.pdf",
                document_type='document',
                filepath='documents/storyboards/barnacle_storyboards_part2.pdf',
                description='Storyboards for father-son dialogue scenes and climax',
                created_by='Director'
            )
            db.session.add(storyboard_2)

            # Production Documents
            production_bible = Document(
                title="BARNACLE - Production Bible",
                filename="barnacle_production_bible.pdf",
                document_type='document',
                filepath='documents/production/barnacle_production_bible.pdf',
                description='Complete production guide with character backgrounds, locations, and technical specs',
                created_by='Producer'
            )
            db.session.add(production_bible)

            # Location Scouting
            location_photos = Document(
                title="Location Scouting Photos",
                filename="location_scouting_photos.pdf",
                document_type='photo',
                filepath='documents/locations/location_scouting_photos.pdf',
                description='Reference photos from Bole\'s Residency and surrounding marsh areas',
                created_by='Location Manager'
            )
            db.session.add(location_photos)

            # Character References
            character_refs = Document(
                title="Character Reference Guide",
                filename="character_reference_guide.pdf",
                document_type='document',
                filepath='documents/characters/character_reference_guide.pdf',
                description='Character descriptions, motivations, and relationship dynamics',
                created_by='Director'
            )
            db.session.add(character_refs)

            db.session.commit()

def find_available_port(start_port=5000, max_attempts=10):
    """Find an available port starting from start_port"""
    import socket
    
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', port))
                return port
        except OSError:
            continue
    return None

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create initial call sheet for September 21st
        create_tables()
    
    # Try to find an available port
    port = find_available_port(5000, 20)  # Try ports 5000-5019
    if port:
        print(f"🚀 Starting BARNACLE on port {port}")
        print(f"🌐 Access at: http://localhost:{port}")
        print(f"🔑 Crew Portal: http://localhost:{port}/crew/login")
        app.run(debug=True, host='0.0.0.0', port=port)
    else:
        print("❌ No available ports found. Please free up a port and try again.")
        exit(1)
