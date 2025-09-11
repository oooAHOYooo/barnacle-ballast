/**
 * Crew Portal JavaScript for Barnacle Ballast Inc.
 * Enhanced functionality for crew members
 */

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize crew-specific features
    initializeCrewFeatures();
    
    // Set up real-time updates
    setupRealTimeUpdates();
    
    // Initialize file upload handlers
    initializeFileUploads();
    
    // Set up mobile optimizations
    setupMobileOptimizations();
});

function initializeCrewFeatures() {
    // Auto-refresh weather data every 5 minutes
    if (document.getElementById('weather-widget')) {
        setInterval(updateWeatherWidget, 300000);
    }
    
    // Auto-refresh countdown every minute
    if (document.getElementById('countdown')) {
        setInterval(updateCountdownWidget, 60000);
    }
    
    // Initialize emergency contact quick dial
    initializeEmergencyContacts();
    
    // Set up call sheet notifications
    setupCallSheetNotifications();
}

function setupRealTimeUpdates() {
    // Update dashboard data every 30 seconds
    if (window.location.pathname.includes('/crew/dashboard')) {
        setInterval(updateDashboardData, 30000);
    }
    
    // Update schedule data every minute
    if (window.location.pathname.includes('/crew/schedule')) {
        setInterval(updateScheduleData, 60000);
    }
}

function initializeFileUploads() {
    const uploadForms = document.querySelectorAll('form[enctype="multipart/form-data"]');
    
    uploadForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            handleFileUpload(this);
        });
    });
    
    // Drag and drop file upload
    const dropZones = document.querySelectorAll('.file-drop-zone');
    dropZones.forEach(zone => {
        zone.addEventListener('dragover', handleDragOver);
        zone.addEventListener('drop', handleFileDrop);
    });
}

function setupMobileOptimizations() {
    // Add touch-friendly interactions
    const touchElements = document.querySelectorAll('.btn, .card, .nav-link');
    touchElements.forEach(element => {
        element.addEventListener('touchstart', function() {
            this.classList.add('touch-active');
        });
        
        element.addEventListener('touchend', function() {
            setTimeout(() => {
                this.classList.remove('touch-active');
            }, 150);
        });
    });
    
    // Optimize images for mobile
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        if (window.innerWidth < 768) {
            img.classList.add('img-fluid');
        }
    });
}

// Weather widget functionality
async function updateWeatherWidget() {
    try {
        const weatherData = await fetch('/api/weather');
        const data = await weatherData.json();
        
        const widget = document.getElementById('weather-widget');
        if (widget) {
            widget.innerHTML = `
                <div class="text-center">
                    <div class="fs-4 text-primary">${data.temperature}</div>
                    <div class="small text-muted">${data.condition}</div>
                    <div class="small text-muted">${data.location}</div>
                    <div class="small text-muted">Updated: ${data.updated}</div>
                </div>
            `;
        }
    } catch (error) {
        console.error('Weather update failed:', error);
    }
}

// Countdown widget functionality
async function updateCountdownWidget() {
    try {
        const countdownData = await fetch('/api/countdown');
        const data = await countdownData.json();
        
        const countdown = document.getElementById('countdown');
        if (countdown) {
            countdown.textContent = data.countdown;
        }
    } catch (error) {
        console.error('Countdown update failed:', error);
    }
}

// Emergency contact functionality
function initializeEmergencyContacts() {
    const emergencyButtons = document.querySelectorAll('.emergency-contact');
    
    emergencyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const phone = this.querySelector('small').textContent;
            if (phone) {
                // On mobile, this will open the phone dialer
                window.location.href = `tel:${phone.replace(/[^\d]/g, '')}`;
            }
        });
    });
}

