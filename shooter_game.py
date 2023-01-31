import pygame  
import sys
from random import randint
pygame.init()
pygame.mixer.init()
 
screen = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()
points = 0
fire_sound = pygame.mixer.Sound("fire.ogg")
pygame.mixer.music.load("space.ogg")
pygame.mixer.music.set_volume(0.1)
# ТЕКСТ
 
# Шрифт
shrift = pygame.font.SysFont('Times New Roman',30)
 
# Кол-во очков
a = shrift.render(str(points),False,(0,100,20))
 
 
# КАРТИНКИ И ХИТБОКСЫ
# Картинка фона
screen_textur = pygame.image.load('galaxy.jpg')
screen_textur = pygame.transform.scale(screen_textur, (500,500))
 
# Ракета
rocket = pygame.image.load("rocket.png")
rocket = pygame.transform.scale(rocket, (50, 50))
rocket_box = pygame.Rect(100, 430, 50, 50)
 
# Кнопка (начать игру)
 
start_bitton = pygame.image.load("start.png")
start_bitton = pygame.transform.scale(start_bitton, (200, 40))
start_bitton_box = pygame.Rect(150, 230, 150, 30)
 
# Пуля
bullet = pygame.image.load("bullet.png")
bullet = pygame.transform.scale(bullet, (10, 20))
bullets = []
 
# НЛО
ufo = pygame.image.load("ufo.png")
ufo = pygame.transform.scale(ufo, (60, 30))
ufos = []
def create_ufos():
    global ufos
    for i in range(10):
        ufo_box = pygame.Rect(randint(0, 420), randint(-240, -40), 60, 30)
        ufos.append(ufo_box)
 
    for i in range(10):
        ufo_box = pygame.Rect(randint(0, 420), randint(-640, -440), 60, 30)
        ufos.append(ufo_box)
 
    for i in range(10):
        ufo_box = pygame.Rect(randint(0, 420), randint(-1040, -840), 60, 30)
        ufos.append(ufo_box)
 
create_ufos()
 
# Сердечки
heart_img = pygame.image.load('heart.png')
heart_img = pygame.transform.scale(heart_img, (30, 30))
hearts = []
for i in range(3):
    heart_box = pygame.Rect(450 - i * 40, 20, 30, 30)
    hearts.append(heart_box)
 
# Счет пуль
buttel_img = pygame.image.load('bullet.png')
buttel_img = pygame.transform.scale(buttel_img, (30, 30))
buttels1 = []
for i in range(3):
    buttels_box = pygame.Rect(450 - i * 40, 80, 30, 30)
    buttels1.append(buttels_box)
 
direction = "none"
lives_left = 3
shots_count = 0
buttels_left = 3
iterations = 0
current_screen = 0
 
 
while True:
    screen.blit(screen_textur, (0, 0))
    # Обработка событий
    if current_screen == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x >= start_bitton_box.x and x <= start_bitton_box.x + start_bitton_box.width and y >= start_bitton_box.y and  y <= start_bitton_box.y + start_bitton_box.height :
                    pygame.mixer.music.play()
                    current_screen = 1

 
        screen.blit(start_bitton, start_bitton_box)
    elif current_screen == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    direction = "right"
                if event.key == pygame.K_LEFT:
                    direction = "left"
                if event.key == pygame.K_SPACE:
                    if shots_count != 3:
                        bullet_box = pygame.Rect(rocket_box.x + 22, rocket_box.y + 20, 10, 20)
                        bullets.append(bullet_box)
                        shots_count += 1
                        buttels_left -= 1
                        fire_sound.play()
 
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    direction = "none"
 
        # Движение игрока
        if direction == "right" :
            if rocket_box.x < 450:
                rocket_box.x += 10
        if direction == "left" :
            if rocket_box.x > 0:
                rocket_box.x -= 10
 
        # Движение НЛО
        for i in ufos:
            i.y += 2
            if i.y > 500:
                i.y = randint(-200, -40)
                i.x = randint(0, 420)
 
 
 
        # Cтолкновение пули и НЛО
        for i in range(len(ufos)):
            hit = False
            for b in range(len(bullets)):
                if ufos[i].colliderect(bullets[b]):
                    del ufos[i]
                    del bullets[b]
                    points += 1
                    a = shrift.render(str(points), False, (0, 100, 20))
                    hit = True
                    break 
            if hit:
                break
 
        # Движение пули
        for b in bullets:
            b.y -= 10
            if b.y < 20:
                del b
 
 
 
        # Победа
        if len(ufos) == 0:
            pygame.mixer.music.pause()
            current_screen = 0
            ufos = []
            create_ufos()
            bullets = []
            a = shrift.render(str(points), False, (0, 100, 20))
            rocket_box.x = 100
            rocket_box.y = 430
            points = 0
            lives_left = 3
            buttels_left = 3
 
        # Поражение
        for i in range(len(ufos)):
            if rocket_box.colliderect(ufos[i]):
                lives_left -= 1
                del ufos[i]
                break
 
        if lives_left == 0:
            pygame.mixer.music.pause()
            current_screen = 0
            ufos = []
            create_ufos()
            bullets = []
            a = shrift.render(str(points), False, (0, 100, 20))
            rocket_box.x = 100
            rocket_box.y = 430
            points = 0
            lives_left = 3
            buttels_left = 3
 
        # Отрисовка
        screen.blit(rocket, rocket_box)
        screen.blit(a, (40,40))
 
        for b in bullets:
            screen.blit(bullet, b)
 
        for i in ufos:
            screen.blit(ufo, i)
 
        if shots_count == 3:
            iterations += 1
            if iterations == 90:
                iterations = 0
                shots_count = 0
                buttels_left = 3
 
        for i in range(lives_left):
            screen.blit(heart_img, hearts[i])
 
        for i in range(buttels_left):
            screen.blit(buttel_img, buttels1[i])
 
    pygame.display.update()
    clock.tick(60)