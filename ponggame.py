import pygame
pygame.init()

width, height = 800,600
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Ping Pong")

fps = 60

white = (255,255,255)
black = (0,0,0)
pink = (244,194,194)
teal = (0,255,255)
lavender = (152,115,172)

pheight, pwidth = 100,20

ballrad = 7

scorefont = pygame.font.SysFont("comicsans", 30)

winningscore = 10

class Paddle:
    color = lavender #attributes
    velocity = 5

    def __init__(self, x, y, width, height): #what a paddle is
        self.x = self.originalx =  x
        self.y = self.originaly = y
        self.width = width
        self.height = height
    
    def draw(self, win): #drawing a rectangle 
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
    
    def move(self, up=True): 
        if up:
            self.y -= self.velocity
        else:
            self.y += self.velocity      
    def reset(self):
        self.x = self.originalx
        self.y = self.originaly

class Ball:
    maxvel = 6
    color = lavender

    def __init__(self, x, y, radius):
        self.x = self.originalx = x
        self.y = self.originaly = y
        self.radius = radius
        self.xvel = self.maxvel
        self.yvel = 0

    def draw(self,win): 
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
    
    def move(self):
        self.x += self.xvel
        self.y += self.yvel
    
    def reset(self):
        self.x = self.originalx
        self.y = self.originaly
        self.yvel = 0
        self.xvel *= -1


def draw(win, paddles, ball, lscore, rscore):
    win.fill(pink)

    lscoretext = scorefont.render(f"{lscore}", 1, lavender)
    rscoretext = scorefont.render(f"{rscore}", 1, lavender)
   

    win.blit(lscoretext, (width//4 - lscoretext.get_width()//2, 20)) #put the scores here
    win.blit(rscoretext, (width* (3/4) - rscoretext.get_width()//2, 20))

    for paddle in paddles: #call the draw for paddles
        paddle.draw(win)

    for i in range(10, height, height//20): #supposed to be  adash line - not sure why its a line
        if i %2 == 1:
            continue
        pygame.draw.rect(win, lavender, (width//2 - 5, i, 10, height//20))
    
    ball.draw(win)
    pygame.display.update()

def paddlemove(keys,lpaddle, rpaddle):
    if keys[pygame.K_w] and lpaddle.y - lpaddle.velocity >= 0:
        lpaddle.move(up=True)
    if keys[pygame.K_s] and lpaddle.y + lpaddle.velocity +lpaddle.height <= height:
        lpaddle.move(up=False)
    if keys[pygame.K_UP] and rpaddle.y - rpaddle.velocity >= 0:
        rpaddle.move(up=True)
    if keys[pygame.K_DOWN] and rpaddle.y + rpaddle.velocity +rpaddle.height <= height:
        rpaddle.move(up=False)

def collision(ball, lpaddle, rpaddle): 
    if ball.y + ball.radius >= height:
        ball.yvel *= -1
    elif ball.y- ball.radius <= 0:
        ball.yvel *= -1
    
    if ball.xvel < 0:
        if ball.y >= lpaddle.y and ball.y <= lpaddle.y + lpaddle.height:
            if ball.x - ball.radius <= lpaddle.x + lpaddle.width:
                ball.xvel *= -1 

                middley = lpaddle.y + lpaddle.height / 2
                diffy = middley - ball.y
                rfactor = (lpaddle.height/2)/ball.maxvel
                yvel = diffy/rfactor
                ball.yvel = -1 * yvel
    else:
        if ball.y >= rpaddle.y and ball.y <= rpaddle.y + rpaddle.height:
            if ball.x + ball.radius >= rpaddle.x:
                ball.xvel *= -1
                middley = rpaddle.y + rpaddle.height / 2
                diffy = middley - ball.y
                rfactor = (rpaddle.height/2)/ball.maxvel
                yvel = diffy/rfactor
                ball.yvel = -1 * yvel



def main():
    action = True 
    clock = pygame.time.Clock()

    lpaddle = Paddle(10,height//2 - pheight//2, pwidth, pheight) #dimensions
    rpaddle = Paddle(width - 10 - pwidth,height//2 - pheight//2, pwidth, pheight)

    ball = Ball(width//2, height//2, ballrad) #dimensions

    lscore = 0 #set score
    rscore = 0
   
    while action:
        clock.tick(fps)
        draw(win,[lpaddle,rpaddle], ball, lscore, rscore)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                action = False
                break
        
        keys = pygame.key.get_pressed()
        paddlemove(keys, lpaddle, rpaddle)

        ball.move()
        collision(ball,lpaddle,rpaddle)

        if ball.x < 0:
            rscore += 1
            ball.reset()
        elif ball.x > width:
            lscore += 1
            ball.reset()

        won = False

        if lscore >= winningscore:
            won = True 
            win_text =  "Left player won"

        elif rscore>= winningscore:
            won = True
            win_text = "Right player won"

        if won:
            text = scorefont.render(win_text, 1, lavender)
            win.blit(text, (width//2 - text.get_width()//2, height//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            lpaddle.reset()
            rpaddle.reset()
            lscore = 0
            rscore = 0
            pygame.quit

if __name__ == '__main__':
    main()


