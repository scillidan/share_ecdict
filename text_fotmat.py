# Write by Gemini 2.5 Flash🧙‍♂️, scillidan🤡
# Usage: python text_format.py <input_file> <output_file>

import sys
import re

def reformat_dictionary_file(input_filepath, output_filepath):
    """
    Reformats a dictionary file according to the specified rules:
    1. Removes trailing '<br />' from lines.
    2. Processes the starting pattern '<Word1>(a Tab)<Word2><br /><br />'
       - If Word1 == Word2 (case-insensitive), converts to 'Word1<Tab>'.
       - Otherwise, converts to 'Word1|Word2<Tab>'.
    3. Handles the BOM (Byte Order Mark) often seen as '﻿' at the start
       of the file/line.
    """

    # Define the pattern to find the start of an entry:
    # (Optional BOM) + Word1 + Tab + Word2 + <br /><br />
    # We use re.DOTALL to allow the pattern to match across the whole line
    # for the substitution logic.
    ENTRY_PATTERN = re.compile(r'^\ufeff?(?P<word1>[^\t]+?)\t(?P<word2>[^\s]+?)<br /><br />', re.IGNORECASE)

    # Pattern for the trailing '<br />'
    TRAILING_BR_PATTERN = re.compile(r'<br />\s*$', re.IGNORECASE)

    try:
        # Open input file for reading
        with open(input_filepath, 'r', encoding='utf-8') as infile:
            # Read all lines
            lines = infile.readlines()
    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_filepath}'")
        return
    except Exception as e:
        print(f"Error reading input file: {e}")
        return

    output_lines = []

    # Process each line
    for line in lines:
        # 1. Remove trailing '<br />'
        # Note: We must strip the newline first to check for the trailing <br />
        # and then re-add the newline later.
        line_stripped = line.rstrip('\r\n')
        line_cleaned = TRAILING_BR_PATTERN.sub('', line_stripped)

        # 2. Process the starting pattern
        match = ENTRY_PATTERN.match(line_cleaned)

        if match:
            word1 = match.group('word1')
            word2 = match.group('word2')

            # The rest of the line (the definition)
            definition = line_cleaned[match.end():]

            # 2.1. If Word1 and Word2 are the same (case-insensitive)
            if word1.lower() == word2.lower():
                # Format: <Word1>(a Tab)
                new_prefix = f"{word1}\t"
            # 2.2. If Word1 and Word2 are different
            else:
                # Format: <Word1>|<Word2>(a Tab)
                new_prefix = f"{word1}|{word2}\t"

            # Construct the new line: NewPrefix + Definition + Newline
            output_line = new_prefix + definition + '\n'

        else:
            # If the starting pattern is not found, keep the line as cleaned
            # but ensure a newline is added back for consistency.
            output_line = line_cleaned + '\n'

        output_lines.append(output_line)

    try:
        # Open output file for writing
        # Note: Using 'utf-8' encoding for output as is standard for text files.
        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            outfile.writelines(output_lines)

        print(f"Successfully processed {len(lines)} lines.")
        print(f"Output written to: {output_filepath}")

    except Exception as e:
        print(f"Error writing to output file: {e}")

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python reformat_dict.py <input_file> <output_file>")
        print("Example: python reformat_dict.py dict.txt cleaned_dict.txt")
        sys.exit(1)

    # Get file paths from command line arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Run the main function
    reformat_dictionary_file(input_file, output_file)