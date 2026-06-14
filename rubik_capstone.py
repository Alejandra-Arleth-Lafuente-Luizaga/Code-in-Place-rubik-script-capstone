# -*- coding: utf-8 -*-
"""
Ecosistema Rubik 3x3 - versión final para GitHub
=================================================
Aplicación educativa y lúdica para cubo Rubik 3x3.

Módulos principales:
1) No sé armar el cubo: acompañamiento inicial, vocabulario simple y solución guiada.
2) Ya tengo experiencia: reto con cronómetro manual, tiempo de máquina y vista 3D-lite.
3) Patrones especiales: catálogo ampliable con ruta para llegar y ruta para volver.
4) Rubik Script: retos interactivos para aprender Python con el cubo Rubik.

Dependencias recomendadas:
    pip install pygame kociemba

Nota técnica:
- La solución del cubo usa el motor de dos fases `kociemba` cuando está instalado.
- La vista 3D es una visualización Pygame ligera, no un motor OpenGL real.
"""

from __future__ import annotations

import json
import math
import random
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional, Iterable, cast

import pygame

try:
    import kociemba
    KOCIEMBA_AVAILABLE = True
except Exception:
    kociemba = None
    KOCIEMBA_AVAILABLE = False


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

WIDTH, HEIGHT = 1220, 840
FPS = 60
SCORE_FILE = Path("rubik_scores.json")
APP_VERSION = ""

COLOR_MAP: Dict[str, Tuple[int, int, int]] = {
    "W": (255, 255, 255),
    "O": (255, 88, 0),
    "G": (0, 155, 72),
    "R": (183, 18, 52),
    "B": (0, 70, 173),
    "Y": (255, 213, 0),
    "BG": (24, 24, 31),
    "PANEL": (42, 42, 53),
    "PANEL2": (31, 31, 40),
    "TEXT": (240, 240, 245),
    "MUTED": (172, 176, 190),
    "ALERT": (255, 204, 0),
    "BORDER": (70, 70, 85),
    "SUCCESS": (0, 210, 115),
    "DANGER": (230, 60, 70),
    "NEON": (0, 255, 255),
    "PURPLE": (160, 32, 240),
    "SPIKE": (255, 72, 72),
}

COLOR_NAMES = {
    "ES": {"W": "Blanco", "O": "Naranja", "G": "Verde", "R": "Rojo", "B": "Azul", "Y": "Amarillo"},
    "EN": {"W": "White", "O": "Orange", "G": "Green", "R": "Red", "B": "Blue", "Y": "Yellow"},
}

FACE_TO_COLOR = {"U": "W", "L": "O", "F": "G", "R": "R", "B": "B", "D": "Y"}
COLOR_TO_FACE = {v: k for k, v in FACE_TO_COLOR.items()}
FACE_ORDER_KOCIEMBA = ["U", "R", "F", "D", "L", "B"]
FACE_DRAW_ORDER = ["U", "L", "F", "R", "B", "D"]
GRID_POSITIONS = {"U": (1, 0), "L": (0, 1), "F": (1, 1), "R": (2, 1), "B": (3, 1), "D": (1, 2)}

TEXT = {
    "ES": {
        "title": "ECOSISTEMA RUBIK 3x3",
        "subtitle": "Aprende el cubo Rubik y practica Python jugando.",
        "project_info": "Proyecto: Final Capstone Project · Code in Place 2026",
        "author_info": "Autora: Alejandra Lafuente",
        "year_info": "Año: 2026 · PyCharm/GitHub",
        "purpose_title": "Propósito del proyecto",
        "purpose_body": "Proyecto final Code in Place 2026: aplicación educativa para aprender el cubo Rubik 3x3, crear patrones y practicar Python con retos tipo Karel basados en variables, condicionales y bucles.",
        "continue": "CONTINUAR",
        "back": "VOLVER",
        "reset": "REINICIAR CUBO",
        "solve": "GENERAR GUÍA",
        "stop": "PARAR MI TIEMPO",
        "start_challenge": "INICIAR RETO",
        "profile_title": "¿Cuál es tu punto de partida?",
        "profile_sub": "Elige una ruta. Puedes volver aquí en cualquier momento.",
        "beginner": "NO SÉ ARMAR EL CUBO RUBIK",
        "beginner_desc": "Guía ejecutable desde tu propio cubo real, con comandos sencillos y visor 3D de apoyo.",
        "expert": "YA TENGO EXPERIENCIA",
        "expert_desc": "Reto con cronómetro, lenguaje técnico, tiempo de máquina y récord personal.",
        "manual": "¿QUÉ ES EL CUBO RUBIK?",
        "manual_desc": "Manual visual separado: caras, centros, aristas, esquinas, objetivo y orientación.",
        "patterns": "PATRONES ESPECIALES",
        "patterns_desc": "Ajedrez, serpiente, puntos, superflip y más rutas para crear y deshacer patrones.",
        "arcade": "RUBIK SCRIPT: APRENDE PYTHON",
        "arcade_desc": "Aprende variables, condicionales y bucles programando acciones del cubo.",
        "orientation": "Orientación fija: centro BLANCO arriba y centro VERDE frente a tus ojos.",
        "palette": "PALETA",
        "guide_empty": "Pinta los stickers de tu cubo real y presiona GENERAR GUÍA.",
        "guide_empty_expert": "Carga tu cubo, inicia el reto y detén manualmente tu cronómetro al terminar.",
        "solved": "El cubo ya está resuelto. Desármalo físicamente o elige un patrón.",
        "kociemba_missing": "Falta instalar kociemba: pip install kociemba",
        "bad_counts": "Revisa conteos: cada color debe tener exactamente 9 stickers.",
        "invalid_cube": "Combinación no física. Revisa centros, aristas o esquinas.",
        "step": "PASO",
        "next": "SIGUIENTE",
        "prev": "ANTERIOR",
        "manual_next": "LECCIÓN SIGUIENTE",
        "manual_prev": "LECCIÓN ANTERIOR",
        "manual_start": "IR A LA GUÍA",
        "manual_title": "Manual visual: ¿qué es el cubo Rubik?",
        "what_is_cube": "¿QUÉ ES EL CUBO RUBIK?",
        "pattern_route": "Ruta para llegar",
        "pattern_back": "Ruta para volver",
        "pattern_note": "Catálogo clásico y ampliable. No existe una lista finita de 'todos' los patrones posibles.",
        "pattern_select_hint": "Selecciona un patrón en la lista para ver sus movimientos paso a paso.",
        "arcade_menu": "RUBIK SCRIPT - APRENDE PYTHON CON EL CUBO",
        "play_world": "INICIAR RETO",
        "game_over": "ERROR: el script chocó con un bug del cubo.",
        "retry": "Presiona ESPACIO para reintentar o vuelve al menú de retos.",
        "victory": "RETO PYTHON COMPLETADO",
        "campaign": "CAMPAÑA COMPLETA: dominaste variables, condicionales y bucles.",
    },
    "EN": {
        "title": "RUBIK 3x3 ECOSYSTEM",
        "subtitle": "Learn the Rubik cube and practice Python by playing.",
        "project_info": "Project: Final Capstone Project · Code in Place 2026",
        "author_info": "Author: Alejandra Lafuente",
        "year_info": "Year: 2026 · PyCharm/GitHub",
        "purpose_title": "Project purpose",
        "purpose_body": "Code in Place 2026 final project: an educational app to learn the Rubik 3x3 cube, create patterns, and practice Python through Karel-style challenges based on variables, conditionals, and loops.",
        "continue": "CONTINUE",
        "back": "BACK",
        "reset": "RESET CUBE",
        "solve": "GENERATE GUIDE",
        "stop": "STOP MY TIME",
        "start_challenge": "START CHALLENGE",
        "profile_title": "What is your starting point?",
        "profile_sub": "Choose a path. You can return here at any moment.",
        "beginner": "I DO NOT KNOW HOW TO SOLVE IT",
        "beginner_desc": "Executable guide from your real cube, with simple commands and a 3D support viewer.",
        "expert": "I ALREADY HAVE EXPERIENCE",
        "expert_desc": "Timer challenge, technical language, machine time, and personal record.",
        "manual": "WHAT IS THE RUBIK CUBE?",
        "manual_desc": "Separate visual manual: faces, centers, edges, corners, goal, and orientation.",
        "patterns": "SPECIAL PATTERNS",
        "patterns_desc": "Checkerboard, snake, dots, superflip, and more create/return routes.",
        "arcade": "RUBIK SCRIPT: LEARN PYTHON",
        "arcade_desc": "Learn variables, conditionals, and loops by programming cube actions.",
        "orientation": "Fixed orientation: WHITE center up and GREEN center facing your eyes.",
        "palette": "PALETTE",
        "guide_empty": "Paint the stickers of your real cube and press GENERATE GUIDE.",
        "guide_empty_expert": "Load your cube, start the challenge, and stop your timer manually when done.",
        "solved": "The cube is already solved. Scramble it physically or choose a pattern.",
        "kociemba_missing": "Missing kociemba: pip install kociemba",
        "bad_counts": "Check counts: every color must appear exactly 9 times.",
        "invalid_cube": "Non-physical combination. Check centers, edges, or corners.",
        "step": "STEP",
        "next": "NEXT",
        "prev": "PREVIOUS",
        "manual_next": "NEXT LESSON",
        "manual_prev": "PREVIOUS LESSON",
        "manual_start": "GO TO GUIDE",
        "manual_title": "Visual manual: what is the Rubik cube?",
        "what_is_cube": "WHAT IS THE RUBIK CUBE?",
        "pattern_route": "Route to build it",
        "pattern_back": "Route to return",
        "pattern_note": "Classic and expandable catalog. There is no finite list of all possible patterns.",
        "pattern_select_hint": "Select a pattern from the list to see its moves step by step.",
        "arcade_menu": "RUBIK SCRIPT - LEARN PYTHON WITH THE CUBE",
        "play_world": "START CHALLENGE",
        "game_over": "ERROR: the script hit a cube bug.",
        "retry": "Press SPACE to retry or return to the challenge menu.",
        "victory": "PYTHON CHALLENGE COMPLETED",
        "campaign": "CAMPAIGN COMPLETE: you mastered variables, conditionals, and loops.",
    },
}


# Diccionario de movimientos en lenguaje sencillo, inspirado en la versión original.
# Cada instrucción debe leerse manteniendo la orientación fija: blanco arriba y verde al frente.
MOVE_TEXT = {
    "ES": {
        "U": "Capa SUPERIOR / blanca hacia la IZQUIERDA.",
        "U'": "Capa SUPERIOR / blanca hacia la DERECHA.",
        "U2": "Capa SUPERIOR / blanca: medio giro completo de 180 grados.",
        "D": "Capa INFERIOR / amarilla hacia la DERECHA.",
        "D'": "Capa INFERIOR / amarilla hacia la IZQUIERDA.",
        "D2": "Capa INFERIOR / amarilla: medio giro completo de 180 grados.",
        "F": "Capa FRONTAL / verde hacia la DERECHA.",
        "F'": "Capa FRONTAL / verde hacia la IZQUIERDA.",
        "F2": "Cara FRONTAL / verde: medio giro completo de 180 grados.",
        "B": "Capa TRASERA / azul hacia la IZQUIERDA.",
        "B'": "Capa TRASERA / azul hacia la DERECHA.",
        "B2": "Cara TRASERA / azul: medio giro completo de 180 grados.",
        "R": "Capa DERECHA / roja hacia ARRIBA (atrás, se aleja de ti).",
        "R'": "Capa DERECHA / roja hacia ABAJO (hacia ti).",
        "R2": "Cara DERECHA / roja: medio giro completo de 180 grados.",
        "L": "Capa IZQUIERDA / naranja hacia ABAJO (hacia ti).",
        "L'": "Capa IZQUIERDA / naranja hacia ARRIBA (atrás, se aleja de ti).",
        "L2": "Cara IZQUIERDA / naranja: medio giro completo de 180 grados.",
    },
    "EN": {
        "U": "TOP / white layer to the LEFT.",
        "U'": "TOP / white layer to the RIGHT.",
        "U2": "TOP / white layer: full 180-degree half turn.",
        "D": "BOTTOM / yellow layer to the RIGHT.",
        "D'": "BOTTOM / yellow layer to the LEFT.",
        "D2": "BOTTOM / yellow layer: full 180-degree half turn.",
        "F": "FRONT / green face to the RIGHT.",
        "F'": "FRONT / green face to the LEFT.",
        "F2": "FRONT / green face: full 180-degree half turn.",
        "B": "BACK / blue face to the LEFT.",
        "B'": "BACK / blue face to the RIGHT.",
        "B2": "BACK / blue face: full 180-degree half turn.",
        "R": "RIGHT / red face UPWARD, away from you.",
        "R'": "RIGHT / red face DOWNWARD, toward you.",
        "R2": "RIGHT / red face: full 180-degree half turn.",
        "L": "LEFT / orange face DOWNWARD, toward you.",
        "L'": "LEFT / orange face UPWARD, away from you.",
        "L2": "LEFT / orange face: full 180-degree half turn.",
    },
}

MOVE_TECH = {
    "ES": {
        "U": "Clave: U = capa superior. Giro horario visto desde arriba.",
        "U'": "Clave: U' = capa superior. Giro inverso.",
        "U2": "Clave: U2 = capa superior dos cuartos de giro.",
        "D": "Clave: D = capa inferior. Giro horario visto desde abajo.",
        "D'": "Clave: D' = capa inferior. Giro inverso.",
        "D2": "Clave: D2 = capa inferior dos cuartos de giro.",
        "F": "Clave: F = cara frontal. Giro horario mirando la cara verde.",
        "F'": "Clave: F' = cara frontal. Giro inverso.",
        "F2": "Clave: F2 = cara frontal dos cuartos de giro.",
        "B": "Clave: B = cara trasera. Giro horario mirando la cara azul.",
        "B'": "Clave: B' = cara trasera. Giro inverso.",
        "B2": "Clave: B2 = cara trasera dos cuartos de giro.",
        "R": "Clave: R = cara derecha. Giro horario mirando la cara roja.",
        "R'": "Clave: R' = cara derecha. Giro inverso.",
        "R2": "Clave: R2 = cara derecha dos cuartos de giro.",
        "L": "Clave: L = cara izquierda. Giro horario mirando la cara naranja.",
        "L'": "Clave: L' = cara izquierda. Giro inverso.",
        "L2": "Clave: L2 = cara izquierda dos cuartos de giro.",
    },
    "EN": {
        "U": "Key: U = upper layer. Clockwise as viewed from the top.",
        "U'": "Key: U' = upper layer. Inverse turn.",
        "U2": "Key: U2 = upper layer, two quarter turns.",
        "D": "Key: D = bottom layer. Clockwise as viewed from below.",
        "D'": "Key: D' = bottom layer. Inverse turn.",
        "D2": "Key: D2 = bottom layer, two quarter turns.",
        "F": "Key: F = front face. Clockwise facing the green side.",
        "F'": "Key: F' = front face. Inverse turn.",
        "F2": "Key: F2 = front face, two quarter turns.",
        "B": "Key: B = back face. Clockwise facing the blue side.",
        "B'": "Key: B' = back face. Inverse turn.",
        "B2": "Key: B2 = back face, two quarter turns.",
        "R": "Key: R = right face. Clockwise facing the red side.",
        "R'": "Key: R' = right face. Inverse turn.",
        "R2": "Key: R2 = right face, two quarter turns.",
        "L": "Key: L = left face. Clockwise facing the orange side.",
        "L'": "Key: L' = left face. Inverse turn.",
        "L2": "Key: L2 = left face, two quarter turns.",
    },
}

BEGINNER_LESSONS = {
    "ES": [
        "Objetivo: cada cara debe quedar con un solo color. Los centros no se mueven; ellos definen el color final de cada cara.",
        "Nombres básicos: U=arriba, D=abajo, F=frente, B=atrás, R=derecha, L=izquierda. Una prima (') significa giro inverso; 2 significa medio giro.",
        "Cómo usar esta guía: mantén blanco arriba y verde al frente, pinta tu cubo real en la red 2D y ejecuta cada paso sin cambiar la orientación física.",
        "Consejo: primero aprende la notación. Luego practica series cortas de 3 a 5 movimientos antes de intentar resolver todo el cubo.",
    ],
    "EN": [
        "Goal: every face must end with one color. Centers do not move; they define each face's final color.",
        "Basic names: U=up, D=down, F=front, B=back, R=right, L=left. A prime (') means inverse turn; 2 means half turn.",
        "How to use this guide: keep white on top and green in front, paint your real cube on the 2D net, and execute each step without changing the physical orientation.",
        "Tip: learn notation first. Then practice short sequences of 3 to 5 moves before solving the full cube.",
    ],
}

