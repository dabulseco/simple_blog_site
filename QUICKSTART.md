# Quick Start Guide

## 5-Minute Setup

### Step 1: Database Setup (2 minutes)

```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE IF NOT EXISTS FCS3;
exit;

# Import tables
mysql -u root -p FCS3 < create_tables.sql
```

### Step 2: Configure (1 minute)

Edit `config.py`:
```python
DB_CONFIG = {
    'user': 'root',           # Your MySQL username
    'password': 'your_pass',  # Your MySQL password
    'database': 'FCS3',
}
```

### Step 3: Install Python Packages (1 minute)

```bash
pip install -r requirements.txt
```

### Step 4: Run Admin Dashboard (30 seconds)

```bash
streamlit run admin_dashboard.py
```

Browser opens automatically at `http://localhost:8501`

### Step 5: Create First Post (30 seconds)

1. Click "Create New Post"
2. Fill in the form
3. **Upload a formatted Word document (.docx)** OR write HTML
4. Preview the converted content
5. Click "Add Blog Post"

Done! ✅

---

## Generate Your Site

### Step 1: Run Site Generator

```bash
streamlit run site_generator.py
```

### Step 2: Generate

1. Click "Generate Site" button
2. Download the `index.html` file

### Step 3: Deploy

Upload these to your web host:
- `index.html`
- `/images/` folder

Your blog is live! 🎉

---

## Common Commands

### Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### Run Admin Dashboard
```bash
streamlit run admin_dashboard.py
```

### Run Site Generator
```bash
streamlit run site_generator.py
```

### Backup Database
```bash
mysqldump -u root -p FCS3 > backup.sql
```

### Restore Database
```bash
mysql -u root -p FCS3 < backup.sql
```

---

## Troubleshooting

**Can't connect to database?**
- Check MySQL is running
- Verify credentials in config.py
- Ensure FCS3 database exists

**Port already in use?**
```bash
streamlit run admin_dashboard.py --server.port 8502
```

**Module not found?**
```bash
pip install -r requirements.txt
```

---

## Next Steps

1. ✅ Customize colors in Site Settings
2. ✅ Add your logo
3. ✅ Create 5-10 blog posts
4. ✅ Generate and deploy site
5. ✅ Set up regular backups

Need more help? See `README.md`
