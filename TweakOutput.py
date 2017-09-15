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
                neighbor_info=re.findall('.*Neighbor (.+), age',line)
                if len(neighbor_info)>0:
                    interfaces[int]["neighbor_mac"] = neighbor_info[0]

    interface_names = interfaces.keys()
    interface_names.sort()
    for interface in interface_names:
        #print interface + " connected to " +interfaces[interface].get("neighbor_mac","MAC_Unknown") + ". Device name:  " +interfaces[interface].get("neighbor_name","Neighbor_name_unknown")
        print "%-17s%-15s%-35s%-20s%-20s" % (interface,"connected to",interfaces[interface].get("neighbor_mac","MAC_Unknown")," Device name:  ",interfaces[interface].get("neighbor_name","Neighbor_name_unknown"))


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
      

def tweakmroute(group,source,flag):
  test=0
  test1=0
  group_section=0
  with open('ipmroute') as f:
    lines = f.readlines()
  for line in lines:
    line=line.rstrip()
    if group in line:
      test=1
    if test==1 and flag==0:
      if len(re.findall("\s+", line)) == 0 and group not in line:
        break
      print line
    elif flag==1:
        if source in line:
          test1=1
        if test1==1:
          if len(re.findall(".*flags.*", line)) == 1 and source not in line:
            break
          print line

def main():
  tweakmroute('224.0.5.223','159.125.70.194',1)

if __name__ == "__main__":
    main()
