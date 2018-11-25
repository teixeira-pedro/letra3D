import pygame
from pygame.locals import *
import numpy
from math import sqrt
import copy
import operator


# Configuracoes

# ESCOLHA O MODO PARA EXIBIR A LETRA
MODO = 3 # SELECIONAR 1 PARA WIREFRAME, 2 PARA NAO TRANSPARENTE, 3 PARA ILUMINADO



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



initial_position = [50, 50, 0]

# transform
position = initial_position.copy()
rotation = [0, 0, 90]

# etc
m = sqrt(2) # Menor aresta (calculada manualmente), usada como espessura
velocity = [0.00005, 0.00020, 0]
rotation_velocity = [0, 00.5, 00.1]


# Definindo funcoes


def scaling_matrix (scale):
    return [[scale, 0, 0, 0], [0, scale, 0, 0], [0, 0, scale, 0], [0, 0, 0, 1]]


def translation_matrix (x, y, z):
    return [[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]]

def oblique_parallel_projection_matrix (degrees, l = 1):
    degrees = numpy.deg2rad(degrees)
    return [[1, 0, l * numpy.cos(degrees), 0], [0, 1, l * numpy.sin(degrees), 0], [0, 0, 0, 0], [0, 0, 0, 1]]

def back_face_culling (object3D, projection, observer_point):
    temp_proj = copy.deepcopy(projection)
    for i in range(len(temp_proj)):
        if (temp_proj[i][i] == 0):
            temp_proj[i][i] == 1
    
    temp_obj = []
    for face in object3D:
        temp_obj += [list(numpy.matmul(face, numpy.transpose(temp_proj)))]

    new_object = []
    for i in range(len(temp_obj)):
        face_normal = normal_vector(temp_obj[i])
        a = list(map(operator.sub, temp_obj[i][0], observer_point))[:3]
        if (numpy.dot(a, face_normal) < 0):
            new_object += [object3D[i]]
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

N = reversed_normal(N)

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
        new_face = copy.deepcopy([object_3D[1][v], object_3D[1][(v + 1) % pts], object_3D[0][(v + 1) % pts], object_3D[0][v]])
        #new_face = reversed_normal(new_face)
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

def desenha_faces(O, projection):
    for face in O:
        desenha_face(face, projection)

def desenha_face(face, projection):
    polygon2D = list(numpy.matmul(face, numpy.transpose(projection)))
    for i in range(-1, len(polygon2D)-1):
        pointA = pointSRUtoScreen(polygon2D[i])
        pointB = pointSRUtoScreen(polygon2D[i-1])
        draw2DLine(screen, pointA, pointB, color, width)

def pinta_faces(object3D, projection, observer_point, color, luz_ponto=None, luz_intensidade=0):
    ordenado = faces_ordenadas_por_menor_dist(object3D, projection, observer_point)
    ordenado.reverse()
    for face in ordenado:
        pinta_face(face, projection, color, luz_ponto, luz_intensidade)

def pinta_face(face, projection, color, luz_direcional=None, luz_intensidade=0, width=0): # Luz pontual
    if (luz_direcional != None and luz_intensidade > 0):
        luz_direcional = list(-1 * numpy.array(luz_direcional))
        print(normal_vector(face))
        #incidence_vector = list(map(operator.sub, face[0], luz_ponto))
        radiance = luz_intensidade * numpy.clip(numpy.dot(normalize_vector3(normal_vector(face)), normalize_vector3(luz_direcional)), -1, 1)#numpy.cos(angle_between(normal_vector(face), luz_direcional))#incidence_vector))
        #color = Color(round(color.r * radiance), round(color.g * radiance), round(color.b * radiance), color.a)
        print(radiance)
        if (radiance < 0.2):
            radiance = 0.2
        color = Color(int(color.r * radiance), int(color.g * radiance), int(color.b * radiance), color.a)
    poligono2D = list(numpy.matmul(face, numpy.transpose(projection)))
    for i in range(len(poligono2D)):
        poligono2D[i] = pointSRUtoScreen(poligono2D[i])
    pygame.draw.polygon(screen, color, poligono2D, width)

def pinta_com_bordas(object3D, projection, observer_point, line_color, face_color):
    ordenado = faces_ordenadas_por_menor_dist(object3D, projection, observer_point)
    ordenado.reverse()
    for face in ordenado:
        pinta_face(face, projection, face_color)
        pinta_face(face, projection, line_color, width = width)

def dist_vet(v): #retorna tamanhao do vetor
    d=0
    for i in v:
        d+=(i**2)
    return sqrt(d)

def VET(A,B): #retorna vetor AB
    resp=[]
    if len(A)!=len(B):
        return []
    for i in range(len(A)):
        resp.append(B[i]-A[i])
    return resp

def dist_face(F,obser): #retorna o ponto mais proximo da face , juntamente com  a face
    i=float("inf")
    for P in F:
        if dist_vet(VET(P[:3],obser[:3]))<i:
            i=dist_vet(VET(P[:3],obser[:3]))
    return [i,F]

def tama(m): #funcao auxiliar pra ordenacao
    return m[0][0]

def faces_ordenadas_por_menor_dist(O, projection, obser): #pega o objeto, o ponto de observacao
    #cria uma lista contendo [o ponto mais proximo da face, a proporia face] de cada face
    #ordena a lista em relacao a distancia entre o ponto mais proximo da face e a observa
    #limpa a lista, deixando so  as faces ordenadas e retorna
    resp=[]
    k=[]

    temp_proj = copy.deepcopy(projection)
    for i in range(len(temp_proj)):
        if (temp_proj[i][i] == 0):
            temp_proj[i][i] == 1
    
    temp_obj = []
    for face in O:
        temp_obj += [list(numpy.matmul(face, numpy.transpose(temp_proj)))]

    for i in range(len(temp_obj)):
        k.append([dist_face(temp_obj[i],obser), i])
    k.sort(reverse=False,key=tama) # ordena em relacao a distancia de cada face em relacao ao O
    
    for i in range(len(temp_obj)):
        resp += [O[k[i][1]]]
    
    return copy.deepcopy(resp)

def normalize_vector2(vector2):
    v = copy.deepcopy(vector2)
    magnitude = sqrt(v[0]**2 + v[1]**2)
    return [v[0]/magnitude, v[1]/magnitude]

def normalize_vector3(vector3):
    v = copy.deepcopy(vector3)
    magnitude = sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    return [v[0]/magnitude, v[1]/magnitude, v[2]/magnitude]

def angle_between(v1, v2):
    v1_u = normalize_vector3(v1)
    v2_u = normalize_vector3(v2)
    return numpy.arccos(numpy.clip(numpy.dot(v1_u, v2_u), -1.0, 1.0))


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

    Z_in_world_coordinates = []
    
    for face in sweep_3D(N, m):
        Z_in_world_coordinates += [numpy.matmul(face, numpy.transpose(transform_matrix)).tolist()]


    observador = [0, 0, 100, 1]

    # Desenha Objeto

    z = Z_in_world_coordinates

    if (MODO == 1):
        desenha_faces(z, oblique_parallel_projection_matrix(120))
    elif (MODO == 2):
        z = back_face_culling(Z_in_world_coordinates, oblique_parallel_projection_matrix(120), observador)
        pinta_com_bordas(z, oblique_parallel_projection_matrix(120), observador, Color("Purple"), Color("Black"))
    elif (MODO == 3):
        z = back_face_culling(Z_in_world_coordinates, oblique_parallel_projection_matrix(120), observador)
        pinta_faces(z, oblique_parallel_projection_matrix(120), observador, Color("Orange"), [200, 200, -100], 1)

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
