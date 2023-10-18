import pygame
pygame.init()

# creates the game window
win = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Noughts and Crosses")

# box object
class box():
    # initialisation
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.nought = False
        self.cross = False

    # drawing itself (whether blank, with a O, or with an X)
    def drawSelf(self):
        pygame.draw.rect(win, (62, 180, 137), (self.x_pos, self.y_pos, 100, 100), 3)
        pygame.draw.rect(win, (255, 255, 255), (self.x_pos, self.y_pos, 100, 100), 0)
        if self.nought:
            pygame.draw.circle(win, (62, 180, 137), (self.x_pos + 50, self.y_pos + 50), 40, 3)
        elif self.cross:
            pygame.draw.line(win, (62, 180, 137), (self.x_pos + 15, self.y_pos + 15), (self.x_pos + 85, self.y_pos + 85), 4)
            pygame.draw.line(win, (62, 180, 137), (self.x_pos + 85, self.y_pos + 15), (self.x_pos + 15, self.y_pos + 85), 4)

    # checking whether it has been clicked, and if so by whom
    def checkClick(self, mouse_x, mouse_y, noughts, crosses):
        if mouse_x >= self.x_pos and mouse_x <= self.x_pos + 100 and mouse_y >= self.y_pos and mouse_y <= self.y_pos + 100:
            if noughts and not self.cross:
                self.nought = True
                return "Noughts"
            elif crosses and not self.nought:
                self.cross = True
                return "Crosses"
            else:
                return "No player"

# player object
class player():
    # initialisation
    def __init__(self, name, playing):
        self.name = name
        self.playing = playing
        self.boxesClicked = []
        self.winner = False

    # checking if the player has won
    def checkWon(self):
        array = self.boxesClicked
        if array.count(0) == 1:
            if array.count(1) == 1 and array.count(2) == 1:
                self.winner = True
            elif array.count(3) == 1 and array.count(6) == 1:
                self.winner = True
            elif array.count(4) == 1 and array.count(8) == 1:
                self.winner = True

        if array.count(2) == 1:
            if array.count(5) == 1 and array.count(8) == 1:
                self.winner = True
            elif array.count(4) == 1 and array.count(6) == 1:
                self.winner = True

        if array.count(4) == 1:
            if array.count(1) == 1 and array.count(7) == 1:
                self.winner = True
            elif array.count(3) == 1 and array.count(5) == 1:
                self.winner = True

        if array.count(6) == 1 and array.count(7) == 1 and array.count(8) == 1:
            self.winner = True

    # updating the array of the boxes the player has clicked
    def setClickedBoxes(self, boxes):
        self.boxesClicked = []
        for i in range(0, 9):
            if self.name == "Noughts" and boxes[i].nought:
                self.boxesClicked.append(i)
            elif self.name == "Crosses" and boxes[i].cross:
                self.boxesClicked.append(i)


# drawing the game window
def gameWindow(boxes, noughts, crosses):
    # giving the game window a pastel green background
    win.fill((209, 255, 224))

    # displaying the game title
    font = pygame.font.SysFont("Arial", 30)
    text = font.render("Katie's Noughts And Crosses Game", 1, (62, 180, 137))
    win.blit(text, (300, 60))
    
    # checking who is playing/who won/if there was a draw
    if noughts.playing:
        text = font.render("O's turn", 1, (62, 180, 137))
        win.blit(text, (450, 150))
    elif crosses.playing:
        text = font.render("X's turn", 1, (62, 180, 137))
        win.blit(text, (450, 150))
    elif noughts.winner:
        text = font.render("O wins", 1, (62, 180, 137))
        win.blit(text, (460, 150))
    elif crosses.winner:
        text = font.render("X wins", 1, (62, 180, 137))
        win.blit(text, (460, 150))
    elif not crosses.winner and not noughts.winner:
        text = font.render("Draw", 1, (62, 180, 137))
        win.blit(text, (470, 150))

    # displaying each of the boxes
    for box in boxes:
        box.drawSelf()

# initialising variables
run = True
boxes = [box(345, 200), box(450, 200), box(555, 200), box(345, 305), box(450, 305), box(555, 305), box(345, 410), box(450, 410), box(555, 410)]
noughts = player("Noughts", True)
crosses = player("Crosses", False)
mouse_x = 0
mouse_y = 0
gameOver = False

# main game loop
while run:

    pygame.time.delay(100)

    for event in pygame.event.get():

        # checking if user has exited the game
        if event.type == pygame.QUIT:
            run = False
            pygame.display.quit()
            pygame.quit()

        # checking if the mouse has been clicked (only if there isn't currently a winner/draw)
        if event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
            mouse_pos = pygame.mouse.get_pos()
            mouse_x = mouse_pos[0]
            mouse_y = mouse_pos[1]
            
            
            # checking if the user has clicked a box and if that makes them a winner/makes a draw 
            clickedCounter = 0
            for box in boxes:
                player = box.checkClick(mouse_x, mouse_y, noughts.playing, crosses.playing)
                if player == "Noughts":
                    noughts.setClickedBoxes(boxes)
                    noughts.checkWon()
                    noughts.playing = False
                    crosses.playing = True
                elif player == "Crosses":
                    crosses.setClickedBoxes(boxes)
                    crosses.checkWon()
                    crosses.playing = False
                    noughts.playing = True

                if box.nought or box.cross:
                    clickedCounter = clickedCounter + 1
  
            if noughts.winner or crosses.winner or clickedCounter == 9:
                noughts.playing = False
                crosses.playing = False
                gameOver = True

    # updating the game window
    if run:
        player = gameWindow(boxes, noughts, crosses)
        pygame.display.update()
