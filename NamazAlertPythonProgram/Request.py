import requests

def GetdatabyGetMethod(link, parameters=None):
    # if params are available
    request = None;

    try:
        if(parameters is not None):
            request = requests.get(url=link, params=parameters)
        else:
            request = requests.get(url=link)
    except:
        return None;
    
    data = request.json()

    return data;


