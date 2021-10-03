from requests import get
from Request import GetdatabyGetMethod

def getmyipaddr():
    url = "https://jsonip.com"
    return GetdatabyGetMethod(link=url)

if __name__ == "__main__":
    print(getmyipaddr())