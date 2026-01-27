"""
Setup Validation Script
Run this to check if everything is configured correctly
"""

import sys
import os

print("=" * 60)
print("AI Education Blog - Setup Validation")
print("=" * 60)
print()

# Check Python version
print("1. Checking Python version...")
if sys.version_info < (3, 8):
    print("   ❌ Python 3.8 or higher required")
    print(f"   Current version: {sys.version}")
    sys.exit(1)
else:
    print(f"   ✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

# Check required files
print("\n2. Checking required files...")
required_files = [
    'config.py',
    'database.py',
    'generator.py',
    'admin_dashboard.py',
    'site_generator.py',
    'requirements.txt',
    'create_tables.sql'
]

missing_files = []
for file in required_files:
    if os.path.exists(file):
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} - NOT FOUND")
        missing_files.append(file)

if missing_files:
    print(f"\n   ⚠️  Missing files: {', '.join(missing_files)}")
    sys.exit(1)

# Check required directories
print("\n3. Checking directories...")
required_dirs = ['images', 'output']

for dir_name in required_dirs:
    if os.path.exists(dir_name):
        print(f"   ✅ {dir_name}/")
    else:
        print(f"   ⚠️  {dir_name}/ - Creating...")
        os.makedirs(dir_name, exist_ok=True)
        print(f"   ✅ {dir_name}/ created")

# Check Python packages
print("\n4. Checking Python packages...")
required_packages = {
    'streamlit': 'streamlit',
    'mysql.connector': 'mysql-connector-python',
    'PIL': 'Pillow'
}

missing_packages = []
for module, package in required_packages.items():
    try:
        __import__(module)
        print(f"   ✅ {package}")
    except ImportError:
        print(f"   ❌ {package} - NOT INSTALLED")
        missing_packages.append(package)

if missing_packages:
    print(f"\n   ⚠️  Install missing packages:")
    print(f"   pip install {' '.join(missing_packages)}")
    sys.exit(1)

# Check config
print("\n5. Checking configuration...")
try:
    from config import DB_CONFIG, SITE_CONFIG, UPLOAD_CONFIG, OUTPUT_CONFIG
    print("   ✅ config.py loaded")
    
    # Check if default password
    if DB_CONFIG['password'] == 'your_password':
        print("   ⚠️  WARNING: Using default password in config.py")
        print("   Please update with your MySQL password")
    else:
        print("   ✅ Database password configured")
        
except ImportError:
    print("   ❌ config.py not found or has errors")
    print("   Copy config.example.py to config.py and edit it")
    sys.exit(1)
except Exception as e:
    print(f"   ❌ Error in config.py: {e}")
    sys.exit(1)

# Test database connection
print("\n6. Testing database connection...")
try:
    from database import DatabaseManager
    db = DatabaseManager()
    success, message = db.test_connection()
    
    if success:
        print(f"   ✅ {message}")
    else:
        print(f"   ❌ {message}")
        print("\n   Troubleshooting:")
        print("   - Check MySQL is running")
        print("   - Verify credentials in config.py")
        print("   - Ensure FCS3 database exists")
        print("   - Run: mysql -u root -p FCS3 < create_tables.sql")
        sys.exit(1)
        
except Exception as e:
    print(f"   ❌ Connection failed: {e}")
    sys.exit(1)

# Check database tables
print("\n7. Checking database tables...")
try:
    conn = db.get_connection()
    cursor = conn.cursor()
    
    required_tables = ['blog_posts', 'categories', 'site_config']
    cursor.execute("SHOW TABLES")
    existing_tables = [table[0] for table in cursor.fetchall()]
    
    all_exist = True
    for table in required_tables:
        if table in existing_tables:
            print(f"   ✅ Table '{table}' exists")
        else:
            print(f"   ❌ Table '{table}' missing")
            all_exist = False
    
    cursor.close()
    conn.close()
    
    if not all_exist:
        print("\n   Run this to create tables:")
        print("   mysql -u root -p FCS3 < create_tables.sql")
        sys.exit(1)
        
except Exception as e:
    print(f"   ❌ Error checking tables: {e}")
    sys.exit(1)

# Success!
print("\n" + "=" * 60)
print("✅ All checks passed! Setup is complete.")
print("=" * 60)
print("\nNext steps:")
print("1. Run admin dashboard: streamlit run admin_dashboard.py")
print("2. Run site generator: streamlit run site_generator.py")
print()
print("Happy blogging! 🎉")
