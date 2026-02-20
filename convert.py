# Import necessary tools (libraries) to help us do the work
import argparse  # Helps us read commands from the terminal
import sys       # Helps us interact with the computer system (like exiting the program)
import os        # Helps us work with files and folders
import re        # Helps us match text patterns
import base64    # Helps us encode data for URLs
import tempfile  # Helps us create temporary files
import shutil    # Helps us copy files
import requests  # Helps us make web requests (for Mermaid rendering)
import urllib3   # Used to suppress SSL warnings in corporate environments
import pypandoc  # The main tool that converts files (like a translator)

# Suppress SSL warnings when verify=False (common in corporate proxy environments)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def strip_yaml_front_matter(text):
    """
    Removes YAML front matter (the block between --- markers at the top of a file)
    so that Pandoc doesn't choke on special YAML characters like * or &.
    Handles BOM, Windows line endings, and ... as closing delimiter.
    """
    # Remove BOM if present
    text = text.lstrip('\ufeff')
    # Match opening --- and closing --- or ... with flexible whitespace/line endings
    result = re.sub(r'\A---[ \t]*\r?\n.*?\r?\n(?:---|\.\.\.)[ \t]*\r?\n', '', text, count=1, flags=re.DOTALL)
    if result == text:
        print("WARNING: No YAML front matter detected to strip.")
    else:
        print("INFO: YAML front matter was stripped before conversion.")
    return result


def render_mermaid_blocks(content, temp_dir):
    """
    Finds all ```mermaid code blocks in the Markdown content,
    renders each one to a PNG image using the Mermaid Ink service,
    and replaces the code block with a Markdown image reference.
    Images are saved to a local temp directory to avoid UNC path issues with Pandoc.
    """
    # Pattern to match ```mermaid ... ``` blocks
    pattern = re.compile(r'```mermaid\s*\n(.*?)```', flags=re.DOTALL)
    matches = list(pattern.finditer(content))

    if not matches:
        return content

    # Use a local temp directory so Pandoc can always resolve the image paths
    diagrams_dir = os.path.join(temp_dir, 'mermaid_diagrams')
    os.makedirs(diagrams_dir, exist_ok=True)

    print(f"INFO: Found {len(matches)} Mermaid diagram(s), rendering to images...")

    for i, match in enumerate(reversed(matches), 1):
        diagram_code = match.group(1).strip()
        diagram_num = len(matches) - i + 1
        image_path = os.path.join(diagrams_dir, f'mermaid_{diagram_num}.png')

        try:
            # Encode the Mermaid code as base64 for the Mermaid Ink URL
            encoded = base64.urlsafe_b64encode(diagram_code.encode('utf-8')).decode('ascii')
            url = f'https://mermaid.ink/img/{encoded}'

            response = requests.get(url, timeout=30, verify=False)
            response.raise_for_status()

            with open(image_path, 'wb') as f:
                f.write(response.content)

            # Replace the code block with an image reference (use forward slashes for Pandoc)
            pandoc_path = image_path.replace('\\', '/')
            replacement = f'![Diagram {diagram_num}]({pandoc_path})'
            content = content[:match.start()] + replacement + content[match.end():]
            print(f"  Rendered diagram {diagram_num} → {image_path}")

        except Exception as e:
            print(f"  WARNING: Failed to render diagram {diagram_num}: {e}")
            print(f"  The Mermaid code block will be kept as-is.")

    return content


def convert_md_to_docx(input_file, output_file):
    """
    Converts a Markdown file to a DOCX file using pypandoc.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)

    try:
        input_dir = os.path.dirname(os.path.abspath(input_file))
        cwd = os.getcwd()
        resource_path_arg = os.pathsep.join([input_dir, cwd])
        extra_args = [f'--resource-path={resource_path_arg}']

        # Read the file and replace standalone --- lines (horizontal rules)
        # with *** to prevent Pandoc from misinterpreting them as YAML blocks.
        with open(input_file, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        content = strip_yaml_front_matter(content)
        content = re.sub(r'^---\s*$', '***', content, flags=re.MULTILINE)

        # Use a local temp directory for Mermaid images and Pandoc output
        # to avoid issues with UNC paths, spaces, and file locks.
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Render any Mermaid diagrams to PNG images in the temp directory
            content = render_mermaid_blocks(content, tmp_dir)

            # Write output to a local temp file first, then copy to final destination
            tmp_output = os.path.join(tmp_dir, 'output.docx')
            pypandoc.convert_text(content, 'docx', format='markdown', outputfile=tmp_output, extra_args=extra_args)
            shutil.copy2(tmp_output, output_file)

        print(f"Successfully converted '{input_file}' to '{output_file}'.")

    except OSError as e:
        print(f"Error during conversion: {e}")
        print("Make sure Pandoc is installed and available in your system path.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


def convert_docx_to_md(input_file, output_file):
    """
    Converts a DOCX file to a Markdown file using pypandoc.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)

    try:
        # Extract images into a subfolder next to the output file
        output_dir = os.path.dirname(os.path.abspath(output_file))
        media_dir = os.path.join(output_dir, 'media')

        extra_args = [
            '--wrap=none',                          # Don't hard-wrap lines
            f'--extract-media={media_dir}',         # Save embedded images
        ]

        pypandoc.convert_file(input_file, 'markdown', outputfile=output_file, extra_args=extra_args)
        print(f"Successfully converted '{input_file}' to '{output_file}'.")
        if os.path.isdir(media_dir):
            print(f"Extracted images saved to '{media_dir}'.")

    except OSError as e:
        print(f"Error during conversion: {e}")
        print("Make sure Pandoc is installed and available in your system path.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


def detect_direction(input_file):
    """
    Auto-detects the conversion direction based on the input file extension.
    Returns ('md2docx', default_output) or ('docx2md', default_output).
    """
    ext = os.path.splitext(input_file)[1].lower()
    base = os.path.splitext(input_file)[0]
    if ext in ('.docx',):
        return 'docx2md', base + '.md'
    else:
        return 'md2docx', base + '.docx'


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert between Markdown and DOCX (auto-detects direction).")
    parser.add_argument("input_file", nargs="?", help="Path to the input file (.md or .docx).")
    parser.add_argument("output_file", nargs="?", help="Path to the output file.")

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    # Interactive mode: ask for input file if not provided
    if not input_file:
        try:
            input_file = input("Enter input file path (.md or .docx): ").strip()
            input_file = input_file.strip('"').strip("'")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            sys.exit(0)

    if not input_file:
        print("Error: Input file is required.")
        sys.exit(1)

    # Auto-detect conversion direction
    direction, default_output = detect_direction(input_file)
    direction_label = "DOCX → Markdown" if direction == 'docx2md' else "Markdown → DOCX"
    print(f"Detected conversion: {direction_label}")

    # Ask for output file if not provided
    if not output_file:
        try:
            output_file = input(f"Enter output file path (default: {default_output}): ").strip()
            output_file = output_file.strip('"').strip("'")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            sys.exit(0)

        if not output_file:
            output_file = default_output

    # Run the appropriate conversion
    if direction == 'docx2md':
        convert_docx_to_md(input_file, output_file)
    else:
        convert_md_to_docx(input_file, output_file)
