import pygame
from pygame.locals import * #importar todos los nombres de constantes y variables definidas en el módulo locals de la biblioteca Pygame.
from pygame import mixer  #Para la música
import random 
import sys
import os #Acceso a variables y funcionalidades del entorno

#Inicializar pygame
pygame.init()

#Colores
Black = (0,0,0)
White = (255,255,255)
Red = (255,0,0)

#Titulo del juego
pygame.display.set_caption("Adventure in the jungle")

#Crear Ventana
width = 1225
height = 750

#Inicializar la pantalla
pantalla = pygame.display.set_mode((width,height))

#Crear Fondo
fondo = pygame.image.load("Fondo_Videojuego.png").convert()
fondo = pygame.transform.scale(fondo, (width,height)) #Para que la imagen se adecue segun la pantalla
clock = pygame.time.Clock()
fondo_inicio = pygame.image.load("fondo_1.png").convert()
fondo_inicio = pygame.transform.scale(fondo_inicio,(width,height))
fondo_game_over = pygame.image.load("game_over.png").convert()
fondo_game_over = pygame.transform.scale(fondo_game_over, (750,700))
fondo_ganar = pygame.image.load("Fondo_ganar.jpg")
fondo_ganar = pygame.transform.scale(fondo_ganar, (750,700))
#Para centrar el game over
game_over_x = (width - fondo_game_over.get_width()) // 2
game_over_y = (height - fondo_game_over.get_height()) // 2
#Para centrar el fondo ganar
ganar_over_x = (width - fondo_ganar.get_width()) // 2
ganar_over_y = (height - fondo_ganar.get_height()) // 2

#Imagenes
correr = [pygame.image.load(os.path.join("Personaje_run_0.png")),pygame.image.load(os.path.join("Personaje_run_1.png")),pygame.image.load(os.path.join("Personaje_run_2.png")),
          pygame.image.load(os.path.join("Personaje_run_3.png")),pygame.image.load(os.path.join("Personaje_run_4.png")),pygame.image.load(os.path.join("Personaje_run_5.png")),
          pygame.image.load(os.path.join("Personaje_run_6.png")),pygame.image.load(os.path.join("Personaje_run_7.png"))]
saltar = pygame.image.load(os.path.join("jump_3.png"))
agachado = [pygame.image.load(os.path.join("agachado.png")),
            pygame.image.load(os.path.join("agachado.png"))]
puas_1 = [pygame.image.load(os.path.join("spikes_1.png")),
                   pygame.image.load(os.path.join("spikes_1.png")),
                   pygame.image.load(os.path.join("spikes_1.png"))]
puas_2 = [pygame.image.load(os.path.join("spikes_2.png")),
                pygame.image.load(os.path.join("spikes_2.png")),
                pygame.image.load(os.path.join("spikes_2.png"))]
proyectil_obstaculo = [pygame.image.load(os.path.join("proyectil_normal.png")),
        pygame.image.load(os.path.join("proyectil_normal.png"))]
final_boss = [pygame.image.load(os.path.join("goku_black_parado.png")),pygame.image.load(os.path.join("goku_black_botando_poder_2.png"))]
proyectil_jefe_1 = pygame.image.load(os.path.join("proyectil_jefe.png"))

