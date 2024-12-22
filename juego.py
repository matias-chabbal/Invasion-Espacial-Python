import pygame
import random
import math
from pygame import mixer
#inicializo pygame
pygame.init()
mixer.music.load("MusicaFondo.mp3")
mixer.music.play(-1)
#creo pantalla
pantalla = pygame.display.set_mode((800,600))

#titulo icono fondo
pygame.display.set_caption('mi primer juego.')
icono = pygame.image.load('consola-de-video.png')
pygame.display.set_icon(icono)
fondo = pygame.image.load('Fondo.jpg')
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10
def mostrar_puntaje(x, y):
    texto = fuente.render(f"puntos: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))
#jugador 1
img_jugador = pygame.image.load('cohete.png')
jugador_x = 368
jugador_y = 450
jugador_x_mover = 0
puntaje = 0
def jugador(x, y):
    pantalla.blit(img_jugador, (jugador_x, jugador_y))

#enemigo
img_enemigo = pygame.image.load('enemigo.png')
enemigo_x = random.randint(0, 736)
enemigo_y = random.randint(0, 200)
enemigo_x_move = 0.3
enemigo_y_move = 50
velocidad = 0.3
def enemigo(x, y):
    pantalla.blit(img_enemigo, (x, y))

#bala
img_bala = pygame.image.load('bala.png')
bala_x = 0
bala_y = 450
bala_x_move = 0
bala_y_move = 1
bala_visible = False
def bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))
#detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_1 - y_2, 2))
    if distancia < 27:
        return True
    else:
        return False
#ejecucion del programa
ejecutar = True
while ejecutar:
    pantalla.blit(fondo, (0,0))
    #color de pantalla
    #pantalla.fill((255,100,255))
    #evnetos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutar = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a:
                jugador_x_mover -= 0.5
            if evento.key == pygame.K_d:
                jugador_x_mover += 0.5 
            if evento.key == pygame.K_UP:
                if not bala_visible:
                    sonido_bala = mixer.Sound("disparo.mp3")
                    sonido_bala.play()
                    bala_x = jugador_x
                    bala(bala_x, bala_y)
                
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_a or evento.key == pygame.K_d:
                jugador_x_mover = 0
        
    #actualizar posicion de jugador
    jugador_x += jugador_x_mover
    #actualizar posicion bala
    
    #mantener jugador dentro del cuadrado
    if jugador_x <= 0:
        jugador_x = 0
    if jugador_x >= 736:
        jugador_x = 736
    #actualizar posicion de enemigo
    enemigo_x += enemigo_x_move
    if enemigo_x <=0:
        enemigo_x_move = velocidad
        enemigo_y += enemigo_y_move
    if enemigo_x >= 736:
        enemigo_x_move = -velocidad
        enemigo_y += enemigo_y_move
    if enemigo_y >= 400:
        break
    #posicion bala
    if bala_y <= -64:
        bala_y = 450
        bala_visible = False
    if bala_visible:
        bala(bala_x, bala_y)
        bala_y -= bala_y_move
    #colision
    colision = hay_colision(enemigo_x, enemigo_y, bala_x, bala_y)
    if colision:
        sonido_colision = mixer.Sound("Golpe.mp3")
        sonido_colision.play()
        enemigo_x = random.randint(0, 736)
        enemigo_y = random.randint(0, 200)
        bala_y = 450
        bala_visible = False
        puntaje += 1
        velocidad += 0.1
        
    mostrar_puntaje(texto_x, texto_y)
    jugador(jugador_x, jugador_y)
    enemigo(enemigo_x, enemigo_y)
    
    
    #actualizar pantalla
    pygame.display.update()