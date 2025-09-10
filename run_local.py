#!/usr/bin/env python3
"""
Quick start script for Barnacle Ballast local development
"""
import os
import sys

def setup_environment():
    """Set up local development environment"""
    
    # Create necessary directories
    directories = [
        'static/uploads',
        'static/css',
        'static/js',
        'static/images',
        'templates/public',
        'templates/crew',
        'instance'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    # Set environment variables for development
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    os.environ['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    os.environ['CREW_PASSWORD'] = 'STUDIO!@#'
    
    print("✓ Environment variables set")
    
    # Check if required packages are installed
    try:
        import flask
        import flask_sqlalchemy
        print("✓ Flask packages available")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)

def main():
    print("🦀 Barnacle Ballast Inc. - Local Setup")
    print("=" * 40)
    
    setup_environment()
    
    print("\n🎬 Ready for production!")
    print("\nNext steps:")
    print("1. Run: python app.py")
    print("2. Visit: http://localhost:5000")
    print("3. Crew Portal: http://localhost:5000/crew")
    print("   Username: ACTORVIEW")
    print("   Password: STUDIO!@#")
    print("\n📅 September 21st call sheet is pre-loaded!")

if __name__ == '__main__':
    main()

