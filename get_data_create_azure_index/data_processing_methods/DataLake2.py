import re

def extract_specific_field(body:str, start_index_string:str, end_index_string:str):
    start_index = body.find(start_index_string)
    end_index = body.find(end_index_string)
    body = body[start_index:end_index]
    # Additional logic if needed -> start_index = body.find('next piece of text')
    return body[start_index+6:end_index].strip()

def data_lake2_extract(data_lake2_input, data_lake2_format):
    # Change data_lake2_input to ensure consistency
    data_lake2_input = {key: value.replace("\u200b","") for key, value in data_lake2_input.items()} # don't care about \u200b's anymore
    data_lake2_input = {key: re.sub(r'\(\s*TOP\s*\)', '(TOP)', value, flags=re.I) for key, value in data_lake2_input.items()} # fixes top issue
    data_lake2_input = {key: re.sub(r'\s+', ' ', value).strip() for key, value in data_lake2_input.items()} # fixes spacing issue -> should be 1 space between every word now
    # Initialize data_lake2_output with the keys from format and blank values
    data_lake2_output = data_lake2_format
    # Match identical fields
    data_lake2_output["title"] = data_lake2_input["title"]
    data_lake2_output["link"] = data_lake2_input["link"]
    data_lake2_output["data_source"] = "data_lake2"
    # Call methods from above
    data_lake2_output["additional_information"] = extract_specific_field(data_lake2_input["body"],"start_index_string","end_index_string")
    # Return
    return data_lake2_output