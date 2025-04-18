import json 
import re

# Anonymize_json method uses the other methods

# List of keywords that must not be altered
KEYWORDS = {}

# u200b = [] # Everything that has u200b attached or just multiple u200b's

def anonymize_word(word:str):
    characters = word.split()
    new_text = ""
    for char in word:
        if char.isalpha():  # char is a letter
            new_text = new_text + 'X'
        elif char.isnumeric():  # char is a number
            new_text = new_text + '9'
        elif char=='-':
            new_text = new_text + '-'
        else:
            if len(word) > 6 and word.find(' ')!=-1: # assuming this is \u200b... and no spaces
                new_text2 = []
                for each in word.split('\u200b'):
                    if len(each) > 0:
                        new_text2.append(" \u200b " + each)
                new_word = "".join(new_text2)
                anonymize_word(new_word)
            else:
                # for chars in char:
                #     print("chars: ",chars)
                #     u200b.append(chars)
                continue
            new_text = new_text + char  # retain spaces and other characters
    return new_text

def anonymize_with_special_chars(text: str): # Split text while preserving delimiters using regex 
    parts = re.split(r'([\-._/:(),\\><!@#$%^&*"+={}?%])', text) 
    # Apply anonymization to non-delimiter parts 
    new_value = [anonymize_word(word) if word not in '-._/:(),\\><!@#$%^&*"+={}?%' else word for word in parts] 
    return "".join(new_value) 

def anonymize_u200b(word:str):
    return None

def anonymize_text(value:str): 
    new_value = []
    # for text in re.findall(r'\S+|\s',value):
    for text in value.split(' '):
        if type(text)!=str: # \n and other stuff might be NoneType
            new_value.append(text)
            continue # continue skips the rest of loop below which assumes the text is a string

        if bool(re.search(r'[\-._/:(),\\><!@#$%^&*"+={}?%]', text)): # has dash, period, etc. (not letters, not numbers, not special char)
            new_value.append(anonymize_with_special_chars(text))
            continue

        if re.search(r'[^\w\s]',text): # \u200b and other stuff, ^ is not, \w is word char like number, letter, etc., \s is whitespace
            if len(text)==1: # just \u200b has length of 1
                new_value.append('u200b')
            else: # \u200b... or ...\u200b... or ...\u200b and you could have \u200b stacked next to each other
                # u200b.append(text.split('\u200b'))
                for word in text.split('\u200b'):
                    if len(word)==0: # since splitting by \u200b, no length will be \u200b
                        new_value.append('u200b')
                    else:
                        anonymize_u200b(word)
            continue
        
        if (text in KEYWORDS) or (not text.strip()): # KEYWORDS defined at top of script or empty strings (i.e. spaces) will not change
            new_value.append(text)
            continue

        if text.strip().isalnum(): # no dashes -> all chars in text are letters or numbers
            new_value.append(anonymize_word(text))
    return new_value

def anonymize_json(input_file_path, output_file_path):
    with open(input_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    anonymized_data = {key: anonymize_text(value) for key, value in data.items()}
    anonymized_data = {key: " ".join(value) for key, value in anonymized_data.items()}

    with open(output_file_path, "w", encoding="utf-8") as file:
        json.dump(anonymized_data, file, ensure_ascii=False, indent=4)