proyectiles = []
#Creamos la clase de nuestro personaje
class Personaje:
    posicion_x = 50
    posicion_y = 450
    posicion_agachado_y = 480
    salto = 7
    def __init__(self):
        self.correr_img = correr
        self.saltar_img = saltar
        self.agachado_img = agachado

        self.ardilla_correr = True
        self.ardilla_saltar = False
        self.ardilla_agachado = False
        
        self.step_index = 0
        self.velocidad_salto = self.salto
        self.image = self.correr_img[0]
        self.ardilla_rect = self.image.get_rect()
        self.ardilla_rect.x = self.posicion_x
        self.ardilla_rect.y = self.posicion_y

    def update(self,userInput):
        if self.ardilla_correr:
            self.correr()
        if self.ardilla_saltar:
            self.saltar()
        if self.ardilla_agachado:
            self.abajo()
        if self.step_index >= 10:
            self.step_index = 0
        if userInput[pygame.K_UP] and not self.ardilla_saltar:
            self.ardilla_saltar = True
            self.ardilla_correr = False
            self.ardilla_agachado = False
        elif userInput[pygame.K_DOWN] and not self.ardilla_saltar:
            self.ardilla_saltar = False
            self.ardilla_correr = False
            self.ardilla_agachado = True
        elif not (self.ardilla_saltar or userInput[pygame.K_DOWN]):
            self.ardilla_agachado = False
            self.ardilla_correr = True
            self.ardilla_saltar = False
    def abajo(self):
        self.image = self.agachado_img[self.step_index // 5]
        self.ardilla_rect = self.image.get_rect()
        self.ardilla_rect.x = self.posicion_x
        self.ardilla_rect.y = self.posicion_agachado_y
        self.step_index += 1
    def correr(self):
        self.image = self.correr_img[self.step_index // 5]
        self.ardilla_rect = self.image.get_rect()
        self.ardilla_rect.x = self.posicion_x
        self.ardilla_rect.y = self.posicion_y
        self.step_index += 1
    def saltar(self):
        self.image = self.saltar_img
        if self.ardilla_saltar:
            self.ardilla_rect.y -= self.velocidad_salto*3.5 #Tipo Gravedad
            self.velocidad_salto -= 0.5 #Velocidad del salto 
        if self.velocidad_salto < - self.salto:
            self.ardilla_saltar = False
            self.velocidad_salto = self.salto
    def draw(self,screen):
        screen.blit(self.image, (self.ardilla_rect.x,self.ardilla_rect.y))

#Creamos la clase Jefe Final
class JefeFinal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad_y = 5 #velocidad movimiento eje y
        self.direccion_y = 1 # direccion movimiento eje y (1 para arriba y -1 para abajo)
        self.imagenes = final_boss  
        self.indice = 0
        self.rect = self.imagenes[self.indice].get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.tiempo_ultimo_disparo = pygame.time.get_ticks()
        self.animacion_disparo = [pygame.image.load(os.path.join("goku_black_botando_poder_2.png"))]
    def update(self):
        self.y += self.velocidad_y * self.direccion_y #actualiza posicion vertical
        #Para que el jefe no se salga de la pantalla
        if self.y <= 100:
            self.direccion_y = 1
        elif self.y >300:
            self.direccion_y = -1
        self.rect.y = self.y

        global contador_disparo_jefe
        contador_disparo_jefe = 0 
        contador_disparo_jefe += 1
        tiempo_disparo = 1
        if contador_disparo_jefe >= tiempo_disparo:
            self.disparar(proyectiles)
            contador_disparo_jefe = 0
            
        self.imagenes = final_boss

    def disparar(self,proyectiles):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_ultimo_disparo >= 2000:  # 2000 milisegundos = 2 segundos
            self.imagenes = self.animacion_disparo
            pantalla.blit(self.imagenes[self.indice], self.rect) #para mostrar animacion
            pygame.time.delay(80)
            pygame.display.update() #actualiza la pantalla
            proyectil = Proyectil_Jefe(self.x, self.y)
            proyectiles.append(proyectil)
            self.tiempo_ultimo_disparo = tiempo_actual

    def draw(self, pantalla):
        pantalla.blit(self.imagenes[self.indice], self.rect)
        

#Creamos la clase proyectil jefe, es lo que el jefe final disparará
class Proyectil_Jefe:
    def __init__(self, x, y):
        self.x = x - 50
        self.y = y + 220
        self.velocidad = 40 #velocidad del proyectil
        self.imagen = proyectil_jefe_1 
        self.rect = self.imagen.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.direccion_y = 1
    def update(self):
        self.x -= self.velocidad
        self.rect.x = self.x
        if self.rect.right < 0:
            proyectiles.pop()
        if self.y <= 100:
            self.direccion_y = 1
        elif self.y >150:
            self.direccion_y = -10
        self.rect.y = self.y

    def draw(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))

#Creamos la clase obstaculos para tener obstrucciones en el juego      
class obstaculos_game:
    def __init__(self, imagen, tipo):
        self.imagen = imagen
        self.tipo = tipo
        self.rect = self.imagen[self.tipo].get_rect()
        self.rect.x = width
    def update(self): 
        self.rect.x -= 15
        if self.rect.x < -self.rect.width:
            obstaculos_añadir.pop()
    def draw(self,pantalla):
        pantalla.blit(self.imagen[self.tipo],self.rect)

#La clase obstaculo_1, 2 y 3 hereda de obstaculos
class obstaculo_1(obstaculos_game):
    def __init__(self,imagen):
        self.tipo = random.randint(0,2)
        super().__init__(imagen,self.tipo)
        self.rect.y = 510

class obstaculo_2(obstaculos_game):
    def __init__(self,imagen):
        self.tipo = random.randint(0,2)
        super().__init__(imagen,self.tipo)
        self.rect.y = 510

class obstaculo_3(obstaculos_game):
    def __init__(self,imagen):
        self.tipo = 0
        super().__init__(imagen,self.tipo)
        self.rect.y = 400
        self.indice = 0

    def draw(self,pantalla):
        if self.indice >= 9:
            self.indice = 0
        pantalla.blit(self.imagen[self.indice//5], self.rect)
        self.indice +=2

#Definiendo el puntaje
tipo_de_letra = pygame.font.Font("freesansbold.ttf", 45)
def puntaje():
    global puntos, tipo_de_letra
    puntos += 100
    texto = tipo_de_letra.render("Score: " +  str(puntos), True, (White))
    textRect = texto.get_rect()
    textRect.center = (1050,40)
    pantalla.blit(texto, textRect)

#Maximo Score
def max_score():
    global máximo_score,puntos
    if puntos > máximo_score:
        máximo_score = puntos
        return máximo_score
    else:
        return máximo_score
    
#Bucle principal
def main():
    global obstaculos_añadir, velocidad_movimiento_pantalla, puntos, máximo_score
    clock = pygame.time.Clock()
    player = Personaje()
    velocidad_movimiento_pantalla = 0
    obstaculos_añadir = []
    conteo_de_muertes = 0
    puntos = 0
    jefe_final = None
    mixer.music.load("a-hero-of-the-80s-126684.mp3")
    mixer.music.play(-1) #para que la musica se repita
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        #Movimiento del fondo de pantalla
        velocidad_movimiento_pantalla -=15
        pantalla.blit(fondo,(velocidad_movimiento_pantalla, 0))
        pantalla.blit(fondo,(velocidad_movimiento_pantalla + width , 0))

        # Condiciones para que la dificultad suba de acuerdo al puntaje(la velocidad sube)
        if puntos >= 5000 and puntos <= 10000:
            velocidad_movimiento_pantalla -= 3
        elif puntos >= 10001 and puntos <= 15000:
            velocidad_movimiento_pantalla -= 5
        elif puntos >= 15000:
            velocidad_movimiento_pantalla -= 7

        if velocidad_movimiento_pantalla <= -width:
            velocidad_movimiento_pantalla = 0

        if puntos >= 15000 and jefe_final is None:
            jefe_final = JefeFinal(width-200, height-500)
            obstaculos_añadir.append(jefe_final)

        #Condicion para ganar el juego
        if puntos == 50000:
            mixer.music.load("cancion_ganador.mp3")
            mixer.music.play()
            ganar()

        #Para ubicar el mouse
        userInput = pygame.key.get_pressed()
        player.draw(pantalla)
        player.update(userInput)

        #Para que los obstaculos aparezcan aleatoriamente
        if puntos < 15000:
            if len(obstaculos_añadir) == 0:
                if random.randint (0,2)== 0:
                    obstaculos_añadir.append(obstaculo_1(puas_1))
                elif random.randint(0,2) == 1:
                    obstaculos_añadir.append(obstaculo_2(puas_2))
                elif random.randint (0,2) == 2:
                    obstaculos_añadir.append(obstaculo_3(proyectil_obstaculo))

        for obstacle in obstaculos_añadir:
            if isinstance(obstacle, JefeFinal):
                obstacle.update()
                obstacle.draw(pantalla)
            else:
                obstacle.draw(pantalla)
                obstacle.rect.x -= 10
                obstacle.update()
                if puntos >= 5000 and puntos <= 10000:
                    obstacle.rect.x -= 13
                elif puntos >= 10001 and puntos <= 15000:
                    obstacle.rect.x -= 15
                elif puntos >= 15000:
                    obstacle.rect.x -= 20

                if velocidad_movimiento_pantalla <= -width:
                    velocidad_movimiento_pantalla = 0 

                if player.ardilla_rect.colliderect(obstacle.rect):
                    if len(proyectiles) > 0:
                        proyectiles.pop()
                        pygame.time.delay(1)
                        conteo_de_muertes += 1
                        menu(conteo_de_muertes)
                    else:
                        mixer.music.load("risa_de_Black.mp3")
                        mixer.music.play()
                        conteo_de_muertes += 1
                        menu(conteo_de_muertes)

        #Para que el jefe final aparezca en la pantalla          
        if jefe_final is not None:
            jefe_final.draw(pantalla)
            jefe_final.update()
            jefe_final.disparar(proyectiles)

        #Que los proyectiles del jefe final se noten en la pantalla
        for proyectil in proyectiles:
            proyectil.update()
            proyectil.draw(pantalla)
            if player.ardilla_rect.colliderect(proyectil.rect):
                mixer.music.load("risa_de_Black.mp3")
                mixer.music.play()
                pygame.time.delay(1)
                proyectiles.pop()
                conteo_de_muertes += 1
                menu(conteo_de_muertes)

        puntaje()
        clock.tick(30)
        pygame.display.update()     
        pygame.display.flip() #Actualiza la ventana
    
def menu(conteo_de_muertes):
    global puntos, máximo_score
    correr = True
    while correr:
        tipo_letra_2=pygame.font.Font("freesansbold.ttf",30)
        #Menu principal
        if conteo_de_muertes == 0:
            pantalla.blit(fondo_inicio,(0,0))

        #Menu Game over
        elif conteo_de_muertes > 0:
            superficie_fondo = pygame.Surface((width,height))
            superficie_fondo.fill(Black)
            pantalla.blit(superficie_fondo,(0,0))
            pantalla.blit(fondo_game_over,(game_over_x,game_over_y))
            texto_menu_2 = tipo_letra_2.render("Presiona cualquier tecla para reintentarlo", True, Black)
            texto_2 = texto_menu_2.get_rect()
            texto_2.center=(600,700)
            pantalla.blit(texto_menu_2,texto_2)
            score = tipo_de_letra.render("Score: " + str(puntos), True, (White))
            score_rect = score.get_rect()
            score_rect.center = ((width/2),(height /2+150))
            pantalla.blit(score,score_rect)
            maximo_score_texto = tipo_de_letra.render("Max score: "+ str(max_score()), True,(White))
            maximo_score_rect = maximo_score_texto.get_rect()
            maximo_score_rect.center = (width//2, height//2 + 200)
            pantalla.blit(maximo_score_texto,maximo_score_rect)
            
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                main()
                
#funcion ganar
def ganar():
    global puntos, máximo_score
    superficie_fondo_2 = pygame.Surface((width,height))
    superficie_fondo_2.fill(Black)
    pantalla.blit(superficie_fondo_2,(0,0))
    pantalla.blit(fondo_ganar, (ganar_over_x, ganar_over_y))
    max_score()
    score = tipo_de_letra.render("Score: " + str(puntos), True, (White))
    score_rect = score.get_rect()
    score_rect.center = ((width/2),(height /2+60))
    pantalla.blit(score,score_rect)
    maximo_score_texto = tipo_de_letra.render("Max score: "+ str(max_score()), True,(White))
    maximo_score_rect = maximo_score_texto.get_rect()
    maximo_score_rect.center = (width//2, height//2 +110)
    pantalla.blit(maximo_score_texto,maximo_score_rect)
    texto_reiniciar = tipo_de_letra.render("Presiona R para reiniciar", True, Red)
    pantalla.blit(texto_reiniciar, (ganar_over_x + 100, ganar_over_y + 600))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()

máximo_score = 0 #debe estar fuera del main, porque sino se actualiza junto con el puntaje
menu(conteo_de_muertes=0)

