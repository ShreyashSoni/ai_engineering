"""LLM service for the Company Brochure Generator."""

import json
from typing import Iterator, Optional
from openai import OpenAI

from config import Config
from utils.prompts import (
    LINK_SELECTION_SYSTEM_PROMPT,
    get_link_selection_user_prompt,
    get_brochure_system_prompt,
    get_brochure_user_prompt
)


class LLMService:
    """Service for interacting with LLM APIs (OpenAI and Gemini)."""
    
    def __init__(self):
        """Initialize the LLM service with API clients."""
        self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.gemini_client = OpenAI(
            api_key=Config.GOOGLE_API_KEY,
            base_url=Config.GEMINI_BASE_URL
        )
    
    def _get_client(self, model_key: str) -> OpenAI:
        """
        Get the appropriate client based on model.
        
        Args:
            model_key: The model key (e.g., 'gpt-5-nano' or 'gemini-2.5-flash')
            
        Returns:
            OpenAI client instance
        """
        model_info = Config.MODELS.get(model_key, Config.MODELS[Config.GEMINI_MODEL])
        provider = model_info["provider"]
        
        if provider == "openai":
            return self.openai_client
        else:
            return self.gemini_client
    
    def select_relevant_links(
        self,
        url: str,
        links: list[str]
    ) -> list[dict]:
        """
        Use LLM to select relevant links from a list.
        
        Args:
            url: The main website URL
            links: List of links found on the page
            
        Returns:
            List of dictionaries with 'type' and 'url' keys
        """
        if not links:
            return []
        
        try:
            # Always use Gemini for link selection (cheaper and good at structured output)
            client = self.gemini_client
            model = Config.GEMINI_MODEL
            
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": LINK_SELECTION_SYSTEM_PROMPT},
                    {"role": "user", "content": get_link_selection_user_prompt(url, links)}
                ],
                response_format={"type": "json_object"}
            )
            
            result = response.choices[0].message.content
            if result:
                parsed = json.loads(result)
                return parsed.get("links", [])
            
            return []
            
        except Exception as e:
            print(f"Error selecting links: {str(e)}")
            return []
    
    def generate_brochure(
        self,
        company_name: str,
        content: str,
        model_key: str,
        tone: str = "professional",
        custom_instructions: str = "",
        temperature: float = 0.7
    ) -> str:
        """
        Generate brochure content without streaming.
        
        Args:
            company_name: Name of the company
            content: Aggregated content from website pages
            model_key: The model to use
            tone: The tone/style to use
            custom_instructions: Optional custom instructions
            temperature: Temperature for generation
            
        Returns:
            Generated brochure content
        """
        try:
            client = self._get_client(model_key)
            
            response = client.chat.completions.create(
                model=model_key,
                messages=[
                    {"role": "system", "content": get_brochure_system_prompt(tone)},
                    {"role": "user", "content": get_brochure_user_prompt(
                        company_name, content, custom_instructions
                    )}
                ],
                temperature=temperature,
                max_tokens=Config.MAX_TOKENS
            )
            
            result = response.choices[0].message.content
            return result if result else ""
            
        except Exception as e:
            raise Exception(f"Error generating brochure: {str(e)}")
    
    def generate_brochure_stream(
        self,
        company_name: str,
        content: str,
        model_key: str,
        tone: str = "professional",
        custom_instructions: str = "",
        temperature: float = 0.7
    ) -> Iterator[str]:
        """
        Generate brochure content with streaming.
        
        Args:
            company_name: Name of the company
            content: Aggregated content from website pages
            model_key: The model to use
            tone: The tone/style to use
            custom_instructions: Optional custom instructions
            temperature: Temperature for generation
            
        Yields:
            Chunks of generated content
        """
        try:
            client = self._get_client(model_key)
            
            stream = client.chat.completions.create(
                model=model_key,
                messages=[
                    {"role": "system", "content": get_brochure_system_prompt(tone)},
                    {"role": "user", "content": get_brochure_user_prompt(
                        company_name, content, custom_instructions
                    )}
                ],
                temperature=temperature,
                max_tokens=Config.MAX_TOKENS,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            raise Exception(f"Error generating brochure stream: {str(e)}")