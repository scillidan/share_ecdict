# (Deprecated)
# While the data sources typically follow standard rules, compiling them into a single dictionary makes the rules messy and difficult to manage.
# It only handles a subset of the tags:
# - Input format: word1<tab>word2<br /><br />meaning
# - Output format: word1|word2<tab>meaning (or word1<tab>meaning if word1 == word2)
# Authors: DeepSeek🧙‍♂️, scillidan🤡
# Usage: python file.py <input> <output>

import sys
import re

def format(input, output):
    # Pattern to identify dictionary entries: word1, tab, word2, then <br /><br />
    ENTRY_PATTERN = re.compile(r'^\ufeff?([^\t]+?)\t([^\s]+?)<br /><br />')

    # Pattern to remove trailing <br /> tags
    TRAILING_BR_PATTERN = re.compile(r'<br />\s*$')

    with open(input, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    results = []
    for line in lines:
        # Remove line endings and trailing <br /> tags
        result = TRAILING_BR_PATTERN.sub('', line.rstrip('\r\n'))
        match = ENTRY_PATTERN.match(result)

        if match:
            word1, word2 = match.group(1), match.group(2)

            # Extract the meaning (everything after the pattern)
            meaning = result[match.end():]

            # Create prefix: combine words with | if different, or use word1 alone if same
            if word1.lower() == word2.lower():
                new_prefix = f"{word1}\t"
            else:
                new_prefix = f"{word1}|{word2}\t"

            # Build the reformatted line
            results.append(new_prefix + meaning + '\n')
        else:
            # Keep unmatched lines as they are
            results.append(result + '\n')

    with open(output, 'w', encoding='utf-8') as f:
        f.writelines(results)

def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <input> <output>")
        sys.exit(1)
    input = sys.argv[1]
    output = sys.argv[2]

    format(input, output)

if __name__ == '__main__':
    main()