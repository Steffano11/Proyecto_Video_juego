# Proyecto_Video_juego
# Adventure in the Jungle

## Descripción

Adventure in the Jungle es un videojuego desarrollado en Python utilizando la biblioteca Pygame. El jugador controla un personaje que debe superar diferentes obstáculos, esquivar proyectiles y sobrevivir al enfrentamiento con un jefe final.

La dificultad aumenta progresivamente conforme se incrementa el puntaje del jugador.

## Requisitos

- Python 3.14 (versión utilizada en el proyecto).
- Pygame Community Edition (`pygame-ce`).
- Visual Studio Code (opcional).
- Archivos de imágenes y sonido incluidos en el proyecto.

## Instalación

### 1. Clonar o descargar el repositorio

Descargar el proyecto y abrir la carpeta desde Visual Studio Code.

### 2. Instalar las dependencias

Abrir una terminal y ejecutar:

```bash
python -m pip install --upgrade pip
python -m pip install pygame-ce
```

### 3. Verificar la instalación

```bash
python -c "import pygame; print(pygame.version.ver)"
```

Si se muestra la versión de Pygame, la instalación se ha realizado correctamente.

## Ejecución

Desde la terminal, ubicarse en la carpeta principal del proyecto y ejecutar:

```bash
python Videojuego.py
```

Se abrirá automáticamente la ventana del videojuego.

## Controles

| Tecla | Acción |
|---|---|
| Cualquier tecla | Iniciar el juego |
| Flecha arriba | Saltar |
| Flecha abajo | Agacharse |
| Cualquier tecla después de perder | Volver a intentarlo |
| R | Reiniciar después de ganar |

## Características del videojuego

- Animaciones del personaje.
- Generación aleatoria de obstáculos.
- Detección de colisiones.
- Sistema de puntuación.
- Registro del puntaje máximo durante la ejecución.
- Dificultad progresiva.
- Enfrentamiento con un jefe final.
- Música y efectos de sonido.
- Pantallas de inicio, derrota y victoria.

## Objetivo del juego

El jugador debe evitar los obstáculos y proyectiles hasta alcanzar los 50 000 puntos. El jefe final aparece al alcanzar los 15 000 puntos.

## Tecnologías utilizadas

- Python.
- Pygame Community Edition.
- Programación orientada a objetos.

## Consideraciones

- Mantener la estructura original de las carpetas del proyecto.
- No modificar los nombres de los archivos de imágenes y sonido.
- Se utiliza `pygame-ce` para evitar problemas de instalación de Pygame 2.6.1 con Python 3.14.