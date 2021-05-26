import re
import os
import sys
import glob
import socket
import signal

def signalHandler(signal, frame):
  print
  print "Well find it yourself, then..."
  sys.exit(0)

# Check storage IPv6 if 22 is listening
def checkPort(ip):
  ret = "Closed"
  s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
  try:
    s.settimeout(1)
    s.connect((ip, 22))
    s.close()
    ret = "Open"
  except:
    pass
  return ret

# Get list of IPv4 LDAP IPs from ldap.conf
def getLDAPIPs():
  try:
    ldapFile = open("/etc/ldap.conf", "r")
  except IOError, e:
    print e

  for line in ldapFile:
    if re.match("uri", line):
      LDAPIPs = re.findall( r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\w+$', line)
      return LDAPIPs

#Check for PXE
def dhcpinfo(host):
  DHCPFILES = glob.glob("/etc/dhcpd.conf_*")
  for dhcp_file in DHCPFILES:
    pxe = "None"
    file = open(dhcp_file, "r")
    for line in file:
      if host.lower() in line:
        while True:
          nxt = file.next()
          if "}" in nxt:
            break
          else:
            if "filename" in nxt:
              pxe = nxt.split()[1].strip("\";")
        print "PXE \t\t\t: " + pxe
    file.close()


# ldaptst for given host
def ldaptst(host):

  for LDAPIP in getLDAPIPs():
    ldaptst_output = os.popen("ldaptst -vvvv -s " + LDAPIP + " -n " + host.lower()).read ().split ('\n')
    vlan = "vlan"
    admip = "admin IPv6"
    stoip = "sto IPv6"
    stomac = "sto MAC"
    netgroup = "netgroup"
    customer = "customer"
    stossh = "Closed"
    rootimage = "Root Image"
    cluster = "Cluster"
    do = "DO"
    netapp = "netapp"
    timezone = "tzl"
    ldap = "ldap"
    siux = "siux"
    stomac = "stomac"
    admmac = "admmac"
    vlstoid = "vlstoid"
    vladmid = "vladmid"
    vlcusid = "vlcusid"

    if len(ldaptst_output) > 5:
      print "\t*** " + host.lower() + " ***"
      print "\t" + ("*" * (len (host) + 8))
    for entry in ldaptst_output:
      if "f_ldapsearch" in entry:
        vlan = re.findall(r'\w{0,4}\_\w{0,3}\_\w{0,1}\_\w{0,4}\-\w{0,8}', entry)
      if "netgroup[0]" in entry:
        netgroup = entry.split("=")[1]
      if "iphostnumber[0]" in entry:
        admip = entry.split("=")[1]
      if "iphostnumbersto[0]" in entry:
        stoip = entry.split("=")[1]
      if "macaddresssto[0]" in entry:
        stomac = entry.split("=")[1]
      if "CUST" in entry:
        customer = entry.split(": ")[1]
      if "TIVSYSID" in entry:
        sger = entry.split(": ")[1]
      if "TIVSYSDO" in entry:
        do =  entry.split(": ")[1]
      if "root-image" in entry:
        rootimage = entry.split(": ")[1]
      if "basissystem[0]" in entry:
        cluster = entry.split("=")[1]
      if "TZL" in entry:
        timezone = entry.split(": ")[1]
      if "NETAPPP" in entry:
        netapp = entry.split(": ")[1]
      if "NTPS" in entry:
        ntp = entry.split(": ")[1]
      if "LDAPSRV" in entry:
        ldap = entry.split(": ")[1]
      if "SIUXIP" in entry:
        siux = entry.split(": ")[1]
      if "macaddresssto[0]" in entry:
        stomac  =  entry.split("=")[1]
      if "macaddress[0]" in entry:
        admmac = entry.split("=")[1]
      if "vlanidsto[0]" in entry:
        vlstoid = entry.split("=")[1]
      if "vlanidadmin[0]" in entry:
        vladmid = entry.split("=")[1]
      if "vlanidcust[0]" in entry:
        vlcusid = entry.split("=")[1]

    if vlan != "f_ldapsearch":
      print "VLAN \t\t\t: " + str(vlan).strip("['']")
    if netgroup != "netgroup":
      print "Netgroup \t\t: " + netgroup
    if admip != "admin IPv6":
      print "ADM IPv6 Address \t: " + admip
    if stoip != "sto IPv6":
      print "STO IPv6 Address \t: " + stoip
    if stoip != "sto IPv6":
      stossh = checkPort(stoip)
      print "STO ssh \t\t: " + stossh
    if do != "DO" and do:
      print "DO number \t\t: " + do
    if rootimage != "Root Image":
      print "RO Image \t\t: " + rootimage
    dhcpinfo(host)
    if cluster != "Cluster":
      print "Cluster \t\t: " + cluster
    if sys.argv[1] == "-v":
      if netapp != "netapp":
        print "NetApp \t\t\t: " + netapp
      if timezone != "tzl":
        print "Timezone \t\t: " + timezone
      if ldap != "ldap":
        print "LDAPSRV \t\t: " + ldap
      if siux != "siux":
        print "SIUX \t\t\t: " + siux
      if stomac != "stomac":
        print "STO MAC \t\t: " + stomac
      if admmac != "admmac":
        print "ADM MAC \t\t: " + admmac
      if vlstoid != "vlstoid":
        print "STO ID \t\t\t: " + vlstoid
      if vladmid != "vladmid":
        print "ADM ID  \t\t: " + vladmid
      if vlcusid != "vlcusid":
        print "CST ID \t\t\t: " + vlcusid
    print ""
    break

if __name__ == "__main__":
  signal.signal(signal.SIGINT, signalHandler)
  if len (sys.argv) == 1:
    print "No free rides, enter hostname! For more information, use '-v'."
  elif len (sys.argv) >= 3 and sys.argv[1] == "-v":
    hosts = sys.argv[2:]
    for host in hosts:
      if len(host) != 14:
        print "Host should have 14 characters."
      else:
        ldaptst(host)
  else:
    hosts = sys.argv[1:]
    for host in hosts:
      if len(host) != 14:
        print "Host should have 14 characters."
      else:
        ldaptst(host)
