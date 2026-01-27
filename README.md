# AI in Education Blog - Static Site Generator

A Python/Streamlit-based blog management system that uses MySQL for content storage and generates static HTML files for deployment.

## 🌟 Features

- ✅ **Python-based** - Clean, maintainable Python code
- ✅ **Streamlit UI** - Beautiful, interactive web interface
- ✅ **MySQL Database** - Reliable local data storage
- ✅ **Static Site Generation** - Generate pure HTML/CSS/JavaScript sites
- ✅ **DOCX Upload** - Upload formatted Word documents, auto-convert to HTML
- ✅ **Live Preview** - See how your DOCX will look before saving
- ✅ **Bootstrap 5** - Modern, responsive design
- ✅ **Image Management** - Upload images locally or use URLs
- ✅ **Category Filtering** - Organize posts by category
- ✅ **No Server Requirements** - Generated sites work on any static host

## 📋 System Requirements

- Python 3.8 or higher
- MySQL 5.7 or higher
- 100MB disk space (minimum)
- Local development environment

## 🚀 Quick Start

### 1. Install MySQL and Create Database

```bash
# Log into MySQL
mysql -u root -p

# Create the FCS3 database if it doesn't exist
CREATE DATABASE IF NOT EXISTS FCS3;

# Exit MySQL
exit;
```

### 2. Set Up Database Tables

```bash
# Import the database schema
mysql -u root -p FCS3 < create_tables.sql
```

Or manually run the SQL commands from `create_tables.sql` in your MySQL client.

### 3. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 4. Configure Database Connection

Edit `config.py` and update your MySQL credentials:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',      # Change this
    'password': 'your_password',  # Change this
    'database': 'FCS3',
    'charset': 'utf8mb4',
    'port': 3306
}
```

### 5. Run the Applications

**Admin Dashboard** (for managing content):
```bash
streamlit run admin_dashboard.py
```

**Site Generator** (for creating static HTML):
```bash
streamlit run site_generator.py
```

## 📂 Project Structure

```
ai-education-blog/
├── admin_dashboard.py      # Streamlit app for content management
├── site_generator.py       # Streamlit app for generating static HTML
├── database.py             # Database operations and queries
├── generator.py            # HTML generation logic
├── config.py               # Configuration settings
├── create_tables.sql       # MySQL table creation script
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── images/                # Uploaded images directory
│   └── (uploaded files)
└── output/                # Generated HTML files
    ├── index.html
    └── about.html
