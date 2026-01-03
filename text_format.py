# (Deprecated)
# While the data sources typically follow standard rules, compiling them into a single dictionary makes the rules messy and difficult to manage.
# It only handles a subset of the tags:
# - Input format: word1<tab>word2<br /><br />meaning
# - Output format: word1|word2<tab>meaning (or word1<tab>meaning if word1 == word2)
# Authors: DeepSeek🧙‍♂️, scillidan🤡
# Usage: python file.py <input_file> <output_file>

import sys
import re

def reformat_dictionary_file(input_filepath, output_filepath):
    # Pattern to identify dictionary entries: word1, tab, word2, then <br /><br />
    ENTRY_PATTERN = re.compile(r'^\ufeff?([^\t]+?)\t([^\s]+?)<br /><br />')

    # Pattern to remove trailing <br /> tags
    TRAILING_BR_PATTERN = re.compile(r'<br />\s*$')

    # Read the input file
    with open(input_filepath, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    output_lines = []

    for line in lines:
        # Remove line endings and trailing <br /> tags
        line_cleaned = TRAILING_BR_PATTERN.sub('', line.rstrip('\r\n'))
        match = ENTRY_PATTERN.match(line_cleaned)

        if match:
            # Extract the two words
            word1, word2 = match.group(1), match.group(2)

            # Extract the meaning (everything after the pattern)
            meaning = line_cleaned[match.end():]

            # Create prefix: combine words with | if different, or use word1 alone if same
            if word1.lower() == word2.lower():
                new_prefix = f"{word1}\t"
            else:
                new_prefix = f"{word1}|{word2}\t"

            # Build the reformatted line
            output_lines.append(new_prefix + meaning + '\n')
        else:
            # Keep unmatched lines as they are
            output_lines.append(line_cleaned + '\n')

    # Write the processed content to output file
    with open(output_filepath, 'w', encoding='utf-8') as outfile:
        outfile.writelines(output_lines)

def main():
    if len(sys.argv) != 3:
        print("Usage: python reformat_dict.py <input_file> <output_file>")
        sys.exit(1)

    reformat_dictionary_file(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()