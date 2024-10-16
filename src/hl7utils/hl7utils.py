import hl7 

# maybe try this package for build/send/receive of hl7 messages
import hl7apy
from hl7apy import parser
from hl7apy.core import Group, Segment
from hl7apy.exceptions import UnsupportedVersion

import os

indent = "    "
indent_seg = "    "
indent_fld = "        "

def subgroup (group, indent):
    indent = indent + "    "
    print (indent , group)
    for group_segment in group.children:
        if isinstance(group_segment, Group):
            subgroup (group_segment)
        else: 
            print(indent_seg, indent ,group_segment)
            for attribute in group_segment.children:
                print(indent_fld, indent ,attribute, attribute.value)


def show_message(file_path: str) -> None:
    """

    """
    if not os.path.exists(file_path):
        raise ValueError('File does not exist: '+file_path)

    with open(file_path, 'r') as file:
        dat = file.readlines()
    dat = ''.join(dat).replace('\n', '\r')
    msg = parser.parse_message(dat)

    print(msg.children[1])
    for segment in msg.children:
        if isinstance(segment, Segment):
            print (indent ,segment)
            for attribute in segment.children:
                print(indent_fld, indent, attribute, attribute.value)
        if isinstance(segment, Group):
            for group in segment.children:
                print (indent,group)
                for group_segment in group.children:
                    if isinstance (group_segment, Group): 
                        subgroup (group_segment, indent)
                    else:
                        print(indent_seg, indent ,group_segment)
                        for attribute in group_segment.children:
                            print(indent_fld, indent, attribute, attribute.value)


def from_text_file(file_path: str, find_groups=True) -> hl7apy.core.Message:
    """

    """

    if not os.path.exists(file_path):
        raise ValueError('File does not exist: '+file_path)

    with open(file_path, 'r') as file:
        msg = file.readlines()
    msg = ''.join(msg).replace('\n', '\r')

    return parser.parse_message(msg, find_groups=find_groups)

def message_type(hl7_msg: hl7.Message) -> str:
    """

    """
    return hl7_msg.msh.msh_9.value


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

def children_names(children: list) -> list:
    """

    """
    return [child.name for child in children]

def get_reasons_for_study(hl7_msg: hl7apy.core.Message) -> str:
    """

    """
    reasons=[]
    for i in hl7_msg.children:
        if i.name == 'ORU_R01_RESPONSE':
            #print(i.name)
            for j in i.children:
                if j.name == 'ORU_R01_ORDER_OBSERVATION':
                    #print("  " + j.name)
                    for k in j.children:
                        if k.name == 'OBR':
                            #print("    " + k.name)
                            for l in k.children:
                                #print("      " + l.name)
                                if l.name == 'OBR_31':
                                    #print("        " + l.value)
                                    reasons.append(l.value)
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



    