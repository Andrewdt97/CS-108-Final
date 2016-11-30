#from bs4 import BeautifulSoup
import urllib.parse
import urllib.request

url = 'https://www.amazon.com/dp/B01C4TPP86/'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
values = {'name' : 'Andrew Thomas',
          'location' : 'Grand Rapids',
          'language' : 'Python' }
headers = { 'User-Agent' : user_agent }

data = urllib.parse.urlencode(values)
binary_data = data.encode('ASCII')
req = urllib.request.Request(url, binary_data, headers)
response = urllib.request.urlopen(req)
the_page = response.read()

print(the_page)
print(sys.path)
'''class Item:
    
    def __init__(self):
        
        self._soup = BeautifulSoup(https://www.amazon.com/Razor-Roller-Freestyle-20-Inch-Yellow/dp/B01C4TPP86/ref=sr_1_1?s=digital-text&ie=UTF8&qid=1480375719&sr=8-1&keywords=bike)
        '''