# Crawler-Duel UI Preview

This document provides a text-based preview of the Streamlit dashboard interface.

## Dashboard Layout

```
╔════════════════════════════════════════════════════════════════════════════════╗
║                          🕷️ Crawler-Duel 🕷️                                  ║
║              Multi-Agent Web Crawling & Benchmarking Suite                     ║
╚════════════════════════════════════════════════════════════════════════════════╝

┌──────────────────────┬─────────────────────────────────────────────────────────┐
│  ⚙️ Configuration   │                                                         │
│  ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄  │  🏁 Live Race Progress                                  │
│                      │  ─────────────────────────────────────────────────────  │
│  Target URL:         │                                                         │
│  ┌─────────────────┐ │  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐│
│  │https://...      │ │  │ Lightweight   │ │ Browser-Based │ │ AI-Agentic    ││
│  └─────────────────┘ │  │               │ │               │ │               ││
│                      │  │ ⏳ Waiting... │ │ ⏳ Waiting... │ │ ⏳ Waiting... ││
│  Select Crawlers     │  │               │ │               │ │               ││
│  ☑ Lightweight       │  └───────────────┘ └───────────────┘ └───────────────┘│
│  ☑ Browser-Based     │                                                         │
│  ☐ AI-Agentic        │                                                         │
│                      │  🚀 Racing 2 crawler(s) against https://example.com     │
│  🛡️ Anti-Bot        │                                                         │
│  ☑ Enable Features   │  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐│
│                      │  │ Lightweight   │ │ Browser-Based │ │ AI-Agentic    ││
│  Proxies:            │  │               │ │               │ │               ││
│  ┌─────────────────┐ │  │ ✅ Complete! │ │ 🏃 Running...│ │ ❌ Not Run    ││
│  │                 │ │  │ 1.23s         │ │               │ │               ││
│  └─────────────────┘ │  │ 📊 8.5 KB     │ │               │ │               ││
│                      │  └───────────────┘ └───────────────┘ └───────────────┘│
│  ┌──────────────────┐│                                                         │
│  │ 🏁 Start Race    ││  🏁 Race Complete!                                      │
│  └──────────────────┘│                                                         │
│                      │  ─────────────────────────────────────────────────────  │
│  ℹ️ About           │                                                         │
│  ─────────────────── │  🏆 Race Results                                        │
│  Crawler-Duel        │  🥇 Winner: Lightweight                                 │
│  benchmarks three    │  ℹ️  Completed in 1.23s, good data integrity           │
│  types of crawlers   │                                                         │
│                      │  📊 Detailed Scores                                     │
│  Features:           │  Lightweight: 52.0/100                                  │
│  • Live racing       │  Browser-Based: 45.3/100                                │
│  • Performance       │                                                         │
│  • Integrity checks  │  ─────────────────────────────────────────────────────  │
│  • Cost analysis     │                                                         │
│                      │  📊 Comparison Table                                    │
│                      │  ┌──────────────┬────────┬─────────┬────────┬────────┐ │
│                      │  │ Crawler      │Success │ Time(s) │ Status │ Size   │ │
│                      │  ├──────────────┼────────┼─────────┼────────┼────────┤ │
│                      │  │ Lightweight  │   ✓    │  1.23   │  200   │ 8.3 KB │ │
│                      │  │ Browser-Based│   ✓    │  3.45   │  200   │ 12.1KB │ │
│                      │  └──────────────┴────────┴─────────┴────────┴────────┘ │
│                      │                                                         │
│                      │  💰 Cost-Benefit Analysis                               │
│                      │  ┌──────────────┬──────┬──────────┬────────┬─────────┐│
│                      │  │ Crawler      │ Cost │ Benefit  │ Ratio  │ Rec.    ││
│                      │  ├──────────────┼──────┼──────────┼────────┼─────────┤│
│                      │  │ Lightweight  │  1   │  52.0    │ 52.00  │🌟Excell ││
│                      │  │ Browser-Based│  5   │  45.3    │  9.06  │✓ Good   ││
│                      │  └──────────────┴──────┴──────────┴────────┴─────────┘│
│                      │                                                         │
│                      │  ▼ 📈 Summary Statistics                                │
│                      │    Total Crawls: 2 | Successful: 2 | Avg: 2.34s       │
│                      │                                                         │
│                      │  ▼ 🔍 Detailed Results                                 │
│                      │    [JSON view of each crawler's metadata]              │
└──────────────────────┴─────────────────────────────────────────────────────────┘
```

## Key UI Components

### Sidebar (Left Panel)

1. **Configuration Section**
   - URL input field
   - Crawler selection checkboxes
   - Anti-bot feature toggle
   - Proxy configuration textarea
   - API key input (for AI crawler)

2. **Action Button**
   - Large "Start Race" button
   - Primary color styling
   - Full-width layout

3. **About Section**
   - Project description
   - Feature list
   - Help information

### Main Panel (Right Side)

1. **Live Race Progress**
   - Three columns (one per crawler)
   - Real-time status updates
   - Progress indicators (⏳/🏃/✅/❌)
   - Timing information
   - Data size metrics

2. **Results Section** (appears after race)
   - Winner announcement with trophy emoji
   - Detailed scoring breakdown
   - Success message

3. **Comparison Table**
   - Pandas DataFrame display
   - Sortable columns
   - Success/failure indicators
   - Key metrics (time, status, size, integrity, quality)

4. **Cost-Benefit Analysis**
   - Another DataFrame
   - Relative costs
   - Benefit scores
   - Cost-benefit ratios
   - Recommendations (🌟/✓/○/✗)

5. **Expandable Sections**
   - Summary Statistics (collapsible)
   - Detailed Results (collapsible)
   - JSON view of metadata

## Color Scheme

The dashboard uses a clean, professional color scheme:

- **Success**: Green backgrounds (✓)
- **Warning**: Yellow backgrounds (⏳)
- **Error**: Red backgrounds (✗)
- **Primary**: Blue accent color
- **Cards**: Light gray borders
- **Background**: White/Light gray

## Interactive Elements

1. **Text Inputs**: URL, API key fields
2. **Checkboxes**: Crawler and feature selection
3. **Text Areas**: Multi-line proxy configuration
4. **Buttons**: Start race (primary action)
5. **Expanders**: Collapsible detail sections
6. **DataFrames**: Sortable, scrollable tables
7. **Metrics**: Large number displays with labels

## Responsive Design

The dashboard adapts to different screen sizes:
- Wide layout for desktop
- Sidebar can collapse on mobile
- Tables scroll horizontally on narrow screens

## Real-Time Updates

During the race, the UI updates in real-time:
1. Status changes from "Waiting" → "Running" → "Complete/Failed"
2. Timing information appears as crawlers finish
3. Results populate dynamically
4. Winner announced immediately after all complete

## User Experience Flow

1. User enters URL in sidebar
2. Selects desired crawlers
3. (Optional) Configures anti-bot settings
4. Clicks "Start Race"
5. Watches live progress in three columns
6. Sees winner announcement
7. Reviews comparison tables
8. Explores detailed results in expandable sections
9. Can start another race with different settings
