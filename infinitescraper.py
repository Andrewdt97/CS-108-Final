from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import random

'''
The following code was taken from the python documentation at the following url:
https://docs.python.org/3.1/howto/urllib2.html
'''
#url = 'http://www.ebay.com/itm/141326306007'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
values = {'name' : 'Andrew Thomas',
          'location' : 'Grand Rapids',
          'language' : 'Python' }
headers = { 'User-Agent' : user_agent }

data = urllib.parse.urlencode(values)
binary_data = data.encode('ASCII')
'''
End borrowed code
'''

numFound = 0
numPooed = 0
while True:
    productID = ''
    for i in range(12):
        productID += str(random.randint(0,9))
    #print(productID)
    
    url = 'http://www.ebay.com/itm/' + productID
        
    '''
    The following code was taken from the python documentation at the following url:
    https://docs.python.org/3.1/howto/urllib2.html
    '''
    try:
        req = urllib.request.Request(url, binary_data, headers)
        response = urllib.request.urlopen(req)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        numFound += 1
    except:
        continue
    try:
        title = soup.find(id='vi-lkhdr-itmTitl').string
        
        try:
            price = soup.find(id='prcIsum').string
        except:
            price = soup.find(class_='notranslate vi-VR-cvipPrice').string
            
        price = price.strip()[4:]
            
        imgURL = soup.find(id='icImg')
        imgURL = imgURL['src']
    except Exception as e:
        numPooed +=1
        print(e)
        print(productID)
        print('---------------------------------')
        continue
    
    
    

    
'''
End borrowed code
'''
