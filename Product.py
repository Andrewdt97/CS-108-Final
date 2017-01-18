from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import random



class Product:
    
    def __init__(self, test=False, name=None, price=None, id = '252680412030'):
        
        # For testing purposes, if test is set to true, take other parameters as input, rather than searching randomly
        if test:
            self._name = name
            self._price = price
        
        else:
            '''
            The following code was taken from the python documentation at the following url:
            https://docs.python.org/3.1/howto/urllib2.html
            Because eBay is not a fan of automated access to their website, this code makes python's
            request look like it came from someone's browser.
            '''
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
            # Loop runs until a valid item is found, see future comments for more explination
            while True:
                # Randomly creates a 12 digit ID if a manual one is not entered and puts it into a URL
                if id == None:
                    productID = ''
                    for i in range(12):
                        productID += str(random.randint(0,9))
                else:
                    productID = id
                    
                productID = '252680412030'
                
                url = 'http://www.ebay.com/itm/' + productID
                print('Trying ID#: ' + productID)
                    
                '''
                The following code was taken from the python documentation at the following url:
                https://docs.python.org/3.1/howto/urllib2.html
                It scrapes the html data from the url and allows Beautiful Soup to search it
                '''
                try:
                    req = urllib.request.Request(url, binary_data, headers)
                    response = urllib.request.urlopen(req) # Most of a time this line will throw a HTTP Error 404: Not Found error because the 12 digit id generated is not assigned by eBay to an item
                    html = response.read()
                    soup = BeautifulSoup(html, 'html.parser')
                    '''
                    End borrowed code
                    '''
                    
                    '''Title Search'''
                    # Searches the html for 'id=vi-lkhdr-itmTitl' which is where the title is stored.
                    # Occasionally the page is actually a search result in which case an error is thrown
                    self._title = soup.find(id='vi-lkhdr-itmTitl').string
                    if self._title == None:
                        raise ValueError('Search page found instead of item')
                    
                    
                    '''Price Search'''
                    
                    self._price = None
                    
                    # See if the page has a foreign currency and if so, get the USD price
                    # If Beautiful Soup cannot find the tag given, it throws an error which, in this means, the item was listed in USD
                    try:
                        self._price = soup.find(id='convbinPrice').string
                    except:
                        pass
                    
                    # Try the primary then the secondary method eBay stores USD prices in the html
                    if self._price == None:
                        try:
                            self._price = soup.find(id='prcIsum').string
                        except:
                            self._price = soup.find(class_='notranslate vi-VR-cvipPrice').string
                    
                    # Remove the commas from the price, take off any whitespace and currency sign, then convert it to a number
                    self._price = self._price.replace(',', '')   
                    self._price = float(self._price.strip()[4:])
                    
                    # Most items will have their prices floored, this prevents items
                    # less than a dollar becoming 0
                    if self._price < 1.0:
                        continue
                    
                    '''Img URL search'''    
                    self._imgURL = soup.find(id='icImg')
                    self._imgURL = self._imgURL['src']
                    
                    # If everything ran smoothly, finish the __init__
                    print('Success!')
                    break
                
                # If anything above went wrong (namely a 404 error or finding an eBay search result), look for another item
                except Exception as e:
                    # Print the ID tried and the error to console, then continue
                    print(e)
                    print('-----------')
                    continue
            
    def getTitle(self):
        return self._title
    
    def getPrice(self):
        return self._price
    
    def getImgUBase64(self):
        return self._imgBase64
            
if __name__ == '__main__':
    item = Product()
    print(item._title)
    print(item._price)
    print(item._imgURL)
    
