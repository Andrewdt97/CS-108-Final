'''Game that takes a totally random item off of eBay and implements various minigames from The Price is Right on them
Created Fall 2016
CS 108 Final Project
@author: Andrew Thomas (adt8)
'''

from tkinter import * # TkInter used for GUI
from OneAway import * # One of the games used
from RangeGame import * # Another game used
from Product import * # Product class that stores the values from eBay items
import PIL.Image # Image processing library called Pillow (a fork of PIL) used to created an image from the URL data
from PIL import ImageTk # Takes PIL.Image and creates an image object that can be displayed by TkInter
import io # Encoding package to encode the data from the image URL to be read by PIL.Image
import requests # 3rd party package to open image URLs is a way they can be encoded
import math # Used for various math functions

class App:
    
    def __init__(self, window, game=None, id = None):
        self.window = window
        self.window.title('The Price is Right')
        
        # By default and when a new game is started, game == None and the selection menu will run
        if game == None:
            '''Game selection menu'''
            # _gameSelect will be the game variable passed in the next time the app is created
            # Various radio buttons set _gameSelect
            self._gameSelect = StringVar()
            Label(text='Please select the game you wish to play:', anchor=N).pack()
            Radiobutton(window, text='One Away', variable=self._gameSelect, value='One Away').pack()
            Radiobutton(window, text='Range Game', variable=self._gameSelect, value='RangeGame').pack()
            
            # Confirm recreates the app with _gameSelect passed into the game parameter
            Button(text='Confirm', command=lambda: self.startGame(self._gameSelect.get())).pack()
            Button(text='Quit', command=self.quit).pack()
            
            Label(window, text='For instructions and other important information\nsee README.txt').pack()
            
        # If the app is recreated with One Away selected, the following code will run    
        if game == 'One Away':
            '''Setup'''
            # Initialize a product, this can take several minutes. See the Product module for more information
            self.item = Product(id=id)
            # Creates an instance of the One Away class with the item just created. See the One Away module for more information
            self.game = OneAway(self.item)
            
            Label(window, text='One Away', font=('Impact', 24)).grid(row=0, column=0)
            
            self.drawItemWindow()
            
            self.gameFrame = Frame(self.window)
            self.gameFrame.grid(row=0, column=1, rowspan=2, sticky=N)
            
            '''Main GUI'''
            numInColumn = 0
            self._priceNums =[] # List containing number objects found in One Aaway
            for idx in range(len(self.game._intsInPrice)):
                # For each number in the price, created a StringVar and set it to the shuffled price
                self._priceNums.append(StringVar())
                self._priceNums[idx].set(self.game._intsInPrice[idx].getShuffledValue())
                
                # Create buttons for each number to increase and decrease them
                # Lambda expression is used to allow each button to input a parameter into the function call
                Button(self.gameFrame, text='^', command=lambda idx=idx: self.incNum(idx)).grid(row=0, column=numInColumn)
                Label(self.gameFrame, textvariable=self._priceNums[idx]).grid(row=1, column=numInColumn)
                Button(self.gameFrame, text='v', command=lambda idx=idx: self.decNum(idx)).grid(row=2, column=numInColumn)
                # Change the column each loop so things are not putting on top of eachother
                numInColumn += 1
            
            # Set up StringVar to display numbers right    
            self._displayNumsRight = StringVar()
            self._displayNumsRight.set('Numbers right: 0')
            Label(self.gameFrame, textvariable=self._displayNumsRight).grid(row=3, column=0, columnspan=5, stick=W)
            
            # Get the previous guess and display it to the user. Will start blank.
            self._previousGuess = StringVar()
            self._previousGuess.set('')
            Label(self.gameFrame, textvariable=self._previousGuess).grid(row=4,column=0, columnspan=3, sticky=W)
            
            # StringVar to tell the user if they won or not
            self._didYouWin = StringVar()
            self._didYouWin.set('')
            Label(self.gameFrame, textvariable=self._didYouWin).grid(row=5, column=0, columnspan=20)
            
            
            # Button to enter a guess    
            self._enterPriceButton = Button(self.gameFrame, text='Enter Price', command=self.checkNums)
            self._enterPriceButton.grid(row=5, column=0, columnspan=4, sticky=W)
            
            
            # New Game and Quit buttons
            Button(self.gameFrame, text='New Game', command=self.newGame).grid(row=6, column=0, columnspan=4, sticky=W)
            Button(self.gameFrame, text='Quit', command=self.quit).grid(row=7, column=0)
    
    
        if game == 'RangeGame':
            '''Setup'''
            self.item = Product(id=id)
                
            self.game = RangeGame(self.item)
                      
            Label(self.window, text='Range Game', font=('Impact', 24)).grid(row=0, column=0, sticky = N)
            
            self.drawItemWindow()

            self.gameFrame = Frame(self.window)
            self.gameFrame.grid(row=0, column=1, rowspan=2, sticky=N)
            
            '''Main GUI'''
            # _scaleModifer increases by 1 each tick up to 150 which is the point
            # where the guess range will hit the top. _rangeGameRunning will be used in rangeGameMainLoop
            self._scaleModifier = 0
            self._rangeGameRunning = True
            
            # Canvas containing scale and function call to draw on it
            self._scaleCanvas = Canvas(self.gameFrame, height=700, width=250)
            self.drawScale()
            self._scaleCanvas.grid(row=0, column=0, rowspan=5)
            
            # Buttons to perform commands
            Button(self.gameFrame, text='Start', command=self.RangeGameMainLoop, font=('Times', 30),).grid(row=1, column=1, sticky=W)
            Button(self.gameFrame, text='Stop', command=self.RangeGameStop, font=('Times', 30)).grid(row=2, column=1, sticky=W)
            Button(self.gameFrame, text='New Game', command=self.newGame).grid(row=5, column=0, sticky=N)
            Button(self.gameFrame, text='Quit', command=self.quit).grid(row=5, column=1)        
            
            # Label telling user their victory status
            self._didYouWin = StringVar()
            Label(self.gameFrame, textvariable=self._didYouWin).grid(row=3, column=1, columnspan=2)
            self._didYouWin.set('')
    
    def drawItemWindow(self):
        '''Draws the window that contains the item title and picture'''
        # Creates a fram to hold information
        self.itemFrame = Frame(self.window)
        self.itemFrame.grid(row=1, column=0, sticky=N)
        
        # Puts the title of the item in the frame
        Label(self.itemFrame, text=self.item.getTitle(), font=('Times', 15)).pack()
        
        # Opens the URL
        self._imgData = requests.get(self.item._imgURL)
        # Creates an image file with the encoding (io.BytesIO) of the _imgData
        self._imgFile = PIL.Image.open(io.BytesIO(self._imgData.content))
        # Takes that image and makes it an image TKinter can use
        self._img = ImageTk.PhotoImage(self._imgFile)
        # Puts a label in the frame that displays the image
        Label(self.itemFrame, image=self._img).pack()
        
    def startGame(self, gameSelect):
        '''Restarts the program with the selected game run'''
        global game
        game = gameSelect
        
        self.window.destroy() 
        
    def newGame(self):
        '''Returns to the game selection menu'''
        global game
        game = None
        
        self.window.destroy()
    
    def quit(self):
        '''Terminates the while loop in the main code and closes windows'''
        global keepGoing
        keepGoing = False
        self.window.quit()
    
    '''The following methods are used for the One Away game'''
            
    def checkNums(self):
        '''Runs end turns commands, returns whether the user won or lost,
        and if the game it not over, resets StringVars'''
        if self.game._gameOver == False:
            # Runs the end turn function in the game class
            self._gameResult = self.game.endTurn()
            
            # Updates the number right and the victory status
            self._displayNumsRight.set('Numbers right: ' + str(self.game.getNumsRight()))
            if self._gameResult == True:
                self._enterPriceButton.grid_forget()
                self._didYouWin.set('Congratulations, you won! Please start a new game.')
                return None
            elif self._gameResult == False:
                self._didYouWin.set('Sorry, you did not guess the correct price.The correct price was ' + str(self.item._price)[:-2])
                self._enterPriceButton.grid_forget()
                return None
           
            # Displays the user's previous guess to help remind them
            self._previousGuess.set('Previous guess: ' + self.game._previousGuess)   
             
    
            # Resets all the numbers in the GUI only if the game is not over
            for idx in range(len(self._priceNums)):
                self._priceNums[idx].set(self.game._intsInPrice[idx]._shuffledValue)
            
            
    def incNum(self, idx):
        '''Increase the number at index by running the namesake function in the OneAwayNum class'''
        if self.game._gameOver == False:
            self._priceNums[idx].set(self.game._intsInPrice[idx].incNum())
        
    def decNum(self, idx):
        '''Decreases the number at index by runing the namesake function in the OneAwayNum class'''
        if self.game._gameOver == False:
            self._priceNums[idx].set(self.game._intsInPrice[idx].decNum())
     
     
            
    '''The following methods are used for the Range Game'''
            
            
    def drawScale(self):
        '''Draws the scale based on the _scaleModifier variable'''
        # Clears the canvas, required for any sort of animation
        self._scaleCanvas.delete('all')
        # Background rectangle
        backgroundScale = self._scaleCanvas.create_rectangle(50, 50, 151, 651)
        
        # Red, guess range rectangle. It goes up as the _scaleModifer increases.
        guessScale = self._scaleCanvas.create_rectangle(50, 500-(self._scaleModifier * 3), 151, 651-(self._scaleModifier * 3), fill='red')
        
        # Price text at bottom of guess rectangle
        self._bottomGuessPrice = self.game.getBoardRangeStart() + (((0.005*self._scaleModifier)*self.game.getPriceRange()))
        self._scaleCanvas.create_text(190, 650-(self._scaleModifier * 3), text='$%.2f' % self._bottomGuessPrice)
        
        # Price text at the top of the guess rectangle
        self._topGuessPrice = self._bottomGuessPrice + self.game.getGuessRange()
        self._scaleCanvas.create_text(190, 500-(self._scaleModifier *3), text=("$%.2f" % self._topGuessPrice))
        
        # Price text at the bottom and top of the whole range (black rectangle)
        self._scaleCanvas.create_text(190, 650, text='$%.2f' % self.game.getBoardRangeStart())
        self._scaleCanvas.create_text(190, 40, text='$%.2f' % (self.game.getBoardRangeStart()+self.game.getPriceRange()))
        
        
    def RangeGameMainLoop(self):
        '''Increases _scaleModifier causing the guess range to rise when drawScale is called'''
        while self._rangeGameRunning:
            self.drawScale()
            self._scaleModifier += 1
            
            # If it reaches the top, end the game. False parameter means the game cannot be won
            if self._scaleModifier > 150:
                self.RangeGameStop(False)
            # Makes the guess range move slowly up rather than jumping
            self._scaleCanvas.after(125)
            self._scaleCanvas.update()
            
            
    def RangeGameStop(self, canWin=True):
        '''Ends game either via stop button or guess range reaching top of scale'''
        self._rangeGameRunning = False
        if canWin:
            # Check is item._price is within the guess range
            if self.item.getPrice() <= self._topGuessPrice and self.item.getPrice() >= self._bottomGuessPrice:
                self._didYouWin.set('Congratulations! You won!\nThe price was: $' + str(self.item._price))
            else: # Runs if the user guessed wrong
                self._didYouWin.set('Sorry, the price was:\n$%.2f' % self.item._price)
        else: # Runs if the scale reached the top without being stopped
            self._didYouWin.set('Sorry, the price was:\n$%.2f' % self.item._price)
        
        
    
    
        
        

if __name__=='__main__':
    # game is set to know, which means the selection menu will run
    # keepGoing is set to True, which allows for new creations of windows as long as 'Quit' is not pressed
    game = None
    keepGoing = True
    while keepGoing:
        root = Tk()     
        root.title('The Price is Right')  
        app = App(root, game)
        root.mainloop()