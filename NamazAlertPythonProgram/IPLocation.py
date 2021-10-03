from Request import GetdatabyGetMethod

def GetIpBasedLocation(ip):
    url = "http://ip-api.com/json?ip={ipaddress}".format(ipaddress = ip);
    return GetdatabyGetMethod(url);