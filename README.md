[日本語版READMEはこちら](./README-jp.md)

**An English version of the README is currently under construction.**

# Callsign Extractor

This program is designed to extract callsigns of aircraft from transcribed air traffic control (ATC) communications using speech recognition. Currently, the program is focused on callsign extraction but is expected to be extensible for extracting other types of information, such as instructions.

## Overview

The project relies on two JSON files located in the `./registered_json` directory: `airline_code_dict.json` and `word_register.json`. The `airline_code_dict.json` file contains callsigns in the format `[callsign: 3-letter code]`. The `word_register.json` file includes individual words that make up callsigns (e.g., "all nippon", "all", "nippon").

After updating the JSON files, you need to install the required dependencies listed in the `requirements.txt` file by running the following command:

```bash
pip install -r requirements.txt
```

Next, run `registered_word_utils.py` to generate dictionaries for g2p and Metaphone based on the registered information in the `registered_json` directory. The generated dictionaries will be saved in the `./generated_json` directory.

```bash
python registered_word_utils.py
```

To extract callsigns, pass the transcribed text to the `main()` function in `main.py`. If a callsign is successfully extracted, it will be returned as a list; otherwise, "Callsign not Found" will be printed.

## Processing Flow
1. Receive the transcribed ATC communication text.
2. Remove unnecessary parts such as hyphens, periods, and commas.
    1. Add spaces between words and numbers.
    2. Remove spaces between consecutive numbers.
3. Attempt to extract the callsign based on the spelling and edit distance from registered callsigns.
4. Return the result if a callsign is extracted.
5. Generate lists of Metaphone keys and G2P representations for each word in the formatted sentence.
6. Calculate the edit distance between the generated lists and the dictionaries created from registered callsigns, and attempt to extract the callsign.
7. Return the result if a callsign is extracted.
8. Generate two lists by combining words in the formatted sentence with an offset, one starting with even-indexed words and the other with odd-indexed words. Perform edit distance calculations with Metaphone and G2P on each list.
9. Return the closest callsign match compared to the known area information.
10. If no callsign is extracted, return an error indicating that no callsign was found.

## External Libraries
This project utilizes the following libraries and modules:

- json: Used for reading and writing JSON files.
- doublemetaphone: Implements the Double Metaphone algorithm.
- re: Used for regular expression operations.
- G2p: A library for Grapheme-to-Phoneme conversion in English.
- Levenshtein.distance: A method for calculating the Levenshtein distance.
These libraries and modules are used for tasks such as text processing, phoneme conversion, and string comparison within the project.

## Function Descriptions
The project contains several Python files with various functions for different purposes. Here's a brief description of each file and its functions:

### sentence_formatter.py
- `insert_space_before_number(word: str) -> str`: Inserts a space before the first digit in a word.
- `extract_number(word: str) -> str`: Extracts the leading numeric part from a word.
- `format_sentence(text: str) -> str`: Formats the given text by removing unwanted characters, replacing hyphens with spaces, and separating words and numbers.
- `word_combination_formatter(sentence: str) -> list[str, str]`: Formats the given sentence by combining consecutive words, except for numbers.
### g2p_metaphone_gen.py
- `generate_g2p(word: str) -> str`: Generates the G2P representation of a given word.
- `generate_g2p_list(sentence: str) -> list[str]`: Generates a list of words with their G2P representations for the given sentence.
- `generate_metaphone_key_list(sentence: str) -> list[str]`: Generates a list of words with their Metaphone keys for the given sentence.
### word_replace.py
- `replace_words_spell(sentence: str) -> list`: Replaces words in the given sentence with registered words based on spelling similarity.
- `replace_words_metaphone(word_list: list[str]) -> list`: Replaces words in the given word list with registered words based on their Metaphone keys.
- `replace_words_g2p(word_list: list[str]) -> list`: Replaces words in the given word list with registered words based on their G2P representations.
### restoration.py
- `restoration_sentence(word_list: list, type: str) -> list`: Restores replaced words using the appropriate dictionary.
- `get_first_element(word_list) -> str`: Gets the first element of a list or returns the original string if it's not a list.
- `get_second_element(word_list) -> str`: Gets the second element of a list or returns the original string if it's not a list.
- `restoration_callSign(word_list: list) -> str`: Restores callsigns in the given word list by replacing them with 3-letter codes.
### extractor.py
- `extract_pattern(sentence: str) -> list`: Extracts callsign patterns from the given sentence.
- `reference_area_info(extracted_callsign: str) -> list`: Finds the closest callsign match from the known area information.
### g2p.py
- `generate_g2p(word: str) -> str`: Generates the G2P representation of a given word.
- `generate_g2p_list(sentence: str) -> list[str]`: Generates a list of words with their G2P representations for the given sentence.
### metaphone.py
- `generate_metaphone_key_list(sentence: str) -> list[str]`: Generates a list of words with their Metaphone keys for the given sentence.
Please note that some function descriptions and code samples have been omitted for brevity. Refer to the source code for more detailed information.


