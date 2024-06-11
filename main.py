from board import Board
from button import Button
import pygame

size = width, height = 800, 900

board = Board(position=(100,150),size=600,padding=20) # default: english version
button = Button('New game', (250,785),(300,80))
button.add_option('English version', board.reset_board,'english')
button.add_option('French version', board.reset_board,'french')

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Peg Solitaire')

clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.SysFont('Arial',80)
button_font = pygame.font.SysFont('Arial',30)
text = ''
text_pos = (width//2,75)


running = True
game_status = 0    
# 0 -> playing
# -1 -> game over (lost)
# 1 -> won

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not button.is_open():
                if event.button == 1:
                    board.pick(event.pos)
            else:
                button.click(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                board.release(event.pos)
    
    game_status = board.check_game_status()
    if game_status == 1:
        text = 'YOU WIN'
    elif game_status == -1:
        text = 'GAME OVER'
    else:
        text = ''

    screen.fill([10]*3)

    text_render = font.render(text, False, (255,255,255))
    dx, dy = text_render.get_rect().width//2, text_render.get_rect().height//2
    
    board.show(screen, pygame.mouse.get_pos(),game_status)
    screen.blit(text_render, (text_pos[0]-dx, text_pos[1]-dy))

    button.update(pygame.mouse.get_pos())
    button.show(screen,button_font)

    pygame.display.update()
    clock.tick(60)

pygame.quit()