```

## 🎯 Workflow

### Step 1: Create Content (Admin Dashboard)

1. Run `streamlit run admin_dashboard.py`
2. Navigate to **"Create New Post"**
3. **Upload your .docx file** - Create your blog post in Microsoft Word with all formatting
4. Preview the converted HTML
5. Fill in post details:
   - Title
   - Excerpt (or use auto-generated)
   - Category
   - Date
   - Image (upload or URL)
6. Click **"Add Blog Post"**
7. Post is saved to MySQL database with properly converted HTML

### Step 2: Generate Site (Site Generator)

1. Run `streamlit run site_generator.py`
2. Review posts to be included
3. Configure output options
4. Click **"Generate Site"**
5. Download the generated `index.html`

### Step 3: Deploy

1. Upload `index.html` to your web host
2. Upload `/images/` folder with all images
3. Optional: Upload `about.html` if created
4. Your static blog is live!

## 📊 Database Schema

### blog_posts Table

```sql
- id (INT, PRIMARY KEY, AUTO_INCREMENT)
- title (VARCHAR(255))
- excerpt (TEXT)
- content (LONGTEXT)
- category (VARCHAR(100))
- image_path (VARCHAR(500))
- date (DATE)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- published (BOOLEAN)
- sort_order (INT)
```

### categories Table

```sql
- id (INT, PRIMARY KEY, AUTO_INCREMENT)
- name (VARCHAR(100), UNIQUE)
- description (TEXT)
- display_order (INT)
- created_at (TIMESTAMP)
```

### site_config Table

```sql
- id (INT, PRIMARY KEY, AUTO_INCREMENT)
- config_key (VARCHAR(100), UNIQUE)
- config_value (TEXT)
- description (VARCHAR(255))
- updated_at (TIMESTAMP)
```

## 🎨 Admin Dashboard Features

### Dashboard Page
- Overview statistics
- Recent posts
- Database connection status
- Quick actions

### Create New Post
- **DOCX-only upload** - Write in Word, upload, done!
- **Auto-convert** Word formatting to clean HTML
- **Live preview** before saving
- **Auto-generate excerpts** from content
- Image upload or URL
- Category management
- Date picker
- Publish/draft toggle

### Manage Posts
- View all posts
- Search functionality
- Edit posts inline
- Delete posts
- Toggle publish status

### Categories
- View all categories
- Add new categories
- See post counts per category

### Site Settings
- Edit site title and tagline
- Customize footer text
- Change theme colors
- Logo management

## 🌐 Site Generator Features

### Preview
- See all posts to be included
- View by category
- Post count statistics

### Generation Options
- Custom output filename
- Optional about page
- Site configuration preview

### Output
- Download generated HTML
- View HTML source
- Generation history

## 🎨 Customization

### Theme Colors

Edit site colors in **Site Settings** or in `config.py`:

```python
SITE_CONFIG = {
    'primary_color': '#2c3e50',  # Dark blue
    'accent_color': '#3498db',   # Light blue
}
```

### Site Information

Edit in **Site Settings** or in `config.py`:

```python
SITE_CONFIG = {
    'site_title': 'Your Blog Title',
    'site_tagline': 'Your tagline here',
    'footer_text': '© 2026 Your Name',
}
```

### HTML Template

Modify `generator.py` to customize the HTML structure and styling.

## 📝 Content Guidelines

### Image Recommendations
- **Format**: JPG, PNG, GIF, or WebP
- **Size**: Max 5MB per image
- **Dimensions**: 1200x600px recommended for headers
- **Optimization**: Compress images before upload

### HTML Content
- Use semantic HTML tags
- Supported tags: `<h3>`, `<p>`, `<ul>`, `<ol>`, `<strong>`, `<em>`, `<a>`, `<img>`
- Include alt text for images
- Use responsive images

### Categories
- Keep category names short and clear
- Use consistent naming (e.g., "Teaching Tools" not "teaching tools")
- Limit to 5-10 main categories

## 🔧 Troubleshooting

### Database Connection Error

```
Error: 'Can't connect to MySQL server'
```

**Solutions:**
- Verify MySQL is running: `mysql.server status` (Mac) or check Task Manager (Windows)
- Check credentials in `config.py`
- Ensure FCS3 database exists
- Check firewall settings

### Table Not Found

```
Error: 'Table blog_posts doesn't exist'
```

**Solution:**
```bash
mysql -u root -p FCS3 < create_tables.sql
```

### Image Upload Issues

**Problem:** Images not saving

**Solutions:**
- Check `images/` folder exists
- Verify write permissions
- Check disk space
- Ensure image is under 5MB

### Streamlit Port Already in Use

**Problem:** `Port 8501 is already in use`

**Solution:**
```bash
streamlit run admin_dashboard.py --server.port 8502
```

### Generated HTML Not Showing Images

**Problem:** Images show broken

**Solutions:**
- Ensure images are uploaded to web server
- Check image paths are correct
- Verify image URLs are accessible
- Use relative paths: `/images/photo.jpg`

## 💡 Best Practices

### Content Management
1. ✅ Write posts in drafts first (published = False)
2. ✅ Preview before publishing
3. ✅ Use consistent categories
4. ✅ Optimize images before upload
5. ✅ Back up database regularly

### Site Generation
1. ✅ Review posts before generating
2. ✅ Test generated HTML locally
3. ✅ Keep backups of generated files
4. ✅ Version control your output
5. ✅ Generate after each content update

### Database Maintenance
1. ✅ Regular backups: `mysqldump -u user -p FCS3 > backup.sql`
2. ✅ Clean up unpublished drafts periodically
3. ✅ Monitor database size
4. ✅ Index optimization for large datasets

## 🔐 Security Notes

- ✅ `config.py` contains sensitive data - never commit to public repos
- ✅ Use strong MySQL passwords
- ✅ Keep Python dependencies updated
- ✅ Generated HTML is safe (no server-side code)
- ✅ Sanitize user input in forms

## 📦 Deployment Options

### Option 1: GitHub Pages
1. Generate site
2. Upload `index.html` and `/images/` to repo
3. Enable GitHub Pages in settings
4. Access at `https://username.github.io/repo`

### Option 2: Netlify
1. Generate site
2. Drag and drop `output/` folder to Netlify
3. Site is live instantly

### Option 3: Traditional Web Host
1. Generate site
2. Upload via FTP/SFTP
3. Place in `public_html/` or `www/` folder

### Option 4: AWS S3 + CloudFront
1. Generate site
2. Upload to S3 bucket
3. Enable static website hosting
4. Optional: CloudFront CDN

## 🔄 Backup and Recovery

### Database Backup

```bash
# Full backup
mysqldump -u root -p FCS3 > backup_$(date +%Y%m%d).sql

# Restore from backup
mysql -u root -p FCS3 < backup_20260126.sql
```

### Image Backup

```bash
# Backup images folder
tar -czf images_backup_$(date +%Y%m%d).tar.gz images/

# Restore images
tar -xzf images_backup_20260126.tar.gz
```

## 📈 Future Enhancements

Possible features to add:

- [ ] Rich text WYSIWYG editor
- [ ] Image optimization on upload
- [ ] Multi-user support with authentication
- [ ] Post scheduling
- [ ] Comments section (static or external service)
- [ ] RSS feed generation
- [ ] Search functionality
- [ ] Tags in addition to categories
- [ ] Analytics integration
- [ ] SEO metadata management

## 🤝 Contributing

This is a personal project, but feel free to:
- Report bugs
- Suggest features
- Share improvements

## 📄 License

All rights reserved. © 2026 Dylan A. Bulseco, Ph.D.

## 🆘 Support

For issues or questions:
1. Check this README
2. Review error messages carefully
3. Check MySQL logs
4. Verify Python dependencies
5. Test database connection

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/)
- [Python MySQL Connector](https://dev.mysql.com/doc/connector-python/en/)

---

**Version:** 1.0.0  
**Last Updated:** January 2026  
**Author:** Dylan A. Bulseco, Ph.D.
