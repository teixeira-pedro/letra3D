import time
import pygame
import os
from math import *
from pygame import *
from pygame.locals import*



#------------------------DISPLAY RESOLUCAO--------------------------
#Resolucao do OS / informacao do video
#print(pygame.display.Info())
#-------------------------------------------------------------------
#---------------------OPERACOES MATEMATICAS-------------------------
#Operaooes matematicas sobre pontos e arestas

def mu_mat(A,B):
    C=[]
    if(len(A)!=len(len(B))):
        return C
    for i in range(len(A)):
        linha=[]
        for j in range(len(B)):
            result=0
            for k in range(len(B)):
                result+=(A[i][k]*B[k][j])
            linha.append(result)
        C.append(linha)
    return C
def imp_mat(A):
    for linha in A:
        print(linha)
def matriz_rotacao_2d(angulo_rdn):
    return [
            [],
            [],
            [],
            ]
def matriz_translacao_2d(t):
    return [
            [1,0,t],
            [0,1,t],
            [0,0,t],
            ]
def anima_translada_2d(O,t,a):
    i=0
    while(i<=1):
        a_a=0
        t_a=0
        i=i+0.02
        
#-------------------------------------------------------------------
#----------------------------------ED-------------------------------
#Definindo SRU
class SRU:
    def __init__(self,i,f,res):
        self._I=i#[0,0]
        self._F=f#[100,100]
        self.resolucao=res
        self.escala=int(res[0]/f[0])
        


    def get_I(self):
        return self._I

    def get_F(self):
        return self._F

    def printt(self):
        print(self.to_string())
    
    def to_string(self):
        return '[SRU]-> I:'+str(self._I)+'; F:'+str(self._F)

    #Python considera sua origem no canto superior esquerdo
    #deve-se converter do sru para o python, e vice-versa para fins de
    #se imprimir na tela pelo motivo explicado anteriormente.
    def SRU_2_py(self,ponto):
        novo=ponto
        F=self.get_F()
        return [ponto[0]*self.escala,(F[0]-ponto[1])*self.escala]

    
#Definindo Aresta
#   a classe ira possuir como atributos,
#   sua metrica, matematicamente definida e ,
#   sua implementaoco ou instanciamento utilizando a biblioteca grafica de python

class Aresta:
    def __init__(self,p_i,p_f,g):
        #pontos inicial e final definidos
        self.I=p_i
        self.F=p_f
        self.gros=g


    def printt(self):
        print(self.to_string())
    
    def to_string(self):
        return '[Aresta]-> I:'+str(self.I)+'; F:'+str(self.F)+'; gros:'+str(self.gros)

    
    def _I(self):
        return self.I
    def _F(self):
        return self.F
    def grossura(self):
        return self.gros
    def set_grossura(self,g):
        self.gros=g
    def I_x(self):
        return self.I[0]
    def I_y(self):
        return self.I[1]
    def F_x(self):
        return self.F[0]
    def F_y(self):
        return self.F[1]
    def set_I_x(self,n):
        self.I[0]=n
    def set_I_y(self,n):
        self.I[1]=n
    def set_F_x(self,n):
        self.F[0]=n
    def set_F_y(self,n):
        self.F[1]=n
        



