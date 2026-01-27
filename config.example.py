"""
Configuration Template
Copy this file to config.py and update with your settings
"""

# ==============================================
# DATABASE CONFIGURATION
# ==============================================
# Update these with your MySQL credentials

DB_CONFIG = {
    'host': 'localhost',           # Usually 'localhost'
    'user': 'root',                # Your MySQL username
    'password': 'your_password',   # Your MySQL password - CHANGE THIS!
    'database': 'FCS3',            # Database name (must exist)
    'charset': 'utf8mb4',          # Character encoding
    'port': 3306                   # MySQL port (default: 3306)
}

# ==============================================
# SITE CONFIGURATION
# ==============================================
# These can also be managed from the admin dashboard

SITE_CONFIG = {
    # Main site information
    'site_title': 'AI in Education',
    'site_tagline': 'Exploring the intersection of artificial intelligence and learning',
    'footer_text': '© 2026, Dylan A. Bulseco, Ph.D., AI in Education Blog. All rights reserved.',
    
    # Logo (optional - can be changed later)
    'logo_path': '/images/logo.png',
    
    # Theme colors (hex format)
    'primary_color': '#2c3e50',    # Dark blue-grey
    'accent_color': '#3498db'      # Bright blue
}

# ==============================================
# UPLOAD CONFIGURATION
# ==============================================
# Settings for image uploads

UPLOAD_CONFIG = {
    # Folder where uploaded images are stored
    'upload_folder': 'images',
    
    # Allowed image file extensions
    'allowed_extensions': ['png', 'jpg', 'jpeg', 'gif', 'webp'],
    
    # Maximum file size in megabytes
    'max_file_size_mb': 5
}

# ==============================================
# OUTPUT CONFIGURATION
# ==============================================
# Settings for generated HTML files

OUTPUT_CONFIG = {
    # Folder where generated HTML files are saved
    'output_folder': 'output',
    
    # Template folder (for future expansion)
    'template_folder': 'templates'
}

# ==============================================
# EXAMPLE CONFIGURATIONS
# ==============================================

# Example 1: Remote MySQL database
"""
DB_CONFIG = {
    'host': '192.168.1.100',
    'user': 'bloguser',
    'password': 'securepassword123',
    'database': 'FCS3',
    'charset': 'utf8mb4',
    'port': 3306
}
"""

# Example 2: Different color scheme (green theme)
"""
SITE_CONFIG = {
    'site_title': 'My Blog',
    'site_tagline': 'Sharing knowledge and insights',
    'footer_text': '© 2026 My Blog. All rights reserved.',
    'logo_path': '/images/logo.png',
    'primary_color': '#27ae60',  # Green
    'accent_color': '#2ecc71'    # Light green
}
"""

# Example 3: Larger upload size
"""
UPLOAD_CONFIG = {
    'upload_folder': 'images',
    'allowed_extensions': ['png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'],
    'max_file_size_mb': 10  # 10MB limit
}
"""
