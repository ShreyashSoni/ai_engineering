# Company Brochure Generator MVP

An AI-powered web application that automatically generates professional company brochures from website URLs using advanced language models.

## 🌟 Features

- **Multi-Model Support**: Choose between GPT-5 Nano and Gemini 2.5 Flash
- **Streaming Output**: Real-time brochure generation with typewriter effect
- **Smart Link Analysis**: AI automatically selects relevant pages to analyze
- **Tone Customization**: 5 pre-built tones (Professional, Friendly, Humorous, Technical, Executive)
- **Export Options**: Download brochures as PDF or standalone HTML
- **Link Preview**: Review and verify which pages will be analyzed
- **Progress Tracking**: Visual feedback during generation process
- **Caching**: Intelligent caching for faster subsequent requests

## 📋 Prerequisites

- Python 3.11 or higher
- OpenAI API key
- Google (Gemini) API key
- UV package manager (recommended) or pip

## 🚀 Quick Start

### 1. Install Dependencies

Using UV (recommended):
```bash
cd 01_company_brochure_generator
uv sync
```

Using pip:
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file in the project root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

### 3. Run the Application

**Option A: Using the run script (Recommended for macOS)**
```bash
./run.sh
```

**Option B: Direct Python**
```bash
python app.py
```

The application will launch at `http://localhost:7860`

> **Note for macOS users**: The app automatically sets up the library path for WeasyPrint (PDF export). If you encounter issues, the `run.sh` script provides a fallback.

## 💻 Usage

### Basic Usage

1. **Enter Company Information**
   - Company Name: Enter the company's name
   - Company Website URL: Enter the main website (e.g., https://huggingface.co)

2. **Select Generation Settings**
   - AI Model: Choose between GPT-5 Nano or Gemini 2.5 Flash
   - Tone & Style: Select desired tone (Professional, Friendly, etc.)
   - Custom Instructions: Optional additional guidance for the AI

3. **Generate Brochure**
   - Click "Generate Brochure" button
   - Watch real-time progress updates
   - See brochure appear with streaming effect

4. **Export** (Optional)
   - Click "Export as PDF" for PDF format
   - Click "Export as HTML" for standalone HTML file
   - Files saved to `exports/` directory

### Advanced Features

#### Link Preview
1. Enter company URL
2. Click "Preview Links" in the Link Preview accordion
3. Review AI-selected links before generation
4. Modify selections if needed

#### Advanced Options
- **Temperature**: Control creativity (0 = focused, 1 = creative)
- **Max Content Length**: Limit characters analyzed (1000-10000)

## 🏗️ Architecture

```
01_company_brochure_generator/
├── app.py                      # Main Gradio application
├── config.py                   # Configuration and constants
├── services/                   # Business logic layer
│   ├── scraper_service.py      # Web scraping with caching
│   ├── llm_service.py          # LLM API interactions
│   ├── brochure_service.py     # Orchestration logic
│   └── export_service.py       # PDF/HTML export
├── utils/                      # Utility functions
│   ├── validators.py           # Input validation
│   └── prompts.py              # LLM prompt templates
├── ui/                         # UI components (reserved)
├── exports/                    # Generated export files
└── README.md                   # This file
```

## 🎨 Tone Styles

### Professional
Formal and authoritative language suitable for investors and stakeholders. Focuses on achievements, metrics, and business value.

### Friendly
Warm and approachable language for general audiences. Emphasizes company values and human elements.

### Humorous
Witty and entertaining while maintaining professionalism. Makes content fun and memorable.

### Technical
Detailed and precise language for technical stakeholders. Highlights innovation and technical capabilities.

### Executive
Concise and high-level for C-suite readers. Strategic vision and key differentiators only.

## 🔧 Configuration

Edit [`config.py`](config.py) to customize:
- Model settings and parameters
- Content length limits
- Timeout values
- Cache duration
- Export formats

## 📊 Model Comparison

| Feature | GPT-5 Nano | Gemini 2.5 Flash |
|---------|------------|------------------|
| Max Tokens | 16,000 | 32,000 |
| Speed | Fast | Very Fast |
| Cost | Moderate | Low |
| Streaming | ✅ | ✅ |
| Best For | Detailed analysis | Quick generation |

## 🐛 Troubleshooting

### API Key Errors
- Ensure `.env` file is in the project root
- Verify API keys are valid and active
- Check API key format (no extra spaces)

### Import Errors
- Run `uv sync` or `pip install -r requirements.txt`
- Ensure Python 3.11+ is being used
- Check virtual environment is activated

### Slow Generation
- Try Gemini 2.5 Flash for faster results
- Reduce max content length in advanced options
- Check internet connection speed

### PDF Export Issues
- WeasyPrint may require system dependencies
- On macOS: `brew install cairo pango gdk-pixbuf libffi`
- On Ubuntu: `apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info`
- Fallback: Use HTML export instead

## 📝 Examples

### Example 1: Tech Company
```
Company: HuggingFace
URL: https://huggingface.co
Model: Gemini 2.5 Flash
Tone: Professional
```

### Example 2: Startup
```
Company: Anthropic
URL: https://www.anthropic.com
Model: GPT-5 Nano
Tone: Technical
Custom Instructions: Focus on AI safety and research
```

## 🔒 Security Considerations

- API keys stored in `.env` (never commit to git)
- Input validation prevents malicious URLs
- Content sanitization removes harmful code
- Rate limiting prevents abuse
- No user data storage

## 📈 Performance Tips

1. **Use Caching**: Repeated requests for same URLs are faster
2. **Choose Gemini**: For speed-optimized generation
3. **Limit Content**: Use advanced options to reduce processing
4. **Pre-select Links**: Use link preview to reduce API calls

## 🤝 Contributing

This is an MVP. Potential improvements:
- Multi-language support
- Batch processing for multiple companies
- Custom branding templates
- User authentication and history
- API endpoint for integrations
- Enhanced analytics

## 🙏 Acknowledgments

- Built with [Gradio](https://gradio.app)
- Powered by OpenAI and Google Gemini
- Web scraping with BeautifulSoup
- PDF generation with WeasyPrint