"""
Static Site Generator
Generates static HTML files from database content
"""

import os
from typing import List, Dict
from datetime import datetime
from config import SITE_CONFIG, OUTPUT_CONFIG


class SiteGenerator:
    """Generate static HTML site from database content"""
    
    def __init__(self, site_config: Dict = None):
        self.site_config = site_config or SITE_CONFIG
        self.output_folder = OUTPUT_CONFIG['output_folder']
        
        # Ensure output folder exists
        os.makedirs(self.output_folder, exist_ok=True)
    
    def generate_index(self, posts: List[Dict], output_filename: str = "index.html") -> str:
        """Generate the main index.html file with all blog posts"""
        
        # Get unique categories
        categories = sorted(set(post['category'] for post in posts if post.get('published', True)))
        
        html = self._generate_html_template(posts, categories)
        
        # Write to file
        output_path = os.path.join(self.output_folder, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return output_path
    
    def _generate_html_template(self, posts: List[Dict], categories: List[str]) -> str:
        """Generate the complete HTML template"""
        
        # Generate blog cards HTML
        blog_cards_html = self._generate_blog_cards(posts)
        
        # Generate category filters
        category_filters_html = self._generate_category_filters(categories)
        
        # Generate JSON data - we'll embed it in a data attribute
        import json
        import html as html_module
        posts_json = self._generate_posts_json(posts)
        # HTML-escape the JSON so it's safe in a data attribute
        posts_json_safe = html_module.escape(posts_json)
        
        # Generate the full HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.site_config['site_title']}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root {{
            --primary-color: {self.site_config.get('primary_color', '#2c3e50')};
            --accent-color: {self.site_config.get('accent_color', '#3498db')};
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8f9fa;
        }}

        .navbar {{
            background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .hero {{
            background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
            color: white;
            padding: 60px 0;
            margin-bottom: 40px;
        }}

        .blog-card {{
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            height: 100%;
            border: none;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .blog-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        }}

        .card-img-top {{
            height: 200px;
            object-fit: cover;
        }}

        .badge-date {{
            background-color: var(--accent-color);
        }}

        .btn-read-more {{
            background-color: var(--accent-color);
            border: none;
        }}

        .btn-read-more:hover {{
            background-color: #2980b9;
        }}

        #fullArticle {{
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .back-btn {{
            color: var(--accent-color);
            text-decoration: none;
            font-weight: 500;
        }}

        .back-btn:hover {{
            color: var(--primary-color);
        }}

        .filter-section {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}

        .filter-btn {{
            margin: 5px;
        }}

        .filter-btn.active {{
            background-color: var(--accent-color);
            color: white;
        }}

        .article-content img {{
            max-width: 100%;
            height: auto;
        }}
    </style>
</head>
<body data-blog-posts="{posts_json_safe}">
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand fw-bold" href="#" onclick="showHome()">
                {self.site_config['site_title']}
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="#" onclick="showHome()">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="about.html">About</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="hero text-center" id="heroSection">
        <div class="container">
            <h1 class="display-4 fw-bold mb-3">{self.site_config['site_title']}</h1>
            <p class="lead">{self.site_config['site_tagline']}</p>
        </div>
    </div>

    <div class="container mb-5">
        <!-- Filter Section -->
        <div id="filterSection" class="filter-section">
            <h5 class="mb-3">Filter by Category:</h5>
            <div id="categoryFilters">
                {category_filters_html}
            </div>
        </div>

        <div id="blogGrid" class="row g-4">
            {blog_cards_html}
        </div>

        <div id="fullArticle" class="p-4 d-none">
            <a href="#" class="back-btn" onclick="showHome()">← Back to all posts</a>
            <article id="articleContent" class="mt-4 article-content">
                <!-- Full article content will be inserted here by JavaScript -->
            </article>
        </div>
    </div>

    <footer class="bg-dark text-white text-center py-4 mt-5">
        <div class="container">
            <p class="mb-0">{self.site_config['footer_text']}</p>
            {f'<p class="mb-0 mt-2"><small>{self.site_config["acknowledgment"]}</small></p>' if self.site_config.get('acknowledgment') else ''}
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Read blog posts data from data attribute
        const postsData = document.body.getAttribute('data-blog-posts');
        const allBlogPosts = JSON.parse(postsData);
        let currentFilter = 'all';

        function filterByCategory(category) {{
            currentFilter = category;
            
            // Update active button
            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            event.target.classList.add('active');
            
            renderBlogCards();
        }}

        function getFilteredPosts() {{
            if (currentFilter === 'all') {{
                return allBlogPosts;
            }}
            return allBlogPosts.filter(post => post.category === currentFilter);
        }}

        function renderBlogCards() {{
            const grid = document.getElementById('blogGrid');
            const posts = getFilteredPosts();

            if (posts.length === 0) {{
                grid.innerHTML = `
                    <div class="col-12 text-center text-muted py-5">
                        <h3>No posts in this category</h3>
                        <p>Check back soon for new content!</p>
                    </div>
                `;
                return;
            }}

            grid.innerHTML = posts.map(post => `
                <div class="col-md-6 col-lg-4" data-category="${{post.category}}">
                    <div class="card blog-card">
                        <img src="${{post.image}}" class="card-img-top" alt="${{post.title}}" onerror="this.src='https://via.placeholder.com/400x200?text=Image+Not+Found'">
                        <div class="card-body d-flex flex-column">
                            <div class="mb-2">
                                <span class="badge badge-date">${{post.category}}</span>
                                <span class="badge bg-secondary ms-2">${{new Date(post.date).toLocaleDateString()}}</span>
                            </div>
                            <h5 class="card-title">${{post.title}}</h5>
                            <p class="card-text flex-grow-1">${{post.excerpt}}</p>
                            <button class="btn btn-primary btn-read-more mt-auto" onclick="showArticle(${{post.id}})">
                                Read More →
                            </button>
                        </div>
                    </div>
                </div>
            `).join('');
        }}

        function showArticle(id) {{
            const post = allBlogPosts.find(p => p.id === id);
            if (!post) return;

            document.getElementById('blogGrid').classList.add('d-none');
            document.getElementById('heroSection').classList.add('d-none');
            document.getElementById('filterSection').style.display = 'none';
            document.getElementById('fullArticle').classList.remove('d-none');
            document.getElementById('articleContent').innerHTML = post.content;
            window.scrollTo(0, 0);
        }}

        function showHome() {{
            document.getElementById('blogGrid').classList.remove('d-none');
            document.getElementById('heroSection').classList.remove('d-none');
            document.getElementById('filterSection').style.display = 'block';
            document.getElementById('fullArticle').classList.add('d-none');
            window.scrollTo(0, 0);
            return false;
        }}

        // Initialize - render all posts
        renderBlogCards();
    </script>
</body>
</html>"""
        
        return html
    
    def _generate_blog_cards(self, posts: List[Dict]) -> str:
        """Generate HTML for all blog post cards"""
        if not posts:
            return """
            <div class="col-12 text-center text-muted py-5">
                <h3>No blog posts yet</h3>
                <p>Check back soon for new content!</p>
            </div>
            """
        
        cards_html = []
        for post in posts:
            if not post.get('published', True):
                continue
            
            date_str = post.get('date', '')
            if isinstance(date_str, datetime):
                date_str = date_str.strftime('%Y-%m-%d')
            
            card = f"""
            <div class="col-md-6 col-lg-4" data-category="{post['category']}">
                <div class="card blog-card">
                    <img src="{post['image_path']}" class="card-img-top" alt="{post['title']}" onerror="this.src='https://via.placeholder.com/400x200?text=Image+Not+Found'">
                    <div class="card-body d-flex flex-column">
                        <div class="mb-2">
                            <span class="badge badge-date">{post['category']}</span>
                            <span class="badge bg-secondary ms-2">{date_str}</span>
                        </div>
                        <h5 class="card-title">{post['title']}</h5>
                        <p class="card-text flex-grow-1">{post['excerpt']}</p>
                        <button class="btn btn-primary btn-read-more mt-auto" onclick="showArticle({post['id']})">
                            Read More →
                        </button>
                    </div>
                </div>
            </div>
            """
            cards_html.append(card)
        
        return '\n'.join(cards_html)
    
    def _generate_category_filters(self, categories: List[str]) -> str:
        """Generate HTML for category filter buttons"""
        buttons = ['<button class="btn btn-outline-primary filter-btn active" onclick="filterByCategory(\'all\')">All Posts</button>']
        
        for category in categories:
            buttons.append(
                f'<button class="btn btn-outline-primary filter-btn" onclick="filterByCategory(\'{category}\')">{category}</button>'
            )
        
        return '\n'.join(buttons)
    
    def _generate_posts_json(self, posts: List[Dict]) -> str:
        """Generate JavaScript array of blog posts"""
        import json
        import html
        
        # Filter only published posts and prepare for JSON
        published_posts = []
        for post in posts:
            if not post.get('published', True):
                continue
            
            # Convert datetime to string
            date_str = post.get('date', '')
            if isinstance(date_str, datetime):
                date_str = date_str.strftime('%Y-%m-%d')
            
            # Clean up content - remove excessive newlines
            content = post['content']
            # Remove multiple consecutive newlines
            import re
            content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
            content = content.strip()
            
            published_posts.append({
                'id': post['id'],
                'title': post['title'],
                'excerpt': post['excerpt'],
                'content': content,
                'category': post['category'],
                'image': post['image_path'],
                'date': date_str
            })
        
        # Use json.dumps which properly escapes everything for JavaScript
        return json.dumps(published_posts, ensure_ascii=False)
    
    def generate_about_page(self, content: str, output_filename: str = "about.html") -> str:
        """Generate an about page"""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About - {self.site_config['site_title']}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root {{
            --primary-color: {self.site_config.get('primary_color', '#2c3e50')};
            --accent-color: {self.site_config.get('accent_color', '#3498db')};
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8f9fa;
        }}

        .navbar {{
            background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .content-section {{
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            padding: 40px;
            margin: 40px 0;
        }}
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand fw-bold" href="index.html">
                {self.site_config['site_title']}
            </a>
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="index.html">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link active" href="about.html">About</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="content-section">
            {content}
        </div>
    </div>

    <footer class="bg-dark text-white text-center py-4 mt-5">
        <div class="container">
            <p class="mb-0">{self.site_config['footer_text']}</p>
            {f'<p class="mb-0 mt-2"><small>{self.site_config["acknowledgment"]}</small></p>' if self.site_config.get('acknowledgment') else ''}
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""
        
        output_path = os.path.join(self.output_folder, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return output_path
