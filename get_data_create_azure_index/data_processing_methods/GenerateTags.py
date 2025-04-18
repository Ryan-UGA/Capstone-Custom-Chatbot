import json 
import csv
import re
import pandas as pd
import os

def generate_tags_from_csv_column(csv_file_path, json_data):
    # Initialize tags and regex_patterns as all patterns in the csv file, specifically in the column named "Title"
    tags = []
    csv = pd.read_csv(csv_file_path)
    regex_patterns = [regexp for regexp in csv["Title"]]

    def extract_values(obj):
        # Recursively extract all textual values from JSON.
        if isinstance(obj, dict):
            for key, value in obj.items():
                yield key
                yield from extract_values(value)
        elif isinstance(obj, list):
            for item in obj:
                yield from extract_values(item)
        elif isinstance(obj, str):
            yield obj

    # Check matches
    for text in extract_values(json_data):
        for pattern in regex_patterns:
            text = text.lower()
            pattern = pattern.lower()
            if text.find(pattern)!=-1:
                tags.append(pattern)

    return list(set(tags))  # Remove duplicates