MANUAL_LESSONS = {
    "ES": [
        {
            "title": "1. ¿Qué es el cubo Rubik 3x3?",
            "body": "Es un rompecabezas de 6 caras. La meta es que cada cara quede de un solo color. Aunque parece que todo se mueve, los centros son la brújula: no cambian de lugar y definen el color final de cada cara.",
            "graphic": "anatomy",
        },
        {
            "title": "2. Piezas: centros, aristas y esquinas",
            "body": "Centros: una sola etiqueta de color y posición fija. Aristas: dos colores. Esquinas: tres colores. Resolver el cubo consiste en colocar y orientar estas piezas sin perder lo ya armado.",
            "graphic": "pieces",
        },
        {
            "title": "3. Orientación para usar la guía",
            "body": "Toma siempre el cubo igual: centro blanco hacia el techo y centro verde hacia tus ojos. Así las instrucciones sencillas como 'cara derecha roja hacia arriba' siempre significan lo mismo.",
            "graphic": "orientation",
        },
        {
            "title": "4. Movimientos sencillos",
            "body": "No necesitas memorizar notación avanzada al inicio. Lee cada paso como una acción física: capa superior blanca a la izquierda, cara frontal verde a la derecha, cara derecha roja hacia ti o alejándose de ti.",
            "graphic": "moves",
        },
        {
            "title": "5. Cómo practicar",
            "body": "Primero identifica colores y caras. Luego practica movimientos sueltos. Después ingresa tu cubo real en la red 2D, presiona GENERAR GUÍA y avanza paso a paso sin cambiar la orientación física.",
            "graphic": "strategy",
        },
    ],
    "EN": [
        {
            "title": "1. What is the 3x3 Rubik cube?",
            "body": "It is a six-face puzzle. The goal is to make every face a single color. Centers are the compass: they do not change position and define each face's final color.",
            "graphic": "anatomy",
        },
        {
            "title": "2. Pieces: centers, edges, and corners",
            "body": "Centers have one color and fixed position. Edges have two colors. Corners have three colors. Solving means placing and orienting these pieces without losing what is already solved.",
            "graphic": "pieces",
        },
        {
            "title": "3. Orientation for the guide",
            "body": "Always hold the cube the same way: white center to the ceiling and green center facing your eyes. Then simple commands keep the same physical meaning.",
            "graphic": "orientation",
        },
        {
            "title": "4. Simple movements",
            "body": "You do not need advanced notation at first. Read every step as a physical action: white top layer left, green front face right, red right face toward you or away from you.",
            "graphic": "moves",
        },
        {
            "title": "5. How to practice",
            "body": "First identify colors and faces. Then practice single moves. Finally enter your real cube into the 2D net, press GENERATE GUIDE, and advance step by step without changing orientation.",
            "graphic": "strategy",
        },
    ],
}

EXPERT_TIPS = {
    "ES": [
        "Lenguaje técnico activo: U, D, F, B, R, L; prima = inverso; 2 = doble giro.",
        "Reto recomendado: desarma tu cubo, ingresa el estado, inicia el cronómetro y resuelve físicamente. La máquina termina primero; tu reloj sigue hasta que presiones PARAR.",
        "Optimización: registra tu mejor tiempo, reduce pausas de reconocimiento y aprende patrones OLL/PLL gradualmente.",
    ],
    "EN": [
        "Active technical language: U, D, F, B, R, L; prime = inverse; 2 = double turn.",
        "Recommended challenge: scramble your cube, enter the state, start the timer, and solve physically. The machine finishes first; your clock keeps running until STOP.",
        "Optimization: track your best time, reduce recognition pauses, and learn OLL/PLL patterns gradually.",
    ],
}

PATTERNS = [
    {
        "name": "Ajedrez / Checkerboard",
        "algo": "U2 D2 L2 R2 F2 B2",
        "desc": "Alterna colores en casi todas las caras.",
    },
    {
        "name": "Seis puntos / Six spots",
        "algo": "U D' R L' F B' U D'",
        "desc": "Crea puntos centrales destacados alrededor del cubo.",
    },
    {
        "name": "Cuatro puntos / Four spots",
        "algo": "F2 B2 U D' R2 L2 U D'",
        "desc": "Variante visual con puntos y simetría lateral.",
    },
    {
        "name": "Cubo dentro de cubo / Cube in cube",
        "algo": "F L F U' R U F2 L2 U' L' B D' B' L2 U",
        "desc": "Efecto de cubo pequeño dentro del cubo grande.",
    },
    {
        "name": "Superflip",
        "algo": "U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2",
        "desc": "Todas las aristas quedan volteadas; patrón clásico avanzado.",
    },
    {
        "name": "Serpiente / Snake",
        "algo": "R L U2 R L' B2 U2 R2 F2 L2 D2 L2 F2",
        "desc": "Trayecto tipo serpiente alrededor de las caras.",
    },
    {
        "name": "Anaconda",
        "algo": "L U B' U' R L' B R' F B' D R D' F'",
        "desc": "Ruta visual envolvente con giro final elegante.",
    },
    {
        "name": "Cruz de victoria / Victory cross",
        "algo": "R2 L' D F2 R' D' R' L U' D R D B2 R' U D2",
        "desc": "Cruces y ejes de color con apariencia de emblema.",
    },
    {
        "name": "Rayas verticales / Vertical stripes",
        "algo": "F U F R L2 B D' R D2 L D' B R2 L F U F",
        "desc": "Forma columnas de color en varias caras.",
    },
    {
        "name": "Escalera / Staircase",
        "algo": "R2 U2 R2 U2 R2 U2 F2 B2 D2 L2 R2",
        "desc": "Patrón escalonado simple para práctica rápida.",
    },
    {
        "name": "Marco / Frame",
        "algo": "F2 L2 B2 R2 U2 D2 R2 B2 L2 F2",
        "desc": "Enfatiza bordes y marcos por cara.",
    },
    {
        "name": "Zigzag",
        "algo": "R U R' U R U2 R' F R U R' U' F'",
        "desc": "Secuencia tipo zigzag inspirada en algoritmos de orientación.",
    },
]

WORLD_SETTINGS = {
    1: {
        "name": "Nivel 1 - Variables del Cubo",
        "subtitle": "aprende listas, índices y colores: recoge tokens correctos y evita SyntaxError",
        "duration": 38.0,
        "speed": 390,
        "spawn_min": 0.95,
        "spawn_max": 1.55,
        "bg": (24, 80, 130),
        "theme": "platform",
    },
    2: {
        "name": "Nivel 2 - Condicionales de Giro",
        "subtitle": "usa lógica if/else: atraviesa puertas R, U, F y esquiva decisiones falsas",
        "duration": 46.0,
        "speed": 560,
        "spawn_min": 0.65,
        "spawn_max": 1.10,
        "bg": (18, 13, 32),
        "theme": "geometry",
    },
    3: {
        "name": "Nivel 3 - Bucles Algorítmicos",
        "subtitle": "automatiza secuencias tipo Karel: repite patrones y depura bugs",
        "duration": 58.0,
        "speed": 690,
        "spawn_min": 0.48,
        "spawn_max": 0.88,
        "bg": (9, 22, 25),
        "theme": "nova",
    },
}


