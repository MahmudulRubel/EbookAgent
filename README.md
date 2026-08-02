# Custom ePub & Kindle E-Book Publisher Skill

An AI Agent Skill for creating, formatting, and packaging valid **ePub 3** e-books and **Kindle PDFs** complete with custom cover art, structured chapter navigation (NCX & Nav), embedded CSS typography, table of contents, running headers, and dynamic page numbering.

## Installation

### Global Installation (All Projects)
Clone this repository into your global AI skills directory:

```bash
git clone https://github.com/MahmudulRubel/Custom-ePub-Creator.git ~/.gemini/config/skills/custom-epub-creator
```

### Workspace Installation (Single Project)
Clone this repository into your project's `.agents/skills` directory:

```bash
git clone https://github.com/MahmudulRubel/Custom-ePub-Creator.git .agents/skills/custom-epub-creator
```

---

## Features

- **ePub 3 Package Generation**: Compliant ePub 3 with TOC navigation, embedded fonts/styles, metadata, and Kindle/Apple Books optimization.
- **6x9 Trade Paperback PDF**: ReportLab-powered PDF compiler with dynamic two-pass canvas (`Page X of Y`), running headers, and page footers.
- **Automated Cover Graphic Generation**: Generates high-resolution cover graphics using Pillow (`PIL`).
- **Python-Powered Stack**: Utilizes `ebooklib`, `reportlab`, `Pillow`, and `pypdf`.

---

## How It Works

When triggered, the AI agent will:
1. Outline front matter, body chapters, and back matter.
2. Render custom high-res cover graphics.
3. Build ePub 3 file with proper NCX TOC and CSS styling.
4. Compile PDF e-book with 6x9 trade layout and dynamic running headers.
5. Validate page metrics and structural integrity.

---

## License

MIT License
