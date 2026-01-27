"""
Site Generator Dashboard - Streamlit App
Generate static HTML files from database content
"""

import streamlit as st
import os
import shutil
from datetime import datetime
from database import DatabaseManager
from generator import SiteGenerator
from config import SITE_CONFIG, OUTPUT_CONFIG

# Page configuration
st.set_page_config(
    page_title="Site Generator",
    page_icon="🌐",
    layout="wide"
)

# Initialize
@st.cache_resource
def get_db_manager():
    return DatabaseManager()

db = get_db_manager()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #27ae60, #2ecc71);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1.5rem;
        background-color: #d4edda;
        border: 2px solid #28a745;
        border-radius: 10px;
        color: #155724;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        color: #0c5460;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🌐 Static Site Generator</h1>
    <p>Generate your static HTML blog site from database content</p>
</div>
""", unsafe_allow_html=True)

# Check database connection
conn_status, conn_msg = db.test_connection()
if not conn_status:
    st.error(f"❌ Database Connection Error: {conn_msg}")
    st.stop()

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📊 Site Preview")
    
    # Get posts from database
    try:
        all_posts = db.get_all_posts(published_only=False)
        published_posts = [p for p in all_posts if p.get('published', True)]
        
        st.metric("Total Posts", len(all_posts))
        st.metric("Published Posts", len(published_posts))
        
        if published_posts:
            st.subheader("Posts to be included in generated site:")
            
            # Show posts by category
            categories = {}
            for post in published_posts:
                cat = post['category']
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(post)
            
            for category, posts in sorted(categories.items()):
                with st.expander(f"📁 {category} ({len(posts)} posts)"):
                    for post in posts:
                        st.write(f"- **{post['title']}** ({post['date']})")
        else:
            st.warning("⚠️ No published posts found. Publish some posts first!")
    
    except Exception as e:
        st.error(f"Error loading posts: {e}")
        published_posts = []

with col2:
    st.header("⚙️ Generation Options")
    
    # Site configuration
    try:
        site_config = db.get_all_site_config()
        if not site_config:
            site_config = SITE_CONFIG
    except:
        site_config = SITE_CONFIG
    
    st.subheader("Site Configuration")
    st.write(f"**Title:** {site_config.get('site_title', 'N/A')}")
    st.write(f"**Tagline:** {site_config.get('site_tagline', 'N/A')}")
    
    # Color preview
    col_a, col_b = st.columns(2)
    with col_a:
        st.color_picker("Primary", site_config.get('primary_color', '#2c3e50'), disabled=True)
    with col_b:
        st.color_picker("Accent", site_config.get('accent_color', '#3498db'), disabled=True)
    
    st.markdown("---")
    
    # Output options
    st.subheader("Output Settings")
    
    output_filename = st.text_input("Output Filename", value="index.html")
    
    include_about = st.checkbox("Generate About Page", value=False)
    if include_about:
        about_content = st.text_area(
            "About Page Content (HTML)",
            value="<h1>About Us</h1><p>Content goes here...</p>",
            height=150
        )

# Generation section
st.markdown("---")
st.header("🚀 Generate Site")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🌐 Generate Site", type="primary"):
        if not published_posts:
            st.error("❌ No published posts to generate site from!")
        else:
            try:
                with st.spinner("Generating site..."):
                    # Create generator
                    generator = SiteGenerator(site_config)
                    
                    # Generate index.html
                    output_path = generator.generate_index(published_posts, output_filename)
                    
                    # Generate about page if requested
                    if include_about:
                        about_path = generator.generate_about_page(about_content, "about.html")
                    
                    st.success("✅ Site generated successfully!")
                    st.balloons()
                    
                    # Show output info
                    st.markdown(f"""
                    <div class="success-box">
                        <h3>✅ Generation Complete!</h3>
                        <p><strong>Output location:</strong> <code>{output_path}</code></p>
                        <p><strong>Posts included:</strong> {len(published_posts)}</p>
                        <p><strong>Categories:</strong> {len(set(p['category'] for p in published_posts))}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Store in session state
                    st.session_state.last_generation = {
                        'path': output_path,
                        'timestamp': datetime.now(),
                        'posts_count': len(published_posts)
                    }
                    
            except Exception as e:
                st.error(f"❌ Error generating site: {e}")

with col2:
    if st.button("👁️ Preview Generated Site"):
        output_path = os.path.join(OUTPUT_CONFIG['output_folder'], output_filename)
        if os.path.exists(output_path):
            with open(output_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            st.markdown("### Preview")
            st.markdown(f"**File:** `{output_path}`")
            st.markdown(f"**Size:** {len(html_content):,} bytes")
            
            with st.expander("View HTML Source"):
                st.code(html_content[:2000] + "..." if len(html_content) > 2000 else html_content, language="html")
        else:
            st.warning("⚠️ No generated site found. Generate site first!")

with col3:
    output_path = os.path.join(OUTPUT_CONFIG['output_folder'], output_filename)
    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        st.download_button(
            label="📥 Download HTML",
            data=html_content,
            file_name=output_filename,
            mime="text/html"
        )

# Last generation info
if 'last_generation' in st.session_state:
    st.markdown("---")
    st.subheader("📝 Last Generation")
    
    info = st.session_state.last_generation
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Generated", info['timestamp'].strftime("%Y-%m-%d %H:%M:%S"))
    with col2:
        st.metric("Posts Included", info['posts_count'])
    with col3:
        st.metric("Output File", os.path.basename(info['path']))

# Instructions
st.markdown("---")
st.header("📖 How to Use")

st.markdown("""
### Workflow:

1. **Create Content** - Use the Admin Dashboard to create and manage blog posts
2. **Review Posts** - Check the preview above to see what will be included
3. **Configure** - Adjust site settings if needed (title, colors, etc.)
4. **Generate** - Click "Generate Site" to create your static HTML
5. **Download** - Download the generated files
6. **Deploy** - Upload the HTML files to your web hosting

### Output Files:

- `index.html` - Main blog page with all posts
- `about.html` - About page (if enabled)
- Images should be uploaded separately to your web server

### Tips:

- ✅ Only **published** posts are included in the generated site
- ✅ Posts are sorted by date (newest first)
- ✅ All content is embedded in the HTML (no database needed on server)
- ✅ The site works with just static HTML + images
- ✅ Category filtering works client-side with JavaScript

### Deployment:

Upload these files to your web host:
- `index.html`
- `about.html` (if created)
- `/images/` folder with all uploaded images
""")

# Footer
st.sidebar.markdown("---")
st.sidebar.title("🌐 Site Generator")
st.sidebar.markdown("Generate static HTML sites from your database")

# Database stats
st.sidebar.markdown("### 📊 Database Stats")
try:
    total = db.get_post_count(published_only=False)
    published = db.get_post_count(published_only=True)
    st.sidebar.metric("Total Posts", total)
    st.sidebar.metric("Published Posts", published)
    st.sidebar.metric("Draft Posts", total - published)
except:
    st.sidebar.warning("Cannot load stats")

# Output folder info
st.sidebar.markdown("---")
st.sidebar.markdown("### 📁 Output Location")
st.sidebar.code(OUTPUT_CONFIG['output_folder'])

if os.path.exists(OUTPUT_CONFIG['output_folder']):
    files = os.listdir(OUTPUT_CONFIG['output_folder'])
    st.sidebar.markdown(f"**Files:** {len(files)}")
    if files:
        with st.sidebar.expander("View Files"):
            for f in files:
                st.write(f"- {f}")
else:
    st.sidebar.warning("Output folder not created yet")
