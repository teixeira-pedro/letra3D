import pygame
from pygame.locals import *
import numpy
from math import sqrt
import copy
import operator


# Configuracoes
color = (123, 49, 125)
width = 6 # espessura da linha desenhada
scale = 4
translate = (200, 150)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640


# Definicao da estrutura de dados

# Como um jogo de ligue-os-pontos, o Z comecara no 0 e se conectara a seu sucessor, 
# ate que chegue em 9, quando ele finalmente se conecta ao 0.
#   0   1       3   4
#
#       7
#
#           
#
#               2
#
#   9   8       6   5

# O formato e da letra N porque comecei a fazer com a letra N, mas como a forma e igual, nao faz diferenca.
# Fui instruido apenas a rotacionar em noventa graus.

# Para calcular a normal de uma face, considero que os pontos de uma face visivel 
# sao descritos na estrutura de dados em sentido horario.


# Escolha das coordenadas da imagem

N = []
N += [[+2.5, -1.5, 0.0, 1.0]]
N += [[+1.5, -2.5, 0.0, 1.0]]
N += [[-1.5, +0.5, 0.0, 1.0]]
N += [[-1.5, -0.5, 0.0, 1.0]]
N += [[-2.5, -2.5, 0.0, 1.0]]
N += [[-2.5, +1.5, 0.0, 1.0]]
N += [[-1.5, +2.5, 0.0, 1.0]]
N += [[+1.5, -0.5, 0.0, 1.0]]
N += [[+1.5, +1.5, 0.0, 1.0]]
N += [[+2.5, +2.5, 0.0, 1.0]]

initial_position = [50, 0, 0]

# transform
position = initial_position.copy()
rotation = [0, 0, 90]

# etc
m = sqrt(2) # Menor aresta (calculada manualmente), usada como espessura
velocity = [0.5, 2.0, 0]
rotation_velocity = [0, 5, 1]


# Definindo funcoes


def scaling_matrix (scale):
    return [[scale, 0, 0, 0], [0, scale, 0, 0], [0, 0, scale, 0], [0, 0, 0, 1]]


def translation_matrix (x, y, z):
    return [[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]]

def oblique_parallel_projection_matrix (degrees, l = 1):
    angle = numpy.deg2rad(degrees)
    return [[1, 0, l * numpy.cos(degrees), 0], [0, 1, l * numpy.sin(degrees), 0], [0, 0, 0, 0], [0, 0, 0, 1]]

def back_face_culling (object3D, observer_point):
    new_object = []
    for i in object3D:
        face_normal = normal_vector(object3D[i])
        if (numpy.dot(map(operator.sub, object3D[i], observer_point), face_normal) < 0):
            new_object += object3D[i]
    return new_object

def rotation_matrix_around_y (degrees):
    degrees = numpy.deg2rad(degrees)
    rotation_matrix = []
    rotation_matrix += [[1, 0, 0, 0]]
    rotation_matrix += [[0, numpy.cos(degrees), -numpy.sin(degrees), 0]]
    rotation_matrix += [[0, numpy.sin(degrees), numpy.cos(degrees), 0]]
    rotation_matrix += [[0, 0, 0, 1]]
    return rotation_matrix

def rotation_matrix_around_z (degrees):
    degrees = numpy.deg2rad(degrees)
    rotation_matrix = []
    rotation_matrix += [[numpy.cos(degrees), -numpy.sin(degrees), 0, 0]]
    rotation_matrix += [[numpy.sin(degrees), numpy.cos(degrees), 0, 0]]
    rotation_matrix += [[0, 0, 1, 0]]
    rotation_matrix += [[0, 0, 0, 1]]
    return rotation_matrix


def reversed_normal (face):
    inverted_face = list(copy.deepcopy(face))
    inverted_face.reverse()
    return inverted_face

def normal_vector (face):
    nface = copy.deepcopy(face)
    a = list(map(operator.sub, nface[0], nface[1])) # v1 - v2
    a = a[0:3]
    b = list(map(operator.sub, nface[0], nface[2])) # v1 - v3
    b = b[0:3]
    return list(numpy.cross(a, b))

