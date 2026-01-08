"""Prompt templates for the Company Brochure Generator."""

# System prompt for link selection
LINK_SELECTION_SYSTEM_PROMPT = """
You are provided with a list of links found on a webpage.

You are able to decide which of the links would be most relevant to include in a brochure about the company,
such as links to an About page, or a Company page, or Careers/Jobs pages.

You should respond in JSON as in this example:

{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"}
    ]
}
"""


# Base system prompt for brochure generation
BASE_BROCHURE_SYSTEM_PROMPT = """
You are an assistant that analyzes the contents of several relevant pages from a company website
and creates a short brochure about the company for prospective customers, investors and recruits.

Respond in markdown without code blocks.

Include details of company culture, customers and careers/jobs if you have the information.
"""


# Tone-specific additions to the system prompt
TONE_PROMPTS = {
    "professional": """
Use formal and authoritative language suitable for investors and stakeholders.
Maintain a professional and corporate tone throughout the brochure.
Focus on achievements, metrics, and business value.
""",
    "friendly": """
Use warm and approachable language that resonates with a general audience.
Make the content engaging and easy to understand.
Emphasize the human side of the company and its values.
""",
    "humorous": """
Use witty and entertaining language while maintaining professionalism.
Include light humor and creative wordplay where appropriate.
Keep the content fun and memorable without sacrificing important information.
""",
    "technical": """
Use detailed and precise language suitable for technical stakeholders.
Include technical details, technologies, and methodologies where relevant.
Focus on innovation, technical capabilities, and engineering excellence.
""",
    "executive": """
Use concise and high-level language appropriate for C-suite readers.
Focus on strategic vision, market position, and key differentiators.
Keep it brief and impactful, highlighting only the most critical information.
"""
}


def get_link_selection_user_prompt(url: str, links: list[str]) -> str:
    """
    Generate the user prompt for link selection.
    
    Args:
        url: The main website URL
        links: List of links found on the page
        
    Returns:
        Formatted user prompt
    """
    user_prompt = f"""
Here is the list of links on the website {url} -
Please decide which of these are relevant web links for a brochure about the company. 
Respond with the full https URL in JSON format.
Do not include Terms of Service, Privacy, email links.

Links (some might be relative links):

"""
    user_prompt += "\n".join(links)
    return user_prompt


def get_brochure_system_prompt(tone: str = "professional") -> str:
    """
    Generate the system prompt for brochure generation based on tone.
    
    Args:
        tone: The desired tone (professional, friendly, humorous, technical, executive)
        
    Returns:
        Complete system prompt
    """
    tone_addition = TONE_PROMPTS.get(tone, TONE_PROMPTS["professional"])
    return BASE_BROCHURE_SYSTEM_PROMPT + "\n" + tone_addition


def get_brochure_user_prompt(
    company_name: str,
    content: str,
    custom_instructions: str = ""
) -> str:
    """
    Generate the user prompt for brochure generation.
    
    Args:
        company_name: Name of the company
        content: Aggregated content from website pages
        custom_instructions: Optional custom instructions from user
        
    Returns:
        Formatted user prompt
    """
    user_prompt = f"""
You are looking at a company called: {company_name}

Here are the contents of its landing page and other relevant pages;
use this information to build a short brochure of the company in markdown without code blocks.

"""
    
    if custom_instructions:
        user_prompt += f"\nAdditional instructions: {custom_instructions}\n\n"
    
    user_prompt += content
    
    return user_prompt