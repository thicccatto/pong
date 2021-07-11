import pygame
from random import randint
from pong import Ball, Paddle, PongEngine
        

pong = PongEngine((700, 500), (10,10), (10, 100), 10, 10)
while not pong.exit_code:
    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
              pong.exit_code = True
        elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x: 
                     pong.exit_code = True
 
    
    pong.move_paddle(pong.paddleA)
    pong.move_paddle(pong.paddleB)
    
    pong.all_sprites_list.update()
    
    pong.check_ball(pong.paddleA, pong.paddleB)
    
    pong.draw()
     
    pong.clock.tick(60)
 
pygame.quit()