import json
import os
import re
from utils.levenshtein import distance
from API.get_area_info import get_callsigns_from_api

script_dir = os.path.dirname(os.path.abspath(__file__))
area_info_path = os.path.join(script_dir, "../ATC_area_info.json")

# area_info_path = os.path.join(script_dir, "../area_info.json")

class Extractor:
    def __init__(self):
        # テスト用の空域情報の利用はこっち
        with open(area_info_path, 'r', encoding='utf-8') as f:
            self.area_info = json.load(f)
        
        # # Horusの空域情報の利用はこっち
        # self.area_info = get_callsigns_from_api()

    def extract_pattern(self, sentence: str) -> list | bool:
        """
        Extract callsign patterns from the given sentence.

        Parameters
        ----------
        sentence : str
            The sentence to be processed.

        Returns
        -------
        list
            A list of extracted callsign patterns, or False if no patterns are found.
        """
        pattern = r'\b([A-Z]{3})\s(\d+)\b'
        matches = re.findall(pattern, sentence)
        if matches:
            extracted_patterns = [''.join(match) for match in matches]
            return extracted_patterns
        else:
            return False
    
    def reference_area_info(self, extracted_callsign: str) -> list:
        """
        Find the closest callsign matches from the known area information.

        Parameters
        ----------
        extracted_callsign : str
            The extracted callsign to be compared.

        Returns
        -------
        list
            A list of lists containing the closest callsign matches and their edit distance.
            If min_distance == 0, the list will contain one entry [[closest_callsign, min_distance]].
            If min_distance > 0, the list will contain all matches with the same min_distance.
        """
        min_distance: int = 128
        closest_callsigns = []

        for area_callsign in self.area_info:
            # Extract alphabetic part
            area_alpha_part = ''.join(filter(str.isalpha, area_callsign))
            extracted_alpha_part = ''.join(filter(str.isalpha, extracted_callsign))

            # Check if alphabetic parts match
            if area_alpha_part != extracted_alpha_part:
                continue

            # Calculate edit distance for numeric parts
            area_num_part = ''.join(filter(str.isdigit, area_callsign))
            extracted_num_part = ''.join(filter(str.isdigit, extracted_callsign))
            d = distance(extracted_num_part, area_num_part)

            if d < min_distance:
                min_distance = d
                closest_callsigns = [[area_callsign, d]]
            elif d == min_distance:
                closest_callsigns.append([area_callsign, d])

        return closest_callsigns