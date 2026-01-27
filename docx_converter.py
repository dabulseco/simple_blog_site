"""
Document Converter
Convert .docx files to HTML with formatting preservation
"""

import mammoth
import re
from io import BytesIO
from typing import Tuple


class DocxConverter:
    """Convert DOCX files to clean HTML"""
    
    @staticmethod
    def convert_to_html(docx_file_path: str) -> Tuple[str, bool, str]:
        """
        Convert a .docx file to HTML
        
        Args:
            docx_file_path: Path to the .docx file
            
        Returns:
            Tuple of (html_content, success, error_message)
        """
        try:
            # Custom style map for better HTML conversion
            style_map = """
            p[style-name='Heading 1'] => h3.heading1:fresh
            p[style-name='Heading 2'] => h4.heading2:fresh
            p[style-name='Heading 3'] => h5.heading3:fresh
            p[style-name='Title'] => h2.title:fresh
            p[style-name='Subtitle'] => h3.subtitle:fresh
            r[style-name='Strong'] => strong
            r[style-name='Emphasis'] => em
            """
            
            # Convert DOCX to HTML
            with open(docx_file_path, "rb") as docx_file:
                result = mammoth.convert_to_html(
                    docx_file,
                    style_map=style_map
                )
            
            html = result.value
            messages = result.messages
            
            # Clean up the HTML
            html = DocxConverter._clean_html(html)
            
            # Check for conversion warnings
            warning_msg = ""
            if messages:
                warning_msg = f"Conversion completed with {len(messages)} warnings"
            
            return html, True, warning_msg
            
        except Exception as e:
            return "", False, f"Error converting document: {str(e)}"
    
    @staticmethod
    def convert_bytes_to_html(docx_bytes: bytes) -> Tuple[str, bool, str]:
        """
        Convert DOCX bytes to HTML
        
        Args:
            docx_bytes: Bytes of the .docx file
            
        Returns:
            Tuple of (html_content, success, error_message)
        """
        try:
            # Custom style map
            style_map = """
            p[style-name='Heading 1'] => h3.heading1:fresh
            p[style-name='Heading 2'] => h4.heading2:fresh
            p[style-name='Heading 3'] => h5.heading3:fresh
            p[style-name='Title'] => h2.title:fresh
            p[style-name='Subtitle'] => h3.subtitle:fresh
            r[style-name='Strong'] => strong
            r[style-name='Emphasis'] => em
            """
            
            # Create a BytesIO object from bytes
            docx_file = BytesIO(docx_bytes)
            
            # Convert from BytesIO
            result = mammoth.convert_to_html(
                docx_file,
                style_map=style_map
            )
            
            html = result.value
            messages = result.messages
            
            # Clean up HTML
            html = DocxConverter._clean_html(html)
            
            # Check for warnings
            warning_msg = ""
            if messages:
                warning_msg = f"Conversion completed with {len(messages)} warnings"
            
            return html, True, warning_msg
            
        except Exception as e:
            return "", False, f"Error converting document: {str(e)}"
    
    @staticmethod
    def _clean_html(html: str) -> str:
        """
        Clean up converted HTML
        
        Args:
            html: Raw HTML from conversion
            
        Returns:
            Cleaned HTML string
        """
        # Remove empty paragraphs
        html = re.sub(r'<p>\s*</p>', '', html)
        html = re.sub(r'<p></p>', '', html)
        
        # Add Bootstrap classes to elements
        html = html.replace('<h3', '<h3 class="mt-4 mb-3"')
        html = html.replace('<h4', '<h4 class="mt-3 mb-2"')
        html = html.replace('<h5', '<h5 class="mt-2 mb-2"')
        html = html.replace('<p>', '<p class="mb-3">')
        html = html.replace('<ul>', '<ul class="mb-3">')
        html = html.replace('<ol>', '<ol class="mb-3">')
        html = html.replace('<img ', '<img class="img-fluid mb-3" ')
        html = html.replace('<table>', '<table class="table table-bordered mb-3">')
        html = html.replace('<blockquote>', '<blockquote class="blockquote mb-3">')
        
        # Ensure images are responsive
        html = re.sub(r'<img(?![^>]*class=)', '<img class="img-fluid" ', html)
        
        # Add some spacing
        html = html.strip()
        
        return html
    
    @staticmethod
    def extract_text(docx_file_path: str) -> str:
        """
        Extract plain text from DOCX file
        
        Args:
            docx_file_path: Path to the .docx file
            
        Returns:
            Plain text content
        """
        try:
            with open(docx_file_path, "rb") as docx_file:
                result = mammoth.extract_raw_text(docx_file)
            return result.value
        except Exception as e:
            return f"Error extracting text: {str(e)}"
    
    @staticmethod
    def get_excerpt_from_html(html: str, max_length: int = 200) -> str:
        """
        Extract a text excerpt from HTML content
        
        Args:
            html: HTML content
            max_length: Maximum length of excerpt
            
        Returns:
            Plain text excerpt
        """
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Truncate to max length
        if len(text) > max_length:
            text = text[:max_length].rsplit(' ', 1)[0] + '...'
        
        return text


# Convenience functions
def convert_docx_to_html(docx_path: str) -> Tuple[str, bool, str]:
    """Convert DOCX file to HTML"""
    return DocxConverter.convert_to_html(docx_path)


def convert_docx_bytes_to_html(docx_bytes: bytes) -> Tuple[str, bool, str]:
    """Convert DOCX bytes to HTML"""
    return DocxConverter.convert_bytes_to_html(docx_bytes)


def extract_excerpt_from_html(html: str, max_length: int = 200) -> str:
    """Get excerpt from HTML"""
    return DocxConverter.get_excerpt_from_html(html, max_length)
