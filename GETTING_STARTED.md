# Getting Started with Crawler-Duel

This guide will help you get started with Crawler-Duel quickly.

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yadavanujkumar/OmniCrawler-Analysis.git
cd OmniCrawler-Analysis
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Playwright Browsers
```bash
playwright install chromium
```

### 4. (Optional) Configure API Keys
If you want to use the AI-Agentic crawler with Firecrawl:

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Firecrawl API key:
   ```
   FIRECRAWL_API_KEY=your_actual_api_key_here
   ```

   Get an API key from: https://firecrawl.dev

## Quick Test

Run the demo script to verify your installation:
```bash
python demo.py
```

This will show you how the benchmarking system works with mock data.

## Running the Dashboard

Start the Streamlit dashboard:
```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Basic Usage

1. **Enter a URL**: Type or paste the URL you want to crawl in the sidebar

2. **Select Crawlers**: Choose which crawlers to include in the race:
   - ☑️ Lightweight (HTTP) - Always available
   - ☑️ Browser-Based (Playwright) - Requires browser installation
   - ☑️ AI-Agentic (Firecrawl) - Requires API key

3. **Configure Anti-Bot** (Optional):
   - Enable anti-bot features for user-agent randomization
   - Add proxies if you want proxy rotation

4. **Start the Race**: Click "🏁 Start Race" and watch the live competition!

## Understanding Results

### Time-to-Complete
Shows how long each crawler took to fetch and process the page.

### Data Integrity
Checks if the crawler was blocked or returned incomplete data:
- ✓ = Clean data
- ✗ = Blocked, empty, or incomplete data

### Quality Score (0-100)
Rates the structural quality of the output:
- **90+**: Structured JSON/Markdown (AI crawlers)
- **55-70**: Clean text extraction (Browser-based)
- **40-50**: Raw HTML (Lightweight)

### Cost-Benefit Analysis
Compares the resource cost vs. value:
- **Lightweight**: Cost=1, Fast but basic
- **Browser-Based**: Cost=5, Good balance
- **AI-Agentic**: Cost=10, Best quality but expensive

## Example URLs to Try

### Good for All Crawlers
- https://example.com - Simple static page
- https://httpbin.org/html - Testing HTML page

### Better for Browser-Based
- Dynamic JavaScript sites
- Single-page applications (SPAs)

### Best for AI-Agentic
- Complex articles with lots of text
- Pages where you need clean markdown
- Sites with structured data

## Troubleshooting

### Playwright Browser Not Found
```bash
playwright install chromium
```

### Network Errors
Check your internet connection and firewall settings.

### Firecrawl API Errors
- Verify your API key in `.env`
- Check your Firecrawl account quota

### Import Errors
```bash
pip install -r requirements.txt --upgrade
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the [code structure](README.md#architecture)
- Try different websites and compare crawler performance
- Experiment with anti-bot settings

## Need Help?

Open an issue on GitHub: https://github.com/yadavanujkumar/OmniCrawler-Analysis/issues
