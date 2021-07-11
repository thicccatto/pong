import pygame
from random import randint

BLACK = (0,0,0)
 
class Paddle(pygame.sprite.Sprite):
    
    
    def __init__(self, color, width, height, upkey, downkey, isAI):
        
        super().__init__()
        
        
        self.isAI = isAI
        self.upkey = upkey
        self.downkey = downkey
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
 
        
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        
        
        self.rect = self.image.get_rect()
        
    def moveUp(self, pixels):
        self.rect.y -= pixels
        
        if self.rect.y < 0:
          self.rect.y = 0
          
    def moveDown(self, pixels):
        self.rect.y += pixels
        
        if self.rect.y > 400:
          self.rect.y = 400
          
class Ball(pygame.sprite.Sprite):
    
    
    def __init__(self, color, width, height):
        
        super().__init__()
        
        
        
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
 
        self.location_log = [(345,195)] * 10
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        
        self.velocity = [randint(4,8), 0]
        
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        
        self.location_log.append((self.rect.x, self.rect.y))
        
        self.location_log.pop(0)

          
    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8,8)

class PongEngine(Ball, Paddle):
    
    def __init__(self, size, ball_size, paddle_size, paddle_pad, difficulty):
        
        pygame.init()
        
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        
        self.ball_size = ball_size
        self.paddle_size = paddle_size
        
        self.size = size
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Pong")
        
        self.exit_code = False
        self.clock = pygame.time.Clock()
        self.all_sprites_list = pygame.sprite.Group()

        self.difficulty_max = 10
        self.difficulty_min = 0
        self.difficulty_range = self.difficulty_max - self.difficulty_min
        
        self.difficulty = difficulty
        
        if not self.difficulty_min <= difficulty <= self.difficulty_max:
            raise ValueError("difficulty must be from {0} - {1}".format(self.difficulty_min, self.difficulty_max))
        
        self.scoreA = 0
        self.scoreB = 0
        
        self.paddleA = self.spawn_paddle(paddle_pad, (size[1]-paddle_size[1])/2, pygame.K_w, pygame.K_s, False)
        self.paddleB = self.spawn_paddle(size[0] - paddle_size[0] - paddle_pad, (size[1]-paddle_size[1])/2, pygame.K_UP, pygame.K_DOWN, True)
        self.ball = self.spawn_ball()
        
        
        
    def spawn_ball(self):
        ball = Ball(self.WHITE,self.ball_size[0],self.ball_size[1])
        ball.rect.x = self.size[0] / 2 - self.ball_size[0] / 2
        ball.rect.y = self.size[1] / 2 - self.ball_size[1] / 2
        self.all_sprites_list.add(ball)

        return ball


    def spawn_paddle(self, x, y, upkey, downkey, isAI):
        paddle = Paddle(self.WHITE, self.paddle_size[0], self.paddle_size[1], upkey, downkey, isAI)
        paddle.rect.x = x
        paddle.rect.y = y
        self.all_sprites_list.add(paddle)
        
        return paddle
        

    def ai_move_paddle(self, paddle):
        
        delay = 10 - self.difficulty
        
        ball_offset = self.ball.location_log[delay][1] - paddle.rect.y - 50 + 5
        
        print(ball_offset)
        if ball_offset > randint(0, self.difficulty_range - self.difficulty) * 2: 
            if ball_offset < self.difficulty:
                paddle.moveDown(ball_offset)
            else:
                paddle.moveDown(self.difficulty)
        
        if ball_offset < randint(self.difficulty - self.difficulty_range, 0) * 2:
            if ball_offset < self.difficulty:
                paddle.moveDown(ball_offset)
            else:
                paddle.moveDown(self.difficulty)
        
    def move_paddle(self, paddle):
        
        if paddle.isAI:
            
            self.ai_move_paddle(paddle)
            
        else:
            keys = pygame.key.get_pressed()
            if keys[paddle.upkey]: paddle.moveUp(5)
            if keys[paddle.downkey]: paddle.moveDown(5)

    def check_ball(self, *args):
        
        if self.ball.rect.x>=690:
            self.scoreA+=1
            self.all_sprites_list.remove(self.ball)
            self.ball = self.spawn_ball()
            
        if self.ball.rect.x<=0:
            self.scoreB+=1
            self.all_sprites_list.remove(self.ball)
            self.ball = self.spawn_ball()
            
        if self.ball.rect.y>490:
            self.ball.velocity[1] = -self.ball.velocity[1]
        if self.ball.rect.y<0:
            self.ball.velocity[1] = -self.ball.velocity[1]
            
        for paddle in args:
            if pygame.sprite.collide_mask(self.ball, paddle):
                self.ball.bounce()
                break 
    
    def draw(self):
        
        self.screen.fill(self.BLACK)
    
        pygame.draw.line(self.screen, self.WHITE, [self.size[0]/2 - 1, 0], [self.size[0]/2 - 1, self.size[1]], 5)
    
        self.all_sprites_list.draw(self.screen) 
    
        font = pygame.font.Font(None, 74)
        text = font.render(str(self.scoreA), 1, self.WHITE)
        self.screen.blit(text, (250,10))
        text = font.render(str(self.scoreB), 1, self.WHITE)
        self.screen.blit(text, (420,10))
 
        pygame.display.flip()