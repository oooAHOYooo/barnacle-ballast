"""
WTForms for Barnacle Films Inc.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField, DateField, TimeField, FileField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, URL
from wtforms.widgets import TextArea

class ContactForm(FlaskForm):
    """Contact form for public site"""
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=5, max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Send Message')

class CrewLoginForm(FlaskForm):
    """Crew portal login form"""
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class CallSheetForm(FlaskForm):
    """Call sheet creation/editing form"""
    title = StringField('Production Title', validators=[DataRequired(), Length(min=5, max=200)])
    date = DateField('Shoot Date', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), Length(min=2, max=200)])
    call_time = TimeField('Call Time', validators=[DataRequired()])
    wrap_time = TimeField('Wrap Time', validators=[DataRequired()])
    weather_contingency = TextAreaField('Weather Contingency', validators=[Optional()])
    cast_notes = TextAreaField('Cast Notes', validators=[Optional()])
    crew_notes = TextAreaField('Crew Notes', validators=[Optional()])
    special_notes = TextAreaField('Special Notes', validators=[Optional()])
    scenes = TextAreaField('Scenes to be Shot', validators=[Optional()])
    submit = SubmitField('Save Call Sheet')

class BlogPostForm(FlaskForm):
    """Blog post creation/editing form"""
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=200)])
    slug = StringField('URL Slug', validators=[DataRequired(), Length(min=5, max=200)])
    content = TextAreaField('Content', validators=[DataRequired()], widget=TextArea())
    excerpt = TextAreaField('Excerpt', validators=[Optional()])
    featured_image = StringField('Featured Image URL', validators=[Optional(), URL()])
    published = BooleanField('Publish Immediately')
    submit = SubmitField('Save Post')

class ContactDirectoryForm(FlaskForm):
    """Contact directory form"""
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    role = StringField('Role/Position', validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField('Phone', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email()])
    department = SelectField('Department', choices=[
        ('cast', 'Cast'),
        ('camera', 'Camera'),
        ('sound', 'Sound'),
        ('production', 'Production'),
        ('art', 'Art Department'),
        ('costume', 'Costume'),
        ('makeup', 'Makeup'),
        ('transportation', 'Transportation'),
        ('catering', 'Catering'),
        ('other', 'Other')
    ])
    emergency_contact = BooleanField('Emergency Contact')
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Add Contact')

class DocumentUploadForm(FlaskForm):
    """Document upload form"""
    title = StringField('Document Title', validators=[DataRequired(), Length(min=2, max=200)])
    document_type = SelectField('Document Type', choices=[
        ('script', 'Script'),
        ('sides', 'Sides'),
        ('dailies', 'Dailies'),
        ('photo', 'Photo'),
        ('document', 'General Document')
    ], validators=[DataRequired()])
    file = FileField('File', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Upload Document')

class AnnouncementForm(FlaskForm):
    """Announcement creation form"""
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=200)])
    content = TextAreaField('Content', validators=[DataRequired()], widget=TextArea())
    priority = SelectField('Priority', choices=[
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], default='normal')
    target_audience = SelectField('Target Audience', choices=[
        ('all', 'All Crew'),
        ('cast', 'Cast Only'),
        ('crew', 'Crew Only'),
        ('camera', 'Camera Department'),
        ('sound', 'Sound Department'),
        ('production', 'Production Department')
    ], default='all')
    submit = SubmitField('Create Announcement')
