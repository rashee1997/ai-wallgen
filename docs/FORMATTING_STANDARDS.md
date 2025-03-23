# Documentation Formatting Standards

![Banner Image](../asset/doc_banners/template_banner.png)

## Overview

This document defines the standardized formatting, structure, and styling for all Wallgen project documentation. Following these guidelines ensures consistency, readability, and maintainability across all project documentation.

## Table of Contents

- [Document Structure](#document-structure)
- [Formatting Guidelines](#formatting-guidelines)
- [Visual Elements](#visual-elements)
- [Code Examples](#code-examples)
- [Tables](#tables)
- [File Naming Conventions](#file-naming-conventions)
- [Cross-Referencing](#cross-referencing)

## Document Structure

Each documentation file should include the following sections in this order:

1. **Title** - H1 heading with the document title
2. **Banner Image** - Relevant banner image (optional but recommended)
3. **Overview** - Brief introduction to the document's purpose
4. **Table of Contents** - For documents longer than 3 sections
5. **Main Content Sections** - Using appropriate heading levels
6. **See Also** - Links to related documentation
7. **Footer** - With logo and last updated date

Example template structure:
```markdown
# Document Title

![Banner Image](path/to/banner.png)

## Overview

Brief description...

## Table of Contents

- [Section 1](#section-1)
- [Section 2](#section-2)

## Section 1

Content...

## Section 2

Content...

## See Also

Related links...

---

<footer>
```

## Formatting Guidelines

### Headings

- **H1 (#)** - Document title only (once per document)
- **H2 (##)** - Major sections
- **H3 (###)** - Subsections
- **H4 (####)** - Minor sections or feature descriptions
- **H5 (#####)** - Special cases only

### Text Formatting

- **Bold** - Use for emphasis, UI elements, and feature names
- *Italic* - Use for introduced terms, parameters, and light emphasis
- `Code` - Use for file names, code elements, and commands
- ~~Strikethrough~~ - Use only for deprecated features

### Lists

- Use ordered lists (1., 2., 3.) for sequential steps and prioritized items
- Use unordered lists (-, *) for collections and feature highlights
- Maintain consistent list type throughout a section

## Visual Elements

### Images

- Banner images should be 1200x300px in size
- Screenshots should include clear context
- Include descriptive alt text for all images
- Use the following format:
  ```markdown
  ![Alt text](../asset/path/to/image.png)
  ```
- Center important images with HTML:
  ```markdown
  <div align="center">
  <img src="../asset/path/to/image.png" alt="Alt text" width="600">
  </div>
  ```

### Diagrams

- Use Mermaid for simple diagrams when possible
- Export complex diagrams as PNG with transparent backgrounds
- Include source files for diagrams in the `asset/diagrams/source` directory

## Code Examples

- Include language specifier with code blocks:
  ````markdown
  ```python
  import example
  
  example.function()
  ```
  ````
- Keep examples concise and focused
- Include comments for complex operations
- Use consistent naming conventions in all examples

## Tables

- Include header row with clear column names
- Align columns appropriately (left for text, right for numbers)
- Keep tables focused and not too wide
- Use the following format:
  ```markdown
  | Column 1 | Column 2 | Column 3 |
  |----------|----------|----------|
  | Value 1  | Value 2  | Value 3  |
  | Value 4  | Value 5  | Value 6  |
  ```

## File Naming Conventions

- Use clear, descriptive names
- Separate words with hyphens
- Use lowercase for regular documentation
- Use UPPERCASE for special reference documents
- Examples:
  - `getting-started.md`
  - `advanced-features.md`
  - `FORMATTING_STANDARDS.md`

## Cross-Referencing

### Internal Links

- Link to other documentation files using relative paths:
  ```markdown
  [Getting Started Guide](./getting-started.md)
  ```

### Section Links

- Link to sections using lowercase and hyphens:
  ```markdown
  [See the examples section](#examples)
  ```

### External Links

- Include descriptive link text:
  ```markdown
  [Google's Imagen 3 Model](https://ai.google.dev/)
  ```

---

<div align="center">
<img src="../asset/logo/gemini.svg" alt="Logo" width="64" height="64">

Documentation last updated: 2024-03-24
</div> 