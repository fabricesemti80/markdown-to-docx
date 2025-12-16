# Markdown to DOCX Converter

This project provides a Python script to convert Markdown files to DOCX format using Pandoc.

## Requirements

- Python 3
- Pandoc (must be installed and in your system PATH)
- Make (optional, for using the Makefile)

## Usage

### 1. Setup

Run the setup command to create a virtual environment and install dependencies.

```bash
make setup
```

### 2. Convert a File

Use the `convert` target to convert a Markdown file to DOCX.

```bash
make convert INPUT="path/to/input.md" OUTPUT="path/to/output.docx"
```

Example:
```bash
make convert INPUT=test.md OUTPUT=test.docx
```

### 3. Cleanup

To remove the virtual environment:

```bash
make clean
```

## Manual Usage (without Make)

1. Create a virtual environment: `python -m venv venv`
2. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
3. Install requirements: `pip install -r requirements.txt`
4. Run the script:
   - **With arguments:** `python convert.py input.md output.docx`
   - **Interactive mode:** `python convert.py` (You will be prompted for file paths)

   *Note: The script automatically handles images located in the same directory as the input file.*
