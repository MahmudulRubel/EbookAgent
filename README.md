# Custom ePub & Kindle E-Book Publisher

[![npm version](https://img.shields.io/npm/v/@mahmudulrubel/custom-epub-creator-skill.svg?style=flat-square&color=cb3837)](https://www.npmjs.com/package/@mahmudulrubel/custom-epub-creator-skill)
[![license](https://img.shields.io/github/license/MahmudulRubel/Custom-ePub-Creator?style=flat-square&color=blue)](LICENSE)
[![npm downloads](https://img.shields.io/npm/dm/@mahmudulrubel/custom-epub-creator-skill.svg?style=flat-square)](https://www.npmjs.com/package/@mahmudulrubel/custom-epub-creator-skill)
[![GitHub stars](https://img.shields.io/github/stars/MahmudulRubel/Custom-ePub-Creator?style=flat-square&color=gold)](https://github.com/MahmudulRubel/Custom-ePub-Creator/stargazers)

> An open-source **AI Agent Skill** for generating production-ready **ePub 3** e-books and **6x9 Trade Paperback Kindle PDFs** complete with automated cover graphic design, structured chapter navigation, dynamic running headers, embedded CSS typography, and page numbering.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Installation Guide](#installation-guide)
  - [Option 1: NPX One-Line Installer (Recommended)](#option-1-npx-one-line-installer-recommended)
  - [Option 2: Skillfish CLI](#option-2-skillfish-cli)
  - [Option 3: Direct Git Clone](#option-3-direct-git-clone)
- [Usage Examples & Prompts](#usage-examples--prompts)
- [Technical Architecture](#technical-architecture)
- [Dependencies](#dependencies)
- [License & Contributing](#license--contributing)

---

## 📖 Overview

**Custom ePub & Kindle E-Book Publisher** equips AI coding assistants (such as Google Gemini, Claude, Antigravity, Cursor, and VS Code AI tools) with standard publishing workflows to author, compile, and format valid digital e-books.

Whether you're creating trivia books, technical handbooks, user documentation, novels, or study guides, this skill instructs your AI assistant on building validated ePub 3 packages (`.epub`) and print-ready PDF files (`.pdf`).

---

## ✨ Key Features

- **📱 ePub 3 Package Compiler**: Valid ePub 3 with metadata (`DC:title`, `DC:creator`, `DC:language`), `toc.ncx` navigation, `nav.xhtml`, and embedded CSS optimized for Kindle, Apple Books, and Kobo.
- **📄 6x9 Trade Paperback PDF**: Compiles standard 6x9 inch publication layouts with dynamic two-pass canvas page numbering (`Page X of Y`), running header rules, and proper margin flows using ReportLab.
- **🎨 Automated High-Res Cover Graphic**: Dynamically renders `1200x1800` PNG cover graphics using Python Pillow (`PIL`) tailored to the book's theme.
- **⚡ One-Command Installation**: Installs seamlessly into global or local project AI skill folders via `npx`.

---

## 🚀 Installation Guide

### Option 1: NPX One-Line Installer (Recommended)

#### Global Installation (For All Projects)
Installs the skill globally into `~/.gemini/config/skills/custom-epub-creator`:

```bash
npx @mahmudulrubel/custom-epub-creator-skill
```

#### Local Workspace Installation
Installs the skill directly into your current project workspace `.agents/skills/custom-epub-creator`:

```bash
npx @mahmudulrubel/custom-epub-creator-skill --local
```

---

### Option 2: Skillfish CLI

If you use `skillfish` for managing AI agent skills:

```bash
npx skillfish add MahmudulRubel/Custom-ePub-Creator
```

---

### Option 3: Direct Git Clone

#### Global Installation
```bash
git clone https://github.com/MahmudulRubel/Custom-ePub-Creator.git ~/.gemini/config/skills/custom-epub-creator
```

#### Local Installation
```bash
git clone https://github.com/MahmudulRubel/Custom-ePub-Creator.git .agents/skills/custom-epub-creator
```

---

## 💡 Usage Examples & Prompts

Once installed, your AI assistant will automatically recognize e-book generation requests. You can prompt your AI with:

### Example Prompts:
> *"Create a 5-chapter trivia e-book about world history in both ePub and PDF formats."*

> *"Generate a formatted Kindle PDF and ePub for my Python beginner guide with custom cover art."*

> *"Compile this markdown documentation into a valid 6x9 inch trade paperback PDF with page numbers."*

---

## 🛠 Technical Architecture

```
Custom-ePub-Creator/
├── SKILL.md                 # Primary YAML frontmatter & AI Agent instructions
├── README.md                # Documentation & installation guide
├── package.json             # NPM package manifest for npx installer
├── bin/
│   └── install.js           # CLI installation runner
└── .gitignore               # Excludes temporary outputs (*.pdf, *.epub, cover.png)
```

---

## 📦 Dependencies

The skill utilizes the following standard Python libraries:

| Library | Purpose |
| :--- | :--- |
| `ebooklib` | Assembles valid ePub 3 manifest files, spine, TOC, and metadata. |
| `reportlab` | Generates 6x9 inch trade paperback PDFs with dynamic headers and footers. |
| `Pillow` (PIL) | Programmatically designs and renders high-resolution cover graphics (`cover.png`). |
| `pypdf` | Inspects page metrics and verifies structural integrity. |

Install Python dependencies if needed:
```bash
pip install ebooklib reportlab pillow pypdf
```

---

## 📄 License & Contributing

Distributed under the **MIT License**. See `LICENSE` for more information.

Contributions, issues, and feature requests are welcome! Feel free to check the [Issues Page](https://github.com/MahmudulRubel/Custom-ePub-Creator/issues).

---

<p center>Created with ❤️ by <a href="https://github.com/MahmudulRubel">Mahmudul Rubel</a></p>
