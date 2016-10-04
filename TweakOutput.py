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
    int1='unassigned'
    int2=''
    int3=''


    print "%-20s%-25s%-25s%-20s%-20s" % ("Interface","IP Address","Status","Protocol","MTU")
   
    for line in output_temp_file.readlines():
        line=line.rstrip() #output as seen exactly in show interfaces
        interface_ip=re.findall(".*Internet address.*",line)
        if len(interface_ip)!=0:
            int1=interface_ip[0].split(" ")[5] #IP address
     
      
        interface_name=re.findall(".*line.*\s+",line)
        if len(interface_name)!=0:
            
            int2=re.findall('(\S*) is (.*), line protocol is ([\S]*)',line) 
      
        

        interface_mtu=re.findall(".*IP MTU.*",line)
        if len(interface_mtu)!=0:
            int3=interface_mtu[0].split(" ")[4] #MTU
      
        if len(interface_mtu)>0:
            print "%-20s%-25s%-25s%-20s%-20s" % (int2[0][0],int1,int2[0][1],int2[0][2],int3)
            int1='unassigned'
      

def main():
    tweaklldp()

if __name__ == "__main__":
    main()
