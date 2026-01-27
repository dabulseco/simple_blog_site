"""
Database utility functions for blog operations
"""

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class DatabaseManager:
    """Handle all database operations"""
    
    def __init__(self):
        self.config = DB_CONFIG
        
    def get_connection(self):
        """Create and return a database connection"""
        try:
            connection = mysql.connector.connect(**self.config)
            return connection
        except Error as e:
            raise Exception(f"Error connecting to MySQL: {e}")
    
    def test_connection(self) -> Tuple[bool, str]:
        """Test database connection"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            conn.close()
            return True, "Connection successful!"
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
    
    # ==================== Blog Posts ====================
    
    def get_all_posts(self, published_only: bool = False) -> List[Dict]:
        """Retrieve all blog posts"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT id, title, excerpt, content, category, image_path, 
                       DATE_FORMAT(date, '%Y-%m-%d') as date, published, sort_order,
                       created_at, updated_at
                FROM blog_posts
            """
            
            if published_only:
                query += " WHERE published = TRUE"
            
            query += " ORDER BY date DESC, sort_order DESC, id DESC"
            
            cursor.execute(query)
            posts = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return posts
        except Error as e:
            raise Exception(f"Error fetching posts: {e}")
    
    def get_post_by_id(self, post_id: int) -> Optional[Dict]:
        """Retrieve a single post by ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT id, title, excerpt, content, category, image_path, 
                       DATE_FORMAT(date, '%Y-%m-%d') as date, published, sort_order
                FROM blog_posts
                WHERE id = %s
            """
            
            cursor.execute(query, (post_id,))
            post = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return post
        except Error as e:
            raise Exception(f"Error fetching post: {e}")
    
    def add_post(self, title: str, excerpt: str, content: str, category: str, 
                 image_path: str, date: str, published: bool = True) -> int:
        """Add a new blog post"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO blog_posts (title, excerpt, content, category, image_path, date, published)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(query, (title, excerpt, content, category, image_path, date, published))
            conn.commit()
            
            post_id = cursor.lastrowid
            
            cursor.close()
            conn.close()
            
            return post_id
        except Error as e:
            raise Exception(f"Error adding post: {e}")
    
    def update_post(self, post_id: int, title: str, excerpt: str, content: str, 
                   category: str, image_path: str, date: str, published: bool) -> bool:
        """Update an existing blog post"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE blog_posts 
                SET title = %s, excerpt = %s, content = %s, category = %s, 
                    image_path = %s, date = %s, published = %s
                WHERE id = %s
            """
            
            cursor.execute(query, (title, excerpt, content, category, image_path, date, published, post_id))
            conn.commit()
            
            rows_affected = cursor.rowcount
            
            cursor.close()
            conn.close()
            
            return rows_affected > 0
        except Error as e:
            raise Exception(f"Error updating post: {e}")
    
    def delete_post(self, post_id: int) -> bool:
        """Delete a blog post"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = "DELETE FROM blog_posts WHERE id = %s"
            cursor.execute(query, (post_id,))
            conn.commit()
            
            rows_affected = cursor.rowcount
            
            cursor.close()
            conn.close()
            
            return rows_affected > 0
        except Error as e:
            raise Exception(f"Error deleting post: {e}")
    
    def get_posts_by_category(self, category: str, published_only: bool = True) -> List[Dict]:
        """Get posts filtered by category"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT id, title, excerpt, content, category, image_path, 
                       DATE_FORMAT(date, '%Y-%m-%d') as date, published
                FROM blog_posts
                WHERE category = %s
            """
            
            if published_only:
                query += " AND published = TRUE"
            
            query += " ORDER BY date DESC, id DESC"
            
            cursor.execute(query, (category,))
            posts = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return posts
        except Error as e:
            raise Exception(f"Error fetching posts by category: {e}")
    
    # ==================== Categories ====================
    
    def get_all_categories(self) -> List[Dict]:
        """Get all categories"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM categories ORDER BY display_order, name"
            cursor.execute(query)
            categories = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return categories
        except Error as e:
            raise Exception(f"Error fetching categories: {e}")
    
    def get_unique_categories_from_posts(self) -> List[str]:
        """Get unique categories from blog posts"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = "SELECT DISTINCT category FROM blog_posts WHERE published = TRUE ORDER BY category"
            cursor.execute(query)
            categories = [row[0] for row in cursor.fetchall()]
            
            cursor.close()
            conn.close()
            
            return categories
        except Error as e:
            raise Exception(f"Error fetching categories: {e}")
    
    def add_category(self, name: str, description: str = "", display_order: int = 0) -> int:
        """Add a new category"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = "INSERT INTO categories (name, description, display_order) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, description, display_order))
            conn.commit()
            
            category_id = cursor.lastrowid
            
            cursor.close()
            conn.close()
            
            return category_id
        except Error as e:
            raise Exception(f"Error adding category: {e}")
    
    # ==================== Site Config ====================
    
    def get_site_config(self, key: str) -> Optional[str]:
        """Get a site configuration value"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = "SELECT config_value FROM site_config WHERE config_key = %s"
            cursor.execute(query, (key,))
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return result[0] if result else None
        except Error as e:
            raise Exception(f"Error fetching config: {e}")
    
    def update_site_config(self, key: str, value: str) -> bool:
        """Update a site configuration value"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO site_config (config_key, config_value) 
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE config_value = %s
            """
            cursor.execute(query, (key, value, value))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return True
        except Error as e:
            raise Exception(f"Error updating config: {e}")
    
    def get_all_site_config(self) -> Dict[str, str]:
        """Get all site configuration"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT config_key, config_value FROM site_config"
            cursor.execute(query)
            results = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return {row['config_key']: row['config_value'] for row in results}
        except Error as e:
            raise Exception(f"Error fetching all config: {e}")
    
    # ==================== Statistics ====================
    
    def get_post_count(self, published_only: bool = True) -> int:
        """Get total number of posts"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = "SELECT COUNT(*) FROM blog_posts"
            if published_only:
                query += " WHERE published = TRUE"
            
            cursor.execute(query)
            count = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            return count
        except Error as e:
            raise Exception(f"Error getting post count: {e}")
    
    def get_category_post_counts(self) -> Dict[str, int]:
        """Get post counts by category"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT category, COUNT(*) as count 
                FROM blog_posts 
                WHERE published = TRUE 
                GROUP BY category 
                ORDER BY category
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return {row[0]: row[1] for row in results}
        except Error as e:
            raise Exception(f"Error getting category counts: {e}")
