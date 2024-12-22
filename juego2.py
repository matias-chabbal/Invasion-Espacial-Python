import pygame
import random
import math
from pygame import mixer

pygame.init()
mixer.music.load("MusicaFondo.mp3")
mixer.music.play(-1)
#clase pantalla
class Pantalla:
    ancho = 800
    alto = 600
    fondo = pygame.image.load('Fondo.jpg')
    icono = pygame.image.load('consola-de-video.png')

#instanciamos pantalla
pantalla = Pantalla()
pygame.display.set_caption('Invasion Espacial')
pygame.display.set_icon(pantalla.icono)
screen = pygame.display.set_mode((pantalla.ancho, pantalla.alto))

fuente = pygame.font.Font('freesansbold.ttf', 32)
fuente_finalizar = pygame.font.Font('freesansbold.ttf', 50)
texto_x = 10
texto_y = 10
def mostrar_puntaje(x, y):
    texto = fuente.render(f"puntos: {puntaje}", True, (255, 255, 255))
    screen.blit(texto, (x, y))
def finalizar():
    fin = fuente_finalizar.render("Ganaste!!!", True, (255, 255, 255))
    screen.blit(fin, (280, 250))
#clase personaje
puntaje = 0
class Personaje:
    imagen = pygame.image.load('cohete.png')
    
    def __init__(self, x, y, movimiento_x):
        self.x = x
        self.y = y
        self.movimiento_x = movimiento_x
    def disparar(self):
        pass
    def move_x(self, valor):
        self.movimiento_x = valor
    def move(self):
        self.x += self.movimiento_x
    def jugador(self,x ,y):
        screen.blit(self.imagen, (self.x, self.y))
    def limites(self):
        if self.x <= 0:
            self.x = 0
        if self.x >= 736:
            self.x = 736

#class bala

#clase enemigo
class Enemigo(Personaje):
    image = pygame.image.load('enemigo.png')

    def __init__(self, x, y, movimiento_x, movimiento_y, velocidad):
        super().__init__(x,y,movimiento_x)
        self.movimiento_y = movimiento_y
        self.velocidad = velocidad

    def arrojar_enemigo(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.movimiento_x
        if self.x >= 736:
            self.movimiento_x = -self.velocidad
            self.y += self.movimiento_y
        if self.x <= 0:
            self.movimiento_x = self.velocidad
            self.y += self.movimiento_y



#instanciamos personaje
personaje = Personaje(368, 450, 0)
#clase bala
class Bala(Personaje):
    imagen = pygame.image.load('bala.png')
    bala_visible = False
    def __init__(self, x, y, movimiento_x, movimiento_y):
        super().__init__(x, y, movimiento_x)
        self.movimiento_y = movimiento_y
    def arrojar_bala(self, x):
        self.bala_visible = True
        self.y -= self.movimiento_y
        screen.blit(self.imagen, (x, self.y))
        
bala = Bala(0, personaje.y, 0, 1)
     
#instanciamos enemigos
cantidad_enemigos = 6
lista_enemigos = []
enemigos_eliminados = 0
for enem in range(cantidad_enemigos):
    enemigo = Enemigo(random.randint(0, 736), random.randint(0, 200), 0.3, 50, 0.3)
    lista_enemigos.append(enemigo)

def hay_colision(x1,y1,x2,y2):
    distancia = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    
    if distancia < 27:
        global puntaje
        puntaje += 1
        return True
    else:
        return False



run = True
while run:
    screen.blit(pantalla.fondo, (0,0))
    #eventos...
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                valor = -0.5
                personaje.move_x(valor)
            if event.key == pygame.K_d:
                valor = 0.5
                personaje.move_x(valor)
            if event.key == pygame.K_UP:
                if not bala.bala_visible:
                    sonido_bala = mixer.Sound("disparo.mp3")
                    sonido_bala.play()
                    bala.arrojar_bala(personaje.x)
                    bala_x = personaje.x
                
                    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                valor = 0
                personaje.move_x(valor)
 #arrojar enemigos al campo...
    for enem in lista_enemigos:
        indice = lista_enemigos.index(enem)
        
        if enem.y >= 370:
            lista_enemigos.clear()
        else:
            enem.arrojar_enemigo()
            enem.move()
            bala.x = personaje.x
            
        #colision enemigo-bala...
        colision = hay_colision(enem.x,enem.y,bala.x,bala.y)
        if colision:
                sonido_colision = mixer.Sound("Golpe.mp3")
                sonido_colision.play()
                bala.y = personaje.y
                bala.bala_visible = False
                lista_enemigos.pop(indice)
                
        
    if puntaje == cantidad_enemigos:
        finalizar()
    else:    
        personaje.move()
    personaje.limites()
    #arrojar bala al campo...
    if bala.bala_visible:
        bala.arrojar_bala(bala_x + 16)
    if bala.y <= -64:
            bala.bala_visible = False 
            bala.y = personaje.y
    
    
    
   

    
    #arrojar jugador al campo...
    personaje.jugador(personaje.x, personaje.y)
    mostrar_puntaje(texto_x, texto_y)
    pygame.display.update()