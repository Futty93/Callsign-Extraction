[日本語](./README-jp.md)

**An English version of the README is currently under construction.**


## Project Description
This project involves adding call signs to two JSON files, `airline_code_dict.json` and `word_register.json`, located in the `./registered_json` directory. In `airline_code_dict.json`, call signs are added in the format [callsign: 3-letter code] as a dictionary. In `word_register.json`, call signs are added individually, considering cases where a call sign consists of multiple words (e.g., "all nippon", "all", "nippon").

After updating the JSON files, you need to install the dependencies listed in `requirements.txt` by executing the following command in the terminal:

```bash
pip install -r requirements.txt
```
Next, you should run `registered_word_utils.py` to generate dictionaries for `g2p` and `metaphone` from the registered information in the `registered_json` directory. The generated dictionaries will be saved in the `./generated_json` directory.

```bash
python registered_word_utils.py
```
In `main.py`, the `main()` function accepts a transcribed text result as input. If call signs are found, they will be returned as an array. If no call signs are found, the output will be "Callsign not Found".

## External Libraries Used
This project utilizes the following libraries and modules:

- `json`: Used for reading and writing JSON files.
- `doublemetaphone`: A library implementing the Double Metaphone algorithm.
- `re`: Utilized for regular expression operations.
- `G2p`: A library for Grapheme-to-Phoneme conversion in English.
- `Levenshtein.distance`: Method for calculating Levenshtein distance.

These libraries and modules are used for tasks such as text processing, phonetic conversion, and string comparison within the project.