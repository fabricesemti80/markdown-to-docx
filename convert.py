# Import necessary tools (libraries) to help us do the work
import argparse  # Helps us read commands from the terminal
import sys       # Helps us interact with the computer system (like exiting the program)
import os        # Helps us work with files and folders
import pypandoc  # The main tool that converts files (like a translator)

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
        # Images are usually in the same folder as the input file.
        # So we find the folder path of the input file.
        input_dir = os.path.dirname(os.path.abspath(input_file))
        
        # We create a special setting to tell the converter: "Look for images here!"
        extra_args = [f'--resource-path={input_dir}']
        
        # 3. Perform the conversion
        # We ask pypandoc to convert the 'input_file' to 'docx' format.
        # We save the result to 'output_file'.
        # We pass our special setting (extra_args) to help it find images.
        output = pypandoc.convert_file(input_file, 'docx', outputfile=output_file, extra_args=extra_args)
        
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

# This is the starting point of the script when you run it
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
