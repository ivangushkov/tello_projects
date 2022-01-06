import pygame


# We get the keypresses through pygame. Pygame is made for making games. Therefore to get the keypress we need a game window opened, which is what the init function does.
def init():
    pygame.init()
    win = pygame.display.set_mode((400, 400))


def getKey(keyName): # Checks if a key is being pressed by getting what key is being pressed and comparing it to the key to be checked keyName
    ans = False
    for eve in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(keyName))
    if keyInput[myKey]:
        ans = True
    pygame.display.update()
    return ans
    # returns: BOOL representing is keyName being pressed

def main():
    #print(getKey("a"))
    if getKey("LEFT"):
        print("Left key pressed")

    if getKey("RIGHT"):
        print("Right key pressed")

if __name__ == '__main__':
    init()
    while True:
        main()