RUBIK_SCRIPT_LEVELS = {1: {'name': {'ES': 'Nivel 1 - Variables del Cubo', 'EN': 'Level 1 - Cube Variables'},
     'goal': {'ES': 'Aprende a representar el cubo con variables, listas, diccionarios, índices y funciones simples.',
              'EN': 'Learn how to represent the cube with variables, lists, dictionaries, indexes, and simple '
                    'functions.'},
     'questions': [{'concept': {'ES': 'Variable + diccionario + matriz', 'EN': 'Variable + dictionary + matrix'},
                    'task': {'ES': 'El cubo se guarda como diccionario de caras. ¿Qué línea consulta el centro de la '
                                   'cara frontal?',
                             'EN': 'The cube is stored as a dictionary of faces. Which line reads the center of the '
                                   'front face?'},
                    'code': ['cubo = {"F": [["V","V","V"], ["V","V","V"], ["V","V","V"]]}',
                             '# fila 1, columna 1 = centro'],
                    'options': {'ES': ['print(cubo["F"][1][1])', 'print(cubo["F"][0][0])', 'print(cubo[1]["F"])'],
                                'EN': ['print(cubo["F"][1][1])', 'print(cubo["F"][0][0])', 'print(cubo[1]["F"])']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: en una matriz 3x3, [1][1] es el centro.',
                                 'EN': 'Correct: in a 3x3 matrix, [1][1] is the center.'},
                    'moves': ['F']},
                   {'concept': {'ES': 'Asignación de variables', 'EN': 'Variable assignment'},
                    'task': {'ES': 'Quieres guardar el centro blanco de la cara superior. ¿Cuál variable está bien '
                                   'escrita?',
                             'EN': 'You want to store the white center of the upper face. Which variable is correct?'},
                    'code': ['# centro de la cara superior', 'cubo["U"][1][1]'],
                    'options': {'ES': ['centro_superior = cubo["U"][1][1]',
                                       'centro superior = cubo["U"]',
                                       'cubo = centro_superior["U"]'],
                                'EN': ['top_center = cubo["U"][1][1]',
                                       'top center = cubo["U"]',
                                       'cubo = top_center["U"]']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: el nombre de variable no lleva espacios y guarda el valor.',
                                 'EN': 'Correct: a variable name has no spaces and stores the value.'},
                    'moves': ['U']},
                   {'concept': {'ES': 'Listas e índices', 'EN': 'Lists and indexes'},
                    'task': {'ES': '¿Qué línea obtiene la primera fila completa de la cara superior?',
                             'EN': 'Which line gets the complete first row of the upper face?'},
                    'code': ['cara_superior = cubo["U"]'],
                    'options': {'ES': ['fila = cubo["U"][0]', 'fila = cubo["U"][1][1]', 'fila = cubo["U"]["fila_1"]'],
                                'EN': ['row = cubo["U"][0]', 'row = cubo["U"][1][1]', 'row = cubo["U"]["row_1"]']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: cubo["U"][0] devuelve toda la primera fila.',
                                 'EN': 'Correct: cubo["U"][0] returns the whole first row.'},
                    'moves': ['U2']},
                   {'concept': {'ES': 'Diccionarios', 'EN': 'Dictionaries'},
                    'task': {'ES': 'Las caras están guardadas por clave. ¿Qué clave representa la cara derecha?',
                             'EN': 'Faces are stored by key. Which key represents the right face?'},
                    'code': ['caras = {"U": arriba, "R": derecha, "F": frente}'],
                    'options': {'ES': ['caras["R"]', 'caras["DERECHA"]', 'caras[2]'],
                                'EN': ['faces["R"]', 'faces["RIGHT"]', 'faces[2]']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: usamos la clave estándar R para la cara derecha.',
                                 'EN': 'Correct: we use the standard key R for the right face.'},
                    'moves': ['R']},
                   {'concept': {'ES': 'Longitud de una lista', 'EN': 'Length of a list'},
                    'task': {'ES': 'Una cara 3x3 tiene 9 stickers. ¿Qué línea comprueba esa cantidad?',
                             'EN': 'A 3x3 face has 9 stickers. Which line checks that amount?'},
                    'code': ['cara = ["B", "B", "B", "B", "B", "B", "B", "B", "B"]'],
                    'options': {'ES': ['len(cara) == 9', 'cara == 9', 'len == cara[9]'],
                                'EN': ['len(face) == 9', 'face == 9', 'len == face[9]']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: len(lista) devuelve la cantidad de elementos.',
                                 'EN': 'Correct: len(list) returns the number of elements.'},
                    'moves': ['B']},
                   {'concept': {'ES': 'Lista de movimientos', 'EN': 'List of moves'},
                    'task': {'ES': 'Quieres guardar una secuencia de giros. ¿Cuál estructura es una lista válida?',
                             'EN': 'You want to store a turn sequence. Which structure is a valid list?'},
                    'code': ["# secuencia: R U R' U'"],
                    'options': {'ES': ['algoritmo = ["R", "U", "R_prima", "U_prima"]',
                                       'algoritmo = "R", "U" sin corchetes',
                                       'algoritmo = {R, U, R_prima}'],
                                'EN': ['algorithm = ["R", "U", "R_prime", "U_prime"]',
                                       'algorithm = "R", "U" without brackets',
                                       'algorithm = {R, U, R_prime}']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: una lista usa corchetes y conserva el orden.',
                                 'EN': 'Correct: a list uses brackets and preserves order.'},
                    'moves': ['R', 'U']},
                   {'concept': {'ES': 'Actualizar una celda', 'EN': 'Update a cell'},
                    'task': {'ES': '¿Qué línea cambia el centro frontal a verde?',
                             'EN': 'Which line changes the front center to green?'},
                    'code': ['cubo["F"] = [["?","?","?"], ["?","?","?"], ["?","?","?"]]'],
                    'options': {'ES': ['cubo["F"][1][1] = "Verde"',
                                       'cubo["F"] = "Verde"[1][1]',
                                       'cubo[1][1]["F"] = "Verde"'],
                                'EN': ['cubo["F"][1][1] = "Green"',
                                       'cubo["F"] = "Green"[1][1]',
                                       'cubo[1][1]["F"] = "Green"']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: primero eliges cara, luego fila y columna.',
                                 'EN': 'Correct: choose face first, then row and column.'},
                    'moves': ['F2']},
                   {'concept': {'ES': 'Tuplas para coordenadas', 'EN': 'Tuples for coordinates'},
                    'task': {'ES': 'Para ubicar una pieza se usa (fila, columna). ¿Cuál coordenada representa la '
                                   'esquina superior izquierda?',
                             'EN': 'To locate a piece we use (row, column). Which coordinate means upper-left corner?'},
                    'code': ['# índices comienzan en 0'],
                    'options': {'ES': ['pos = (0, 0)', 'pos = (1, 1)', 'pos = (3, 3)'],
                                'EN': ['pos = (0, 0)', 'pos = (1, 1)', 'pos = (3, 3)']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: Python empieza a contar desde cero.',
                                 'EN': 'Correct: Python starts counting from zero.'},
                    'moves': ['L']},
                   {'concept': {'ES': 'Copia de lista', 'EN': 'Copy a list'},
                    'task': {'ES': 'Quieres copiar una fila antes de rotarla. ¿Cuál opción evita modificar la original '
                                   'directamente?',
                             'EN': 'You want to copy a row before rotating it. Which option avoids changing the '
                                   'original directly?'},
                    'code': ['fila = cubo["U"][0]'],
                    'options': {'ES': ['fila_copia = fila.copy()',
                                       'fila_copia = fila.mover()',
                                       'fila_copia = copy.fila()'],
                                'EN': ['row_copy = row.copy()', 'row_copy = row.move()', 'row_copy = copy.row()']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: copy() crea una copia superficial de la lista.',
                                 'EN': 'Correct: copy() creates a shallow copy of the list.'},
                    'moves': ['U']},
                   {'concept': {'ES': 'Función simple', 'EN': 'Simple function'},
                    'task': {'ES': 'Quieres consultar un sticker mediante una función. ¿Qué llamada usa tres '
                                   'argumentos correctos?',
                             'EN': 'You want to read a sticker through a function. Which call uses three correct '
                                   'arguments?'},
                    'code': ['def obtener(cara, fila, columna):', '    return cubo[cara][fila][columna]'],
                    'options': {'ES': ['obtener("F", 1, 1)', 'obtener(1, "F")', 'obtener["F"][1][1]'],
                                'EN': ['get("F", 1, 1)', 'get(1, "F")', 'get["F"][1][1]']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: la función recibe cara, fila y columna.',
                                 'EN': 'Correct: the function receives face, row, and column.'},
                    'moves': ['D']},
                   {'concept': {'ES': 'Método append', 'EN': 'append method'},
                    'task': {'ES': 'Quieres registrar los giros realizados. ¿Cómo agregas un giro a la lista '
                                   'historial?',
                             'EN': 'You want to record executed turns. How do you add one turn to the history list?'},
                    'code': ['historial = []'],
                    'options': {'ES': ['historial.append("R")', 'historial.add = "R"', 'append(historial, "R")'],
                                'EN': ['history.append("R")', 'history.add = "R"', 'append(history, "R")']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: append agrega un elemento al final de la lista.',
                                 'EN': 'Correct: append adds one element at the end of the list.'},
                    'moves': ['R']},
                   {'concept': {'ES': 'F-string', 'EN': 'F-string'},
                    'task': {'ES': 'Quieres mostrar el movimiento actual. ¿Qué línea produce un mensaje legible?',
                             'EN': 'You want to display the current move. Which line produces a readable message?'},
                    'code': ['giro = "U"'],
                    'options': {'ES': ['print(f"Movimiento: {giro}")',
                                       'print("Movimiento: giro")',
                                       'print(f Movimiento: giro)'],
                                'EN': ['print(f"Move: {turn}")', 'print("Move: turn")', 'print(f Move: turn)']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: f"...{variable}..." inserta el valor de la variable.',
                                 'EN': 'Correct: f"...{variable}..." inserts the variable value.'},
                    'moves': ['U']}]},
 2: {'name': {'ES': 'Nivel 2 - Condicionales de Giro', 'EN': 'Level 2 - Turn Conditionals'},
     'goal': {'ES': 'Usa if, elif, else, operadores lógicos y comparaciones para decidir movimientos del cubo.',
              'EN': 'Use if, elif, else, logical operators, and comparisons to decide cube moves.'},
     'questions': [{'concept': {'ES': 'if: decisión simple', 'EN': 'if: simple decision'},
                    'task': {'ES': 'Si el centro derecho es rojo, ejecuta el giro R. ¿Qué condición es correcta?',
                             'EN': 'If the right center is red, execute R. Which condition is correct?'},
                    'code': ['centro_derecho = cubo["R"][1][1]'],
                    'options': {'ES': ['if centro_derecho == "Rojo": giro_R()',
                                       'if centro_derecho = "Rojo": giro_R()',
                                       'if "Rojo" in giro_R(): centro_derecho'],
                                'EN': ['if right_center == "Red": turn_R()',
                                       'if right_center = "Red": turn_R()',
                                       'if "Red" in turn_R(): right_center']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: en Python se compara con ==, no con =.',
                                 'EN': 'Correct: Python compares with ==, not =.'},
                    'moves': ['R']},
                   {'concept': {'ES': 'else: plan alternativo', 'EN': 'else: fallback plan'},
                    'task': {'ES': 'Si la esquina no tiene blanco, mueve la capa superior. ¿Qué bloque expresa esa '
                                   'lógica?',
                             'EN': 'If the corner does not have white, move the upper layer. Which block expresses '
                                   'that logic?'},
                    'code': ['tiene_blanco = "Blanco" in esquina'],
                    'options': {'ES': ['if tiene_blanco: colocar_esquina() else: giro_U()',
                                       'if tiene_blanco: giro_U() else colocar_esquina()',
                                       'else tiene_blanco: giro_U()'],
                                'EN': ['if has_white: place_corner() else: turn_U()',
                                       'if has_white: turn_U() else place_corner()',
                                       'else has_white: turn_U()']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: else cubre el caso contrario.',
                                 'EN': 'Correct: else handles the opposite case.'},
                    'moves': ['U']},
                   {'concept': {'ES': 'elif: varias rutas', 'EN': 'elif: several routes'},
                    'task': {'ES': 'El robot del cubo debe elegir entre F, R o U. ¿Qué estructura es válida?',
                             'EN': 'The cube robot must choose between F, R, or U. Which structure is valid?'},
                    'code': ['color = pieza_objetivo'],
                    'options': {'ES': ['if color == "Verde": giro_F() elif color == "Rojo": giro_R() else: giro_U()',
                                       'if color == "Verde": giro_F() else if color == "Rojo": giro_R()',
                                       'elif color == "Verde": giro_F() if else: giro_U()'],
                                'EN': ['if color == "Green": turn_F() elif color == "Red": turn_R() else: turn_U()',
                                       'if color == "Green": turn_F() else if color == "Red": turn_R()',
                                       'elif color == "Green": turn_F() if else: turn_U()']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: Python usa if, elif y else.',
                                 'EN': 'Correct: Python uses if, elif, and else.'},
                    'moves': ['F', 'R']},
                   {'concept': {'ES': 'Operador !=', 'EN': 'Operator !='},
                    'task': {'ES': 'Quieres girar U mientras el color superior no sea blanco. ¿Qué condición usa '
                                   'diferente de?',
                             'EN': 'You want to turn U while the top color is not white. Which condition means not '
                                   'equal?'},
                    'code': ['color_superior = cubo["U"][0][0]'],
                    'options': {'ES': ['if color_superior != "Blanco": giro_U()',
                                       'if color_superior <> "Blanco": giro_U()',
                                       'if color_superior =! "Blanco": giro_U()'],
                                'EN': ['if top_color != "White": turn_U()',
                                       'if top_color <> "White": turn_U()',
                                       'if top_color =! "White": turn_U()']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: != significa distinto de.', 'EN': 'Correct: != means not equal.'},
                    'moves': ['U']},
                   {'concept': {'ES': 'Operador in', 'EN': 'Operator in'},
                    'task': {'ES': 'La esquina tiene tres colores. ¿Qué condición revisa si contiene blanco?',
                             'EN': 'A corner has three colors. Which condition checks whether it contains white?'},
                    'code': ['esquina = ["Blanco", "Rojo", "Verde"]'],
                    'options': {'ES': ['if "Blanco" in esquina: colocar()',
                                       'if esquina has "Blanco": colocar()',
                                       'if "Blanco" == esquina: colocar()'],
                                'EN': ['if "White" in corner: place()',
                                       'if corner has "White": place()',
                                       'if "White" == corner: place()']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: in revisa pertenencia dentro de listas o strings.',
                                 'EN': 'Correct: in checks membership in lists or strings.'},
                    'moves': ['R', 'U']},
                   {'concept': {'ES': 'and: dos condiciones', 'EN': 'and: two conditions'},
                    'task': {'ES': 'Quieres girar F solo si la pieza tiene verde y blanco. ¿Qué condición corresponde?',
                             'EN': 'You want to turn F only if the piece has green and white. Which condition fits?'},
                    'code': ['pieza = ["Verde", "Blanco"]'],
                    'options': {'ES': ['if "Verde" in pieza and "Blanco" in pieza: giro_F()',
                                       'if "Verde" and "Blanco" == pieza: giro_F()',
                                       'if "Verde" in pieza or not "Blanco": giro_F()'],
                                'EN': ['if "Green" in piece and "White" in piece: turn_F()',
                                       'if "Green" and "White" == piece: turn_F()',
                                       'if "Green" in piece or not "White": turn_F()']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: and exige que ambas condiciones sean verdaderas.',
                                 'EN': 'Correct: and requires both conditions to be true.'},
                    'moves': ['F']},
                   {'concept': {'ES': 'or: alternativas', 'EN': 'or: alternatives'},
                    'task': {'ES': 'Si la pieza está en R o en L, conviene corregir laterales. ¿Qué condición usa or?',
                             'EN': 'If the piece is in R or L, fix the side layers. Which condition uses or?'},
                    'code': ['cara_actual = "R"'],
                    'options': {'ES': ['if cara_actual == "R" or cara_actual == "L": corregir()',
                                       'if cara_actual == "R" and "L": corregir()',
                                       'if cara_actual or "R" == "L": corregir()'],
                                'EN': ['if current_face == "R" or current_face == "L": fix()',
                                       'if current_face == "R" and "L": fix()',
                                       'if current_face or "R" == "L": fix()']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: or acepta cualquiera de las dos condiciones.',
                                 'EN': 'Correct: or accepts either condition.'},
                    'moves': ['L']},
                   {'concept': {'ES': 'not: negación', 'EN': 'not: negation'},
                    'task': {'ES': 'Si la cara no está resuelta, aplica un algoritmo. ¿Qué condición usa not '
                                   'correctamente?',
                             'EN': 'If the face is not solved, apply an algorithm. Which condition uses not '
                                   'correctly?'},
                    'code': ['cara_resuelta = False'],
                    'options': {'ES': ['if not cara_resuelta: algoritmo()',
                                       'if cara_resuelta not: algoritmo()',
                                       'if no cara_resuelta: algoritmo()'],
                                'EN': ['if not face_solved: algorithm()',
                                       'if face_solved not: algorithm()',
                                       'if no face_solved: algorithm()']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: not invierte un valor booleano.',
                                 'EN': 'Correct: not reverses a Boolean value.'},
                    'moves': ['R', 'U', "R'"]},
                   {'concept': {'ES': 'Comparación numérica', 'EN': 'Numeric comparison'},
                    'task': {'ES': 'Si hay menos de 9 blancos arriba, sigue buscando. ¿Qué condición es válida?',
                             'EN': 'If there are fewer than 9 whites on top, keep searching. Which condition is '
                                   'valid?'},
                    'code': ['blancos = contar(cubo["U"], "Blanco")'],
                    'options': {'ES': ['if blancos < 9: giro_U()',
                                       'if blancos => 9: giro_U()',
                                       'if blancos menor 9: giro_U()'],
                                'EN': ['if whites < 9: turn_U()',
                                       'if whites => 9: turn_U()',
                                       'if whites less 9: turn_U()']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: < compara si un número es menor que otro.',
                                 'EN': 'Correct: < checks whether a number is smaller.'},
                    'moves': ['U']},
                   {'concept': {'ES': 'Booleanos', 'EN': 'Booleans'},
                    'task': {'ES': 'Una función devuelve True si el cubo está resuelto. ¿Qué if es más limpio?',
                             'EN': 'A function returns True if the cube is solved. Which if is cleanest?'},
                    'code': ['resuelto = cubo_resuelto()'],
                    'options': {'ES': ['if resuelto: felicitar()',
                                       'if resuelto == "True": felicitar()',
                                       'if resuelto = True: felicitar()'],
                                'EN': ['if solved: celebrate()',
                                       'if solved == "True": celebrate()',
                                       'if solved = True: celebrate()']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: un booleano puede usarse directamente en if.',
                                 'EN': 'Correct: a Boolean can be used directly in if.'},
                    'moves': ['D']},
                   {'concept': {'ES': 'Orden de decisiones', 'EN': 'Decision order'},
                    'task': {'ES': 'Primero revisa si está resuelto; si no, calcula guía. ¿Qué opción respeta ese '
                                   'orden?',
                             'EN': 'First check if solved; if not, compute guide. Which option follows that order?'},
                    'code': ['resuelto = cubo_resuelto()'],
                    'options': {'ES': ['if resuelto: mostrar_ok() else: calcular_guia()',
                                       'else: calcular_guia() if resuelto',
                                       'if calcular_guia(): resuelto else: ok'],
                                'EN': ['if solved: show_ok() else: compute_guide()',
                                       'else: compute_guide() if solved',
                                       'if compute_guide(): solved else: ok']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: if/else separa los dos caminos lógicos.',
                                 'EN': 'Correct: if/else separates the two logical paths.'},
                    'moves': ['F2']},
                   {'concept': {'ES': 'Condición compuesta', 'EN': 'Compound condition'},
                    'task': {'ES': 'Solo quieres girar R si el color es rojo y la cara activa es derecha. ¿Qué '
                                   'condición es correcta?',
                             'EN': 'You only want to turn R if the color is red and the active face is right. Which '
                                   'condition is correct?'},
                    'code': ['color = "Rojo"', 'cara = "R"'],
                    'options': {'ES': ['if color == "Rojo" and cara == "R": giro_R()',
                                       'if color = "Rojo" and cara = "R": giro_R()',
                                       'if color == "Rojo" or cara == "F": giro_R()'],
                                'EN': ['if color == "Red" and face == "R": turn_R()',
                                       'if color = "Red" and face = "R": turn_R()',
                                       'if color == "Red" or face == "F": turn_R()']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: se combinan dos comparaciones con and.',
                                 'EN': 'Correct: combine two comparisons with and.'},
                    'moves': ['R2']}]},
 3: {'name': {'ES': 'Nivel 3 - Bucles Algorítmicos', 'EN': 'Level 3 - Algorithmic Loops'},
     'goal': {'ES': 'Automatiza movimientos como en Karel: usa for, while, range, break y funciones repetibles.',
              'EN': 'Automate moves like Karel: use for, while, range, break, and reusable functions.'},
     'questions': [{'concept': {'ES': 'for: recorrer giros', 'EN': 'for: iterate through turns'},
                    'task': {'ES': 'Quieres ejecutar R U R_prima U_prima. ¿Qué bucle recorre la lista?',
                             'EN': 'You want to execute R U R_prime U_prime. Which loop iterates through the list?'},
                    'code': ['algoritmo = ["R", "U", "R_prima", "U_prima"]'],
                    'options': {'ES': ['for giro in algoritmo: ejecutar(giro)',
                                       'for algoritmo in giro: ejecutar(algoritmo)',
                                       'if giro in algoritmo: ejecutar(for)'],
                                'EN': ['for turn in algorithm: execute(turn)',
                                       'for algorithm in turn: execute(algorithm)',
                                       'if turn in algorithm: execute(for)']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: for toma cada giro de la lista y lo ejecuta.',
                                 'EN': 'Correct: for takes each turn from the list and executes it.'},
                    'moves': ['R', 'U', "R'", "U'"]},
                   {'concept': {'ES': 'range: repetir N veces', 'EN': 'range: repeat N times'},
                    'task': {'ES': 'El algoritmo debe repetirse 6 veces. ¿Qué código lo expresa?',
                             'EN': 'The algorithm must repeat 6 times. Which code expresses that?'},
                    'code': ['algoritmo_base = ["R", "U", "R_prima", "U_prima"]'],
                    'options': {'ES': ['for _ in range(6): ejecutar(algoritmo_base)',
                                       'range(6) for ejecutar(algoritmo_base)',
                                       'while range == 6: algoritmo_base()'],
                                'EN': ['for _ in range(6): execute(base_algorithm)',
                                       'range(6) for execute(base_algorithm)',
                                       'while range == 6: base_algorithm()']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: range(6) genera seis repeticiones.',
                                 'EN': 'Correct: range(6) produces six repetitions.'},
                    'moves': ['R', 'U', "R'", "U'", 'R', 'U']},
                   {'concept': {'ES': 'while: meta pendiente', 'EN': 'while: pending goal'},
                    'task': {'ES': 'Quieres seguir girando hasta que haya 9 blancos arriba. ¿Qué while es correcto?',
                             'EN': 'You want to keep turning until there are 9 whites on top. Which while is correct?'},
                    'code': ['contar_blancos(cubo["U"])'],
                    'options': {'ES': ['while contar_blancos(cubo["U"]) < 9: siguiente_giro()',
                                       'while contar_blancos(cubo["U"]) = 9: parar()',
                                       'for contar_blancos < 9: while giro()'],
                                'EN': ['while count_whites(cubo["U"]) < 9: next_turn()',
                                       'while count_whites(cubo["U"]) = 9: stop()',
                                       'for count_whites < 9: while turn()']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: while repite mientras la condición sea verdadera.',
                                 'EN': 'Correct: while repeats while the condition is true.'},
                    'moves': ['U', 'R', "U'", "R'"]},
                   {'concept': {'ES': 'break: detener búsqueda', 'EN': 'break: stop search'},
                    'task': {'ES': 'Buscas la primera arista blanca y quieres detener el bucle al encontrarla. ¿Qué '
                                   'palabra usas?',
                             'EN': 'You search for the first white edge and want to stop the loop when found. Which '
                                   'keyword do you use?'},
                    'code': ['for arista in aristas:', '    if "Blanco" in arista:'],
                    'options': {'ES': ['break', 'continue forever', 'stop for'],
                                'EN': ['break', 'continue forever', 'stop for']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: break sale del bucle inmediatamente.',
                                 'EN': 'Correct: break exits the loop immediately.'},
                    'moves': ['F']},
                   {'concept': {'ES': 'continue: saltar caso', 'EN': 'continue: skip case'},
                    'task': {'ES': 'Quieres ignorar centros porque no se mueven y seguir con la siguiente pieza. ¿Qué '
                                   'palabra sirve?',
                             'EN': 'You want to ignore centers because they do not move and continue to the next '
                                   'piece. Which keyword works?'},
                    'code': ['for pieza in piezas:', '    if pieza.tipo == "centro":'],
                    'options': {'ES': ['continue', 'break', 'return False'],
                                'EN': ['continue', 'break', 'return False']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: continue salta al siguiente ciclo del bucle.',
                                 'EN': 'Correct: continue jumps to the next loop cycle.'},
                    'moves': ['D']},
                   {'concept': {'ES': 'enumerate', 'EN': 'enumerate'},
                    'task': {'ES': 'Necesitas índice y valor de cada sticker. ¿Qué bucle usa enumerate correctamente?',
                             'EN': 'You need index and value of each sticker. Which loop uses enumerate correctly?'},
                    'code': ['fila = ["B", "R", "V"]'],
                    'options': {'ES': ['for i, color in enumerate(fila): revisar(i, color)',
                                       'for color, i in fila: revisar(i, color)',
                                       'enumerate for fila: revisar()'],
                                'EN': ['for i, color in enumerate(row): check(i, color)',
                                       'for color, i in row: check(i, color)',
                                       'enumerate for row: check()']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: enumerate entrega índice y elemento.',
                                 'EN': 'Correct: enumerate gives index and element.'},
                    'moves': ['L']},
                   {'concept': {'ES': 'Bucle anidado', 'EN': 'Nested loop'},
                    'task': {'ES': 'Para revisar una cara 3x3 necesitas recorrer filas y columnas. ¿Qué estructura es '
                                   'correcta?',
                             'EN': 'To inspect a 3x3 face you must loop through rows and columns. Which structure is '
                                   'correct?'},
                    'code': ['cara = cubo["F"]'],
                    'options': {'ES': ['for fila in cara: for color in fila: revisar(color)',
                                       'for color in cara[3][3]: revisar(color)',
                                       'while fila in color in cara'],
                                'EN': ['for row in face: for color in row: check(color)',
                                       'for color in face[3][3]: check(color)',
                                       'while row in color in face']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: un bucle recorre filas y otro recorre colores.',
                                 'EN': 'Correct: one loop walks rows and another walks colors.'},
                    'moves': ['F2']},
                   {'concept': {'ES': 'Función que ejecuta algoritmo', 'EN': 'Function that runs algorithm'},
                    'task': {'ES': 'Quieres reutilizar secuencias. ¿Qué definición de función es válida?',
                             'EN': 'You want to reuse sequences. Which function definition is valid?'},
                    'code': ['algoritmo = ["R", "U", "R_prima"]'],
                    'options': {'ES': ['def ejecutar_algoritmo(lista): for giro in lista: ejecutar(giro)',
                                       'function ejecutar_algoritmo(lista): ejecutar(lista)',
                                       'def ejecutar_algoritmo = lista: ejecutar()'],
                                'EN': ['def run_algorithm(list_): for turn in list_: execute(turn)',
                                       'function run_algorithm(list_): execute(list_)',
                                       'def run_algorithm = list_: execute()']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: def crea una función reutilizable.',
                                 'EN': 'Correct: def creates a reusable function.'},
                    'moves': ['R', 'U', "R'"]},
                   {'concept': {'ES': 'Acumulador', 'EN': 'Accumulator'},
                    'task': {'ES': 'Quieres contar stickers blancos. ¿Qué patrón de acumulador es correcto?',
                             'EN': 'You want to count white stickers. Which accumulator pattern is correct?'},
                    'code': ['contador = 0'],
                    'options': {'ES': ['if color == "Blanco": contador += 1',
                                       'if color == "Blanco": contador = 1 siempre',
                                       'contador += "Blanco"'],
                                'EN': ['if color == "White": counter += 1',
                                       'if color == "White": counter = 1 always',
                                       'counter += "White"']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: += 1 aumenta el contador cada vez que aparece blanco.',
                                 'EN': 'Correct: += 1 increases the counter each time white appears.'},
                    'moves': ['U']},
                   {'concept': {'ES': 'Lista por comprensión', 'EN': 'List comprehension'},
                    'task': {'ES': 'Quieres quedarte solo con giros de la cara U. ¿Qué comprensión es válida?',
                             'EN': 'You want to keep only turns from the U face. Which comprehension is valid?'},
                    'code': ['algoritmo = ["U", "R", "U2", "F"]'],
                    'options': {'ES': ['giros_u = [g for g in algoritmo if g.startswith("U")]',
                                       'giros_u = for g in algoritmo if U',
                                       'giros_u = algoritmo.startswith("U")'],
                                'EN': ['u_turns = [t for t in algorithm if t.startswith("U")]',
                                       'u_turns = for t in algorithm if U',
                                       'u_turns = algorithm.startswith("U")']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: filtra los elementos que empiezan con U.',
                                 'EN': 'Correct: it filters elements that start with U.'},
                    'moves': ['U2']},
                   {'concept': {'ES': 'while con límite', 'EN': 'while with limit'},
                    'task': {'ES': 'Para evitar bucle infinito, agregas un máximo de intentos. ¿Qué condición es '
                                   'segura?',
                             'EN': 'To avoid an infinite loop, you add a maximum number of attempts. Which condition '
                                   'is safe?'},
                    'code': ['intentos = 0', 'max_intentos = 20'],
                    'options': {'ES': ['while not resuelto and intentos < max_intentos: intentar()',
                                       'while not resuelto or intentos < infinito: intentar()',
                                       'while intentos = max_intentos: intentar()'],
                                'EN': ['while not solved and attempts < max_attempts: try_move()',
                                       'while not solved or attempts < infinity: try_move()',
                                       'while attempts = max_attempts: try_move()']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: combina meta pendiente y límite de seguridad.',
                                 'EN': 'Correct: it combines a pending goal and a safety limit.'},
                    'moves': ['B']},
                   {'concept': {'ES': 'Depuración', 'EN': 'Debugging'},
                    'task': {'ES': 'El cubo no cambia como esperabas. ¿Qué línea ayuda a ver el giro actual?',
                             'EN': 'The cube does not change as expected. Which line helps you see the current turn?'},
                    'code': ['giro_actual = "R"'],
                    'options': {'ES': ['print(f"Ejecutando {giro_actual}")',
                                       'delete(giro_actual)',
                                       'while print = giro_actual'],
                                'EN': ['print(f"Executing {current_turn}")',
                                       'delete(current_turn)',
                                       'while print = current_turn']},
                    'answer': 0,
                    'feedback': {'ES': 'Correcto: imprimir estados intermedios ayuda a depurar.',
                                 'EN': 'Correct: printing intermediate states helps debugging.'},
                    'moves': ['R2']}]}}



# ============================================================
# UTILIDADES DE TEXTO, BOTONES Y PERSISTENCIA
# ============================================================

def load_scores() -> Dict[str, object]:
    default = {"expert_best": None, "arcade_high": {"1": 0, "2": 0, "3": 0}, "arcade_completed": []}
    try:
        if SCORE_FILE.exists():
            with SCORE_FILE.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            default.update(data)
    except Exception:
        pass
    return default


def save_scores(data: Dict[str, object]) -> None:
    try:
        with SCORE_FILE.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
    except Exception:
        pass


def inverse_move(move: str) -> str:
    move = move.strip()
    if not move:
        return move
    if move.endswith("2"):
        return move
    if move.endswith("'"):
        return move[:-1]
    return move + "'"


def inverse_algorithm(moves: List[str]) -> List[str]:
    return [inverse_move(mv) for mv in reversed(moves)]


def parse_algorithm(algo: str) -> List[str]:
    return [part.strip() for part in algo.replace("\n", " ").split(" ") if part.strip()]


def normalize_move(move: str) -> Tuple[str, int]:
    move = move.strip()
    if not move:
        raise ValueError("Movimiento vacío")
    face = move[0]
    if face not in "URFDLB":
        raise ValueError(f"Movimiento no soportado: {move}")
    if move.endswith("2"):
        turns = 2
    elif move.endswith("'"):
        turns = -1
    else:
        turns = 1
    return face, turns


def wrap_text(font: pygame.font.Font, text: str, max_width: int) -> List[str]:
    words = text.split()
    lines: List[str] = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(surface: pygame.Surface, font: pygame.font.Font, text: str, color: Tuple[int, int, int],
                 x: int, y: int, max_width: int, line_gap: int = 5, max_lines: Optional[int] = None) -> int:
    lines = wrap_text(font, text, max_width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        surface.blit(font.render(line, True, color), (x, y))
        y += font.get_height() + line_gap
    return y


def draw_button(surface: pygame.Surface, font: pygame.font.Font, rect: pygame.Rect, label: str,
                bg: Tuple[int, int, int], fg: Tuple[int, int, int] = (255, 255, 255),
                border: Optional[Tuple[int, int, int]] = None, radius: int = 6) -> pygame.Rect:
    pygame.draw.rect(surface, bg, rect, border_radius=radius)
    if border:
        pygame.draw.rect(surface, border, rect, width=2, border_radius=radius)
    text_surface = font.render(label, True, fg)
    surface.blit(text_surface, (rect.centerx - text_surface.get_width() // 2,
                                rect.centery - text_surface.get_height() // 2))
    return rect


def safe_render(font: pygame.font.Font, text: str, color: Tuple[int, int, int]) -> pygame.Surface:
    return font.render(text, True, color)


# ============================================================
# MODELO DE CUBO 3x3 CON ROTACIONES FÍSICAS BÁSICAS
# ============================================================

Vec3 = Tuple[int, int, int]
Sticker = Dict[str, object]


def rotate_vec(v: Vec3, axis: Vec3, quarter_turns: int) -> Vec3:
    """Rota un vector 90 grados por turnos alrededor de un eje cardinal."""
    x, y, z = v
    ax, ay, az = axis
    q = quarter_turns % 4
    for _ in range(q):
        if ax == 1:
            x, y, z = x, -z, y
        elif ax == -1:
            x, y, z = x, z, -y
        elif ay == 1:
            x, y, z = z, y, -x
        elif ay == -1:
            x, y, z = -z, y, x
        elif az == 1:
            x, y, z = -y, x, z
        elif az == -1:
            x, y, z = y, -x, z
    return int(x), int(y), int(z)


FACE_SPECS = {
    # face: normal, positions in displayed order
    "U": ((0, 1, 0), lambda r, c: (c - 1, 1, r - 1)),
    "D": ((0, -1, 0), lambda r, c: (c - 1, -1, 1 - r)),
    "F": ((0, 0, 1), lambda r, c: (c - 1, 1 - r, 1)),
    "B": ((0, 0, -1), lambda r, c: (1 - c, 1 - r, -1)),
    "R": ((1, 0, 0), lambda r, c: (1, 1 - r, 1 - c)),
    "L": ((-1, 0, 0), lambda r, c: (-1, 1 - r, c - 1)),
}

MOVE_AXIS_LAYER = {
    "U": ((0, 1, 0), 1),
    "D": ((0, -1, 0), -1),
    "F": ((0, 0, 1), 1),
    "B": ((0, 0, -1), -1),
    "R": ((1, 0, 0), 1),
    "L": ((-1, 0, 0), -1),
}


def axis_coordinate_index(axis: Vec3) -> int:
    if axis[0] != 0:
        return 0
    if axis[1] != 0:
        return 1
    return 2


class CubeModel:
    def __init__(self) -> None:
        self.stickers: List[Sticker] = []
        self.reset()

    def reset(self) -> None:
        self.stickers = []
        for face in FACE_DRAW_ORDER:
            normal, pos_fun = FACE_SPECS[face]
            for r in range(3):
                for c in range(3):
                    self.stickers.append({
                        "pos": pos_fun(r, c),
                        "normal": normal,
                        "color": FACE_TO_COLOR[face],
                    })

    def clone(self) -> "CubeModel":
        other = CubeModel()
        other.stickers = [dict(st) for st in self.stickers]
        return other

    def find_sticker(self, pos: Vec3, normal: Vec3) -> Optional[Sticker]:
        for st in self.stickers:
            if st["pos"] == pos and st["normal"] == normal:
                return st
        return None

    def set_facelet_color(self, face: str, index: int, color: str) -> None:
        r, c = divmod(index, 3)
        normal, pos_fun = FACE_SPECS[face]
        sticker = self.find_sticker(pos_fun(r, c), normal)
        if sticker:
            sticker["color"] = color

    def facelets(self) -> Dict[str, List[str]]:
        faces: Dict[str, List[str]] = {}
        for face in FACE_DRAW_ORDER:
            normal, pos_fun = FACE_SPECS[face]
            arr: List[str] = []
            for r in range(3):
                for c in range(3):
                    st = self.find_sticker(pos_fun(r, c), normal)
                    arr.append(str(st["color"]) if st else "?")
            faces[face] = arr
        return faces

    def apply_move(self, move: str) -> None:
        face, turns = normalize_move(move)
        axis, layer_value = MOVE_AXIS_LAYER[face]
        # Clockwise as viewed from outside is approximated as -1 around the face normal.
        quarter_turns = -turns
        idx = axis_coordinate_index(axis)
        for st in self.stickers:
            pos = st["pos"]
            if isinstance(pos, tuple) and pos[idx] == layer_value:
                st["pos"] = rotate_vec(pos, axis, quarter_turns)
                st["normal"] = rotate_vec(st["normal"], axis, quarter_turns)  # type: ignore[arg-type]

    def apply_algorithm(self, moves: Iterable[str]) -> None:
        for move in moves:
            self.apply_move(move)

    def is_solved(self) -> bool:
        faces = self.facelets()
        return all(all(color == FACE_TO_COLOR[face] for color in faces[face]) for face in FACE_DRAW_ORDER)

    def counts(self) -> Dict[str, int]:
        result = {"W": 0, "O": 0, "G": 0, "R": 0, "B": 0, "Y": 0}
        for arr in self.facelets().values():
            for color in arr:
                if color in result:
                    result[color] += 1
        return result

    def to_kociemba_string(self) -> Tuple[bool, str, str]:
        counts = self.counts()
        if any(counts[color] != 9 for color in counts):
            return False, "", "bad_counts"
        faces = self.facelets()
        face_string = ""
        for face in FACE_ORDER_KOCIEMBA:
            for color in faces[face]:
                if color not in COLOR_TO_FACE:
                    return False, "", "bad_counts"
                face_string += COLOR_TO_FACE[color]
        return True, face_string, "ok"


# ============================================================
# APLICACIÓN PRINCIPAL
# ============================================================

class RubikCapstoneApp:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Ecosistema Rubik 3x3")
        self.clock = pygame.time.Clock()

        self.lang = "ES"
        self.state = "CARATULA"
        self.cube = CubeModel()
        self.selected_color = "W"
        self.solution_steps: List[str] = []
        self.solution_index = 0
        self.solution_message = ""
        self.machine_time = 0.0
        self.machine_solution_len = 0
        self.machine_finished = False

        self.beginner_lesson = 0
        self.manual_lesson = 0
        self.expert_tip = 0
        self.timer_running = False
        self.user_time = 0.0
        self.challenge_message = ""

        self.pattern_index = -1
        self.pattern_steps: List[str] = []
        self.pattern_cursor = 0
        self.pattern_mode = "build"
        self.pattern_catalog_open = True

        self.arcade_world = 1
        self.arcade_elapsed = 0.0
        self.arcade_score = 0
        self.arcade_game_over = False
        self.arcade_victory = False
        self.arcade_obstacles: List[Dict[str, object]] = []
        self.arcade_spawn_timer = 1.0
        self.script_question_index = 0
        self.script_selected_option: Optional[int] = None
        self.script_feedback = ""
        self.script_answered = False
        self.script_level_complete = False
        self.player_y = 630.0
        self.player_vy = 0.0
        self.player_on_ground = True
        self.player_angle = 0.0
        self.player_colors = ["W", "R", "B", "G", "O", "Y", "W", "R", "B"]

        self.scores = load_scores()

        random.seed(27)
        self.bg_squares = [
            (random.randint(0, WIDTH), random.randint(0, HEIGHT), random.choice(["W", "O", "G", "R", "B", "Y"]))
            for _ in range(100)
        ]

        self.font_xs = pygame.font.SysFont("Courier", 12, bold=True)
        self.font_sm = pygame.font.SysFont("Courier", 14, bold=True)
        self.font_md = pygame.font.SysFont("Helvetica", 16, bold=True)
        self.font_lg = pygame.font.SysFont("Helvetica", 23, bold=True)
        self.font_xl = pygame.font.SysFont("Helvetica", 30, bold=True)
        self.font_title = pygame.font.SysFont("Helvetica", 40, bold=True)

        self.rects: Dict[str, pygame.Rect] = {}
        self.sticker_rects: List[Tuple[pygame.Rect, str, int]] = []

    # --------------------------------------------------------
    # DIBUJO COMÚN
    # --------------------------------------------------------
    def t(self, key: str) -> str:
        return TEXT[self.lang][key]

    def draw_background(self) -> None:
        self.screen.fill(COLOR_MAP["BG"])
        for i, (x, y, code) in enumerate(self.bg_squares):
            size = 8 + (i % 3) * 3
            pygame.draw.rect(self.screen, COLOR_MAP[code], (x, y, size, size), border_radius=2)

    def draw_top_language(self) -> None:
        self.rects["lang_es"] = draw_button(
            self.screen, self.font_sm, pygame.Rect(1020, 22, 70, 30), "ES",
            COLOR_MAP["SUCCESS"] if self.lang == "ES" else (64, 64, 76)
        )
        self.rects["lang_en"] = draw_button(
            self.screen, self.font_sm, pygame.Rect(1100, 22, 70, 30), "EN",
            COLOR_MAP["B"] if self.lang == "EN" else (64, 64, 76)
        )

    def draw_card(self, rect: pygame.Rect, title: str, body: str, color: Tuple[int, int, int]) -> pygame.Rect:
        pygame.draw.rect(self.screen, COLOR_MAP["PANEL"], rect, border_radius=12)
        pygame.draw.rect(self.screen, color, rect, width=2, border_radius=12)
        title_font = self.font_lg
        if title_font.size(title)[0] > rect.width - 44:
            title_font = self.font_md
        self.screen.blit(title_font.render(title, True, color), (rect.x + 20, rect.y + 18))
        draw_wrapped(self.screen, self.font_md, body, COLOR_MAP["TEXT"], rect.x + 20, rect.y + 56, rect.width - 40, 5, max_lines=3)
        return rect

    def draw_wire_cube(self, x: int, y: int, size: int = 105, tick: float = 0.0) -> None:
        """Cubo 3D-lite solo con bordes: sin stickers ni colores internos."""
        half = size // 2
        pulse = int(4 * math.sin(tick * 2.0))
        front = [
            (x - half, y - half + pulse),
            (x + half, y - half + pulse),
            (x + half, y + half + pulse),
            (x - half, y + half + pulse),
        ]
        dx, dy = 42, -34
        back = [(px + dx, py + dy) for px, py in front]
        edges = [
            (front[0], front[1]), (front[1], front[2]), (front[2], front[3]), (front[3], front[0]),
            (back[0], back[1]), (back[1], back[2]), (back[2], back[3]), (back[3], back[0]),
            (front[0], back[0]), (front[1], back[1]), (front[2], back[2]), (front[3], back[3]),
        ]
        for a, b in edges:
            pygame.draw.line(self.screen, COLOR_MAP["NEON"], a, b, 2)


    def _quad_point(self, quad: List[Tuple[int, int]], u: float, v: float) -> Tuple[int, int]:
        """Interpolación bilineal dentro de un cuadrilátero para dibujar caras 3D."""
        q0, q1, q2, q3 = quad
        x = (1-u)*(1-v)*q0[0] + u*(1-v)*q1[0] + u*v*q2[0] + (1-u)*v*q3[0]
        y = (1-u)*(1-v)*q0[1] + u*(1-v)*q1[1] + u*v*q2[1] + (1-u)*v*q3[1]
        return int(x), int(y)

    def _draw_projected_face(self, quad: List[Tuple[int, int]], colors: List[str], border_color: Tuple[int, int, int] = (16, 16, 20)) -> None:
        """Dibuja una cara 3x3 proyectada en perspectiva."""
        for r in range(3):
            for c in range(3):
                u0, u1 = c / 3, (c + 1) / 3
                v0, v1 = r / 3, (r + 1) / 3
                cell = [
                    self._quad_point(quad, u0, v0),
                    self._quad_point(quad, u1, v0),
                    self._quad_point(quad, u1, v1),
                    self._quad_point(quad, u0, v1),
                ]
                code = colors[r * 3 + c]
                pygame.draw.polygon(self.screen, COLOR_MAP.get(code, COLOR_MAP["MUTED"]), cell)
                pygame.draw.polygon(self.screen, border_color, cell, width=2)

    def draw_colored_cover_cube(self, x: int, y: int, size: int = 132, tick: float = 0.0) -> None:
        """Cubo de carátula bien proporcionado: solo cambia la cara frontal 3x3; las otras caras son bordes."""
        half = size // 2
        dx, dy = 34, -30
        colors = ["W", "O", "G", "R", "B", "Y"]
        shift = int(tick * 1.8) % len(colors)

        front = [(x - half, y - half), (x + half, y - half), (x + half, y + half), (x - half, y + half)]
        back = [(px + dx, py + dy) for px, py in front]
        right = [front[1], back[1], back[2], front[2]]
        top = [front[0], front[1], back[1], back[0]]

        # Bordes de profundidad primero.
        for quad in (right, top):
            pygame.draw.polygon(self.screen, (29, 29, 37), quad)
            pygame.draw.polygon(self.screen, COLOR_MAP["NEON"], quad, width=2)

        # Cara frontal: única cara con stickers dinámicos.
        face_colors = [colors[(i + shift) % len(colors)] for i in range(9)]
        self._draw_projected_face(front, face_colors)

        edges = [
            (front[0], front[1]), (front[1], front[2]), (front[2], front[3]), (front[3], front[0]),
            (back[0], back[1]), (back[1], back[2]), (back[2], back[3]), (back[3], back[0]),
            (front[0], back[0]), (front[1], back[1]), (front[2], back[2]), (front[3], back[3]),
        ]
        for a, b in edges:
            pygame.draw.line(self.screen, COLOR_MAP["NEON"], a, b, 2)

    def draw_move_cube(self, x: int, y: int, size: int = 130, move: Optional[str] = None) -> None:
        """Visor 3D pedagógico: cubo Rubik 3x3 real con stickers visibles.

        - Si `move` es None, el cubo se muestra neutro, sin marcar ninguna cara.
        - Si `move` existe, la capa activa se marca con el color de su centro.
        """
        half = size // 2
        dx, dy = int(size * 0.34), -int(size * 0.28)
        front = [(x - half, y - half), (x + half, y - half), (x + half, y + half), (x - half, y + half)]
        back = [(px + dx, py + dy) for px, py in front]
        top = [front[0], front[1], back[1], back[0]]
        right = [front[1], back[1], back[2], front[2]]

        # Siempre dibujar un cubo 3x3 real: top, derecha y frente con stickers.
        faces = self.cube.facelets()
        self._draw_projected_face(top, faces.get("U", ["W"] * 9), border_color=(12, 12, 16))
        self._draw_projected_face(right, faces.get("R", ["R"] * 9), border_color=(12, 12, 16))
        self._draw_projected_face(front, faces.get("F", ["G"] * 9), border_color=(12, 12, 16))

        edges = [
            (front[0], front[1]), (front[1], front[2]), (front[2], front[3]), (front[3], front[0]),
            (back[0], back[1]), (back[1], back[2]), (back[2], back[3]), (back[3], back[0]),
            (front[0], back[0]), (front[1], back[1]), (front[2], back[2]), (front[3], back[3]),
        ]
        for a, b in edges:
            pygame.draw.line(self.screen, COLOR_MAP["NEON"], a, b, 2)

        if not move:
            neutral = "Cubo listo" if self.lang == "ES" else "Cube ready"
            label = self.font_md.render(neutral, True, COLOR_MAP["MUTED"])
            self.screen.blit(label, (x - label.get_width() // 2, y + half + 22))
            return

        face = move[0]
        active = COLOR_MAP.get(FACE_TO_COLOR.get(face, "W"), COLOR_MAP["ALERT"])
        # Caras visibles exactas; las ocultas se indican mediante el plano exterior correspondiente.
        if face == "F":
            poly = front
        elif face == "U":
            poly = top
        elif face == "R":
            poly = right
        elif face == "D":
            poly = [front[3], front[2], (front[2][0] + dx, front[2][1] + dy), (front[3][0] + dx, front[3][1] + dy)]
        elif face == "L":
            poly = [front[0], (front[0][0] + dx, front[0][1] + dy), (front[3][0] + dx, front[3][1] + dy), front[3]]
        else:  # B
            poly = back
        pygame.draw.polygon(self.screen, active, poly, width=6)
        pygame.draw.polygon(self.screen, (255, 255, 255), poly, width=1)
        label = self.font_lg.render(move, True, active)
        self.screen.blit(label, (x - label.get_width() // 2, y + half + 24))

    def draw_palette(self, x: int, y: int, w: int = 150) -> None:
        pygame.draw.rect(self.screen, COLOR_MAP["PANEL"], (x, y, w, 430), border_radius=8)
        self.screen.blit(self.font_md.render(self.t("palette"), True, COLOR_MAP["ALERT"]), (x + 18, y + 14))
        self.rects["palette"] = pygame.Rect(x, y, w, 430)
        for idx, code in enumerate(["W", "O", "G", "R", "B", "Y"]):
            yy = y + 50 + idx * 61
            if self.selected_color == code:
                pygame.draw.rect(self.screen, (255, 255, 255), (x + 14, yy - 3, w - 28, 45), border_radius=6)
            rect = pygame.Rect(x + 20, yy, w - 40, 39)
            self.rects[f"color_{code}"] = pygame.draw.rect(self.screen, COLOR_MAP[code], rect, border_radius=5)
            label_color = (10, 10, 10) if code in ["W", "Y"] else (255, 255, 255)
            self.screen.blit(self.font_sm.render(COLOR_NAMES[self.lang][code], True, label_color), (rect.x + 12, rect.y + 11))

    def draw_cube_net(self, base_x: int, base_y: int, face_w: int = 156, editable: bool = True) -> None:
        faces = self.cube.facelets()
        self.sticker_rects = []
        st = face_w // 3
        for face, (gx, gy) in GRID_POSITIONS.items():
            sx = base_x + gx * (face_w + 13)
            sy = base_y + gy * (face_w + 13)
            pygame.draw.rect(self.screen, (8, 8, 12), (sx, sy, face_w, face_w), border_radius=5)
            label = f"{face} / {COLOR_NAMES[self.lang][FACE_TO_COLOR[face]]}"
            self.screen.blit(self.font_xs.render(label, True, COLOR_MAP["MUTED"]), (sx, sy - 17))
            for idx, color in enumerate(faces[face]):
                r, c = divmod(idx, 3)
                rect = pygame.Rect(sx + c * st + 1, sy + r * st + 1, st - 2, st - 2)
                pygame.draw.rect(self.screen, COLOR_MAP.get(color, (100, 100, 100)), rect, border_radius=3)
                pygame.draw.rect(self.screen, (20, 20, 22), rect, width=1, border_radius=3)
                if editable:
                    self.sticker_rects.append((rect, face, idx))

    def draw_solution_panel(self, rect: pygame.Rect, simple_language: bool = True) -> None:
        """Panel inferior amplio con doble lectura: lenguaje sencillo y clave técnica."""
        pygame.draw.rect(self.screen, COLOR_MAP["PANEL2"], rect, border_radius=9)
        pygame.draw.rect(self.screen, COLOR_MAP["BORDER"], rect, width=1, border_radius=9)

        if self.solution_message:
            color = COLOR_MAP["DANGER"] if "Revisa" in self.solution_message or "Falta" in self.solution_message or "Missing" in self.solution_message else COLOR_MAP["ALERT"]
            draw_wrapped(self.screen, self.font_lg, self.solution_message, color, rect.x + 25, rect.y + 35, rect.width - 50, 8)
            return

        if not self.solution_steps:
            msg = self.t("guide_empty") if simple_language else self.t("guide_empty_expert")
            draw_wrapped(self.screen, self.font_lg, msg, COLOR_MAP["MUTED"], rect.x + 25, rect.y + 45, rect.width - 50, 8)
            return

        total = len(self.solution_steps)
        current = self.solution_steps[self.solution_index]
        self.draw_dual_command_panel(rect, current, self.solution_index, total, simple_language=simple_language)

    def draw_dual_command_panel(self, rect: pygame.Rect, current: str, index: int, total: int, simple_language: bool = True) -> None:
        """Panel limpio: solo lenguaje sencillo, badge del movimiento y progreso arriba a la derecha."""
        face = current[0]
        color_code = FACE_TO_COLOR.get(face, "W")
        color_name = COLOR_NAMES[self.lang].get(color_code, color_code)
        active = COLOR_MAP[color_code]

        # Modo compacto para patrones: el comando debe verse completo aunque la ventana tenga barra de tareas.
        if rect.height <= 125:
            progress_text = f"PASO {index + 1} de {total}" if self.lang == "ES" else f"STEP {index + 1} of {total}"
            progress_rect = pygame.Rect(rect.right - 172, rect.y + 2, 154, 30)
            pygame.draw.rect(self.screen, (28, 28, 39), progress_rect, border_radius=7)
            pygame.draw.rect(self.screen, active, progress_rect, width=2, border_radius=7)
            progress_surface = self.font_sm.render(progress_text, True, COLOR_MAP["SUCCESS"])
            self.screen.blit(progress_surface, (progress_rect.centerx - progress_surface.get_width() // 2,
                                               progress_rect.centery - progress_surface.get_height() // 2))

            header_x = rect.x + 18
            header_y = rect.y + 20
            pygame.draw.circle(self.screen, active, (header_x + 13, header_y + 15), 13)
            pygame.draw.circle(self.screen, (255, 255, 255), (header_x + 13, header_y + 15), 13, width=2)
            move_label = f"{current} / {color_name}"
            self.screen.blit(self.font_md.render(move_label, True, active), (header_x + 36, header_y + 3))

            simple = MOVE_TEXT[self.lang].get(current, current)
            literal_title = "LENGUAJE SENCILLO" if self.lang == "ES" else "PLAIN LANGUAGE"
            btn_w, btn_h = 96, 36
            btn_prev_x = rect.right - 232
            btn_next_x = rect.right - 118
            text_x = rect.x + 172
            text_y = rect.y + 6
            text_w = max(500, btn_prev_x - text_x - 18)
            simple_box = pygame.Rect(text_x, text_y, text_w, 66)
            pygame.draw.rect(self.screen, (15, 72, 43), simple_box, border_radius=9)
            pygame.draw.rect(self.screen, COLOR_MAP["SUCCESS"], simple_box, width=2, border_radius=9)
            self.screen.blit(self.font_xs.render(literal_title, True, COLOR_MAP["ALERT"]), (simple_box.x + 12, simple_box.y + 8))
            draw_wrapped(self.screen, self.font_sm, simple, COLOR_MAP["TEXT"],
                         simple_box.x + 12, simple_box.y + 29, simple_box.width - 24, 2, max_lines=2)

            btn_y = rect.y + 40
            self.rects["sol_prev"] = draw_button(self.screen, self.font_xs, pygame.Rect(btn_prev_x, btn_y, 108, btn_h),
                                                 self.t("prev"), (65, 65, 78))
            self.rects["sol_next"] = draw_button(self.screen, self.font_xs, pygame.Rect(btn_next_x, btn_y, 108, btn_h),
                                                 self.t("next"), COLOR_MAP["SUCCESS"])
            return

        # Marcador de paso en la esquina superior derecha, como pidió el usuario.
        progress_text = f"PASO {index + 1} de {total}" if self.lang == "ES" else f"STEP {index + 1} of {total}"
        progress_w, progress_h = 188, 36
        progress_rect = pygame.Rect(rect.right - progress_w - 18, rect.y + 12, progress_w, progress_h)
        pygame.draw.rect(self.screen, (28, 28, 39), progress_rect, border_radius=8)
        pygame.draw.rect(self.screen, active, progress_rect, width=2, border_radius=8)
        progress_surface = self.font_md.render(progress_text, True, COLOR_MAP["SUCCESS"])
        self.screen.blit(progress_surface, (progress_rect.centerx - progress_surface.get_width() // 2,
                                           progress_rect.centery - progress_surface.get_height() // 2))

        # Encabezado del movimiento: pequeño, sin ocupar una columna completa.
        header_x = rect.x + 26
        header_y = rect.y + 18
        pygame.draw.circle(self.screen, active, (header_x + 16, header_y + 18), 15)
        pygame.draw.circle(self.screen, (255, 255, 255), (header_x + 16, header_y + 18), 15, width=2)
        move_label = f"{current} / {color_name}"
        self.screen.blit(self.font_lg.render(move_label, True, active), (header_x + 42, header_y + 5))

        # Texto principal: una sola caja grande para que no se corte.
        simple = MOVE_TEXT[self.lang].get(current, current)
        literal_title = "LENGUAJE SENCILLO" if self.lang == "ES" else "PLAIN LANGUAGE"
        nav_w = 210
        text_x = rect.x + 255
        text_y = rect.y + 48
        text_w = max(560, rect.width - 285 - nav_w)
        simple_box = pygame.Rect(text_x, text_y, text_w, 96)

        pygame.draw.rect(self.screen, (15, 72, 43), simple_box, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_MAP["SUCCESS"], simple_box, width=2, border_radius=10)
        self.screen.blit(self.font_sm.render(literal_title, True, COLOR_MAP["ALERT"]), (simple_box.x + 16, simple_box.y + 10))
        draw_wrapped(self.screen, self.font_lg, simple, COLOR_MAP["TEXT"],
                     simple_box.x + 16, simple_box.y + 38, simple_box.width - 32, 4, max_lines=2)

        # Navegación fija a la derecha, separada del texto.
        btn_w, btn_h = 92, 44
        btn_y = rect.y + 72
        btn_prev_x = rect.right - 205
        btn_next_x = rect.right - 105
        self.rects["sol_prev"] = draw_button(self.screen, self.font_xs, pygame.Rect(btn_prev_x - 18, btn_y, 110, btn_h),
                                             self.t("prev"), (65, 65, 78))
        self.rects["sol_next"] = draw_button(self.screen, self.font_xs, pygame.Rect(btn_next_x - 6, btn_y, 110, btn_h),
                                             self.t("next"), COLOR_MAP["SUCCESS"])

        hint = "Usa flechas o ESPACIO" if self.lang == "ES" else "Use arrows or SPACE"
        self.screen.blit(self.font_xs.render(hint, True, COLOR_MAP["MUTED"]), (btn_prev_x - 12, rect.y + 142))

    def reset_cube(self) -> None:
        self.cube.reset()
        self.solution_steps = []
        self.solution_index = 0
        self.solution_message = ""
        self.machine_time = 0.0
        self.machine_solution_len = 0
        self.machine_finished = False
        self.challenge_message = ""

    def generate_solution(self) -> bool:
        self.solution_steps = []
        self.solution_index = 0
        self.solution_message = ""
        self.machine_finished = False
        if not KOCIEMBA_AVAILABLE:
            self.solution_message = self.t("kociemba_missing")
            return False
        if self.cube.is_solved():
            self.solution_message = self.t("solved")
            return False
        ok, cube_string, status = self.cube.to_kociemba_string()
        if not ok:
            self.solution_message = self.t("bad_counts")
            return False
        try:
            start = pygame.time.get_ticks()
            solution = kociemba.solve(cube_string)  # type: ignore[union-attr]
            self.machine_time = (pygame.time.get_ticks() - start) / 1000.0
            self.solution_steps = parse_algorithm(solution)
            self.machine_solution_len = len(self.solution_steps)
            self.machine_finished = True
            return True
        except Exception:
            self.solution_message = self.t("invalid_cube")
            return False

    # --------------------------------------------------------
    # PANTALLAS
    # --------------------------------------------------------
    def draw_cover(self, tick: float) -> None:
        self.draw_background()
        self.draw_top_language()
        panel = pygame.Rect(55, 62, 1110, 720)
        pygame.draw.rect(self.screen, COLOR_MAP["PANEL"], panel, border_radius=14)
        pygame.draw.rect(self.screen, COLOR_MAP["BORDER"], panel, width=2, border_radius=14)

        self.screen.blit(self.font_title.render(self.t("title"), True, COLOR_MAP["TEXT"]), (95, 105))
        self.screen.blit(self.font_lg.render(self.t("subtitle"), True, COLOR_MAP["ALERT"]), (100, 158))

        # Información formal: separada y con suficiente alto para que no se corte.
        info = pygame.Rect(95, 220, 610, 142)
        pygame.draw.rect(self.screen, COLOR_MAP["PANEL2"], info, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_MAP["BORDER"], info, width=1, border_radius=8)
        self.screen.blit(self.font_md.render(self.t("project_info"), True, COLOR_MAP["TEXT"]), (info.x + 18, info.y + 18))
        draw_wrapped(self.screen, self.font_sm, self.t("author_info"), COLOR_MAP["TEXT"], info.x + 18, info.y + 55, info.width - 36, 5, max_lines=2)
        self.screen.blit(self.font_md.render(self.t("year_info"), True, COLOR_MAP["TEXT"]), (info.x + 18, info.y + 108))

        purpose = pygame.Rect(95, 390, 690, 116)
        pygame.draw.rect(self.screen, (55, 45, 20), purpose, border_radius=8)
        self.screen.blit(self.font_lg.render(self.t("purpose_title"), True, COLOR_MAP["ALERT"]), (purpose.x + 18, purpose.y + 14))
        draw_wrapped(self.screen, self.font_md, self.t("purpose_body"), COLOR_MAP["TEXT"], purpose.x + 18, purpose.y + 50, purpose.width - 36, 5, max_lines=3)

        # Cubo Rubik de colores en carátula: cambia de colores para dar vida al proyecto.
        self.draw_colored_cover_cube(905, 252, 128, tick)
        draw_wrapped(self.screen, self.font_sm, "3x3 • PyCharm/GitHub • Pygame", COLOR_MAP["MUTED"], 820, 430, 300, 4)

        bullets = [
            "Diagnóstico inicial: no sé armarlo / ya tengo experiencia.",
            "Manual separado: ¿qué es el cubo Rubik?",
            "Guía paso a paso con comandos sencillos y visor 3D.",
            "Reto con cronómetro, tiempo de máquina y récord personal.",
            "Patrones especiales y Rubik Script para aprender Python jugando.",
        ] if self.lang == "ES" else [
            "Initial diagnosis: beginner / experienced solver.",
            "Separate manual: what is the Rubik cube?",
            "Step-by-step guide with simple commands and 3D viewer.",
            "Timer challenge, machine time, and personal record.",
            "Special patterns and Rubik Script for learning Python through play.",
        ]
        y = 525
        for bullet in bullets:
            draw_wrapped(self.screen, self.font_md, "• " + bullet, COLOR_MAP["TEXT"], 105, y, 820, 5, max_lines=1)
            y += 28

        self.rects["continue"] = draw_button(self.screen, self.font_lg, pygame.Rect(460, 723, 300, 48),
                                             self.t("continue"), COLOR_MAP["SUCCESS"])
        pygame.display.flip()


    def draw_profile(self) -> None:
        self.draw_background()
        self.draw_top_language()
        self.screen.blit(self.font_title.render(self.t("profile_title"), True, COLOR_MAP["TEXT"]), (78, 64))
        self.screen.blit(self.font_lg.render(self.t("profile_sub"), True, COLOR_MAP["ALERT"]), (82, 114))

        # Dos rutas principales arriba.
        top_y = 170
        self.rects["beginner"] = self.draw_card(pygame.Rect(60, top_y, 510, 148), self.t("beginner"), self.t("beginner_desc"), COLOR_MAP["SUCCESS"])
        self.rects["expert"] = self.draw_card(pygame.Rect(650, top_y, 510, 148), self.t("expert"), self.t("expert_desc"), COLOR_MAP["B"])

        # Tres módulos complementarios abajo.
        low_y = 360
        self.rects["manual"] = self.draw_card(pygame.Rect(60, low_y, 328, 156), self.t("manual"), self.t("manual_desc"), COLOR_MAP["NEON"])
        self.rects["patterns"] = self.draw_card(pygame.Rect(446, low_y, 328, 156), self.t("patterns"), self.t("patterns_desc"), COLOR_MAP["ALERT"])
        self.rects["arcade"] = self.draw_card(pygame.Rect(832, low_y, 328, 156), self.t("arcade"), self.t("arcade_desc"), COLOR_MAP["DANGER"])

        note = "Las instrucciones generales se enseñan en el manual; la ruta guiada queda limpia para ejecutar movimientos." if self.lang == "ES" else "General instructions live in the manual; the guided route stays clean for executing moves."
        note_box = pygame.Rect(60, 548, 950, 56)
        pygame.draw.rect(self.screen, COLOR_MAP["PANEL2"], note_box, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_MAP["BORDER"], note_box, width=1, border_radius=8)
        draw_wrapped(self.screen, self.font_sm, note, COLOR_MAP["MUTED"], note_box.x + 16, note_box.y + 16, note_box.width - 32, 4, max_lines=2)

        self.rects["back_cover"] = draw_button(self.screen, self.font_md, pygame.Rect(60, 635, 150, 40), self.t("back"), (70, 70, 82))
        pygame.display.flip()

    def draw_manual_graphic(self, rect: pygame.Rect, graphic: str) -> None:
        pygame.draw.rect(self.screen, COLOR_MAP["PANEL2"], rect, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_MAP["BORDER"], rect, width=1, border_radius=10)
        cx, cy = rect.center
        if graphic in ["anatomy", "orientation"]:
            active = "F" if graphic == "orientation" else None
            self.draw_move_cube(cx - 90, cy - 10, 150, active)
            if graphic == "anatomy":
                labels = [("Centro fijo", "Y"), ("Arista", "B"), ("Esquina", "R")] if self.lang == "ES" else [("Fixed center", "Y"), ("Edge", "B"), ("Corner", "R")]
            else:
                labels = [("Blanco arriba", "W"), ("Verde al frente", "G"), ("No cambiar orientación", "Y")] if self.lang == "ES" else [("White up", "W"), ("Green front", "G"), ("Do not change orientation", "Y")]
            yy = rect.y + 85
            for txt, code in labels:
                pygame.draw.circle(self.screen, COLOR_MAP[code], (rect.x + 560, yy + 10), 8)
                self.screen.blit(self.font_md.render(txt, True, COLOR_MAP["TEXT"]), (rect.x + 580, yy))
                yy += 42
        elif graphic == "pieces":
            items = [("CENTRO", "1 color"), ("ARISTA", "2 colores"), ("ESQUINA", "3 colores")] if self.lang == "ES" else [("CENTER", "1 color"), ("EDGE", "2 colors"), ("CORNER", "3 colors")]
            colors = ["Y", "B", "R"]
            for i, ((title, sub), code) in enumerate(zip(items, colors)):
                x = rect.x + 80 + i * 250
                y = rect.y + 105
                pygame.draw.rect(self.screen, COLOR_MAP[code], (x, y, 88, 88), border_radius=8)
                pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 88, 88), width=3, border_radius=8)
                self.screen.blit(self.font_lg.render(title, True, COLOR_MAP["TEXT"]), (x - 10, y - 42))
                self.screen.blit(self.font_md.render(sub, True, COLOR_MAP["MUTED"]), (x - 5, y + 110))
        elif graphic == "moves":
            moves = ["R", "R'", "F", "U", "D", "L"]
            for i, mv in enumerate(moves):
                x = rect.x + 55 + (i % 3) * 250
                y = rect.y + 52 + (i // 3) * 115
                pygame.draw.rect(self.screen, COLOR_MAP["PANEL"], (x, y, 205, 82), border_radius=8)
                pygame.draw.rect(self.screen, COLOR_MAP[FACE_TO_COLOR[mv[0]]], (x, y, 205, 82), width=2, border_radius=8)
                self.screen.blit(self.font_lg.render(mv, True, COLOR_MAP[FACE_TO_COLOR[mv[0]]]), (x + 14, y + 15))
                draw_wrapped(self.screen, self.font_xs, MOVE_TEXT[self.lang][mv], COLOR_MAP["TEXT"], x + 55, y + 10, 135, 2, max_lines=3)
        else:
            texts = ["Caras", "Giros", "Guía", "Práctica"] if self.lang == "ES" else ["Faces", "Turns", "Guide", "Practice"]
            for i, txt in enumerate(texts):
                x = rect.x + 110 + i * 180
                y = rect.y + 140
                pygame.draw.circle(self.screen, COLOR_MAP["SUCCESS"], (x, y), 38)
                self.screen.blit(self.font_lg.render(str(i + 1), True, (0, 0, 0)), (x - 7, y - 14))
                self.screen.blit(self.font_md.render(txt, True, COLOR_MAP["TEXT"]), (x - 45, y + 55))
                if i < 3:
                    pygame.draw.line(self.screen, COLOR_MAP["ALERT"], (x + 45, y), (x + 135, y), 4)

    def draw_manual(self) -> None:
        self.draw_background()
        self.draw_top_language()
        self.rects["back_profile"] = draw_button(self.screen, self.font_sm, pygame.Rect(20, 20, 125, 34), self.t("back"), (66, 66, 78))
        self.screen.blit(self.font_title.render(self.t("manual_title"), True, COLOR_MAP["TEXT"]), (165, 70))
        lesson = MANUAL_LESSONS[self.lang][self.manual_lesson]
        self.screen.blit(self.font_lg.render(lesson["title"], True, COLOR_MAP["ALERT"]), (165, 130))
        draw_wrapped(self.screen, self.font_md, lesson["body"], COLOR_MAP["TEXT"], 165, 178, 880, 7, max_lines=4)
        self.draw_manual_graphic(pygame.Rect(165, 300, 890, 295), str(lesson["graphic"]))
        self.rects["manual_prev_btn"] = draw_button(self.screen, self.font_md, pygame.Rect(165, 650, 210, 42), self.t("manual_prev"), (66, 66, 78))
        self.rects["manual_next_btn"] = draw_button(self.screen, self.font_md, pygame.Rect(395, 650, 210, 42), self.t("manual_next"), COLOR_MAP["SUCCESS"])
        self.rects["manual_start_btn"] = draw_button(self.screen, self.font_md, pygame.Rect(625, 650, 210, 42), self.t("manual_start"), COLOR_MAP["B"])
        progress = f"{self.manual_lesson + 1} / {len(MANUAL_LESSONS[self.lang])}"
        self.screen.blit(self.font_lg.render(progress, True, COLOR_MAP["MUTED"]), (880, 657))
        pygame.display.flip()

    def draw_beginner(self) -> None:
        self.draw_background()
        self.draw_top_language()
        self.rects["back_profile"] = draw_button(self.screen, self.font_sm, pygame.Rect(20, 18, 125, 34), self.t("back"), (66, 66, 78))
        title = "Ruta guiada: No sé armar el cubo" if self.lang == "ES" else "Guided route: I do not know how to solve it"
        self.screen.blit(self.font_lg.render(title, True, COLOR_MAP["TEXT"]), (170, 22))

        # Banner de orientación sin tapar idioma ni el cubo 2D.
        banner = pygame.Rect(170, 58, 660, 30)
        pygame.draw.rect(self.screen, (43, 38, 20), banner, border_radius=6)
        self.screen.blit(self.font_xs.render(self.t("orientation"), True, COLOR_MAP["ALERT"]), (banner.x + 14, banner.y + 9))

        # Área principal: red 2D completa y más baja para no quedar bajo el banner.
        self.draw_palette(20, 96, 145)
        self.draw_cube_net(198, 122, 124, editable=True)

        # Botones principales bajo la red 2D.
        self.rects["reset"] = draw_button(self.screen, self.font_md, pygame.Rect(198, 600, 205, 40), self.t("reset"), COLOR_MAP["DANGER"])
        self.rects["solve"] = draw_button(self.screen, self.font_md, pygame.Rect(423, 600, 220, 40), self.t("solve"), COLOR_MAP["SUCCESS"])
        manual_label = "¿QUÉ ES EL CUBO?" if self.lang == "ES" else "WHAT IS THE CUBE?"
        self.rects["open_manual_top"] = draw_button(self.screen, self.font_sm, pygame.Rect(663, 600, 190, 40), manual_label, COLOR_MAP["B"])

        # Panel derecho: cubo Rubik 3D real; sin marca activa hasta generar guía.
        side = pygame.Rect(900, 105, 295, 535)
        pygame.draw.rect(self.screen, COLOR_MAP["PANEL"], side, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_MAP["NEON"], side, width=1, border_radius=10)
        side_title = "DADO 3D: CAPA ACTIVA" if self.lang == "ES" else "3D CUBE: ACTIVE LAYER"
        self.screen.blit(self.font_md.render(side_title, True, COLOR_MAP["NEON"]), (side.x + 22, side.y + 20))
        current = self.solution_steps[self.solution_index] if self.solution_steps else None
        self.draw_move_cube(side.centerx - 8, side.y + 210, 136, current)

        if current:
            face = current[0]
            code = FACE_TO_COLOR.get(face, "W")
            pygame.draw.circle(self.screen, COLOR_MAP[code], (side.x + 48, side.y + 410), 18)
            pygame.draw.circle(self.screen, (255, 255, 255), (side.x + 48, side.y + 410), 18, width=2)
            layer_txt = f"{face} / {COLOR_NAMES[self.lang][code]}"
            self.screen.blit(self.font_lg.render(layer_txt, True, COLOR_MAP[code]), (side.x + 82, side.y + 396))
            guide_hint = "La capa iluminada es la que debes mover." if self.lang == "ES" else "The highlighted layer is the one to turn."
        else:
            neutral = "Sin capa activa" if self.lang == "ES" else "No active layer"
            self.screen.blit(self.font_lg.render(neutral, True, COLOR_MAP["MUTED"]), (side.x + 48, side.y + 396))
            guide_hint = "Primero pinta tu cubo real y presiona GENERAR GUÍA." if self.lang == "ES" else "First paint your real cube and press GENERATE GUIDE."
        draw_wrapped(self.screen, self.font_sm, guide_hint, COLOR_MAP["MUTED"], side.x + 25, side.y + 455, side.width - 50, 4, max_lines=3)

        # Panel inferior ampliado: comandos completos sin esconder texto.
        self.draw_solution_panel(pygame.Rect(198, 646, 997, 188), simple_language=True)
        pygame.display.flip()

    def draw_expert(self, tick: float) -> None:
        self.draw_background()
        self.draw_top_language()
        self.screen.blit(self.font_lg.render("Ruta de competencia: Ya tengo experiencia" if self.lang == "ES" else "Competition route: Experienced solver",
                                            True, COLOR_MAP["TEXT"]), (170, 25))
        self.rects["back_profile"] = draw_button(self.screen, self.font_sm, pygame.Rect(20, 20, 125, 34), self.t("back"), (66, 66, 78))

        # Entrada precisa 2D + preview 3D-lite grande para el reto.
        self.draw_palette(20, 85, 130)
        self.draw_cube_net(165, 85, 132, editable=True)

        self.rects["reset"] = draw_button(self.screen, self.font_md, pygame.Rect(165, 586, 200, 40), self.t("reset"), COLOR_MAP["DANGER"])
        start_label = self.t("stop") if self.timer_running else self.t("start_challenge")
        start_color = COLOR_MAP["DANGER"] if self.timer_running else COLOR_MAP["SUCCESS"]
        self.rects["challenge_toggle"] = draw_button(self.screen, self.font_md, pygame.Rect(385, 586, 230, 40), start_label, start_color)

        right = pygame.Rect(760, 85, 440, 540)
        pygame.draw.rect(self.screen, COLOR_MAP["PANEL"], right, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_MAP["NEON"], right, width=1, border_radius=10)
        self.screen.blit(self.font_lg.render("3D-LITE CHALLENGE VIEW", True, COLOR_MAP["NEON"]), (right.x + 35, right.y + 24))
        self.draw_wire_cube(right.centerx - 20, right.y + 205, 170, tick)

        timer_title = f"TU TIEMPO: {self.user_time:0.2f} s" if self.lang == "ES" else f"YOUR TIME: {self.user_time:0.2f} s"
        self.screen.blit(self.font_xl.render(timer_title, True, COLOR_MAP["SUCCESS"]), (right.x + 35, right.y + 330))
        cpu_text = f"Máquina: {self.machine_time:0.3f} s | {self.machine_solution_len} movimientos"
        if self.lang == "EN":
            cpu_text = f"Machine: {self.machine_time:0.3f} s | {self.machine_solution_len} moves"
        self.screen.blit(self.font_md.render(cpu_text, True, COLOR_MAP["TEXT"]), (right.x + 35, right.y + 380))
        best = self.scores.get("expert_best")
        best_text = "Récord personal: --" if best is None else f"Récord personal: {float(best):0.2f} s"
        if self.lang == "EN":
            best_text = "Personal best: --" if best is None else f"Personal best: {float(best):0.2f} s"
        self.screen.blit(self.font_md.render(best_text, True, COLOR_MAP["ALERT"]), (right.x + 35, right.y + 412))

        tip = EXPERT_TIPS[self.lang][self.expert_tip]
        draw_wrapped(self.screen, self.font_sm, tip, COLOR_MAP["MUTED"], right.x + 35, right.y + 452, right.width - 70, 5)
        self.rects["expert_tip_next"] = draw_button(self.screen, self.font_xs, pygame.Rect(right.right - 145, right.bottom - 42, 120, 28),
                                                    "TIP +", COLOR_MAP["B"])

        bottom = pygame.Rect(165, 655, 1035, 150)
        pygame.draw.rect(self.screen, COLOR_MAP["PANEL2"], bottom, border_radius=8)
        if self.challenge_message:
            draw_wrapped(self.screen, self.font_md, self.challenge_message, COLOR_MAP["ALERT"], bottom.x + 20, bottom.y + 20, bottom.width - 40, 6)
        elif self.solution_message:
            draw_wrapped(self.screen, self.font_md, self.solution_message, COLOR_MAP["DANGER"], bottom.x + 20, bottom.y + 20, bottom.width - 40, 6)
        else:
            draw_wrapped(self.screen, self.font_md, self.t("guide_empty_expert"), COLOR_MAP["MUTED"], bottom.x + 20, bottom.y + 28, bottom.width - 40, 6)
        pygame.display.flip()

    def draw_patterns(self) -> None:
        self.draw_background()
        self.draw_top_language()
        self.screen.blit(self.font_lg.render(self.t("patterns"), True, COLOR_MAP["TEXT"]), (170, 25))
        self.rects["back_profile"] = draw_button(self.screen, self.font_sm, pygame.Rect(20, 20, 125, 34), self.t("back"), (66, 66, 78))

        has_pattern = bool(self.pattern_steps) and self.pattern_index >= 0
        selected = PATTERNS[self.pattern_index] if has_pattern else None
        current_idx = 0
        current_move = None
        if has_pattern:
            current_move = self.pattern_steps[0] if self.pattern_cursor <= 0 else self.pattern_steps[min(self.pattern_cursor - 1, len(self.pattern_steps) - 1)]
            current_idx = 0 if self.pattern_cursor <= 0 else min(self.pattern_cursor - 1, len(self.pattern_steps) - 1)

        self.draw_cube_net(145, 92, 128, editable=False)

        self.rects["pattern_prev"] = draw_button(self.screen, self.font_xs, pygame.Rect(145, 542, 130, 36), self.t("prev"), (66, 66, 78))
        self.rects["pattern_next"] = draw_button(self.screen, self.font_xs, pygame.Rect(292, 542, 130, 36), self.t("next"), COLOR_MAP["SUCCESS"])
        self.rects["pattern_reset"] = draw_button(self.screen, self.font_xs, pygame.Rect(439, 542, 145, 36), "REINICIAR" if self.lang == "ES" else "RESET", COLOR_MAP["DANGER"])

        algo_box = pygame.Rect(145, 590, 720, 92)
        pygame.draw.rect(self.screen, COLOR_MAP["PANEL2"], algo_box, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_MAP["BORDER"], algo_box, width=1, border_radius=8)
        if has_pattern:
            algo = " ".join(self.pattern_steps)
            inv = " ".join(inverse_algorithm(self.pattern_steps))
            applied = f"Aplicados: {self.pattern_cursor} / {len(self.pattern_steps)}" if self.lang == "ES" else f"Applied: {self.pattern_cursor} / {len(self.pattern_steps)}"
            self.screen.blit(self.font_sm.render(applied, True, COLOR_MAP["ALERT"]), (algo_box.x + 14, algo_box.y + 8))
            draw_wrapped(self.screen, self.font_xs, f"{self.t('pattern_route')}: {algo}", COLOR_MAP["TEXT"], algo_box.x + 14, algo_box.y + 30, algo_box.width - 28, 2, max_lines=2)
            draw_wrapped(self.screen, self.font_xs, f"{self.t('pattern_back')}: {inv}", COLOR_MAP["MUTED"], algo_box.x + 14, algo_box.y + 58, algo_box.width - 28, 2, max_lines=2)
        else:
            draw_wrapped(self.screen, self.font_md, self.t("pattern_select_hint"), COLOR_MAP["ALERT"], algo_box.x + 18, algo_box.y + 24, algo_box.width - 36, 5, max_lines=2)

        panel = pygame.Rect(890, 86, 305, 596)
        pygame.draw.rect(self.screen, COLOR_MAP["PANEL"], panel, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_MAP["ALERT"] if self.pattern_catalog_open else COLOR_MAP["NEON"], panel, width=1, border_radius=10)
        toggle_label = ("OCULTAR LISTA ▲" if self.pattern_catalog_open else "VER LISTA DE PATRONES ▼") if self.lang == "ES" else ("HIDE LIST ▲" if self.pattern_catalog_open else "SHOW PATTERN LIST ▼")
        self.rects["pattern_catalog_toggle"] = draw_button(self.screen, self.font_xs, pygame.Rect(panel.x + 18, panel.y + 18, panel.width - 36, 32), toggle_label, COLOR_MAP["B"] if not self.pattern_catalog_open else COLOR_MAP["DANGER"])
        self.rects = {k: v for k, v in self.rects.items() if not k.startswith("pat_select_")}

        if self.pattern_catalog_open:
            self.screen.blit(self.font_md.render("SELECCIONA UN PATRÓN" if self.lang == "ES" else "SELECT A PATTERN", True, COLOR_MAP["ALERT"]), (panel.x + 22, panel.y + 66))
            start_y = panel.y + 102
            for i, pattern in enumerate(PATTERNS):
                yy = start_y + i * 32
                if yy > panel.bottom - 70:
                    break
                bg = COLOR_MAP["SUCCESS"] if i == self.pattern_index else (60, 60, 72)
                rect = pygame.Rect(panel.x + 18, yy, panel.width - 36, 27)
                self.rects[f"pat_select_{i}"] = draw_button(self.screen, self.font_xs, rect, pattern["name"][:36], bg)
            note_rect = pygame.Rect(panel.x + 18, panel.bottom - 58, panel.width - 36, 43)
            pygame.draw.rect(self.screen, (45, 38, 18), note_rect, border_radius=6)
            draw_wrapped(self.screen, self.font_xs, self.t("pattern_note"), COLOR_MAP["ALERT"], note_rect.x + 10, note_rect.y + 8, note_rect.width - 20, 3, max_lines=2)
        else:
            guide_title = "CUBO 3D: MOVIMIENTOS APLICADOS" if self.lang == "ES" else "3D CUBE: APPLIED MOVES"
            self.screen.blit(self.font_md.render(guide_title, True, COLOR_MAP["NEON"]), (panel.x + 20, panel.y + 68))
            self.draw_move_cube(panel.centerx - 8, panel.y + 245, 150, current_move)
            if current_move:
                code = FACE_TO_COLOR.get(current_move[0], "W")
                pygame.draw.circle(self.screen, COLOR_MAP[code], (panel.x + 54, panel.y + 435), 18)
                pygame.draw.circle(self.screen, (255, 255, 255), (panel.x + 54, panel.y + 435), 18, width=2)
                self.screen.blit(self.font_lg.render(f"{current_move[0]} / {COLOR_NAMES[self.lang][code]}", True, COLOR_MAP[code]), (panel.x + 88, panel.y + 421))
                hint = "Al presionar SIGUIENTE, el cubo aplica el movimiento." if self.lang == "ES" else "When you press NEXT, the cube applies the move."
            else:
                hint = self.t("pattern_select_hint")
            draw_wrapped(self.screen, self.font_sm, hint, COLOR_MAP["MUTED"], panel.x + 25, panel.y + 482, panel.width - 50, 4, max_lines=3)

        bottom = pygame.Rect(145, 700, 1050, 112)
        pygame.draw.rect(self.screen, COLOR_MAP["PANEL2"], bottom, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_MAP["BORDER"], bottom, width=1, border_radius=8)
        if has_pattern and current_move:
            self.screen.blit(self.font_sm.render(selected["name"], True, COLOR_MAP["ALERT"]), (bottom.x + 16, bottom.y + 7))
            self.draw_dual_command_panel(pygame.Rect(bottom.x + 6, bottom.y + 28, bottom.width - 12, 78), current_move, current_idx, len(self.pattern_steps), simple_language=True)
        else:
            draw_wrapped(self.screen, self.font_lg, self.t("pattern_select_hint"), COLOR_MAP["MUTED"], bottom.x + 25, bottom.y + 38, bottom.width - 50, 6, max_lines=2)
        pygame.display.flip()

    def draw_arcade_menu(self) -> None:
        self.draw_background()
        self.draw_top_language()
        self.rects["back_profile"] = draw_button(self.screen, self.font_sm, pygame.Rect(20, 20, 125, 34), self.t("back"), (66, 66, 78))

        title = self.t("arcade_menu")
        self.screen.blit(self.font_title.render(title, True, COLOR_MAP["TEXT"]), (80, 56))
        intro = "Programa el cubo como si fuera Karel: lee datos, decide giros y repite algoritmos." if self.lang == "ES" else "Program the cube like Karel: read data, choose turns, and repeat algorithms."
        draw_wrapped(self.screen, self.font_md, intro, COLOR_MAP["ALERT"], 84, 106, 650, 5, max_lines=2)

        left_panel = pygame.Rect(70, 155, 660, 600)
        pygame.draw.rect(self.screen, COLOR_MAP["PANEL"], left_panel, border_radius=12)
        pygame.draw.rect(self.screen, COLOR_MAP["BORDER"], left_panel, width=1, border_radius=12)
        panel_label = "SELECCIONA UN NIVEL" if self.lang == "ES" else "SELECT A LEVEL"
        self.screen.blit(self.font_lg.render(panel_label, True, COLOR_MAP["NEON"]), (left_panel.x + 22, left_panel.y + 18))

        completed = set(str(x) for x in self.scores.get("arcade_completed", []))
        colors = [COLOR_MAP["SUCCESS"], COLOR_MAP["B"], COLOR_MAP["PURPLE"]]
        for idx, world in WORLD_SETTINGS.items():
            rect = pygame.Rect(left_panel.x + 22, left_panel.y + 66 + (idx - 1) * 130, left_panel.width - 44, 108)
            active = self.arcade_world == idx
            color = colors[idx - 1]
            pygame.draw.rect(self.screen, COLOR_MAP["PANEL2"], rect, border_radius=10)
            pygame.draw.rect(self.screen, color if active else COLOR_MAP["BORDER"], rect, width=2, border_radius=10)
            self.rects[f"world_{idx}"] = rect
            marker = "COMPLETADO" if str(idx) in completed else "PENDIENTE"
            if self.lang == "EN":
                marker = "COMPLETED" if str(idx) in completed else "PENDING"
            high = int(self.scores.get("arcade_high", {}).get(str(idx), 0))
            self.screen.blit(self.font_lg.render(world["name"], True, color), (rect.x + 18, rect.y + 12))
            draw_wrapped(self.screen, self.font_sm, str(world["subtitle"]), COLOR_MAP["TEXT"], rect.x + 18, rect.y + 48, rect.width - 170, 3, max_lines=2)
            score_prefix = "Puntaje" if self.lang == "ES" else "Score"
            self.screen.blit(self.font_xs.render(f"{score_prefix}: {high}", True, COLOR_MAP["ALERT"]), (rect.right - 126, rect.y + 42))
            self.screen.blit(self.font_xs.render(marker, True, COLOR_MAP["MUTED"]), (rect.right - 126, rect.y + 66))

        start_label = self.t("play_world")
        self.rects["arcade_start"] = draw_button(self.screen, self.font_md, pygame.Rect(left_panel.x + 174, left_panel.bottom - 78, 312, 50), start_label, COLOR_MAP["SUCCESS"])
        if len(completed) >= 3:
            draw_wrapped(self.screen, self.font_sm, self.t("campaign"), COLOR_MAP["SUCCESS"], left_panel.x + 24, left_panel.bottom - 126, left_panel.width - 48, 4, max_lines=2)

        guide = pygame.Rect(760, 155, 420, 600)
        pygame.draw.rect(self.screen, COLOR_MAP["PANEL"], guide, border_radius=12)
        pygame.draw.rect(self.screen, COLOR_MAP["NEON"], guide, width=1, border_radius=12)
        guide_title = "CÓMO SE JUEGA" if self.lang == "ES" else "HOW TO PLAY"
        self.screen.blit(self.font_lg.render(guide_title, True, COLOR_MAP["NEON"]), (guide.x + 22, guide.y + 18))

        if self.lang == "ES":
            lines = [
                "1. Elige un nivel del panel izquierdo.",
                "2. Presiona INICIAR RETO.",
                "3. Lee el enunciado y el código propuesto.",
                "4. Elige la opción correcta con clic o con 1, 2 o 3.",
                "5. Si aciertas, el cubo aplica movimientos y sumas puntos.",
                "6. Avanza hasta completar todas las preguntas del nivel.",
            ]
            command_lines = [
                "U = capa superior | D = capa inferior",
                "F = frente | B = atrás",
                "R = derecha | L = izquierda",
                "' = giro inverso",
                "2 = medio giro de 180 grados",
            ]
            note = "Consejo: piensa como Karel. Primero lees el estado del cubo, luego decides y por último repites secuencias."
        else:
            lines = [
                "1. Choose a level from the left panel.",
                "2. Press START CHALLENGE.",
                "3. Read the prompt and the proposed code.",
                "4. Choose the right option with a click or with 1, 2, or 3.",
                "5. If correct, the cube applies moves and you gain points.",
                "6. Keep going until you complete all questions in the level.",
            ]
            command_lines = [
                "U = upper layer | D = down layer",
                "F = front | B = back",
                "R = right | L = left",
                "' = inverse turn",
                "2 = half turn of 180 degrees",
            ]
            note = "Tip: think like Karel. First read the cube state, then decide, and finally repeat sequences."

        y = guide.y + 66
        for line in lines:
            y = draw_wrapped(self.screen, self.font_sm, line, COLOR_MAP["TEXT"], guide.x + 22, y, guide.width - 44, 3, max_lines=2)
            y += 8

        sep_y = y + 2
        pygame.draw.line(self.screen, COLOR_MAP["BORDER"], (guide.x + 22, sep_y), (guide.right - 22, sep_y), 1)
        self.screen.blit(self.font_md.render("COMANDOS DEL CUBO" if self.lang == "ES" else "CUBE COMMANDS", True, COLOR_MAP["ALERT"]), (guide.x + 22, sep_y + 16))
        y = sep_y + 52
        for line in command_lines:
            self.screen.blit(self.font_sm.render(line, True, COLOR_MAP["TEXT"]), (guide.x + 22, y))
            y += 26

        note_box = pygame.Rect(guide.x + 18, guide.bottom - 94, guide.width - 36, 70)
        pygame.draw.rect(self.screen, COLOR_MAP["PANEL2"], note_box, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_MAP["ALERT"], note_box, width=1, border_radius=8)
        draw_wrapped(self.screen, self.font_xs, note, COLOR_MAP["ALERT"], note_box.x + 12, note_box.y + 12, note_box.width - 24, 3, max_lines=3)

        pygame.display.flip()

    def draw_code_terminal(self, rect: pygame.Rect, lines: List[str]) -> None:
        pygame.draw.rect(self.screen, (9, 12, 18), rect, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_MAP["BORDER"], rect, width=1, border_radius=8)
        self.screen.blit(self.font_sm.render("rubik_script.py", True, COLOR_MAP["NEON"]), (rect.x + 16, rect.y + 10))
        y = rect.y + 38
        for line in lines[:6]:
            self.screen.blit(self.font_xs.render(line, True, COLOR_MAP["TEXT"]), (rect.x + 16, y))
            y += 22

    def draw_arcade_play(self) -> None:
        self.draw_background()
        self.draw_top_language()
        self.rects["arcade_back"] = draw_button(self.screen, self.font_sm, pygame.Rect(20, 20, 145, 34), self.t("back"), (66, 66, 78))

        level = cast(Dict[str, Any], RUBIK_SCRIPT_LEVELS[self.arcade_world])
        questions = cast(List[Dict[str, Any]], level["questions"])
        question = questions[self.script_question_index]
        q_total = len(questions)

        level_name = cast(Dict[str, str], level["name"])[self.lang]
        level_goal = cast(Dict[str, str], level["goal"])[self.lang]
        self.screen.blit(self.font_title.render(level_name, True, COLOR_MAP["TEXT"]), (78, 64))
        draw_wrapped(self.screen, self.font_md, level_goal, COLOR_MAP["ALERT"], 82, 116, 760, 5, max_lines=2)

        progress_text = (f"Pregunta {self.script_question_index + 1} de {q_total}" if self.lang == "ES" else f"Question {self.script_question_index + 1} of {q_total}")
        score_text = (f"Puntaje: {self.arcade_score}" if self.lang == "ES" else f"Score: {self.arcade_score}")
        self.screen.blit(self.font_md.render(progress_text, True, COLOR_MAP["SUCCESS"]), (930, 78))
        self.screen.blit(self.font_md.render(score_text, True, COLOR_MAP["ALERT"]), (930, 108))

        # Panel izquierdo: cubo 2D, cubo 3D y recordatorio de comandos.
        left = pygame.Rect(50, 165, 350, 595)
        pygame.draw.rect(self.screen, COLOR_MAP["PANEL"], left, border_radius=12)
        pygame.draw.rect(self.screen, COLOR_MAP["BORDER"], left, width=1, border_radius=12)
        self.screen.blit(self.font_lg.render("CUBO RUBIK 3x3" if self.lang == "ES" else "RUBIK 3x3 CUBE", True, COLOR_MAP["NEON"]), (left.x + 18, left.y + 16))
        self.draw_cube_net(left.x + 38, left.y + 52, 58, editable=False)

        move_hint = None
        if question.get("moves"):
            move_hint = str(question["moves"][0])
        self.screen.blit(self.font_md.render("VISTA 3D" if self.lang == "ES" else "3D VIEW", True, COLOR_MAP["ALERT"]), (left.x + 20, left.y + 352))
        self.draw_move_cube(left.centerx + 65, left.y + 440, 58, move_hint)
        if move_hint:
            simple_hint = MOVE_TEXT[self.lang].get(move_hint, move_hint)
            draw_wrapped(self.screen, self.font_xs, simple_hint, COLOR_MAP["TEXT"], left.x + 18, left.y + 380, 165, 3, max_lines=3)

        cmd_box = pygame.Rect(left.x + 16, left.bottom - 120, left.width - 32, 96)
        pygame.draw.rect(self.screen, COLOR_MAP["PANEL2"], cmd_box, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_MAP["BORDER"], cmd_box, width=1, border_radius=8)
        self.screen.blit(self.font_sm.render("COMANDOS" if self.lang == "ES" else "COMMANDS", True, COLOR_MAP["ALERT"]), (cmd_box.x + 12, cmd_box.y + 10))
        cmd_lines = ["U/D = arriba/abajo", "F/B = frente/atrás", "R/L = derecha/izquierda", "' inverso · 2 medio giro"] if self.lang == "ES" else ["U/D = up/down", "F/B = front/back", "R/L = right/left", "' inverse · 2 half turn"]
        yy = cmd_box.y + 34
        for line in cmd_lines:
            self.screen.blit(self.font_xs.render(line, True, COLOR_MAP["TEXT"]), (cmd_box.x + 12, yy))
            yy += 16

        # Panel principal: concepto, enunciado, código, opciones, feedback y navegación.
        main = pygame.Rect(425, 165, 790, 595)
        pygame.draw.rect(self.screen, COLOR_MAP["PANEL"], main, border_radius=12)
        pygame.draw.rect(self.screen, COLOR_MAP["BORDER"], main, width=1, border_radius=12)
        concept = cast(Dict[str, str], question["concept"])[self.lang]
        task = cast(Dict[str, str], question["task"])[self.lang]
        code_lines = cast(List[str], question["code"])
        options = cast(Dict[str, List[str]], question["options"])[self.lang]

        self.screen.blit(self.font_lg.render(concept, True, COLOR_MAP["SUCCESS"]), (main.x + 22, main.y + 18))
        draw_wrapped(self.screen, self.font_md, task, COLOR_MAP["TEXT"], main.x + 22, main.y + 58, main.width - 44, 5, max_lines=3)

        code_rect = pygame.Rect(main.x + 22, main.y + 130, main.width - 44, 112)
        self.draw_code_terminal(code_rect, code_lines)

        self.rects = {k: v for k, v in self.rects.items() if not k.startswith("script_opt_")}
        opt_y = main.y + 258
        for i, option in enumerate(options):
            rect = pygame.Rect(main.x + 22, opt_y + i * 58, main.width - 44, 46)
            bg = (58, 58, 72)
            if self.script_answered:
                if i == int(question["answer"]):
                    bg = COLOR_MAP["SUCCESS"]
                elif self.script_selected_option == i:
                    bg = COLOR_MAP["DANGER"]
            self.rects[f"script_opt_{i}"] = draw_button(self.screen, self.font_xs, rect, f"{i + 1}. {option}", bg)

        feedback_box = pygame.Rect(main.x + 22, main.bottom - 118, main.width - 290, 82)
        pygame.draw.rect(self.screen, COLOR_MAP["PANEL2"], feedback_box, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_MAP["BORDER"], feedback_box, width=1, border_radius=8)
        if self.script_feedback:
            color = COLOR_MAP["SUCCESS"] if self.script_answered and self.script_selected_option == int(question["answer"]) else COLOR_MAP["DANGER"]
            draw_wrapped(self.screen, self.font_md, self.script_feedback, color, feedback_box.x + 14, feedback_box.y + 16, feedback_box.width - 28, 5, max_lines=2)
        else:
            msg = "Elige el bloque de código correcto para controlar el cubo." if self.lang == "ES" else "Choose the correct code block to control the cube."
            draw_wrapped(self.screen, self.font_sm, msg, COLOR_MAP["MUTED"], feedback_box.x + 14, feedback_box.y + 16, feedback_box.width - 28, 4, max_lines=2)

        side_box = pygame.Rect(main.right - 235, main.bottom - 118, 213, 82)
        pygame.draw.rect(self.screen, COLOR_MAP["PANEL2"], side_box, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_MAP["BORDER"], side_box, width=1, border_radius=8)
        if self.script_answered:
            next_label = ("SIGUIENTE RETO" if self.lang == "ES" else "NEXT CHALLENGE")
            self.rects["script_next"] = draw_button(self.screen, self.font_sm, pygame.Rect(side_box.x + 17, side_box.y + 21, side_box.width - 34, 40), next_label, COLOR_MAP["SUCCESS"])
        else:
            hint = "Presiona 1, 2 o 3" if self.lang == "ES" else "Press 1, 2, or 3"
            draw_wrapped(self.screen, self.font_sm, hint, COLOR_MAP["ALERT"], side_box.x + 16, side_box.y + 28, side_box.width - 32, 4, max_lines=2)

        pygame.display.flip()

    # --------------------------------------------------------
    # EVENTOS Y ACTUALIZACIÓN
    # --------------------------------------------------------
    def start_arcade(self) -> None:
        """Inicia Rubik Script: preguntas de Python aplicadas al cubo Rubik."""
        self.arcade_elapsed = 0.0
        self.arcade_score = 0
        self.arcade_game_over = False
        self.arcade_victory = False
        self.arcade_obstacles = []
        self.arcade_spawn_timer = 1.0
        self.script_question_index = 0
        self.script_selected_option = None
        self.script_feedback = ""
        self.script_answered = False
        self.script_level_complete = False
        self.cube.reset()
        self.state = "ARCADE_PLAY"

    def update_arcade(self, dt: float) -> None:
        """Actualiza el reloj interno de Rubik Script.

        El módulo ya no es un runner/arcade de obstáculos. Se mantiene este
        método porque el bucle principal llama a `update_arcade(dt)` en cada
        frame.
        """
        if self.state == "ARCADE_PLAY" and not self.script_level_complete:
            self.arcade_elapsed += dt

    def update_arcade_highscore(self, completed: bool = False) -> None:
        """Guarda el mejor puntaje por nivel y registra niveles completados."""
        highs = cast(Dict[str, int], self.scores.setdefault("arcade_high", {"1": 0, "2": 0, "3": 0}))
        key = str(self.arcade_world)
        previous = int(highs.get(key, 0))
        highs[key] = max(previous, int(self.arcade_score))
        if completed:
            completed_set = set(str(x) for x in self.scores.get("arcade_completed", []))
            completed_set.add(key)
            self.scores["arcade_completed"] = sorted(completed_set)
        save_scores(self.scores)

    def current_script_question(self) -> Dict[str, Any]:
        """Devuelve la pregunta actual del nivel Rubik Script."""
        level = cast(Dict[str, Any], RUBIK_SCRIPT_LEVELS[self.arcade_world])
        questions = cast(List[Dict[str, Any]], level["questions"])
        return questions[self.script_question_index]

    def apply_script_success(self, question: Dict[str, Any]) -> None:
        """Aplica al cubo los movimientos asociados a una respuesta correcta."""
        moves = cast(List[str], question.get("moves", []))
        for move in moves:
            try:
                self.cube.apply_move(move)
            except ValueError:
                # Movimiento mal escrito en el banco de preguntas; se ignora para no romper el juego.
                continue

    def answer_script_option(self, option_index: int) -> None:
        if self.state != "ARCADE_PLAY" or self.script_answered:
            return
        question = self.current_script_question()
        self.script_selected_option = option_index
        answer = int(question["answer"])
        correct = option_index == answer
        self.script_answered = True
        if correct:
            feedback = cast(Dict[str, str], question["feedback"])
            self.arcade_score += 100
            self.script_feedback = feedback[self.lang]
            self.apply_script_success(question)
        else:
            self.script_feedback = "Revisa la sintaxis y vuelve a intentarlo en la siguiente pregunta." if self.lang == "ES" else "Check the syntax and try again on the next question."

    def advance_script_question(self) -> None:
        if self.state != "ARCADE_PLAY":
            return
        level = cast(Dict[str, Any], RUBIK_SCRIPT_LEVELS[self.arcade_world])
        questions = cast(List[Dict[str, Any]], level["questions"])
        total = len(questions)
        if self.script_question_index + 1 >= total:
            self.script_level_complete = True
            self.arcade_victory = True
            self.update_arcade_highscore(completed=True)
            self.state = "ARCADE_MENU"
            return
        self.script_question_index += 1
        self.script_selected_option = None
        self.script_feedback = ""
        self.script_answered = False

    def handle_common_click(self, pos: Tuple[int, int]) -> bool:
        if self.rects.get("lang_es", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
            self.lang = "ES"
            return True
        if self.rects.get("lang_en", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
            self.lang = "EN"
            return True
        return False

    def handle_cube_edit_click(self, pos: Tuple[int, int]) -> bool:
        for code in ["W", "O", "G", "R", "B", "Y"]:
            if self.rects.get(f"color_{code}", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.selected_color = code
                return True
        for rect, face, idx in self.sticker_rects:
            if rect.collidepoint(pos):
                if idx == 4:  # centros fijos
                    return True
                self.cube.set_facelet_color(face, idx, self.selected_color)
                self.solution_steps = []
                self.solution_index = 0
                self.solution_message = ""
                self.challenge_message = ""
                return True
        return False

    def select_pattern(self, index: int) -> None:
        self.pattern_index = index % len(PATTERNS)
        self.pattern_steps = parse_algorithm(PATTERNS[self.pattern_index]["algo"])
        self.pattern_cursor = 0
        self.rebuild_pattern_cube()

    def rebuild_pattern_cube(self) -> None:
        self.cube.reset()
        for mv in self.pattern_steps[:self.pattern_cursor]:
            try:
                self.cube.apply_move(mv)
            except Exception:
                pass

    def stop_challenge(self) -> None:
        self.timer_running = False
        best = self.scores.get("expert_best")
        if best is None or self.user_time < float(best):
            self.scores["expert_best"] = self.user_time
            save_scores(self.scores)
            record_msg = "Nuevo récord personal" if self.lang == "ES" else "New personal best"
        else:
            record_msg = "Buen intento" if self.lang == "ES" else "Good attempt"

        if self.user_time < 20:
            level = "nivel élite" if self.lang == "ES" else "elite level"
        elif self.user_time < 45:
            level = "muy buen ritmo" if self.lang == "ES" else "very strong pace"
        elif self.user_time < 90:
            level = "vas bien; puedes optimizar reconocimiento" if self.lang == "ES" else "good start; optimize recognition"
        else:
            level = "sigue practicando con la ruta guiada" if self.lang == "ES" else "keep practicing with the guided route"
        self.challenge_message = f"{record_msg}: {self.user_time:.2f}s. Resultado: {level}. ¿Quieres bajar tu tiempo? Practica patrones y vuelve al reto."

    def handle_click(self, pos: Tuple[int, int]) -> None:
        if self.handle_common_click(pos):
            return

        if self.state == "CARATULA":
            if self.rects.get("continue", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.state = "PROFILE"

        elif self.state == "PROFILE":
            if self.rects.get("back_cover", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.state = "CARATULA"
            elif self.rects.get("beginner", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.reset_cube()
                self.state = "BEGINNER"
            elif self.rects.get("expert", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.reset_cube()
                self.state = "EXPERT"
            elif self.rects.get("manual", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.state = "MANUAL"
            elif self.rects.get("patterns", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.pattern_index = -1
                self.pattern_steps = []
                self.pattern_cursor = 0
                self.pattern_catalog_open = True
                self.cube.reset()
                self.state = "PATTERNS"
            elif self.rects.get("arcade", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.state = "ARCADE_MENU"

        elif self.state == "MANUAL":
            if self.rects.get("back_profile", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.state = "PROFILE"
            elif self.rects.get("manual_prev_btn", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.manual_lesson = (self.manual_lesson - 1) % len(MANUAL_LESSONS[self.lang])
            elif self.rects.get("manual_next_btn", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.manual_lesson = (self.manual_lesson + 1) % len(MANUAL_LESSONS[self.lang])
            elif self.rects.get("manual_start_btn", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.reset_cube()
                self.state = "BEGINNER"

        elif self.state == "BEGINNER":
            if self.rects.get("back_profile", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.state = "PROFILE"
                return
            if self.handle_cube_edit_click(pos):
                return
            if self.rects.get("reset", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.reset_cube()
            elif self.rects.get("solve", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.generate_solution()
            elif self.rects.get("open_manual", pygame.Rect(0, 0, 0, 0)).collidepoint(pos) or self.rects.get("open_manual_top", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.state = "MANUAL"
            elif self.solution_steps and self.rects.get("sol_prev", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.solution_index = max(0, self.solution_index - 1)
            elif self.solution_steps and self.rects.get("sol_next", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.solution_index = min(len(self.solution_steps) - 1, self.solution_index + 1)

        elif self.state == "EXPERT":
            if self.rects.get("back_profile", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.timer_running = False
                self.state = "PROFILE"
                return
            if self.handle_cube_edit_click(pos):
                return
            if self.rects.get("reset", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.reset_cube()
                self.user_time = 0.0
                self.timer_running = False
            elif self.rects.get("challenge_toggle", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                if not self.timer_running:
                    if self.generate_solution():
                        self.user_time = 0.0
                        self.timer_running = True
                        self.challenge_message = f"La máquina terminó en {self.machine_time:.3f}s. Tu reloj sigue corriendo." if self.lang == "ES" else f"Machine finished in {self.machine_time:.3f}s. Your timer keeps running."
                else:
                    self.stop_challenge()
            elif self.rects.get("expert_tip_next", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.expert_tip = (self.expert_tip + 1) % len(EXPERT_TIPS[self.lang])

        elif self.state == "PATTERNS":
            if self.rects.get("back_profile", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.reset_cube()
                self.state = "PROFILE"
                return
            if self.rects.get("pattern_catalog_toggle", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.pattern_catalog_open = not self.pattern_catalog_open
                return
            if self.pattern_catalog_open:
                for i in range(len(PATTERNS)):
                    if self.rects.get(f"pat_select_{i}", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                        self.select_pattern(i)
                        self.pattern_catalog_open = True
                        return
            if self.pattern_steps and (self.rects.get("pattern_prev", pygame.Rect(0, 0, 0, 0)).collidepoint(pos) or self.rects.get("sol_prev", pygame.Rect(0, 0, 0, 0)).collidepoint(pos)):
                self.pattern_cursor = max(0, self.pattern_cursor - 1)
                self.rebuild_pattern_cube()
            elif self.pattern_steps and (self.rects.get("pattern_next", pygame.Rect(0, 0, 0, 0)).collidepoint(pos) or self.rects.get("sol_next", pygame.Rect(0, 0, 0, 0)).collidepoint(pos)):
                self.pattern_cursor = min(len(self.pattern_steps), self.pattern_cursor + 1)
                self.rebuild_pattern_cube()
            elif self.pattern_steps and self.rects.get("pattern_reset", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.pattern_cursor = 0
                self.rebuild_pattern_cube()

        elif self.state == "ARCADE_MENU":
            if self.rects.get("back_profile", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.state = "PROFILE"
                return
            for idx in WORLD_SETTINGS:
                if self.rects.get(f"world_{idx}", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                    self.arcade_world = idx
                    return
            if self.rects.get("arcade_start", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.start_arcade()

        elif self.state == "ARCADE_PLAY":
            if self.rects.get("arcade_back", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.update_arcade_highscore()
                self.state = "ARCADE_MENU"
                return
            for i in range(4):
                if self.rects.get(f"script_opt_{i}", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                    self.answer_script_option(i)
                    return
            if self.rects.get("script_next", pygame.Rect(0, 0, 0, 0)).collidepoint(pos):
                self.advance_script_question()
                return

    def handle_key(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_ESCAPE:
            if self.state in ["MANUAL", "BEGINNER", "EXPERT", "PATTERNS", "ARCADE_MENU"]:
                self.state = "PROFILE"
            elif self.state == "ARCADE_PLAY":
                self.state = "ARCADE_MENU"
            return

        if self.state == "MANUAL":
            if event.key in [pygame.K_RIGHT, pygame.K_SPACE]:
                self.manual_lesson = (self.manual_lesson + 1) % len(MANUAL_LESSONS[self.lang])
            elif event.key == pygame.K_LEFT:
                self.manual_lesson = (self.manual_lesson - 1) % len(MANUAL_LESSONS[self.lang])

        elif self.state == "BEGINNER" and self.solution_steps:
            if event.key in [pygame.K_LEFT, pygame.K_UP]:
                self.solution_index = max(0, self.solution_index - 1)
            elif event.key in [pygame.K_RIGHT, pygame.K_DOWN, pygame.K_SPACE]:
                self.solution_index = min(len(self.solution_steps) - 1, self.solution_index + 1)

        elif self.state == "EXPERT" and event.key == pygame.K_SPACE:
            if not self.timer_running:
                if self.generate_solution():
                    self.user_time = 0.0
                    self.timer_running = True
                    self.challenge_message = f"La máquina terminó en {self.machine_time:.3f}s. Tu reloj sigue corriendo." if self.lang == "ES" else f"Machine finished in {self.machine_time:.3f}s. Your timer keeps running."
            else:
                self.stop_challenge()

        elif self.state == "PATTERNS":
            if event.key in [pygame.K_RIGHT, pygame.K_SPACE]:
                self.pattern_cursor = min(len(self.pattern_steps), self.pattern_cursor + 1)
                self.rebuild_pattern_cube()
            elif event.key == pygame.K_LEFT:
                self.pattern_cursor = max(0, self.pattern_cursor - 1)
                self.rebuild_pattern_cube()

        elif self.state == "ARCADE_PLAY":
            if event.key in [pygame.K_1, pygame.K_KP1]:
                self.answer_script_option(0)
            elif event.key in [pygame.K_2, pygame.K_KP2]:
                self.answer_script_option(1)
            elif event.key in [pygame.K_3, pygame.K_KP3]:
                self.answer_script_option(2)
            elif event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_RIGHT]:
                if self.script_answered:
                    self.advance_script_question()

    def update(self, dt: float) -> None:
        if self.timer_running:
            self.user_time += dt
        self.update_arcade(dt)

    def draw(self, tick: float) -> None:
        self.rects = {}
        if self.state == "CARATULA":
            self.draw_cover(tick)
        elif self.state == "PROFILE":
            self.draw_profile()
        elif self.state == "MANUAL":
            self.draw_manual()
        elif self.state == "BEGINNER":
            self.draw_beginner()
        elif self.state == "EXPERT":
            self.draw_expert(tick)
        elif self.state == "PATTERNS":
            self.draw_patterns()
        elif self.state == "ARCADE_MENU":
            self.draw_arcade_menu()
        elif self.state == "ARCADE_PLAY":
            self.draw_arcade_play()

    def run(self) -> None:
        running = True
        tick = 0.0
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            tick += dt
            self.update(dt)
            self.draw(tick)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = RubikCapstoneApp()
    app.run()
