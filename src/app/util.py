import re

    
def limpar_json(json_data):
    json_data = re.sub(r"^```json\s*|\s*```$", "", json_data.strip(), flags=re.IGNORECASE | re.MULTILINE)
    return json_data