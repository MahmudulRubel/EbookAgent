---
name: custom-epub-creator
display_name: Custom ePub & Kindle E-Book Publisher
description: Complete toolset and instructions for creating, formatting, and packaging valid ePub 3 e-books and Kindle PDFs from text, markdown, HTML, or structured data. Use whenever the user asks to create an ePub, publish a Kindle book, compile an e-book, generate EPUB files, or build formatted PDF e-books.
category: Documents & Publishing
author: Rubel
version: 1.0.0
tags: [epub, kindle, ebook, pdf, publishing, markdown-to-epub]
---

# Custom ePub & Kindle E-Book Publisher

## Overview

A dedicated skill for generating production-ready **ePub 3** and **Kindle PDF** digital books complete with custom cover graphic generation, structured chapter navigation (NCX & Nav), embedded CSS typography, table of contents, running headers, page numbers, and metadata.

## When to Trigger This Skill

Trigger this skill whenever the user asks to:
- Create, compile, or export an **ePub** or **Kindle PDF** e-book.
- Build a trivia book, handbook, user guide, novel, or documentation in e-book format.
- Format digital books with custom cover art, running headers, and table of contents.
- Convert markdown, text, or HTML into valid ePub 3 packages (`.epub`).

---

## Core Capabilities & Technical Requirements

### 1. Dependencies
This skill utilizes standard Python libraries for book generation:
- `ebooklib`: Constructs valid ePub 3 packages (`.epub`).
- `reportlab`: Builds PDF e-books with custom 6x9 trade layout, headers/footers, and page numbers.
- `Pillow` (PIL): Generates custom, high-resolution cover graphics (`cover.png`).
- `pypdf`: Validates generated PDF page counts and structural integrity.

### 2. Workflow & Principles
When creating a book using this skill:
1. **Plan Content & Outline**: Define clear chapters, front matter (Title page, Copyright, Preface, TOC), body chapters, and back matter (Answer keys, index, author notes).
2. **Generate Cover Art**: Automatically render a high-resolution cover image (`1200x1800` or `1200x1600` PNG) matching the book's visual theme using `Pillow`.
3. **Assemble ePub 3 Package**:
   - Set metadata (`DC:title`, `DC:creator`, `DC:language`, `DC:identifier`).
   - Include `cover.png` and embedded cover XHTML.
   - Inject styled CSS for Kindle and Apple Books (`style/style.css`).
   - Generate `toc.ncx` and `nav.xhtml` for e-reader chapter selection.
4. **Assemble Kindle PDF**:
   - Apply 6x9 inch trade paperback page size (`(6*72, 9*72)`).
   - Use dynamic two-pass canvas (`NumberedCanvas`) for running headers and page footers (`Page X of Y`).
   - Enforce proper image flowable dimensions (`340x530` max height) to prevent ReportLab `LayoutError`.
5. **Validation**: Verify that both `.epub` and `.pdf` files build without error and check page metrics using `pypdf`.

---

## Output Architecture

```
custom-epub-creator/
├── SKILL.md                          - Primary instructions & metadata
├── scripts/
│   └── epub_builder.py              - Reusable Python builder script template
└── references/
    └── epub_spec_guide.md           - Technical guidelines for ePub 3 & Kindle PDF formatting
```
