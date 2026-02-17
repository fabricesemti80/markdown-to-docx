# Import necessary tools (libraries) to help us do the work
import argparse  # Helps us read commands from the terminal
import sys       # Helps us interact with the computer system (like exiting the program)
import os        # Helps us work with files and folders
import re        # Helps us match text patterns
import pypandoc  # The main tool that converts files (like a translator)


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

def convert_md_to_docx(input_file, output_file):
    """
    Converts a Markdown file to a DOCX file using pypandoc.
    """
    # 1. Check if the input file actually exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1) # Stop the program with an error code

    try:
        # 2. Prepare the conversion
        
        # We need to tell the converter where to look for images.
        # 1. The folder where the input file is (so relative paths like 'image.png' or '../img.png' work)
        input_dir = os.path.dirname(os.path.abspath(input_file))
        # 2. The current working directory (where we are running the script from)
        cwd = os.getcwd()
        
        # Combine these paths using the system's separator (semicolon for Windows, colon for others)
        resource_path_arg = os.pathsep.join([input_dir, cwd])
        
        # We create a special setting to tell the converter: "Look for images in these folders!"
        extra_args = [f'--resource-path={resource_path_arg}']
        
        # 3. Read the file and replace standalone --- lines (horizontal rules)
        #    with *** to prevent Pandoc from misinterpreting them as YAML blocks.
        #    Also strip any real YAML front matter at the top of the file.
        with open(input_file, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        content = strip_yaml_front_matter(content)
        # Replace remaining --- horizontal rules with *** (which Pandoc never treats as YAML)
        content = re.sub(r'^---\s*$', '***', content, flags=re.MULTILINE)
        
        # 4. Perform the conversion from the cleaned Markdown string
        output = pypandoc.convert_text(content, 'docx', format='markdown', outputfile=output_file, extra_args=extra_args)
        
        # 4. Success! Tell the user it worked.
        print(f"Successfully converted '{input_file}' to '{output_file}'.")

    # If something goes wrong specifically with the operating system (like file permissions)
    except OSError as e:
         print(f"Error during conversion: {e}")
         print("Make sure Pandoc is installed and available in your system path.")
         sys.exit(1)
    # If any other unexpected error happens
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

# This is the starting point of the script when you run it directly.
# In Python, we define functions first (like 'begin'), and then we call them at the bottom.
# This check (if __name__ == "__main__") ensures this code only runs when you execute the script,
# not when you import it into another script.
if __name__ == "__main__":
    # Setup the tool to understand command line arguments
    parser = argparse.ArgumentParser(description="Convert Markdown to DOCX.")
    
    # We look for two optional pieces of information: input file and output file
    # nargs="?" means "this is optional"
    parser.add_argument("input_file", nargs="?", help="Path to the input Markdown file.")
    parser.add_argument("output_file", nargs="?", help="Path to the output DOCX file.")

    # Read the arguments provided by the user
    args = parser.parse_args()
    
    input_file = args.input_file
    output_file = args.output_file

    # Interactive mode: If the user didn't provide an input file in the command, ask for it now.
    if not input_file:
        try:
            input_file = input("Enter input Markdown file path: ").strip()
            # Remove quotes if user added them (common when copying paths in Windows)
            input_file = input_file.strip('"').strip("'")
        except KeyboardInterrupt:
            # If the user presses Ctrl+C, stop nicely
            print("\nOperation cancelled.")
            sys.exit(0)
    
    # If we still don't have an input file, we can't continue.
    if not input_file:
        print("Error: Input file is required.")
        sys.exit(1)

    # If the user didn't provide an output file, ask for it or guess it.
    if not output_file:
        # Create a default name by taking the input filename and changing extension to .docx
        default_output = os.path.splitext(input_file)[0] + ".docx"
        try:
            # Ask the user, showing them the default we calculated
            output_file = input(f"Enter output DOCX file path (default: {default_output}): ").strip()
            output_file = output_file.strip('"').strip("'")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            sys.exit(0)
        
        # If the user just pressed Enter (didn't type anything), use the default
        if not output_file:
            output_file = default_output

    # Finally, call the function to do the actual work
    convert_md_to_docx(input_file, output_file)