def sweep_3D (object_2D, depth):
    object_3D = [copy.deepcopy(object_2D)]
    object_3D += [copia_face_principal_para_plano_z(object_2D, depth)] # será revertido no final
    pts = len(object_2D)
    for v in range(pts):
        new_face = copy.deepcopy([object_3D[0][v], object_3D[0][(v + 1) % pts], object_3D[1][(v + 1) % pts], object_3D[1][v]])
        object_3D += [new_face]
    object_3D[1] = reversed_normal(object_3D[1])
    return object_3D

        

def copia_face_principal_para_plano_z(face,z):
    copia=copy.deepcopy(face)
    for i in range(len(copia)):
        copia[i][2]=copia[i][2]+z
    return copia

        

def draw2DLine (screen, a, b, color, width):
    pygame.draw.line(screen, color, a, b, width)

def pointSRUtoScreen (point):
    new = point.copy()
    # Decidi usar a maior dimensao para evitar deformacoes indesejadas
    new[0] = new[0] * max(SCREEN_WIDTH, SCREEN_HEIGHT) / 100.0
    new[1] = SCREEN_HEIGHT - new[1] * max(SCREEN_WIDTH, SCREEN_HEIGHT) / 100.0
    return [new[0], new[1]]

def desenha_faces(O):
    for face in O:
        desenha_face(face)

def desenha_face(face):
    for i in range(-1, len(face)-1):
        pointA = pointSRUtoScreen(face[i])
        pointB = pointSRUtoScreen(face[i-1])
        draw2DLine(screen, pointA, pointB, color, width)


# Inicializando tela

pygame.init()
pygame.display.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
screen.fill((0, 0, 0))


# Desenhando a imagem

running = True

while running:
    # A matriz original do objeto fica a esquerda
    transform_matrix = rotation_matrix_around_z(rotation[2])
    transform_matrix = numpy.matmul(rotation_matrix_around_y(rotation[1]), transform_matrix)

    transform_matrix = numpy.matmul(scaling_matrix(scale), transform_matrix)
    transform_matrix = numpy.matmul(translation_matrix(position[0], position[1], position[2]), transform_matrix)
    transform_matrix = numpy.matmul(oblique_parallel_projection_matrix(120), transform_matrix)

    Z_in_world_coordinates = []
    
    for face in sweep_3D(N, m):
        Z_in_world_coordinates += [numpy.matmul(face, numpy.transpose(transform_matrix)).tolist()]

    

    #copy.deepcopy(N)
    #for i in range(-1, len(N)-1):
    #    Z_in_world_coordinates[i][0] += position[0]
    #    Z_in_world_coordinates[i][1] += position[1]
    #    Z_in_world_coordinates[i][2] += position[2]

    #print(Z_in_world_coordinates)


    # Desenha Objeto
    desenha_faces(Z_in_world_coordinates)
    #for i in range(-1, len(N)-1):
    #    pointA = pointSRUtoScreen(Z_in_world_coordinates[i][:2])
    #    pointB = pointSRUtoScreen(Z_in_world_coordinates[i-1][:2])
    #    draw2DLine(screen, pointA, pointB, color, width)

    # Desenha Borda
    draw2DLine(screen, [0, 0], [0, SCREEN_HEIGHT], Color("white"), 5)
    draw2DLine(screen, [0, SCREEN_HEIGHT], [SCREEN_WIDTH, SCREEN_HEIGHT], Color("white"), 5)
    draw2DLine(screen, [SCREEN_WIDTH, SCREEN_HEIGHT], [SCREEN_WIDTH, 0], Color("white"), 5)
    draw2DLine(screen, [SCREEN_WIDTH, 0], [0, 0], Color("white"), 5)

    pygame.time.wait(50)
    pygame.display.flip()

    # Se for na posicao inicial, esperar um pouco antes de comecar o movimento
    if (position == initial_position):
        pygame.time.wait(5000)

    screen.fill((0, 0, 0))

    position[0] += velocity[0]
    position[1] += velocity[1]
    position[2] += velocity[2]
    rotation[0] += rotation_velocity[0]
    rotation[1] += rotation_velocity[1]
    rotation[2] += rotation_velocity[2]

    if (position[0] < 0 and position[1] > 100):
        running = False



pygame.time.wait(5000)
