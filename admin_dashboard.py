"""
Admin Dashboard - Streamlit App
Manage blog posts, categories, and content
"""

import streamlit as st
import os
from datetime import datetime, date
from PIL import Image
import shutil
from database import DatabaseManager
from config import UPLOAD_CONFIG, SITE_CONFIG
from docx_converter import convert_docx_bytes_to_html, extract_excerpt_from_html
import tempfile

# Page configuration
st.set_page_config(
    page_title="Blog Admin Dashboard",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database manager
@st.cache_resource
def get_db_manager():
    return DatabaseManager()

db = get_db_manager()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2c3e50, #3498db);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        color: #721c24;
        margin: 1rem 0;
    }
    .stat-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #3498db;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📝 Blog Admin Dashboard</h1>
    <p>Manage your AI in Education blog content</p>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Dashboard",
    "Create New Post",
    "Manage Posts",
    "Categories",
    "Site Settings"
])

# ==================== DASHBOARD PAGE ====================
if page == "Dashboard":
    st.header("📊 Dashboard Overview")
    
    # Test database connection
    conn_status, conn_msg = db.test_connection()
    if conn_status:
        st.success(f"✅ {conn_msg}")
    else:
        st.error(f"❌ {conn_msg}")
        st.stop()
    
    # Statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        try:
            total_posts = db.get_post_count(published_only=False)
            published_posts = db.get_post_count(published_only=True)
            st.markdown(f"""
            <div class="stat-card">
                <h3>{total_posts}</h3>
                <p>Total Posts</p>
                <small>{published_posts} published</small>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading post count: {e}")
    
    with col2:
        try:
            categories = db.get_unique_categories_from_posts()
            st.markdown(f"""
            <div class="stat-card">
                <h3>{len(categories)}</h3>
                <p>Categories</p>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading categories: {e}")
    
    with col3:
        try:
            category_counts = db.get_category_post_counts()
            top_category = max(category_counts.items(), key=lambda x: x[1])[0] if category_counts else "N/A"
            st.markdown(f"""
            <div class="stat-card">
                <h3>{top_category}</h3>
                <p>Top Category</p>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading top category: {e}")
    
    # Recent posts
    st.subheader("Recent Posts")
    try:
        posts = db.get_all_posts()
        if posts:
            for post in posts[:5]:  # Show 5 most recent
                with st.expander(f"📄 {post['title']} - {post['date']}"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**Category:** {post['category']}")
                        st.write(f"**Excerpt:** {post['excerpt']}")
                        st.write(f"**Status:** {'✅ Published' if post['published'] else '❌ Draft'}")
                    with col2:
                        st.write(f"**ID:** {post['id']}")
                        st.write(f"**Date:** {post['date']}")
        else:
            st.info("No posts yet. Create your first post!")
    except Exception as e:
        st.error(f"Error loading posts: {e}")
    
    # Quick actions
    st.subheader("Quick Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Create New Post"):
            st.session_state.page = "Create New Post"
            st.rerun()
    with col2:
        if st.button("🔄 Generate Site"):
            st.info("Go to the 'Site Generator' app to generate your static site!")

# ==================== CREATE NEW POST PAGE ====================
elif page == "Create New Post":
    st.header("➕ Create New Blog Post")
    
    # Initialize session state for form data
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {
            'title': '',
            'excerpt': '',
            'category': '',
            'date': date.today(),
            'image_path': '',
            'content': '',
            'published': True
        }
    
    # DOCX Upload Section (OUTSIDE form so file uploader works)
    st.subheader("📄 Step 1: Upload Your Blog Post Document")
    st.info("Create your blog post in Microsoft Word with formatting (headings, bold, lists, images, etc.), then upload the .docx file here.")
    
    docx_file = st.file_uploader(
        "Upload DOCX File *",
        type=['docx'],
        help="Upload a Word document with your blog content",
        key="docx_uploader"
    )
    
    content = ""
    
    if docx_file:
        # Convert DOCX to HTML
        with st.spinner("Converting document..."):
            try:
                html_content, success, message = convert_docx_bytes_to_html(docx_file.read())
                
                if success:
                    st.success("✅ Document converted successfully!")
                    if message:
                        st.info(message)
                    
                    # Store the converted HTML in session state
                    st.session_state.form_data['content'] = html_content
                    content = html_content
                    
                    # Show preview
                    st.subheader("📋 Preview of Converted Content")
                    
                    # Create tabs for preview and HTML source
                    preview_tab, html_tab = st.tabs(["Visual Preview", "HTML Source"])
                    
                    with preview_tab:
                        st.markdown(
                            f"""
                            <div style="border: 1px solid #ddd; padding: 20px; border-radius: 5px; background-color: white;">
                                {html_content}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    
                    with html_tab:
                        st.code(html_content, language="html")
                        st.caption("This is the HTML that will be saved to the database and displayed on your blog.")
                    
                    # Auto-generate excerpt suggestion
                    auto_excerpt = extract_excerpt_from_html(html_content, 200)
                    if auto_excerpt and not st.session_state.form_data.get('excerpt'):
                        st.info(f"💡 Suggested excerpt: {auto_excerpt}")
                        if st.button("📋 Use This Excerpt"):
                            st.session_state.form_data['excerpt'] = auto_excerpt
                            st.rerun()
                else:
                    st.error(f"❌ {message}")
                    st.warning("Please upload a valid .docx file.")
            except Exception as e:
                st.error(f"Error converting document: {e}")
                st.info("Make sure your file is a valid .docx format (not .doc)")
    else:
        if st.session_state.form_data.get('content'):
            st.info("✅ Content loaded from previous upload")
            content = st.session_state.form_data['content']
            
            # Show a preview of loaded content
            with st.expander("👁️ View Loaded Content"):
                st.markdown(
                    f"""
                    <div style="border: 1px solid #ddd; padding: 20px; border-radius: 5px; background-color: white;">
                        {content[:500]}{'...' if len(content) > 500 else ''}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.warning("⚠️ Please upload a .docx file to continue")
    
    st.markdown("---")
    st.subheader("📝 Step 2: Upload Header Image")
    
    # Initialize image state if needed
    if 'current_image_path' not in st.session_state:
        st.session_state.current_image_path = None
    
    # Image handling (OUTSIDE form to prevent duplicate uploads)
    image_option = st.radio("Image Source", ["Upload Image", "Use URL"], key="image_source_radio")
    
    image_path = ""
    
    if image_option == "Upload Image":
        uploaded_image = st.file_uploader(
            "Choose a header image", 
            type=['png', 'jpg', 'jpeg', 'gif', 'webp'],
            key="image_uploader"
        )
        
        if uploaded_image:
            try:
                # Show preview
                image = Image.open(uploaded_image)
                st.image(image, caption="Image Preview", width=400)
                
                # Create unique filename using timestamp + original name
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}_{uploaded_image.name}"
                
                # Get upload folder and create if needed
                upload_folder = UPLOAD_CONFIG['upload_folder']
                
                # Get absolute path
                import os
                current_dir = os.getcwd()
                abs_upload_folder = os.path.join(current_dir, upload_folder)
                
                # Create folder if it doesn't exist
                os.makedirs(abs_upload_folder, exist_ok=True)
                
                # Full file path
                file_path = os.path.join(abs_upload_folder, filename)
                
                # Show debug info
                st.info(f"📂 Current directory: `{current_dir}`")
                st.info(f"📁 Upload folder: `{abs_upload_folder}`")
                st.info(f"💾 Saving to: `{file_path}`")
                
                # Save the file
                try:
                    with open(file_path, "wb") as f:
                        f.write(uploaded_image.getvalue())
                    
                    # Check if file was actually saved
                    if os.path.exists(file_path):
                        file_size = os.path.getsize(file_path)
                        st.success(f"✅ Image saved successfully!")
                        st.success(f"📊 File size: {file_size:,} bytes")
                        st.success(f"📄 Filename: {filename}")
                    else:
                        st.error("❌ File was not saved (file doesn't exist after save)")
                        
                except Exception as save_error:
                    st.error(f"❌ Error saving file: {save_error}")
                    st.stop()
                
                # Store relative path (for web use) - NO leading slash
                image_path = f"images/{filename}"
                st.session_state.current_image_path = image_path
                st.session_state.form_data['image_path'] = image_path
                
                st.info(f"🌐 Path for website: `{image_path}`")
                
            except Exception as e:
                st.error(f"❌ Error processing image: {e}")
                import traceback
                st.code(traceback.format_exc())
            
        elif st.session_state.current_image_path:
            # No file selected but we have one from before
            image_path = st.session_state.current_image_path
            st.info(f"✅ Using previously uploaded image: {image_path}")
    else:
        # URL option
        image_url = st.text_input("Image URL *", placeholder="https://example.com/image.jpg", key="image_url_input")
        if image_url:
            image_path = image_url
            st.session_state.current_image_path = image_url
            st.session_state.form_data['image_path'] = image_url
            try:
                st.image(image_url, caption="Image Preview", width=400)
            except:
                st.warning("Cannot preview this URL. Make sure it's a valid image URL.")
    
    st.markdown("---")
    st.subheader("📋 Step 3: Fill in Post Details")
    
    # Now the form for other fields
    with st.form("new_post_form"):
        # Post title
        title = st.text_input(
            "Post Title *", 
            placeholder="Enter post title",
            value=st.session_state.form_data.get('title', '')
        )
        
        # Excerpt
        excerpt = st.text_area(
            "Excerpt *", 
            placeholder="Brief summary for the card preview", 
            height=100,
            value=st.session_state.form_data.get('excerpt', '')
        )
        
        # Category and Date
        col1, col2 = st.columns(2)
        with col1:
            try:
                existing_categories = db.get_unique_categories_from_posts()
            except:
                existing_categories = []
            
            category_input = st.text_input("Category *", placeholder="e.g., Teaching Tools")
            if existing_categories:
                st.caption(f"Existing categories: {', '.join(existing_categories)}")
        
        with col2:
            post_date = st.date_input("Publication Date *", value=date.today())
        
        # Get image path from session state (already uploaded outside form)
        image_path = st.session_state.form_data.get('image_path', '')
        if image_path:
            st.info(f"✅ Header image: {image_path}")
        else:
            st.warning("⚠️ Please upload a header image in Step 2 above")
        
        # Content is already uploaded outside form
        content = st.session_state.form_data.get('content', '')
        if content:
            st.success("✅ Content loaded from uploaded DOCX file")
        else:
            st.error("❌ No content uploaded. Please upload a DOCX file in Step 1 above.")


        
        # Published status
        published = st.checkbox("Publish immediately", value=True)
        
        # Submit button
        submitted = st.form_submit_button("Add Blog Post")
        
        if submitted:
            # Validation
            if not title or not excerpt or not content or not category_input or not image_path:
                st.error("❌ Please fill in all required fields!")
            else:
                try:
                    # Format content with header
                    formatted_content = f"""
                    <h2>{title}</h2>
                    <p class="text-muted">Published on {post_date.strftime('%B %d, %Y')} | Category: {category_input}</p>
                    <img src="{image_path}" class="img-fluid rounded mb-4" alt="{title}">
                    {content}
                    """
                    
                    # Add to database
                    post_id = db.add_post(
                        title=title,
                        excerpt=excerpt,
                        content=formatted_content,
                        category=category_input,
                        image_path=image_path,
                        date=post_date.strftime('%Y-%m-%d'),
                        published=published
                    )
                    
                    st.success(f"✅ Post created successfully! (ID: {post_id})")
                    st.balloons()
                    
                    # Clear session state
                    st.session_state.form_data = {
                        'title': '',
                        'excerpt': '',
                        'category': '',
                        'date': date.today(),
                        'image_path': '',
                        'content': '',
                        'published': True
                    }
                    st.session_state.current_image_path = None
                    
                    # Wait a moment then rerun to clear form
                    import time
                    time.sleep(2)
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error creating post: {e}")

# ==================== MANAGE POSTS PAGE ====================
elif page == "Manage Posts":
    st.header("📚 Manage Blog Posts")
    
    # Filter options
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍 Search posts", placeholder="Search by title...")
    with col2:
        show_unpublished = st.checkbox("Show unpublished posts", value=True)
    
    try:
        # Get all posts
        posts = db.get_all_posts(published_only=not show_unpublished)
        
        # Filter by search
        if search:
            posts = [p for p in posts if search.lower() in p['title'].lower()]
        
        st.write(f"**Total posts:** {len(posts)}")
        
        # Display posts
        for post in posts:
            with st.expander(f"{'✅' if post['published'] else '❌'} {post['title']} - {post['date']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Category:** {post['category']}")
                    st.write(f"**Excerpt:** {post['excerpt'][:200]}...")
                    st.write(f"**Status:** {'Published' if post['published'] else 'Draft'}")
                    
                    # Edit form
                    with st.form(f"edit_form_{post['id']}"):
                        st.subheader("Edit Post")
                        
                        new_title = st.text_input("Title", value=post['title'], key=f"title_{post['id']}")
                        new_excerpt = st.text_area("Excerpt", value=post['excerpt'], key=f"excerpt_{post['id']}")
                        new_category = st.text_input("Category", value=post['category'], key=f"category_{post['id']}")
                        new_date = st.date_input("Date", value=datetime.strptime(post['date'], '%Y-%m-%d'), key=f"date_{post['id']}")
                        new_published = st.checkbox("Published", value=post['published'], key=f"pub_{post['id']}")
                        
                        col_save, col_delete = st.columns(2)
                        with col_save:
                            if st.form_submit_button("💾 Save Changes"):
                                try:
                                    db.update_post(
                                        post_id=post['id'],
                                        title=new_title,
                                        excerpt=new_excerpt,
                                        content=post['content'],  # Keep original content
                                        category=new_category,
                                        image_path=post['image_path'],
                                        date=new_date.strftime('%Y-%m-%d'),
                                        published=new_published
                                    )
                                    st.success("✅ Post updated!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error: {e}")
                        
                        with col_delete:
                            if st.form_submit_button("🗑️ Delete Post"):
                                try:
                                    db.delete_post(post['id'])
                                    st.success("✅ Post deleted!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error: {e}")
                
                with col2:
                    if post['image_path']:
                        try:
                            st.image(post['image_path'], caption="Header Image", width=300)
                        except:
                            st.caption(f"Image: {post['image_path']}")
    
    except Exception as e:
        st.error(f"Error loading posts: {e}")

# ==================== CATEGORIES PAGE ====================
elif page == "Categories":
    st.header("🏷️ Manage Categories")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Categories in Use")
        try:
            categories = db.get_unique_categories_from_posts()
            category_counts = db.get_category_post_counts()
            
            if categories:
                for cat in categories:
                    count = category_counts.get(cat, 0)
                    st.write(f"📁 **{cat}** ({count} posts)")
            else:
                st.info("No categories yet. Create a post to add categories.")
        except Exception as e:
            st.error(f"Error loading categories: {e}")
    
    with col2:
        st.subheader("Add New Category")
        with st.form("add_category_form"):
            new_category = st.text_input("Category Name")
            new_description = st.text_area("Description (optional)")
            
            if st.form_submit_button("Add Category"):
                if new_category:
                    try:
                        db.add_category(new_category, new_description)
                        st.success(f"✅ Category '{new_category}' added!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.error("Please enter a category name")

# ==================== SITE SETTINGS PAGE ====================
elif page == "Site Settings":
    st.header("⚙️ Site Settings")
    
    try:
        # Get current config from database
        current_config = db.get_all_site_config()
        
        with st.form("site_settings_form"):
            st.subheader("General Settings")
            
            site_title = st.text_input(
                "Site Title",
                value=current_config.get('site_title', SITE_CONFIG['site_title'])
            )
            
            site_tagline = st.text_input(
                "Site Tagline",
                value=current_config.get('site_tagline', SITE_CONFIG['site_tagline'])
            )
            
            footer_text = st.text_area(
                "Footer Text",
                value=current_config.get('footer_text', SITE_CONFIG['footer_text'])
            )
            
            acknowledgment = st.text_area(
                "Acknowledgment (optional)",
                value=current_config.get('acknowledgment', SITE_CONFIG.get('acknowledgment', '')),
                help="Optional acknowledgment text that appears below the footer (e.g., funding sources, AI assistance)"
            )
            
            st.subheader("Theme Colors")
            col1, col2 = st.columns(2)
            
            with col1:
                primary_color = st.color_picker(
                    "Primary Color",
                    value=current_config.get('primary_color', SITE_CONFIG['primary_color'])
                )
            
            with col2:
                accent_color = st.color_picker(
                    "Accent Color",
                    value=current_config.get('accent_color', SITE_CONFIG['accent_color'])
                )
            
            if st.form_submit_button("💾 Save Settings"):
                try:
                    db.update_site_config('site_title', site_title)
                    db.update_site_config('site_tagline', site_tagline)
                    db.update_site_config('footer_text', footer_text)
                    db.update_site_config('acknowledgment', acknowledgment)
                    db.update_site_config('primary_color', primary_color)
                    db.update_site_config('accent_color', accent_color)
                    
                    st.success("✅ Settings saved successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving settings: {e}")
        
        # Show current settings
        st.subheader("Current Configuration")
        st.json(current_config)
    
    except Exception as e:
        st.error(f"Error loading settings: {e}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 📝 Blog Admin Dashboard")
st.sidebar.markdown("Manage your AI in Education blog")
st.sidebar.markdown(f"**Version:** 1.0.0")
