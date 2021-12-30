import pygame 
import os
from pygame import draw 

pygame.font.init()
pygame.mixer.init()

HEIGHT,WIDTH = 600,900
SPACESHIP_WIDTH,SPACESHIP_HEIGHT = 55,40

BGCOLOR = (29, 16, 110) # rgb values of color 
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60

border = pygame.Rect(WIDTH/2-5,0,10,600)
HEALTH_TEXT = pygame.font.SysFont('DS-Digital',40)
WINNER_TEXT = pygame.font.SysFont('DS-Digital',100)


spaceshipSpeed = 4
bulletSpeed = 8
maxBullet = 5
yellowHit = pygame.USEREVENT + 1
redHit = pygame.USEREVENT+ 2

 # sound
HITSOUND =pygame.mixer.Sound(os.path.join('assets','Assets','Grenade.mp3' ))
FIRESOUND = pygame.mixer.Sound(os.path.join('assets','Assets','GunSilencer.mp3' ))



# making a window
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

# resizing image to fit in window
yellowSpaceshipImage = pygame.image.load(os.path.join('assets','Assets','spaceship_yellow.png' ))
yellowspaceship = pygame.transform.rotate(pygame.transform.scale(yellowSpaceshipImage,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)
redSpaceshipImage = pygame.image.load(os.path.join('assets','Assets','spaceship_red.png'))
redspaceship = pygame.transform.rotate(pygame.transform.scale(redSpaceshipImage,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),-90)


pygame.display.set_caption("Space War") # setting up title of the window


def drawWindow(red,yellow,yellowbullets,redbullets,red_health, yellow_health):
    WIN.fill((BGCOLOR))
    pygame.draw.rect(WIN,(0,0,0),border) # windows and color in rgb
    # to draw something on window or making a surface all things in pygame is surface so to make a surface use blit 
    WIN.blit(yellowspaceship,(yellow.x,yellow.y)) 
    WIN.blit(redspaceship,(red.x,red.y))
    
    red_health_text = HEALTH_TEXT.render('Health : '+str(red_health),1,RED)
    yellow_health_text = HEALTH_TEXT.render('Health : '+str(yellow_health),1,YELLOW)
    
    WIN.blit(red_health_text,(WIDTH-(red_health_text.get_width())-5,5))
    WIN.blit(yellow_health_text,(5,5))

    for bullet in redbullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellowbullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()

# handeling the movement of spaceship
#yellow ship 
def movementyellow(keysPressed,character):
    if keysPressed[pygame.K_d] and character.x < (WIDTH/2-SPACESHIP_WIDTH):
            character.x +=spaceshipSpeed
    if keysPressed[pygame.K_a] and character.x > 10:
            character.x -=spaceshipSpeed
    if keysPressed[pygame.K_w] and character.y > 10:
            character.y -=spaceshipSpeed
    if keysPressed[pygame.K_s] and character.y < (HEIGHT-SPACESHIP_HEIGHT-20):
            character.y +=spaceshipSpeed
# red ship  
def movementred(keysPressed,character):
    if keysPressed[pygame.K_RIGHT] and character.x < WIDTH-SPACESHIP_WIDTH-5:
        character.x +=spaceshipSpeed
    if keysPressed[pygame.K_LEFT] and character.x > (WIDTH/2 + 10):
        character.x -=spaceshipSpeed
    if keysPressed[pygame.K_UP] and character.y > 10:
        character.y -=spaceshipSpeed 
    if keysPressed[pygame.K_DOWN] and character.y < (HEIGHT-SPACESHIP_HEIGHT-20):
        character.y +=spaceshipSpeed

# handling the bullets movements and collision 
def handleBullets(firstBullet,secondBullet,first,second):
    for bullet in firstBullet:
        bullet.x += bulletSpeed
        if second.colliderect(bullet): # colliderect check if two rectangle colliding or not 
            pygame.event.post(pygame.event.Event(redHit))
            firstBullet.remove(bullet)
        elif bullet.x > WIDTH:
            firstBullet.remove(bullet)
    for bullet in secondBullet:
        bullet.x -= bulletSpeed
        if first.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellowHit))
            secondBullet.remove(bullet)

        elif bullet.x < 0:
            secondBullet.remove(bullet)

# Winner text
def drawWinner(text):
    drawText = WINNER_TEXT.render(text,1,RED)
    WIN.blit(drawText,(WIDTH/2-drawText.get_width()//2,HEIGHT/2-drawText.get_height()//2))
    pygame.time.delay(1000)
    pygame.display.update()
    pygame.time.delay(3000)

# main function 
def main():
    # as we can't move actual image surface we will create to rectangle to move images 
    # this will also use in checking the collision with bullets 
    red = pygame.Rect(700  ,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)

    redBullet = []
    yellowBullet = []
    yellow_health = 10
    red_health = 10 

    clock = pygame.time.Clock()
    run = True
    while run :
        clock.tick(FPS)
        for event in pygame.event.get(): # check for events 
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LCTRL and len(yellowBullet) < maxBullet:
                    bullet = pygame.Rect(yellow.x+SPACESHIP_WIDTH-5,yellow.y+SPACESHIP_HEIGHT//2,10,5)
                    FIRESOUND.play() 
                    yellowBullet.append(bullet)
                    
                    
                if event.key == pygame.K_RCTRL and len(redBullet) < maxBullet:
                    bullet = pygame.Rect(red.x,red.y+SPACESHIP_HEIGHT//2,10,5)
                    FIRESOUND.play()
                    redBullet.append(bullet)
            if event.type == redHit:
                HITSOUND.play()
                red_health = red_health - 1
                
            if event.type == yellowHit:
                HITSOUND.play()
                yellow_health = yellow_health -1
        winner = ''
        if red_health <= 0:
            winner = 'Yellow Wins !!!'

        if yellow_health <= 0:
            winner = 'Red Wins !!!'
        if winner != '':
            drawWinner(winner)
            break
                
            
        # checking for key pressed amd moving it  
        # yellow spaceship 
        keys_pressed = pygame.key.get_pressed()
        movementyellow(keys_pressed,yellow)
        # red spaceship
        movementred(keys_pressed,red)
        handleBullets(yellowBullet,redBullet,yellow,red)
            
        drawWindow(red,yellow,yellowBullet,redBullet,red_health,yellow_health) # instead of putting it before win.fill put all drawing stuff in order  
        pygame.display.update()  # Update the full display Surface to the screen
    main()

if __name__ == "__main__":
    main()





   