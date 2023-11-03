import json

def dict_to_php_array(d, indent=0):
    """
    Function to convert a Python dictionary to a PHP associative array.
    """
    php_array = "array(\n"
    indent_str = "  " * (indent + 1)
    for key, value in d.items():
        php_key = f"'{key}'"
        if isinstance(value, dict):
            php_value = dict_to_php_array(value, indent=indent+1)
        else:
            escaped_value = str(value).replace('\\', '\\\\').replace('\'', '\\\'')
            php_value = f"'{escaped_value}'"
        php_array += f"{indent_str}{php_key} => {php_value},\n"
    php_array += "  " * indent + ")"
    if indent == 0:
        php_array += ";"
    return php_array

def convert_js_to_php(json_file_path, php_file_path):
    with open(json_file_path, 'r') as file:
        json_content = file.read()

    try:
        json_data = json.loads(json_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing JSON: {e}")

    php_array_str = "<?php\n\n$lang = " + dict_to_php_array(json_data)

    with open(php_file_path, 'w') as php_file:
        php_file.write(php_array_str)
