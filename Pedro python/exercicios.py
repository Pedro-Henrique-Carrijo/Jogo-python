import pygame
from pygame import mixer
from pathlib import Path
import random

DIRETORIO_ATUAL = str(Path(__file__).parent.absolute())

pygame.init()
mixer.init()

tela = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Sonic Game")
try:
    sonic_img = pygame.image.load(DIRETORIO_ATUAL + '/imagens/sonic-stop.png')
    fundo = pygame.image.load(DIRETORIO_ATUAL + '/imagens/green-hills.png')
    vilao_img = pygame.image.load(DIRETORIO_ATUAL + '/imagens/vilao.png')
except pygame.error as e:
    print(f"Erro ao carregar as imagens: {e}")
    pygame.quit()
    exit()

try:
    mixer.music.load(DIRETORIO_ATUAL + '/musicas/musica1.wav')
    mixer.music.play(-1)
except pygame.error as e:
    print(f"Erro ao carregar ou tocar a música: {e}")
    pygame.quit()
    exit()

score = 0
clock = pygame.time.Clock()

class Sonic:
    def __init__(self):
        self.x = 100
        self.y = 350
        self.speed = 10
        self.image = sonic_img

    def draw(self):
        tela.blit(self.image, (self.x, self.y))

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.x = max(0, min(self.x, 800 - self.image.get_width()))
        self.y = max(0, min(self.y, 600 - self.image.get_height()))

class Vilao:
    def __init__(self):
        self.x = random.randint(200, 700)
        self.y = random.randint(100, 500)
        self.speed = 5
        self.image = vilao_img
        self.direction = random.choice([-1, 1])

    def draw(self):
        tela.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.speed * self.direction
        if self.x <= 0 or self.x >= 800 - self.image.get_width():
            self.direction *= -1

def colidiu(obj1, obj2):
    return obj1.x < obj2.x + obj2.image.get_width() and obj1.x + obj1.image.get_width() > obj2.x \
           and obj1.y < obj2.y + obj2.image.get_height() and obj1.y + obj1.image.get_height() > obj2.y

sonic = Sonic()
vilao = Vilao()

executando = True

while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_UP]:
        dy = -1
    elif keys[pygame.K_DOWN]:
        dy = 1
    if keys[pygame.K_LEFT]:
        dx = -1
    elif keys[pygame.K_RIGHT]:
        dx = 1
    sonic.move(dx, dy)


    vilao.move()

    if colidiu(sonic, vilao):
        print("Game Over! Sonic colidiu com o vilão.")
        executando = False

    score += 1

    tela.blit(fundo, (0, 0))
    sonic.draw()
    vilao.draw()

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    tela.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
