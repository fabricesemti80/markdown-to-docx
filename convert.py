import argparse
import sys
import os
import pypandoc

def convert_md_to_docx(input_file, output_file):
    """
    Converts a Markdown file to a DOCX file using pypandoc.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)

    try:
        # Check if pandoc is installed/available
        # pypandoc.ensure_pandoc_installed() might be useful but requires internet
        # We will assume pandoc is installed or pypandoc can handle it.
        
        # Set resource path to the directory of the input file so images can be found
        input_dir = os.path.dirname(os.path.abspath(input_file))
        extra_args = [f'--resource-path={input_dir}']
        
        output = pypandoc.convert_file(input_file, 'docx', outputfile=output_file, extra_args=extra_args)
        print(f"Successfully converted '{input_file}' to '{output_file}'.")
    except OSError as e:
         print(f"Error during conversion: {e}")
         print("Make sure Pandoc is installed and available in your system path.")
         sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Markdown to DOCX.")
    parser.add_argument("input_file", nargs="?", help="Path to the input Markdown file.")
    parser.add_argument("output_file", nargs="?", help="Path to the output DOCX file.")

    args = parser.parse_args()
    
    input_file = args.input_file
    output_file = args.output_file

    # Interactive mode if arguments are missing
    if not input_file:
        try:
            input_file = input("Enter input Markdown file path: ").strip()
            # Remove quotes if user added them (common when copying paths)
            input_file = input_file.strip('"').strip("'")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            sys.exit(0)
    
    if not input_file:
        print("Error: Input file is required.")
        sys.exit(1)

    if not output_file:
        default_output = os.path.splitext(input_file)[0] + ".docx"
        try:
            output_file = input(f"Enter output DOCX file path (default: {default_output}): ").strip()
            output_file = output_file.strip('"').strip("'")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            sys.exit(0)
        
        if not output_file:
            output_file = default_output

    convert_md_to_docx(input_file, output_file)
