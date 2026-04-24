# Adalyze Design System

## Overview

**Adalyze（アドアライズ）** is a Japanese AI-powered SaaS tool that analyzes advertising copy for fraudulent and exaggerated expressions. It assigns a "danger score" (危険スコア, 0–100) to submitted ad text, using GPT-4, and visualizes the result with color-coded feedback. It targets Japanese marketers, compliance teams, and platform operators.

**Product surface:** A single Streamlit-based web application with four main pages:
- **Home** — Introduction and navigation
- **Fraud Check (危険スコア診断)** — Ad text input + AI scoring
- **Log (診断ログ)** — Browse, filter, search, delete, and export past results
- **Stats (統計・傾向分析)** — Charts and KPIs over time

**Source:** GitHub repository `MMMokka/Adalyze` (https://github.com/MMMokka/Adalyze)

---

## CONTENT FUNDAMENTALS

- **Language:** Japanese-first UI copy. All labels, titles, page names, and instructional text are in Japanese.
- **Tone:** Functional and serious. This is a diagnostic/compliance tool, not a marketing product. Copy is direct, informational, and cautious.
- **Casing:** Japanese text has no concept of case. Where English appears (e.g. "Adalyze", page titles in code), it uses title case.
- **Emoji:** Emoji are used as inline icons throughout the UI — not decoratively, but functionally as signifiers. Examples: 🔍 (search/inspect), ⚠️ (warning), 📚 (logs), 📊 (stats), 📤 (export), 🗑️ (delete). This is a Streamlit convention carried into the brand.
- **I vs. You:** The product addresses the user with polite Japanese forms (ください、してください). Impersonal, tool-like.
- **Disclaimers:** Heavy use of cautionary language — "本サービスの結果はあくまで参考情報です" (results are for reference only). Legal/compliance awareness baked into the copy.
- **Numbers:** Scores are always shown as `NN/100`. Percentages and stats use Japanese number formatting.
- **CTA style:** Simple button labels — "診断する" (Diagnose), "CSVをダウンロード" (Download CSV). Verbs last (Japanese grammar pattern).

---

## VISUAL FOUNDATIONS

### Colors
- **Background (main):** `#202123` — a very dark charcoal, near-black but slightly warm
- **Background (sidebar):** `#000000` — pure black
- **Score: Safe (< 40):** `#2EB8B2` — teal/cyan
- **Score: Warning (40–69):** `#FBB360` — amber/orange
- **Score: Danger (≥ 70):** `#CD4246` — red
- **Text (primary):** `#FFFFFF` — white on dark
- **Fallback/unknown score:** `#CCCCCC` — light gray

Color vibe: **dark tech / terminal aesthetic**. Not blue-purple gradient; rather a purposeful near-monochrome dark palette punctuated by the three-color traffic-light score system.

### Typography
- **Font:** Noto Sans JP — applied globally and forced on all elements
- **Fallback:** sans-serif
- **Base size:** 16px
- **Style:** Monospace roots feel (IBM Plex family); clean, technical, geometric
- Headings rendered by Streamlit defaults on dark bg, not custom-styled beyond font override

### Spacing & Layout
- Streamlit's built-in layout system: `layout="wide"` on all pages
- Sidebar on the left (black bg)
- Main content area in charcoal
- **Border radius:** 8px on buttons and select boxes

### Backgrounds
- No images, illustrations, or textures. Pure flat dark color.
- No gradients in the custom CSS.
- No patterns.

### Animations
- No custom animations defined. Streamlit's default spinner used during AI diagnosis.

### Hover/Press states
- Relies on Streamlit defaults. No custom hover color overrides.

### Borders
- No explicit border system defined in custom CSS. Streamlit defaults apply (subtle).

### Shadows
- No custom shadow system. Streamlit defaults.

### Cards
- Streamlit `st.expander()` used for log entries. No custom card rounding/shadow.

### Iconography
- Emoji as icons (see ICONOGRAPHY below)

### Imagery
- None. This is a pure data/text tool. No photography or illustrations.

### Corner radii
- `8px` on interactive elements (buttons, selects)

---

## ICONOGRAPHY

Adalyze uses **emoji as functional icons** — a Streamlit convention:

| Emoji | Usage |
|-------|-------|
| 🔍 | Search / "What is Adalyze?" section |
| ⚠️ | Fraud Check page header |
| 📚 | Log page header |
| 📊 | Stats page header |
| 📤 | Export action |
| 🗑️ | Delete action |
| 🔗 | Menu / navigation |
| 🕒 | Timestamp in log entries |
| 🧾 | Log list heading |
| 📌 | Notice / disclaimer |

No custom icon font, no SVG icon library, no PNG icons. Emoji are the sole icon system.

The **logo** is a white wordmark SVG (`assets/logo.svg`). It spells "Adalyze" in a clean geometric sans-serif with tight letter spacing.

---

## File Index

```
/
├── README.md                  — This file
├── SKILL.md                   — Agent skill manifest
├── colors_and_type.css        — CSS design tokens (colors, type, spacing)
├── assets/
│   ├── logo.svg               — White wordmark logo (SVG)
│   └── logo.png               — White wordmark logo (PNG)
├── preview/
│   ├── colors-base.html       — Base color palette card
│   ├── colors-score.html      — Score color system card
│   ├── colors-semantic.html   — Semantic color tokens card
│   ├── type-scale.html        — Typography scale card
│   ├── type-specimens.html    — Type specimens card
│   ├── spacing-tokens.html    — Spacing & radius tokens card
│   ├── components-buttons.html — Button components card
│   ├── components-inputs.html  — Input components card
│   ├── components-score.html   — Score display component card
│   ├── components-badges.html  — Badge/tag components card
│   ├── brand-logo.html        — Logo card
│   └── brand-emoji.html       — Emoji icon system card
└── ui_kits/
    └── app/
        ├── README.md          — UI kit notes
        └── index.html         — Interactive Adalyze web app prototype
```
