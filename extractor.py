import json
import re
from Levenshtein import distance

class Extractor:
    def __init__(self):
        with open("area_info.json", 'r', encoding='utf-8') as f:
            self.area_info = json.load(f)

    def extract_pattern(self, sentence: str) -> list:
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
        Find the closest callsign match from the known area information.

        Parameters
        ----------
        extracted_callsign : str
            The extracted callsign to be compared.

        Returns
        -------
        list
            A list containing the closest callsign match and its edit distance.
        """
        min_distance: int = 128
        closest_callsign = ""
        for area_callsign in self.area_info:
            d = distance(extracted_callsign, area_callsign)
            if d < min_distance:
                min_distance = d
                closest_callsign = area_callsign

        return [closest_callsign, min_distance]