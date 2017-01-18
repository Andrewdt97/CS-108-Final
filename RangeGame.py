from Product import *
import math

class RangeGame:
    
    def __init__(self, prod, debug=False):
        # Initialize the length of the price
        self._priceLength = 0
        
        # Grab the price and figure out how large it is
        self._priceSlice = prod.getPrice()
        
        while self._priceSlice > 0:
            self._priceSlice = self._priceSlice // 10
            self._priceLength += 1
        
        # Scale the range of the whole scale to 6 * (10** priceLength-2)
        # So a $4000 item will have a $600 range. A $4 item will have a $0.40 range  
        self._priceRange = 6 * math.pow(10, self._priceLength-2)
        self._priceRange = float('{:.2}'.format(self._priceRange))
        
        # Range of the guess section will be 1/4 of the total price range
        self._guessRange = 1.5*math.pow(10, self._priceLength-2)
        self._guessRange = float('{:.2}'.format(self._guessRange))
        
        # Randomize a number between 0.1 and 0.9 and multiply it by the total price range
        # Take this number and subtract is from the item price to create
        # a random starting place for the guess scale in relation to the item
        self._boardRangeStartMultiplier = 0.5
        
        while float(self._boardRangeStartMultiplier) > 0.9 or float(self._boardRangeStartMultiplier) < 0.1:
            self._boardRangeStartMultiplier = '%:.2f' % random.random()
        self._boardRangeStart = prod._price - (self._boardRangeStartMultiplier * self._priceRange)
        
        
    
    def getBoardRangeStart(self):
        return self._boardRangeStart
    
    def getPriceRange(self):
        return self._priceRange
    
    def getGuessRange(self):
        return self._guessRange
            
    
    
if __name__ == '__main__':
    item = Product()
    game = RangeGame(item)
    print(item._price)
    print(game._priceLength)
    print(game._priceRange)
    print(game._guessRange)
    print(game._boardRangeStartMultiplier)
    print(game._boardRangeStart)