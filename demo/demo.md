---
title: Demo Conversion Document
author: QA Sandbox
date: 2026-02-20
---

# Demo Markdown for Converter Testing

This document contains mixed Markdown features to validate DOCX and PDF conversion.

## 1) Plain Text and Formatting

This paragraph includes **bold**, *italic*, and `inline code`.

This sentence includes a manual line break.  
This line should appear directly below it.

## 2) Lists and Nested Lists

- Item A
- Item B
  - Item B.1
  - Item B.2
    - Item B.2.a
- Item C

1. Step one
2. Step two
3. Step three

## 3) Table

| Column | Type    | Notes                         |
|--------|---------|-------------------------------|
| id     | integer | Primary key                   |
| name   | text    | Display name                  |
| active | boolean | Defaults to `true` in samples |

## 4) Blockquote and Callout Style Content

> This is a blockquote.
> It spans multiple lines.
>
> - It can include list items.
> - It can include `inline code`.

## 5) Code Blocks

### 5.1 Python

```python
def summarize(items):
    return {
        "count": len(items),
        "first": items[0] if items else None,
    }


print(summarize(["alpha", "beta", "gamma"]))
```

### 5.2 JSON

```json
{
  "service": "md-converter",
  "version": "0.1.0",
  "features": ["docx", "pdf", "mermaid"]
}
```

### 5.3 Nested Fence Example (Literal Markdown)

````markdown
Here is a fenced block shown *as content*:

```bash
make convert INPUT=demo/demo.md FORMAT=pdf
```
````

## 6) Mermaid Diagrams

### 6.1 Flowchart

```mermaid
flowchart LR
    A[Markdown Input] --> B[Preprocess]
    B --> C{Output Format}
    C -->|docx| D[Pandoc DOCX]
    C -->|pdf| E[Pandoc PDF]
    E --> F[Fallback xhtml2pdf if needed]
```

### 6.2 Sequence Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant M as Makefile
    participant C as convert.py
    participant P as Pandoc
    U->>M: make convert INPUT=demo.md
    M->>C: python convert.py ...
    C->>P: convert text
    P-->>C: output file
    C-->>U: success message
```

### 6.3 Class Diagram

```mermaid
classDiagram
    class Converter {
      +convert_md_to_output()
      +convert_docx_to_md()
      +render_mermaid_blocks()
    }
    class Logger {
      +log_info()
      +log_warn()
      +log_error()
      +log_success()
    }
    Converter --> Logger : uses
```

## 7) Horizontal Rule

---

## 8) Links and Image Placeholder

- Repository docs: <https://example.com/docs>
- Issue tracker: [Sample Issue Board](https://example.com/issues)

Image markdown example (path may or may not exist in your environment):

![Sample placeholder image](./images/sample.png)

## 9) Escapes and Special Characters

Characters: \*literal asterisks\*, \_literal underscores\_, and backticks: \`

Math-like plain text: a^2 + b^2 = c^2

## 10) Final Checklist

- [x] Includes YAML front matter
- [x] Includes multiple Mermaid blocks
- [x] Includes nested fenced code example
- [x] Includes tables, lists, quotes, links, and image reference

