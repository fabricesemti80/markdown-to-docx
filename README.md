# Markdown and DOCX Converter

This project provides a Python script to convert:

- Markdown -> DOCX
- DOCX -> Markdown

The script auto-detects the direction from the input file extension.

## Requirements

- Python 3
- Pandoc (must be installed and available in `PATH`)
- GNU Make (optional, only if you use the `Makefile`)

## What the script does

- Auto-detects conversion direction:
  - `.md` -> `.docx`
  - `.docx` -> `.md`
- Supports command-line and interactive modes.
- Markdown -> DOCX:
  - Strips YAML front matter before conversion.
  - Replaces standalone `---` lines with `***` to avoid YAML misinterpretation.
  - Resolves image resources from both the input file directory and current working directory.
  - Renders fenced Mermaid blocks (```mermaid ... ```) to PNG images via `https://mermaid.ink`.
- DOCX -> Markdown:
  - Extracts embedded media into a `media` folder next to the output Markdown file.
  - Uses unwrapped lines (`--wrap=none`).

## Using Make

### 1. Initialize environment

```bash
make init
```

This creates `venv` and installs dependencies from `requirements.txt`.

### 2. Convert files

Markdown -> DOCX:

```bash
make convert INPUT=doc.md
make convert INPUT=doc.md OUTPUT=out.docx
```

DOCX -> Markdown:

```bash
make convert INPUT=doc.docx
make convert INPUT=doc.docx OUTPUT=out.md
```

If `OUTPUT` is omitted, the script uses a default based on input filename.

### 3. Clean up

```bash
make clean
```

## Manual usage (without Make)

1. Create a virtual environment:
   `python -m venv venv`
2. Activate it:
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Run the script:
   - With arguments:
     `python convert.py input_file [output_file]`
   - Interactive mode:
     `python convert.py`

Examples:

```bash
python convert.py test.md
python convert.py test.md test.docx
python convert.py document.docx
python convert.py document.docx document.md
```