// Call sheet notifications
function setupCallSheetNotifications() {
    // Check for urgent call sheet updates
    const callSheets = document.querySelectorAll('.card[data-call-sheet]');
    
    callSheets.forEach(sheet => {
        const date = new Date(sheet.dataset.callSheet);
        const today = new Date();
        const diffTime = date - today;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays === 0) {
            sheet.classList.add('border-warning');
            sheet.querySelector('.card-header').innerHTML += '<span class="badge bg-warning ms-2">TODAY</span>';
        } else if (diffDays === 1) {
            sheet.classList.add('border-info');
            sheet.querySelector('.card-header').innerHTML += '<span class="badge bg-info ms-2">TOMORROW</span>';
        }
    });
}

// File upload handling
async function handleFileUpload(form) {
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    
    // Show loading state
    submitButton.textContent = 'Uploading...';
    submitButton.disabled = true;
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showNotification('File uploaded successfully!', 'success');
            form.reset();
        } else {
            showNotification(result.error || 'Upload failed', 'error');
        }
    } catch (error) {
        showNotification('Upload failed: ' + error.message, 'error');
    } finally {
        submitButton.textContent = originalText;
        submitButton.disabled = false;
    }
}

// Drag and drop file handling
function handleDragOver(e) {
    e.preventDefault();
    e.currentTarget.classList.add('drag-over');
}

function handleFileDrop(e) {
    e.preventDefault();
    e.currentTarget.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const fileInput = e.currentTarget.querySelector('input[type="file"]');
        if (fileInput) {
            fileInput.files = files;
            // Trigger form submission
            const form = fileInput.closest('form');
            if (form) {
                handleFileUpload(form);
            }
        }
    }
}

// Dashboard data updates
async function updateDashboardData() {
    // Update any dynamic dashboard content
    await updateWeatherWidget();
    await updateCountdownWidget();
}

// Schedule data updates
async function updateScheduleData() {
    // Refresh schedule information
    const scheduleCards = document.querySelectorAll('.schedule-card');
    
    scheduleCards.forEach(card => {
        // Add subtle animation to indicate update
        card.classList.add('updated');
        setTimeout(() => {
            card.classList.remove('updated');
        }, 1000);
    });
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Quick actions for crew members
function quickCall(phoneNumber) {
    window.location.href = `tel:${phoneNumber}`;
}

function quickEmail(emailAddress) {
    window.location.href = `mailto:${emailAddress}`;
}

function quickSMS(phoneNumber) {
    window.location.href = `sms:${phoneNumber}`;
}

// Password protection for sides
let currentSide = null;

function showPasswordModal(sideId) {
    currentSide = sideId;
    const modal = new bootstrap.Modal(document.getElementById('passwordModal'));
    modal.show();
    
    // Clear previous input and error
    document.getElementById('passwordInput').value = '';
    document.getElementById('passwordError').style.display = 'none';
}

function checkPassword() {
    const password = document.getElementById('passwordInput').value;
    const errorDiv = document.getElementById('passwordError');
    
    // Simple password check - in production, this would be server-side
    const correctPasswords = {
        'side1': 'macdallas2025',
        'side2': 'dominicdallas2025'
    };
    
    if (password === correctPasswords[currentSide]) {
        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('passwordModal'));
        modal.hide();
        
        // Open the document
        if (currentSide === 'side1') {
            window.open('/static/documents/sides/CINTG_SIDE_1_Mac and Dallas - Draft 1.pdf', '_blank');
        } else if (currentSide === 'side2') {
            showNotification('Side 2 is still in development', 'info');
        }
    } else {
        errorDiv.style.display = 'block';
        document.getElementById('passwordInput').value = '';
    }
}

// Handle Enter key in password input
document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('passwordInput');
    if (passwordInput) {
        passwordInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                checkPassword();
            }
        });
    }
});

// Export crew-specific functions
window.CrewPortal = {
    updateWeatherWidget,
    updateCountdownWidget,
    showNotification,
    quickCall,
    quickEmail,
    quickSMS,
    handleFileUpload,
    showPasswordModal,
    checkPassword
};
