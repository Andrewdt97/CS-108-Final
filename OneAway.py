from Product import *
import math
import random


class OneAway:
    
    def __init__(self, prod, debug=False):
        #Initialize game over boolean
        self._gameOver = False
        
        # For each integer in the price of the item, create a number object with that value
        itemPrice = math.floor(prod.getPrice())
        self._intsInPrice = [] 
        while itemPrice > 0:
            self._intsInPrice.append(OneAwayNum(itemPrice % 10))
            itemPrice = itemPrice // 10
            
        # Reverse the list to get the correct order of numbers
        self._intsInPrice = self._intsInPrice[::-1]
        
        # Shuffle each number by either adding or subtracting one
        addSub = [-1, 1]
        
        for idx in range(len(self._intsInPrice)):
            self._intsInPrice[idx]._shuffledValue += random.choice(addSub)
            # Wrap numbers if needed
            if self._intsInPrice[idx]._shuffledValue < 0:
                self._intsInPrice[idx]._shuffledValue = 9
            if self._intsInPrice[idx]._shuffledValue > 9:
                self._intsInPrice[idx]._shuffledValue = 0
            # Initialize the user guess to the shuffled values, this is what appears in the GUI    
            self._intsInPrice[idx]._userGuessValue = self._intsInPrice[idx]._shuffledValue
                
                
        # Declare that it is the first turn
        self._numTurns = 1
                
        if debug == True:
            for itm in self._intsInPrice:    
                print(itm._orgValue)
            print('---------')
            for itm in self._intsInPrice:
                print(itm)
                
                
    def getNumsRight(self):
        return self._numsRight
    
    def getWins(self):
        return self._Win
            
    def incNum(self, idx):
        self._intsInPrice[idx].incNum()
        
    def decNum(self, idx):
        self._intsInPrice[idx].decNum()
            
    def endTurn(self):
        '''Performs all the necessary actions and return whether the user won or not. No return means
        the game is still running
        '''
        # Reset the numbers right to 0
        self._numsRight = 0
        
        # Check how many numbers the user has right
        for idx in range(len(self._intsInPrice)):
            if self._intsInPrice[idx]._userGuessValue == self._intsInPrice[idx]._orgValue:
                self._numsRight += 1
        # If it is all of then, end the game and return victory        
        if self._numsRight == len(self._intsInPrice):
            self._gameOver = True
            return True
        # If the user failed twice, this will end the game and declare defeat
        if self._numTurns ==2:
            self._gameOver = True
            return False
        # Increment the turn, only once will this actually run     
        self._numTurns += 1
        
        # Store the previous guess as a string to remind the user what they guessed
        self._previousGuess = ''
        for idx in range(len(self._intsInPrice)):
            self._previousGuess += str(self._intsInPrice[idx]._userGuessValue) + ' '
        print(self._previousGuess)
        
        # Resets the guess value to the shuffle value and allows editing
        for idx in range(len(self._intsInPrice)):
            self._intsInPrice[idx]._userGuessValue = self._intsInPrice[idx]._shuffledValue
            self._intsInPrice[idx]._wasChanged = False
        
        
        

class OneAwayNum:
    
    def __init__(self, val):
        # Each number should have an original (correct) value, what it was shuffled to,
        # what the user guessed it was, and whether it was changed
        self._orgValue = val
        self._shuffledValue = val
        self._userGuessValue = val
        self._wasChanged = False
        
    def getOrgValue(self):
        return str(self._orgValue)
    
    def getShuffledValue(self):
        return str(self._shuffledValue)
    
    def __str__(self):
        return str(self._userGuessValue)
    
    def incNum(self):
        '''Increases the number and prevents another change until turn is ended
           Return new value to be placed in StringVar'''
        if self._wasChanged == False:
            self._userGuessValue += 1
            if self._userGuessValue > 9:
                self._userGuessValue = 0
                
            self._wasChanged = True
            
        return self._userGuessValue
    
    def decNum(self):
        '''Decreases the number and prevents another change until turn is ended
           Return new value to be placed in StringVar'''
        if self._wasChanged == False:
            self._userGuessValue -= 1
            if self._userGuessValue < 0:
                self._userGuessValue = 9
                
            self._wasChanged = True
        return self._userGuessValue
    
        
    def __eq__(self, other):
        '''Sets equality to be original value'''
        return self._orgValue == other._orgValue
        
if __name__ == '__main__':
    test = Product(True, 'Pizza', 999000.20)
    game = OneAway(test, True)
        
    