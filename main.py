import pygame
import os
pygame.font.init()
pygame.mixer.init()

# create window
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# rectangle shape for window halfway point
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# fonts
HEALTH_FONT = pygame.font.SysFont('SegoeUI', 35)
WINNER_FONT = pygame.font.SysFont('SegoeUI', 100)

# vars
FPS = 60
VEL = 5
AMMO_VEL = 7
MAX_AMMO = 3

#
CHRIS_HIT = pygame.USEREVENT + 1
WILL_HIT = pygame.USEREVENT + 2

# images
HEAD_WIDTH, HEAD_HEIGHT = 60, 80
CHRIS_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Oscars', 'chris head.png')), (HEAD_WIDTH, HEAD_HEIGHT))
CHRIS_HIT_IMAGE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Oscars', 'chris hit.png')), (HEAD_WIDTH+15, HEAD_HEIGHT-5)), -40)
WILL_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Oscars', 'will head.png')), (HEAD_WIDTH, HEAD_HEIGHT))
WILL_HIT_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Oscars', 'will hit.png')), (HEAD_WIDTH, HEAD_HEIGHT))
OSCARS_BG_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Oscars', 'oscars bg.png')), (WIDTH, HEIGHT))

MIC_IMAGE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Oscars', 'microphone.png')), (35, 35)), -45)
HAND_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Oscars', 'hand.png')), (35, 35))

# sounds
MIC_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Oscars', 'chris fire.mp3'))
HAND_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Oscars', 'will fire.mp3'))

CHRIS_HIT_SOUND = pygame.mixer.Sound(os.path.join('Oscars', 'chris hit.mp3'))
WILL_HIT_SOUND = pygame.mixer.Sound(os.path.join('Oscars', 'will hit.mp3'))

CHRIS_WIN_SOUND = pygame.mixer.Sound(os.path.join('Oscars', 'chris win.mp3'))
WILL_WIN_SOUND = pygame.mixer.Sound(os.path.join('Oscars', 'will win_2.mp3'))


def draw_window(chris, will, mics, hands, chris_health, will_health):
    WIN.blit(OSCARS_BG_IMAGE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    chris_health_text = HEALTH_FONT.render("Health " + str(chris_health), 1, WHITE)
    will_health_text = HEALTH_FONT.render("Health " + str(will_health), 1, WHITE)
    WIN.blit(chris_health_text, (10, 10))
    WIN.blit(will_health_text, (WIDTH - will_health_text.get_width() - 20, 20))

    WIN.blit(CHRIS_IMAGE, (chris.x, chris.y))
    WIN.blit(WILL_IMAGE, (will.x, will.y))
    for mic in mics:
        WIN.blit(MIC_IMAGE, (mic.x, mic.y))
    for hand in hands:
        WIN.blit(HAND_IMAGE, (hand.x, hand.y))

    pygame.display.update()

def chris_movement(key_pressed, chris):
    if key_pressed[pygame.K_a] and chris.x >= 0: # LEFT
        chris.x -= VEL
    if key_pressed[pygame.K_d] and chris.x + HEAD_WIDTH < BORDER.x: # RIGHT
        chris.x += VEL
    if key_pressed[pygame.K_w] and chris.y >= 0: # UP
        chris.y -= VEL
    if key_pressed[pygame.K_s] and chris.y + HEAD_HEIGHT <= HEIGHT: # DOWN
        chris.y += VEL

def will_movement(key_pressed, will):
    if key_pressed[pygame.K_LEFT] and will.x >= BORDER.x: # LEFT
        will.x -= VEL
    if key_pressed[pygame.K_RIGHT] and will.x + HEAD_WIDTH <= WIDTH: # RIGHT
        will.x += VEL
    if key_pressed[pygame.K_UP] and will.y >= 0: # UP
        will.y -= VEL
    if key_pressed[pygame.K_DOWN] and will.y + HEAD_HEIGHT <= HEIGHT: # DOWN
        will.y += VEL

def ammo_movement(mics, hands, chris, will):
    for mic in mics:
        mic.x += AMMO_VEL
        if will.colliderect(mic):
            pygame.event.post(pygame.event.Event(WILL_HIT))
            mics.remove(mic)
        elif mic.x > WIDTH:
            mics.remove(mic)
    for hand in hands:
        hand.x -= AMMO_VEL
        if chris.colliderect(hand):
            pygame.event.post(pygame.event.Event(CHRIS_HIT))
            hands.remove(hand)
        elif hand.x < 0:
            hands.remove(hand)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT//2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    chris = pygame.Rect(100, 300, HEAD_WIDTH, HEAD_HEIGHT)
    will = pygame.Rect(700, 300, HEAD_WIDTH, HEAD_HEIGHT)

    mics = []
    hands = []

    chris_health = 10
    will_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(mics) < MAX_AMMO:
                    mic = pygame.Rect(chris.x + chris.width, chris.y + chris.height//2 - 2, 10, 5)
                    mics.append(mic)
                    MIC_FIRE_SOUND.play()
                if event.key == pygame.K_RSHIFT and len(hands) < MAX_AMMO:
                    hand = pygame.Rect(will.x + will.width, will.y + will.height//2 - 2, 10, 5)
                    hands.append(hand)
                    HAND_FIRE_SOUND.play()
            if event.type == CHRIS_HIT:
                chris_health -= 1
                CHRIS_HIT_SOUND.play()
            if event.type == WILL_HIT:
                will_health -= 1
                WILL_HIT_SOUND.play()

        winner_text = ""
        if chris_health <= 0:
            WIN.blit(CHRIS_HIT_IMAGE, (chris.x - 24, chris.y - 15))
            pygame.display.update(chris)
            WILL_WIN_SOUND.play()
            winner_text = "Will Wins!"
        if will_health <= 0:
            WIN.blit(WILL_HIT_IMAGE, (will.x, will.y))
            pygame.display.update(will)
            CHRIS_WIN_SOUND.play()
            winner_text = "Chris Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        key_pressed = pygame.key.get_pressed()
        chris_movement(key_pressed, chris)
        will_movement(key_pressed, will)
        ammo_movement(mics,hands,chris,will)

        draw_window(chris, will, mics, hands, chris_health, will_health)
    main()

if __name__ == "__main__":
    main()
