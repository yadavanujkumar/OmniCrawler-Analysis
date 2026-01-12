# Crawler-Duel 🕷️

A Multi-Agent Web Crawling & Benchmarking Suite that pits three different crawler architectures against each other in a live race.

## 🎯 Overview

Crawler-Duel implements three distinct crawler modules and benchmarks them in real-time:

1. **Lightweight Crawler** - Fast HTTP requests with minimal overhead
2. **Browser-Based Crawler** - Playwright automation for JavaScript-heavy sites
3. **AI-Agentic Crawler** - LLM-powered extraction using Firecrawl or Crawl4AI

## ✨ Features

- **Triple-Crawl Architecture**: Three specialized crawlers with different strengths
- **Live Race Visualization**: Watch crawlers compete in real-time via Streamlit UI
- **Comprehensive Benchmarking**:
  - ⏱️ Time-to-Complete metrics
  - ✅ Data integrity validation (null checks, blocking detection)
  - 📊 Structural quality scoring (HTML vs structured JSON/Markdown)
- **Anti-Bot Bypass**: Proxy rotation and user-agent randomization
- **Cost-Benefit Analysis**: Compare resource usage vs. output quality
- **Interactive Dashboard**: Beautiful Streamlit interface with live updates

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yadavanujkumar/OmniCrawler-Analysis.git
cd OmniCrawler-Analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers (required for Browser-Based crawler):
```bash
playwright install chromium
```

4. (Optional) Set up environment variables for AI crawler:
```bash
cp .env.example .env
# Edit .env and add your FIRECRAWL_API_KEY
```

### Running the Application

Start the Streamlit dashboard:
```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📖 Usage

### Basic Usage

1. Enter a target URL in the sidebar
2. Select which crawlers to include in the race
3. (Optional) Enable anti-bot features
4. (Optional) Add proxies for rotation
5. Click "🏁 Start Race" and watch the live competition!

### Using AI-Agentic Crawler

To use the AI-Agentic crawler with Firecrawl:

1. Get an API key from [Firecrawl](https://firecrawl.dev)
2. Add it to your `.env` file:
   ```
   FIRECRAWL_API_KEY=your_api_key_here
   ```
3. Check the "AI-Agentic (Firecrawl)" option in the dashboard

### Anti-Bot Features

Enable anti-bot features to test which crawler handles blocking better:

- **User-Agent Randomization**: Automatically rotates through realistic user agents
- **Proxy Rotation**: Add proxies (one per line) in the sidebar configuration

## 🏗️ Architecture

```
OmniCrawler-Analysis/
├── crawlers/
│   ├── __init__.py
│   ├── base_crawler.py       # Base class and CrawlResult
│   ├── lightweight_crawler.py # HTTP requests implementation
│   ├── browser_crawler.py     # Playwright implementation
│   └── ai_crawler.py          # Firecrawl/Crawl4AI implementation
├── utils/
│   ├── __init__.py
│   ├── antibot.py            # Anti-bot utilities
│   └── benchmark.py          # Benchmarking engine
├── app.py                    # Streamlit dashboard
├── requirements.txt          # Python dependencies
└── .env.example             # Environment template
```

## 📊 Benchmarking Metrics

### Time-to-Complete
Measures how long each crawler takes to fetch and process the page.

### Data Integrity
Checks for:
- HTTP error codes (403, 429, 503)
- Null or empty responses
- "Blocked" or "Captcha" indicators
- Minimum content length

### Structural Quality Score (0-100)
Evaluates output format:
- **+20**: Clean JSON output
- **+15**: Markdown formatting
- **+15**: Clean text extraction
- **-10**: Raw HTML output

### Cost-Benefit Analysis
Compares relative resource costs vs. benefits:
- **Lightweight**: Cost=1 (cheapest)
- **Browser-Based**: Cost=5 (moderate)
- **AI-Agentic**: Cost=10 (highest, API fees)

## 🧪 Testing

Run a simple test to verify installation:

```bash
python test_crawlers.py
```

## 🛠️ Tech Stack

- **Python 3.8+**: Core language
- **Streamlit**: Interactive dashboard
- **Playwright**: Browser automation
- **Requests + BeautifulSoup**: HTTP crawling
- **Firecrawl API**: AI-powered extraction
- **Pandas**: Data analysis and metrics
- **fake-useragent**: User-agent rotation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Firecrawl for AI-powered web extraction
- Playwright team for browser automation
- Streamlit for the amazing dashboard framework

## 📧 Contact

For questions or support, please open an issue on GitHub.