class Objeto2D :
    def __init__(self,p_i):
        self.P=p_i
        self.arestas=[]
        self.pontos=[]

    def printt(self):
        print(self.to_string())
    
    def to_string(self):
        k='[Objeto2D]-> P:'+str(self.P)+'; \nArestas:['
        for aresta in self.arestas :
            k=k+(aresta.to_string()+' , ')
        k=k+']\nPontos:['
        for ponto in self.pontos :
            k=k+(str(ponto)+' , ')
        k=k+']'
        return k

    def append_ponto(self,P):
        self.pontos.append(P)
    def retira_ponto(self,P):
        for i in range(len(self.pontos)):
            if self.pontos[i][0]==P[0] and self.pontos[i][1]==P[1] :
                self.pontos.remove(self.pontos[i])
    def ponto(self,P):
        for i in range(len(self.pontos)):
            if self.pontos[i][0]==P[0] and self.pontos[i][1]==P[1] :
                return self.pontos[i]
        return []                       
    def set_ponto(self,P,nP):
        for i in range(len(self.pontos)):
            if self.pontos[i][0]==P[0] and self.pontos[i][1]==P[1] :
                self.pontos[i][0]=nP[0]
                self.pontos[i][1]=nP[1]

    def append_aresta(self,A):
        self.arestas.append(A)
    def retira_aresta(self,A):
        for i in range(len(self.arestas)):
            if arestas_iguais(self.arestas[i],A) :
                self.arestas.remove(self.arestas[i])
    def aresta(self,A):
        for i in range(len(self.arestas)):
            if arestas_iguais(self.arestas[i],A) :
                return self.arestas[i]
        return None                     
    def set_aresta(self,A,nA):
        for i in range(len(self.arestas)):
            if arestas_iguais(self.arestas[i],A) :
                self.arestas[i]=nA

    def mostra(self,SR,tela,cor):
        for i in range(len(self.arestas)):
            aresta=self.arestas[i]
            #log('desenhando:',tela,cor,aresta._I(),aresta._F(),aresta.grossura())
            pygame.draw.line(tela,cor,SR.SRU_2_py(aresta._I()),SR.SRU_2_py(aresta._F()),aresta.grossura())
            #conversao do SRU para py in loco
        pygame.display.update()

    def translada_para_pos(self,x,y,tx,ty,SR,tela,cor,matr):
        if not matr:
            while self.P[0]!=x and self.P[1]!=y :
                self.P[0]+=tx
                self.P[1]+=ty
                for i in range(len(self.arestas)):
                    self.arestas[i]._I()[0]+=tx
                    self.arestas[i]._I()[1]+=ty
                    self.arestas[i]._F()[0]+=tx
                    self.arestas[i]._F()[1]+=ty
                for i in range(len(self.pontos)):
                    self.pontos[i][0]+=tx
                    self.pontos[i][1]+=ty
                self.mostra(SR,tela,cor)
                
            return 1
        else:
            return 1

    def f_001(self,x,y,tx,ty,SR,tela,cor,matr):
        if not matr:
            while self.P[0]>=x and self.P[1]<=y :
                self.P[0]+=tx
                self.P[1]+=ty
                for i in range(len(self.arestas)):
                    self.arestas[i]._I()[0]+=tx
                    self.arestas[i]._I()[1]+=ty
                    self.arestas[i]._F()[0]+=tx
                    self.arestas[i]._F()[1]+=ty
                for i in range(len(self.pontos)):
                    self.pontos[i][0]+=tx
                    self.pontos[i][1]+=ty
                self.mostra(SR,tela,cor)
                
            return 1
        else:
            return 1
        
    def f_003(self,it,theta_f,kx_f,ky_f,SR,tela,cor):
        for i in range(it):
            self.mostra(SR,tela,cor)
            z=i+1
            theta=z*theta_f
            x=kx_f*z
            y=z*ky_f
            vt=self.P
            for j in range(len(self.arestas)):
                #print(self.arestas[j]._I()[0],self.arestas[j]._I()[1],self.arestas[j]._F()[0],self.arestas[j]._F()[1])
                #(i,it,theta_f,kx_f,ky_f,z,x,y,theta,self.P)
                #etapa 1, colocando o objeto na origem
                
                self.arestas[j]._I()[0]=self.arestas[j]._I()[0]-vt[0]
                self.arestas[j]._I()[1]=self.arestas[j]._I()[1]-vt[1]
                self.arestas[j]._F()[0]=self.arestas[j]._F()[0]-vt[0]
                self.arestas[j]._F()[1]=self.arestas[j]._F()[1]-vt[1]
                #print(self.P)
                #self.mostra(SR,tela,cor)
                #etapa 2, girando-o e translad
                self.arestas[j]._I()[0]=(self.arestas[j]._I()[0]*cos(radians(theta)))-(self.arestas[j]._I()[1]*sin(radians(theta)))#### += ou = ?
                self.arestas[j]._I()[1]=(self.arestas[j]._I()[0]*sin(radians(theta)))+(self.arestas[j]._I()[1]*cos(radians(theta)))
                self.arestas[j]._F()[0]=(self.arestas[j]._F()[0]*cos(radians(theta)))-(self.arestas[j]._F()[1]*sin(radians(theta)))
                self.arestas[j]._F()[1]=(self.arestas[j]._F()[0]*sin(radians(theta)))+(self.arestas[j]._F()[1]*cos(radians(theta)))
                #etapa 3, colocando o de volta em W
                self.arestas[j]._I()[0]=self.arestas[j]._I()[0]+vt[0]
                self.arestas[j]._I()[1]=self.arestas[j]._I()[1]+vt[1]
                self.arestas[j]._F()[0]=self.arestas[j]._F()[0]+vt[0]
                self.arestas[j]._F()[1]=self.arestas[j]._F()[1]+vt[1]
                #etapa 4, transladando-o #OK
                self.arestas[j]._I()[0]+=x
                self.arestas[j]._I()[1]+=y
                self.arestas[j]._F()[0]+=x
                self.arestas[j]._F()[1]+=y
                #etapa 5, atualizando W
                #self.P[0]+=x
                #self.P[1]+=y
            #fazendo o mesmo pros pontos
            #for j in range(len(self.pontos)):
                #etapa 1, colocando o objeto na origem
            #    self.pontos[j][0]-=self.P[0]
            #    self.pontos[j][1]-=self.P[1]
                #etapa 2, girando-o
            #    self.pontos[j][0]=(self.pontos[j][0]*cos(radians(z*theta_f)))-(self.pontos[j][1]*sin(radians(z*theta_f)))#### += ou = ?
            #    self.pontos[j][1]=(self.pontos[j][0]*sin(radians(z*theta_f)))+(self.pontos[j][1]*cos(radians(z*theta_f)))
                #etapa 3, colocando o de volta em W
            #    self.pontos[j][0]+=self.P[0]
            #    self.pontos[j][1]+=self.P[1]
                #etapa 4, transladando-o
            #    self.pontos[j][0]+=(z*kx_f)
            #    self.pontos[j][1]+=(z*ky_f)
        #etapa 6, mostra na tela
            pygame.time.wait(100)
            self.mostra(SR,tela,cor)    
                
                
                
                
    def f_002(self,max_ang,max_x,max_y,SR,tela,cor):
        theta=0
        #90 0 100
        while theta <=max_ang and self.P[0]>= max_x and self.P[1]<=max_y:
            self.mostra(SR,tela,cor)
            #z=i+1
            #theta=z*theta_f
            #x=kx_f*z
            #y=z*ky_f
            #vt=self.P#-[0,0]
            theta+=1.8
            
            for j in range(len(self.arestas)):
                #print(self.arestas[j]._I()[0],self.arestas[j]._I()[1],self.arestas[j]._F()[0],self.arestas[j]._F()[1])
                #(i,it,theta_f,kx_f,ky_f,z,x,y,theta,self.P)
                #etapa 1, colocando o objeto na origem
                
                #self.arestas[j]._I()[0]=self.arestas[j]._I()[0]-vt[0]
                #self.arestas[j]._I()[1]=self.arestas[j]._I()[1]-vt[1]
                #self.arestas[j]._F()[0]=self.arestas[j]._F()[0]-vt[0]
                #self.arestas[j]._F()[1]=self.arestas[j]._F()[1]-vt[1]
                #print(self.P)
                #self.mostra(SR,tela,cor)
                #etapa 2, girando-o e translad
                self.arestas[j]._I()[0]+=(-1+(self.arestas[j]._I()[0]*cos(radians(theta)))-(self.arestas[j]._I()[1]*sin(radians(theta))))#### += ou = ?
                self.arestas[j]._I()[1]+=(2+(self.arestas[j]._I()[0]*sin(radians(theta)))+(self.arestas[j]._I()[1]*cos(radians(theta))))
                self.arestas[j]._F()[0]+=(-1+(self.arestas[j]._F()[0]*cos(radians(theta)))-(self.arestas[j]._F()[1]*sin(radians(theta))))
                self.arestas[j]._F()[1]+=(2+(self.arestas[j]._F()[0]*sin(radians(theta)))+(self.arestas[j]._F()[1]*cos(radians(theta))))
                #etapa 3, colocando o de volta em W
                #self.arestas[j]._I()[0]=self.arestas[j]._I()[0]+vt[0]
                #self.arestas[j]._I()[1]=self.arestas[j]._I()[1]+vt[1]
                #self.arestas[j]._F()[0]=self.arestas[j]._F()[0]+vt[0]
                #self.arestas[j]._F()[1]=self.arestas[j]._F()[1]+vt[1]
                #etapa 4, transladando-o #OK
                #self.arestas[j]._I()[0]+=(x+(self.arestas[j]._I()[0]*cos(radians(theta)))-(self.arestas[j]._I()[1]*sin(radians(theta))))
                #self.arestas[j]._I()[1]+=(y+(self.arestas[j]._I()[0]*sin(radians(theta)))+(self.arestas[j]._I()[1]*cos(radians(theta))))
                #self.arestas[j]._F()[0]+=(x+(self.arestas[j]._F()[0]*cos(radians(theta)))-(self.arestas[j]._F()[1]*sin(radians(theta))))
                #self.arestas[j]._F()[1]+=(y+(self.arestas[j]._I()[0]*sin(radians(theta)))+(self.arestas[j]._I()[1]*cos(radians(theta))))
                #etapa 5, atualizando W
                self.P[0]+=(-1+(self.P[0]*cos(radians(theta)))-(self.P[1]*sin(radians(theta))))
                self.P[1]+=(2+(self.P[1]*sin(radians(theta)))+(self.P[1]*cos(radians(theta))))
            #fazendo o mesmo pros pontos
            #for j in range(len(self.pontos)):
                #etapa 1, colocando o objeto na origem
            #    self.pontos[j][0]-=self.P[0]
            #    self.pontos[j][1]-=self.P[1]
                #etapa 2, girando-o
            #    self.pontos[j][0]=(self.pontos[j][0]*cos(radians(z*theta_f)))-(self.pontos[j][1]*sin(radians(z*theta_f)))#### += ou = ?
            #    self.pontos[j][1]=(self.pontos[j][0]*sin(radians(z*theta_f)))+(self.pontos[j][1]*cos(radians(z*theta_f)))
                #etapa 3, colocando o de volta em W
            #    self.pontos[j][0]+=self.P[0]
            #    self.pontos[j][1]+=self.P[1]
                #etapa 4, transladando-o
            #    self.pontos[j][0]+=(z*kx_f)
            #    self.pontos[j][1]+=(z*ky_f)
        #etapa 6, mostra na tela
            
            self.mostra(SR,tela,cor)    
            pygame.time.wait(500)

    def log(self,string,arquivo):
        arquivo.write(string+'\n')      
                
                
    def translada_e_gira(self,it,theta_f,kx_f,ky_f,SR,tela,cor,arq):
        for i in range(it):
            self.mostra(SR,tela,cor)
            z=i+1
            theta=z*theta_f
            x=kx_f*z
            y=z*ky_f
            vt=self.P#-[0,0]
            for j in range(len(self.arestas)):
                self.arestas[j]._I()[0]=(x+(self.arestas[j]._I()[0]*cos(radians(theta)))-(self.arestas[j]._I()[1]*sin(radians(theta))))
                self.arestas[j]._I()[1]=(y+(self.arestas[j]._I()[0]*sin(radians(theta)))+(self.arestas[j]._I()[1]*cos(radians(theta))))
                self.arestas[j]._F()[0]=(x+(self.arestas[j]._F()[0]*cos(radians(theta)))-(self.arestas[j]._F()[1]*sin(radians(theta))))
                self.arestas[j]._F()[1]=(y+(self.arestas[j]._F()[0]*sin(radians(theta)))+(self.arestas[j]._F()[1]*cos(radians(theta))))
            pygame.time.wait(200)
            self.log(self.to_string()+'\n'+'\t'+str(it)+'\t'+str(theta)+'\t'+str(x)+'\t'+str(y),arq)
            self.mostra(SR,tela,cor)    
            
            
                
                
            
        


    def translada_direct(self,vx,vy):
        self.P[0]=self.P[0]+vx
        self.P[1]=self.P[1]+vy
        for i in range(len(self.arestas)):
            self.arestas[i]._I()[0]=self.arestas[i]._I()[0]+vx
            self.arestas[i]._I()[1]=self.arestas[i]._I()[1]+vy

        
