import re

    
def limpar_json(json_data):
    # Remove marcações de bloco de código (```json e ```)
    json_data = re.sub(r"^```json\s*|\s*```$", "", json_data.strip(), flags=re.IGNORECASE | re.MULTILINE)
    # Remove quebras de linha literais (\n) e caracteres de escape adicionais como \t
    json_data = json_data.replace("\n", "").replace("\t", "").replace("\r", "")
    return json_data