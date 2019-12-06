# Program to download the image from internet
import random
import urllib.request # a package that reterive the data from internet (Requirment: url)

def download_web_image(url):
    randNumber = random.randrange(1, 100) # random number in the range of 1 to 100
    fullName = str(randNumber) + '.jpg'
    urllib.request.urlretrieve(url, fullName) # requires the url and the name of which you want to save the image 

# Pass the url of the image to be downloaded 
download_web_image('https://sc01.alicdn.com/kf/UTB8yC05B5aMiuJk43PTq6ySmXXa2/Open-Hot-Sexi-Images-Hot-Sexy-Girl.jpg')
