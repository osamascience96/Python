# Program to fetch data from API and give data against region in input

from urllib import request
from requests import request

def GetJsonData():
    url = "https://ip-ranges.amazonaws.com/ip-ranges.json"

    # request the data 
    response = request("GET", url)

    # return the response
    return response

if __name__ == "__main__":
    data = GetJsonData()

    # check data response
    if data.reason == "OK":
        # ips list
        ipsList = []
        # set json data to response
        response = data.json()

        # input region
        region = input("Enter Accurate Region Code: ")

        if(len(region) > 0):
            #  iterate through array objects
            for obj in response['prefixes']:
                if(obj['region'] == region):
                    ipsList.append(obj['ip_prefix'])
            
            print("Received List .....")
            print(ipsList)
        else:
            print("Invalid Region Code")
        
            
    else:
        print(f"Server Response: {data.reason}")