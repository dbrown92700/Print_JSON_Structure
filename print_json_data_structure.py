"""
Prints the structure of a JSON object.
For list items in the structure, it evaluates only the first item in the list.
It will evaluate strings to see if they are actually JSON or XML and will print the
embedded structure of those as well.

Run:
	python print_json_data_structure.py filename.json
"""
import json
import sys
import xml.parsers.expat
import xmltodict
from colorama import Fore, Style


def print_json_structure(data, indent=0, is_key=False):
    data_type = type(data)
    if not is_key:
        print(indent * '  ', end='')
    print(data_type)
    if isinstance(data, list):
        print(indent * '  ', ' [')
        try:
            print_json_structure(data[0], indent=indent + 1)
        except IndexError:
            print((indent + 1) * '  ', Fore.RED + 'No data present' + Style.RESET_ALL)
        print(indent * '  ', ' ]')
    if isinstance(data, dict):
        print(indent * '  ', ' {')
        for key in data:
            print(Fore.GREEN + (indent + 1) * '  ', f'{key+":":50}', end='' + Style.RESET_ALL)
            print_json_structure(data[key], indent=indent + 1, is_key=True)
        print(indent * '  ', ' }')
    if isinstance(data, str):
        try:
        	# Is the string a number? Catch it before it passes the JSON test.
            number_test = float(data)
        except ValueError:
            try:
            	# Is the string XML?
                xdata = xmltodict.parse(data)
                print((indent + 1) * '  ', Fore.RED + 'String is XML Data ... converting to dict' + Style.RESET_ALL)
#                 print(indent * '  ', ' {')
                print_json_structure(xdata, indent=indent + 1)
#                 print(indent * '  ', ' }')
            except xml.parsers.expat.ExpatError:
                try:
                	# Is the string JSON?
                    jdata = json.loads(data)
                    print((indent + 1) * '  ', Fore.RED + 'String is JSON Data ... converting to dict' + Style.RESET_ALL)
                    print(indent * '  ', ' {')
                    print_json_structure(jdata, indent=indent + 1)
                    print(indent * '  ', ' }')
                except json.decoder.JSONDecodeError:
                    # It's just a regular string.
                    pass

if __name__ == '__main__':
	# Open file passed as arg and print structure
    filename = sys.argv[1]
    json_data = json.load(open(filename))
    print_json_structure(json_data)
