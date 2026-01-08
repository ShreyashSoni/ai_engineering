"""Export service for generating PDF and HTML files from brochure content."""

import os
from datetime import datetime
from typing import Optional
import markdown2


class ExportService:
    """Service for exporting brochures to various formats."""
    
    def __init__(self):
        """Initialize the export service."""
        self.exports_dir = "exports"
        os.makedirs(self.exports_dir, exist_ok=True)
    
    def _get_html_template(self, company_name: str, content_html: str) -> str:
        """
        Get HTML template with embedded CSS.
        
        Args:
            company_name: Name of the company
            content_html: HTML content of the brochure
            
        Returns:
            Complete HTML document
        """
        css = """
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background-color: white;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h1 {
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }
            h2 {
                color: #34495e;
                margin-top: 30px;
            }
            h3 {
                color: #7f8c8d;
            }
            a {
                color: #3498db;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            .header {
                text-align: center;
                margin-bottom: 40px;
            }
            .footer {
                margin-top: 60px;
                padding-top: 20px;
                border-top: 1px solid #ecf0f1;
                text-align: center;
                color: #95a5a6;
                font-size: 0.9em;
            }
            @media print {
                body {
                    background-color: white;
                }
                .container {
                    box-shadow: none;
                }
            }
            @media (max-width: 768px) {
                body {
                    padding: 10px;
                }
                .container {
                    padding: 20px;
                }
            }
        </style>
        """
        
        current_date = datetime.now().strftime("%d %B, %Y")
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Company brochure for {company_name}">
    <meta name="generator" content="Company Brochure Generator">
    <title>{company_name} - Company Brochure</title>
    {css}
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{company_name}</h1>
            <p><em>Company Brochure</em></p>
        </div>
        {content_html}
        <div class="footer">
            <p>Generated on {current_date}</p>
            <p>Created with Company Brochure Generator</p>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def export_to_html(
        self,
        markdown_content: str,
        company_name: str,
        filename: Optional[str] = None
    ) -> str:
        """
        Export brochure to standalone HTML file.
        
        Args:
            markdown_content: Brochure content in markdown format
            company_name: Name of the company
            filename: Optional custom filename
            
        Returns:
            Path to the generated HTML file
        """
        try:
            # Convert markdown to HTML
            content_html = markdown2.markdown(
                markdown_content,
                extras=["fenced-code-blocks", "tables", "header-ids"]
            )
            
            # Get complete HTML document
            html = self._get_html_template(company_name, content_html)
            
            # Generate filename
            if not filename:
                safe_name = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{safe_name}_{timestamp}.html"
            
            # Save file
            filepath = os.path.join(self.exports_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            
            return filepath
            
        except Exception as e:
            raise Exception(f"Error exporting to HTML: {str(e)}")
    
    def export_to_pdf(
        self,
        markdown_content: str,
        company_name: str,
        filename: Optional[str] = None
    ) -> str:
        """
        Export brochure to PDF file.
        
        Args:
            markdown_content: Brochure content in markdown format
            company_name: Name of the company
            filename: Optional custom filename
            
        Returns:
            Path to the generated PDF file
        """
        try:
            # First convert to HTML
            content_html = markdown2.markdown(
                markdown_content,
                extras=["fenced-code-blocks", "tables", "header-ids"]
            )
            
            html = self._get_html_template(company_name, content_html)
            
            # Generate filename
            if not filename:
                safe_name = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{safe_name}_{timestamp}.pdf"
            
            filepath = os.path.join(self.exports_dir, filename)
            
            # Try to import weasyprint
            try:
                from weasyprint import HTML
                HTML(string=html).write_pdf(filepath)
                return filepath
            except ImportError:
                # Fallback: save as HTML if weasyprint not available
                html_path = filepath.replace('.pdf', '.html')
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html)
                return html_path + " (PDF generation requires weasyprint - saved as HTML instead)"
                
        except Exception as e:
            raise Exception(f"Error exporting to PDF: {str(e)}")
    
    def get_exports_directory(self) -> str:
        """Get the path to the exports directory."""
        return os.path.abspath(self.exports_dir)