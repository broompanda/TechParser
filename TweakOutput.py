__author__ = 'christie'

import sys
import re

def tweaklldp(output_temp_file):
    interfaces={}
    for line in (output_temp_file).readlines():
        line=line.rstrip()
        interface_name=re.findall('^Interface ([\S]+) detected [^0]',line)
        if len(interface_name)>0:
            int=interface_name[0]
            interfaces[int]={}
        else:
            neighbor_name=re.findall('.*System Name: "(\S+)"',line)
            if len(neighbor_name)>0:
                interfaces[int]["neighbor_name"] = neighbor_name[0]
            else:
                neighbor_info=re.findall('.*Neighbor (\S+), age',line)
                if len(neighbor_info)>0:
                    interfaces[int]["neighbor_mac"] = neighbor_info[0]
    interface_names = interfaces.keys()
    interface_names.sort()
    for interface in interface_names:
        if len(interfaces[interface])>1:
            print interface + " connected to " +interfaces[interface]["neighbor_mac"] + ". Device name:  " +interfaces[interface]["neighbor_name"]
        else:
            print interface + " connected to " +interfaces[interface]["neighbor_mac"]

def tweakipint(output_temp_file):
    pass

def main():
    tweaklldp()

if __name__ == "__main__":
    main()
