import hl7 
import os

def hl7_from_text_file(file_path):

    if not os.path.exists(file_path):
        raise ValueError('File does not exist: '+file_path)

    with open(file_path, 'r') as file:
        msg = file.readlines()

    msg = ''.join(msg).replace('\n', '\r')
    return hl7.parse(msg)


    