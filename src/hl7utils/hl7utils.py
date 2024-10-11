import hl7 
import os

def from_text_file(file_path: str) -> hl7.Message:
    """

    """

    if not os.path.exists(file_path):
        raise ValueError('File does not exist: '+file_path)

    with open(file_path, 'r') as file:
        msg = file.readlines()
    msg = ''.join(msg).replace('\n', '\r')

    return hl7.parse(msg)

def get_segment_list(hl7_msg: hl7.Message) -> list:
    """

    """
    return [segment[0][0] for segment in hl7_msg]


def has_observations(hl7_msg: hl7.Message) -> bool:
    """

    """
    ret=False
    if 'OBX' in get_segment_list(hl7_msg):
        ret=hl7_msg.segment('ORC')[1][0]=='RE'
    return ret


def get_reasons_for_study(hl7_msg: hl7.Message) -> str:
    """

    """
    reasons=None
    if 'OBR' in get_segment_list(hl7_msg):
        reasons = ["|".join(r[0]) for r in hl7_msg.segment('OBR')[31]]

    return reasons

def get_procedure_info(hl7_msg: hl7.Message) -> str:
    """

    """
    ret=None
    if 'OBR' in get_segment_list(hl7_msg):
        ret = [ r[0] for r in hl7_msg.segment('OBR')[4][0]]
    return ret

def get_text_observations(hl7_msg: hl7.Message) -> str:
    """

    """
    ret={}
    if 'OBX' in get_segment_list(hl7_msg):
        segs=hl7_msg.segments('OBX')
        for s in segs:

            # if ValueType is text
            if s[2][0]=='TX':
                cpt=s[3][0][0][0]
                type=s[3][0][0][1]
                desc=s[3][0][1][0]
                value=s[5][0]

                if cpt not in ret:
                    ret[cpt]={'description' : desc, 'observations' : {} }
                    ret[cpt]['observations'][type]=value
                else:   
                    ret[cpt]['observations'][type]=value


    return ret



    