#-------------------------------------------------------------------        
#-----------------------FUNooES AUXILIARES--------------------------
def arestas_iguais(A,B):
    if type(A)!=type(B):
        return 0
    if type(A)!=type(Aresta([],[],0)):
        return 0

    return (((A.I_x()==B.I_x())and(A.I_y()==B.I_y()))and((A.F_x()==B.F_x())and(A.F_y()==B.F_y())) or
            ((A.I_x()==B.F_x())and(A.I_y()==B.F_y()))and((A.F_x()==B.I_x())and(A.F_y()==B.I_y())))####last
#-------------------------------------------------------------------
#-----------------------------EXECUocO------------------------------

    
resolucao=(500,500)
#inicializando SRU
#root=Tk()
pygame.init()
tl=pygame.display.set_mode()
sys_resolution=tl.get_size()
pygame.quit()
SR=SRU([0,0],[100,100],resolucao)
print("I=",SR.get_I())#
print("F=",SR.get_F())#
ff=SR.get_F()
cor=[0,255,0]


#definindo limites pelo SRU
limits_py=SR.SRU_2_py(ff)


#criando objeto
O_l=Objeto2D([50,5])##L
O_l.append_ponto([45,0])#f
O_l.append_ponto([45,10])#a
O_l.append_ponto([47,10])#b
O_l.append_ponto([47,2])#c
O_l.append_ponto([55,2])#d
O_l.append_ponto([55,0])#e
O_l.append_aresta(Aresta([45,0],[45,10],1))#FA
O_l.append_aresta(Aresta([45,10],[47,10],1))#AB
O_l.append_aresta(Aresta([47,10],[47,2],1))#BC
O_l.append_aresta(Aresta([47,2],[55,2],1))#CD
O_l.append_aresta(Aresta([55,2],[55,0],1))#DE
O_l.append_aresta(Aresta([55,0],[45,0],1))#EF



arq=open('log_.txt','w')
arq.write('resolucao da tela:'+str(resolucao)+' resoluoco do sistema:'+str(sys_resolution)+' cor do objeto [R,G,B]: '+str(cor)+"limites_py="+str(limits_py)+' SRU='+str(SR.get_I())+' '+str(SR.get_F())+'\n')
arq.write('**************\n<posicoes de cada aresta>\n<theta>\t<x>\t<y>**************\n')

        

tela=pygame.display.set_mode(resolucao)
#print(tela.display.Info())

#O_l.translada_para_pos(0,100,SR,tela,cor)
    #O_l.P[0]=O_l.P[0]-0.1
    #O_l.P[0]
#O_l.mostra(SR,tela,cor)
#O_l.translada_para_pos(0,100,-1,+1,SR,tela,cor,[])
O_l.translada_e_gira(60,1.5,-0.8333,1.6667,SR,tela,cor,arq)

arq.close()


#O_l.f_002(90,0,100,SR,tela,cor)
#pygame.draw.line(tela,[255,255,255],[50,50],[50,100],5)
#pygame.draw.line(tela,[255,255,255],[50,100],[75,100],5)
#pygame.display.update()
#pygame.display.update()
