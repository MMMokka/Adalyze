# Adalyze App UI Kit

## Overview
High-fidelity recreation of the Adalyze Streamlit web app as a clickable HTML prototype.

## Screens
1. **Home** — Logo, intro, feature list, nav guidance
2. **Fraud Check (診断)** — Category select, ad text input, AI score result
3. **Log (ログ)** — Filterable log list with expanders, export, delete
4. **Stats (統計)** — KPI metrics, charts (bar, line, histogram)

## Design Notes
- Font: IBM Plex Sans JP via Google Fonts
- Background: #202123 (main), #000 (sidebar)
- Score colors: #2EB8B2 / #FBB360 / #CD4246
- Border radius: 8px on interactive elements
- No custom illustrations or photography
- Emoji used as functional icons throughout

## Components (index.html)
- `<Sidebar>` — Black sidebar with nav links
- `<ScoreCard>` — Colored score display card
- `<ScoreBar>` — Horizontal danger meter
- `<LogEntry>` — Expandable log row
- `<StatMetric>` — KPI metric box
- `<BarChart>` — Simple SVG bar chart
- `<CategoryTag>` — Pill tag for category labels
