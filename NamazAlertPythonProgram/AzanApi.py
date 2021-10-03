from Request import GetdatabyGetMethod

def GetAzanTimings(latitude, longitude, date, month, year):
    url = "http://api.aladhan.com/v1/calendar?latitude={lat}&longitude={long}&month={month}&year={year}".format(lat = latitude, long = longitude, month = month, year = year);
    azan_obj = GetdatabyGetMethod(url)['data'][date - 1];
    return azan_obj;
    
    
