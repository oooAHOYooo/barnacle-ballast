#!/usr/bin/env python3
"""
Quick start script for Barnacle Films local development
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

def main():
    print("🦀 BARNACLE - Local Setup")
    print("=" * 40)
    
    setup_environment()
    
    # Find available port
    port = find_available_port(5000, 20)
    
    print("\n🎬 Ready for production!")
    print("\nNext steps:")
    print("1. Run: python app.py")
    if port:
        print(f"2. Visit: http://localhost:{port}")
        print(f"3. Crew Portal: http://localhost:{port}/crew/login")
    else:
        print("2. Visit: http://localhost:5000 (or next available port)")
        print("3. Crew Portal: http://localhost:5000/crew/login")
    print("   Password: STUDIO!@#")
    print("\n📅 September 21st call sheet is pre-loaded!")
    print("\n🔧 The app will automatically find an available port!")

if __name__ == '__main__':
    main()

