"""Main Gradio application for the Company Brochure Generator MVP."""

import gradio as gr
from typing import Iterator
import time

from config import Config
from services.brochure_service import BrochureService
from services.export_service import ExportService
from utils.validators import validate_url, validate_company_name


# Initialize services
brochure_service = BrochureService()
export_service = ExportService()

# Global state for brochure content
current_brochure = {"content": ""}


def validate_inputs(company_name: str, company_url: str) -> tuple[bool, str]:
    """
    Validate user inputs.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Validate company name
    is_valid, error = validate_company_name(company_name)
    if not is_valid:
        return False, error
    
    # Validate URL
    is_valid, result = validate_url(company_url)
    if not is_valid:
        return False, result
    
    return True, ""


def generate_brochure_workflow(
    company_name: str,
    company_url: str,
    model: str,
    tone: str,
    custom_instructions: str,
    temperature: float,
    max_content_length: int,
    progress=gr.Progress()
) -> Iterator[tuple[str, str]]:
    """
    Main workflow for generating brochure with progress tracking.
    
    Yields:
        Tuples of (brochure_content, status_message)
    """
    global current_brochure
    
    # Validate inputs
    is_valid, error = validate_inputs(company_name, company_url)
    if not is_valid:
        yield "", f"❌ Error: {error}"
        return
    
    # Normalize URL
    _, normalized_url = validate_url(company_url)
    
    try:
        # Initialize
        yield "", "🚀 Starting brochure generation..."
        time.sleep(0.5)
        
        # Progress callback
        def update_progress(message: str, percentage: float):
            progress(percentage, desc=message)
        
        # Stream brochure generation
        brochure_content = ""
        
        for chunk in brochure_service.generate_brochure(
            company_name=company_name,
            url=normalized_url,
            model_name=model,
            tone_name=tone,
            custom_instructions=custom_instructions,
            temperature=temperature,
            max_content_length=max_content_length,
            progress_callback=update_progress
        ):
            brochure_content += chunk
            current_brochure["content"] = brochure_content
            yield brochure_content, f"✨ Generating brochure for {company_name}..."
        
        # Final status
        yield brochure_content, f"✅ Brochure generated successfully for {company_name}!"
        
    except Exception as e:
        error_msg = str(e)
        yield "", f"❌ Error: {error_msg}"


def get_link_preview(company_url: str, progress=gr.Progress()):
    """
    Get link suggestions for preview.
    
    Returns:
        Tuple of (status_message, gr.update for CheckboxGroup)
    """
    # Validate URL
    is_valid, result = validate_url(company_url)
    if not is_valid:
        return f"❌ Error: {result}", gr.update(choices=[], value=[])
    
    _, normalized_url = validate_url(company_url)
    
    try:
        progress(0.5, desc="Analyzing website links...")
        selected_links, error = brochure_service.get_link_suggestions(normalized_url)
        
        if error:
            return f"❌ Error: {error}", gr.update(choices=[], value=[])
        
        if not selected_links:
            return "⚠️ No relevant links found", gr.update(choices=[], value=[])
        
        # Format links for display
        link_choices = []
        for link in selected_links:
            link_type = link.get("type", "page")
            link_url = link.get("url", "")
            link_choices.append(f"{link_type}: {link_url}")
        
        # Return with all links selected by default
        return f"✅ Found {len(selected_links)} relevant links", gr.update(
            choices=link_choices,
            value=link_choices  # Pre-select all links
        )
        
    except Exception as e:
        return f"❌ Error: {str(e)}", gr.update(choices=[], value=[])


def export_as_pdf(company_name: str) -> tuple[str, str]:
    """
    Export current brochure as PDF.
    
    Returns:
        Tuple of (file_path, status_message)
    """
    if not current_brochure["content"]:
        return "", "❌ No brochure to export. Generate a brochure first."
    
    try:
        file_path = export_service.export_to_pdf(
            current_brochure["content"],
            company_name
        )
        return file_path, f"✅ PDF exported successfully to {file_path}"
    except Exception as e:
        return "", f"❌ Error exporting PDF: {str(e)}"


def export_as_html(company_name: str) -> tuple[str, str]:
    """
    Export current brochure as HTML.
    
    Returns:
        Tuple of (file_path, status_message)
    """
    if not current_brochure["content"]:
        return "", "❌ No brochure to export. Generate a brochure first."
    
    try:
        file_path = export_service.export_to_html(
            current_brochure["content"],
            company_name
        )
        return file_path, f"✅ HTML exported successfully to {file_path}"
    except Exception as e:
        return "", f"❌ Error exporting HTML: {str(e)}"


def create_app():
    """Create and configure the Gradio interface."""
    
    # Check API keys
    errors = Config.validate_api_keys()
    if errors:
        print("⚠️  Warning: " + ", ".join(errors))
    
    # Custom CSS
    custom_css = """
    .container {
        max-width: 1400px;
        margin: auto;
    }
    .header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .output-box {
        min-height: 400px;
    }
    """
    
    with gr.Blocks(css=custom_css, title="Company Brochure Generator") as app:
        # Header
        gr.HTML("""
        <div class="header">
            <h1>🏢 Company Brochure Generator</h1>
            <p>Create professional company brochures with AI</p>
        </div>
        """)
        
        with gr.Row():
            # Left Column - Inputs
            with gr.Column(scale=1):
                gr.Markdown("### 📝 Company Information")
                
                company_name = gr.Textbox(
                    label="Company Name",
                    placeholder="e.g., HuggingFace",
                    info="Enter the company name (2-100 characters)"
                )
                
                company_url = gr.Textbox(
                    label="Company Website URL",
                    placeholder="e.g., https://huggingface.co",
                    info="Enter the main website URL"
                )
                
                gr.Markdown("### ⚙️ Generation Settings")
                
                model = gr.Dropdown(
                    choices=Config.get_model_choices(),
                    value=Config.get_model_choices()[1],  # Default to Gemini
                    label="AI Model",
                    info="Select the language model to use"
                )
                
                tone = gr.Dropdown(
                    choices=Config.get_tone_choices(),
                    value="Professional",
                    label="Tone & Style",
                    info="Select the writing style"
                )
                
                custom_instructions = gr.Textbox(
                    label="Custom Instructions (Optional)",
                    placeholder="e.g., Focus on their AI products and developer tools",
                    lines=3,
                    info="Additional instructions for the AI"
                )
                
                with gr.Accordion("🔧 Advanced Options", open=False):
                    temperature = gr.Slider(
                        minimum=0,
                        maximum=1,
                        value=0.7,
                        step=0.1,
                        label="Temperature",
                        info="Higher = more creative, Lower = more focused"
                    )
                    
                    max_content_length = gr.Slider(
                        minimum=1000,
                        maximum=10000,
                        value=5000,
                        step=1000,
                        label="Max Content Length",
                        info="Maximum characters to analyze"
                    )
                
                generate_btn = gr.Button(
                    "🚀 Generate Brochure",
                    variant="primary",
                    size="lg"
                )
            
            # Right Column - Outputs
            with gr.Column(scale=2):
                status_box = gr.Textbox(
                    label="Status",
                    interactive=False,
                    show_label=True
                )
                
                # Link Preview Section
                with gr.Accordion("🔗 Link Preview (Optional)", open=False):
                    gr.Markdown("Preview and verify which pages will be analyzed")
                    
                    with gr.Row():
                        preview_btn = gr.Button("Preview Links", size="sm")
                        link_status = gr.Textbox(
                            label="Link Analysis Status",
                            interactive=False,
                            show_label=False
                        )
                    
                    links_preview = gr.CheckboxGroup(
                        label="Selected Links",
                        info="These links will be analyzed (automatically selected by AI)"
                    )
                
                # Brochure Output
                gr.Markdown("### 📄 Generated Brochure")
                
                brochure_output = gr.Markdown(
                    value="*Your brochure will appear here...*",
                    elem_classes=["output-box"]
                )
                
                # Export Options
                gr.Markdown("### 💾 Export Options")
                
                with gr.Row():
                    export_pdf_btn = gr.Button("📥 Export as PDF", size="sm")
                    export_html_btn = gr.Button("📥 Export as HTML", size="sm")
                
                export_status = gr.Textbox(
                    label="Export Status",
                    interactive=False,
                    show_label=False
                )
                
                export_file = gr.File(
                    label="Download File",
                    visible=True
                )
        
        # Footer
        gr.Markdown("""
        ---
        <div style="text-align: center; color: #666; font-size: 0.9em;">
            <p>Powered by OpenAI and Google Gemini | Built with Gradio</p>
            <p>💡 Tip: Start by entering a company name and website, then click Generate Brochure</p>
        </div>
        """)
        
        # Event Handlers
        generate_btn.click(
            fn=generate_brochure_workflow,
            inputs=[
                company_name,
                company_url,
                model,
                tone,
                custom_instructions,
                temperature,
                max_content_length
            ],
            outputs=[brochure_output, status_box]
        )
        
        preview_btn.click(
            fn=get_link_preview,
            inputs=[company_url],
            outputs=[link_status, links_preview]
        )
        
        export_pdf_btn.click(
            fn=export_as_pdf,
            inputs=[company_name],
            outputs=[export_file, export_status]
        )
        
        export_html_btn.click(
            fn=export_as_html,
            inputs=[company_name],
            outputs=[export_file, export_status]
        )
    
    return app


if __name__ == "__main__":
    # Create and launch the app
    app = create_app()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
    