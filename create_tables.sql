-- ============================================
-- AI Education Blog - Database Setup
-- Database: FCS3
-- ============================================

USE FCS3;

-- Drop existing table if you want to start fresh (CAUTION: This deletes all data!)
-- DROP TABLE IF EXISTS blog_posts;

-- Create blog_posts table
CREATE TABLE IF NOT EXISTS blog_posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    excerpt TEXT NOT NULL,
    content LONGTEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    image_path VARCHAR(500) NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    published BOOLEAN DEFAULT TRUE,
    sort_order INT DEFAULT 0,
    
    INDEX idx_category (category),
    INDEX idx_date (date),
    INDEX idx_published (published),
    INDEX idx_sort_order (sort_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create categories table (for managing categories)
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_name (name),
    INDEX idx_display_order (display_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert some default categories (optional)
INSERT IGNORE INTO categories (name, description, display_order) VALUES
    ('Teaching Tools', 'Tools and resources for educators', 1),
    ('AI Research', 'Latest research in AI and education', 2),
    ('Case Studies', 'Real-world examples and success stories', 3),
    ('Best Practices', 'Guidelines and recommendations', 4);

-- Create site_config table (for storing site settings)
CREATE TABLE IF NOT EXISTS site_config (
    id INT AUTO_INCREMENT PRIMARY KEY,
    config_key VARCHAR(100) NOT NULL UNIQUE,
    config_value TEXT,
    description VARCHAR(255),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_config_key (config_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert default site configuration
INSERT IGNORE INTO site_config (config_key, config_value, description) VALUES
    ('site_title', 'AI in Education', 'Main site title'),
    ('site_tagline', 'Exploring the intersection of artificial intelligence and learning', 'Site tagline/subtitle'),
    ('footer_text', '© 2026, Dylan A. Bulseco, Ph.D., AI in Education Blog. All rights reserved.', 'Footer copyright text'),
    ('logo_path', '/images/logo.png', 'Path to site logo'),
    ('primary_color', '#2c3e50', 'Primary theme color'),
    ('accent_color', '#3498db', 'Accent theme color');

-- Show tables created
SHOW TABLES;

-- Show structure of blog_posts table
DESCRIBE blog_posts;

SELECT 'Database tables created successfully!' AS status;
