"""
Utility functions for Barnacle Films Inc.
"""

import os
from datetime import datetime, timedelta
from flask import current_app
import json

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def get_weather_data(location="Bole's Residency"):
    """Get weather data for shoot location"""
    # This is a placeholder - in production you'd use a real weather API
    # For now, return mock data
    return {
        'location': location,
        'temperature': '72°F',
        'condition': 'Partly Cloudy',
        'humidity': '65%',
        'wind': '8 mph NW',
        'forecast': 'Good conditions for outdoor shooting',
        'updated': datetime.now().strftime('%I:%M %p')
    }

def format_countdown(target_date):
    """Format countdown to target date"""
    if isinstance(target_date, str):
        target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
    
    today = datetime.now().date()
    delta = target_date - today
    
    if delta.days < 0:
        return "Shoot completed"
    elif delta.days == 0:
        return "Today!"
    elif delta.days == 1:
        return "Tomorrow"
    else:
        return f"{delta.days} days"

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def get_file_extension(filename):
    """Get file extension from filename"""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def is_image_file(filename):
    """Check if file is an image"""
    image_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
    return get_file_extension(filename) in image_extensions

def is_video_file(filename):
    """Check if file is a video"""
    video_extensions = {'mp4', 'mov', 'avi', 'mkv', 'wmv', 'flv'}
    return get_file_extension(filename) in video_extensions

def is_document_file(filename):
    """Check if file is a document"""
    doc_extensions = {'pdf', 'doc', 'docx', 'txt', 'rtf'}
    return get_file_extension(filename) in doc_extensions

def generate_thumbnail(filepath, size=(300, 200)):
    """Generate thumbnail for image/video files"""
    # This would use PIL or similar to generate thumbnails
    # For now, return the original filepath
    return filepath

def send_notification(message, priority='normal'):
    """Send notification to crew (placeholder for future implementation)"""
    # This could integrate with email, SMS, or push notification services
    print(f"NOTIFICATION [{priority.upper()}]: {message}")

def validate_crew_access():
    """Validate crew member access (placeholder for future implementation)"""
    # This could check session, permissions, etc.
    return True

def get_production_status():
    """Get current production status"""
    return {
        'status': 'In Production',
        'project': 'Creatures in the Tall Grass',
        'phase': 'Equipment Testing',
        'next_shoot': 'September 21, 2025',
        'location': "Bole's Residency"
    }

def format_datetime(dt, format='%B %d, %Y at %I:%M %p'):
    """Format datetime object"""
    if dt is None:
        return 'Not set'
    return dt.strftime(format)

def format_date(dt, format='%B %d, %Y'):
    """Format date object"""
    if dt is None:
        return 'Not set'
    return dt.strftime(format)

def get_emergency_contacts():
    """Get emergency contact information"""
    return [
        {
            'name': 'Mac (Father)',
            'phone': '(555) 123-4567',
            'role': 'Cast - Father',
            'emergency': True
        },
        {
            'name': 'Dallas (Son)',
            'phone': '(555) 234-5678',
            'role': 'Cast - Son',
            'emergency': True
        },
        {
            'name': 'Director',
            'phone': '(555) 345-6789',
            'role': 'Director',
            'emergency': True
        },
        {
            'name': 'Production Office',
            'phone': '(555) 456-7890',
            'role': 'Production',
            'emergency': True
        }
    ]

def create_sitemap():
    """Generate sitemap for SEO"""
    sitemap = {
        'public': [
            {'url': '/', 'title': 'Home', 'priority': 1.0},
            {'url': '/about', 'title': 'About', 'priority': 0.8},
            {'url': '/projects', 'title': 'Projects', 'priority': 0.8},
            {'url': '/blog', 'title': 'Blog', 'priority': 0.7},
            {'url': '/contact', 'title': 'Contact', 'priority': 0.6}
        ],
        'crew': [
            {'url': '/crew/dashboard', 'title': 'Dashboard', 'priority': 1.0},
            {'url': '/crew/callsheets', 'title': 'Call Sheets', 'priority': 0.9},
            {'url': '/crew/scripts', 'title': 'Scripts', 'priority': 0.8},
            {'url': '/crew/schedule', 'title': 'Schedule', 'priority': 0.8},
            {'url': '/crew/dailies', 'title': 'Dailies', 'priority': 0.7},
            {'url': '/crew/gallery', 'title': 'Gallery', 'priority': 0.6},
            {'url': '/crew/contacts', 'title': 'Contacts', 'priority': 0.6},
            {'url': '/crew/documents', 'title': 'Documents', 'priority': 0.5}
        ]
    }
    return sitemap
