#Создай собственный Шутер!
from pygame import *
from random import randint

lost = 0
win = 0
bullets = sprite.Group()
life = 3
num_fire = 0
rel_time = False

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_weight, player_height,  player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_weight, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width -85:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 5:
            self.kill()

class Asteroid(GameSprite):
     def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

win_width = 700
win_height = 500
player_speed = 10
window = display.set_mode((win_width,win_height))

display.set_caption('Shooter Game')
background = transform.scale(image.load('galaxy.jpg'),(win_width,win_height))
player = Player('rocket.png', 350, 420, 70, 90, player_speed)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png',randint(0,500),0,70,50,randint(1,2))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid('asteroid.png',randint(0,500),0,70,80,randint(2,3))
    asteroids.add(asteroid)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

bullet2 = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial',40)


font2 = font.SysFont('Arial',82)
loser = font2.render('YOU LOSE!', True, (205, 0, 0))
winner = font2.render('YOU WIN!', True, (255, 215, 0))

finish = False
run = True
clock = time.Clock()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                bullet2.play()
                player.fire()

    if finish != True:
        text_life = font2.render(str(life),1,(255,255,255))
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        text_win = font1.render('Счет:' + str(win), 1, (255, 255, 255))

        window.blit(background,(0,0))
        window.blit(text_lose,(10,46))
        window.blit(text_win,(10,10))
        window.blit(text_life,(650,10))

        sprites_list = sprite.spritecollide(player, monsters, False)
        sprites_list2 = sprite.groupcollide(monsters, bullets, True, True)
        sprites_list3 = sprite.spritecollide(player, asteroids, False)

        player.update()
        player.reset()

        monsters.draw(window)
        monsters.update()

        asteroids.draw(window)
        asteroids.update() 

        bullets.draw(window)
        bullets.update()


    if sprites_list:
        window.blit(loser,(200,200))
        life -= 1
        if life == 0 or lost >= 6:
            finish = True

    if sprites_list2:
        win += 1
        monster = Enemy('ufo.png',randint(0,500),0,70,50,randint(1,2))
        monsters.add(monster)

    if sprites_list3:
        life -= 1
        if life == 0 or lost >= 6:
            window.blit(loser,(200,200))
            finish = True

    if win >= 20:
        window.blit(winner,(200,200))
        finish = True

    display.update()
    clock.tick(60)
