"""Core brochure generation service that orchestrates the workflow."""

from typing import Callable, Iterator, Optional
from services.scraper_service import ScraperService
from services.llm_service import LLMService
from config import Config


class BrochureService:
    """Service for orchestrating the brochure generation workflow."""
    
    def __init__(self):
        """Initialize the brochure service."""
        self.scraper = ScraperService()
        self.llm = LLMService()
    
    def generate_brochure(
        self,
        company_name: str,
        url: str,
        model_name: str,
        tone_name: str,
        custom_instructions: str = "",
        temperature: float = 0.7,
        max_content_length: int = 5000,
        progress_callback: Optional[Callable[[str, float], None]] = None,
        selected_links: Optional[list[dict]] = None
    ) -> Iterator[str]:
        """
        Generate a company brochure with streaming output.
        
        Args:
            company_name: Name of the company
            url: Company website URL
            model_name: Display name of the model to use
            tone_name: Display name of the tone to use
            custom_instructions: Optional custom instructions
            temperature: Temperature for LLM generation
            max_content_length: Maximum content length to aggregate
            progress_callback: Optional callback for progress updates (message, percentage)
            selected_links: Optional pre-selected links (if None, will auto-select)
            
        Yields:
            Chunks of generated brochure content
        """
        # Convert display names to keys
        model_key = Config.get_model_key_by_name(model_name)
        tone_key = Config.get_tone_key_by_name(tone_name)
        
        try:
            # Step 1: Fetch main page content and links
            if progress_callback:
                progress_callback("Fetching main page content...", 0.1)
            
            main_content, links = self.scraper.fetch_website_content_and_links(url)
            
            # Step 2: Select relevant links if not provided
            if selected_links is None:
                if progress_callback:
                    progress_callback("Analyzing and selecting relevant links...", 0.3)
                
                selected_links = self.llm.select_relevant_links(url, links)
            
            # Step 3: Fetch content from selected links
            if progress_callback:
                progress_callback(f"Fetching content from {len(selected_links)} relevant pages...", 0.5)
            
            # Build aggregated content
            aggregated_content = f"## Landing Page:\n\n{main_content}\n\n## Relevant Pages:\n\n"
            
            for link_info in selected_links:
                link_url = link_info.get("url", "")
                link_type = link_info.get("type", "page")
                
                if link_url:
                    try:
                        content, _ = self.scraper.fetch_website_content_and_links(
                            link_url, 
                            only_content=True
                        )
                        aggregated_content += f"\n### {link_type.title()}\n{content}\n"
                    except Exception as e:
                        print(f"Warning: Failed to fetch {link_url}: {str(e)}")
                        continue
            
            # Truncate if too long
            aggregated_content = aggregated_content[:max_content_length]
            
            # Step 4: Generate brochure with streaming
            if progress_callback:
                progress_callback("Generating brochure...", 0.7)
            
            # Stream the brochure generation
            for chunk in self.llm.generate_brochure_stream(
                company_name=company_name,
                content=aggregated_content,
                model_key=model_key,
                tone=tone_key,
                custom_instructions=custom_instructions,
                temperature=temperature
            ):
                yield chunk
            
            # Final progress update
            if progress_callback:
                progress_callback("Brochure generation complete!", 1.0)
                
        except Exception as e:
            error_msg = f"Error generating brochure: {str(e)}"
            if progress_callback:
                progress_callback(error_msg, 0.0)
            raise Exception(error_msg)
    
    def get_link_suggestions(
        self,
        url: str
    ) -> tuple[list[dict], str]:
        """
        Get link suggestions without generating the brochure.
        
        Args:
            url: Company website URL
            
        Returns:
            Tuple of (selected_links, error_message)
        """
        try:
            # Fetch main page links
            _, links = self.scraper.fetch_website_content_and_links(url)
            
            if not links:
                return [], "No links found on the page"
            
            # Get LLM suggestions
            selected_links = self.llm.select_relevant_links(url, links)
            
            if not selected_links:
                return [], "No relevant links identified"
            
            return selected_links, ""
            
        except Exception as e:
            return [], f"Error getting link suggestions: {str(e)}"
    
    def clear_cache(self):
        """Clear the scraper cache."""
        self.scraper.clear_cache()