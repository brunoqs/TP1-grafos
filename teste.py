#!/usr/bin/env python

import sys
import numpy as np

#abrindo arquivo
nomeArq = sys.argv[1]
arquivo = open(nomeArq, 'rw')

#lendo a primeira linha do arquivo e separando o conteudo
qtVertice = arquivo.readline().split()
d = arquivo.readline(3).split() #variavel para ver se o grafo e direcionado ou nao

#conversao para int
qtVertice = int(qtVertice[0])

qtAresta = len(arquivo.readlines())
print qtAresta

#instanciando matriz com valor 0
w, h = qtVertice, qtVertice
grafo = [[0 for i in range(w)] for j in range(h)]

x,y = 0,0
#percorrendo arquivo linha por linha, cria uma matriz de adjacencia
for linha in arquivo:
	vertice = linha.split() #pega cada linha do arquivo e separa o conteudo
	if len(vertice) == 2: #entra quando tiver 2 conteudos em 1 linha no caso 2 arestas
		x+=4
		y+=4
		verticeX = int(vertice[0])
		verticeY = int(vertice[1])
		grafo[verticeX][verticeY] = 1
	else:
		x = 0
		y = 2
print grafo
#	if d[0] == "ND": #verifica se o grafo e direcionado ou nao e faz devidas alteracoes na matriz
#		grafo[verticeY][verticeX] = 1

print "\n\n"
#checar qt de arestas
#qtAresta = 0
#for pos_linha in range(len(grafo)):
#  	for pos_coluna in range(len(grafo[0])):
#  		if grafo[pos_linha][pos_coluna] == 1:
# 		 	qtAresta += 1
#if d[0] == "ND": #para grafo nao direcionado
#	qtAresta = qtAresta/2
#	print "aresta =", qtAresta
#else: #para grafo direcionado
#	print "aresta =", qtAresta

#converter matriz de adj para lista de adj
L=[]
for pos_linha in range(len(grafo)):
	L.append([]) # cria uma lista dentro de L para cada vertice 
	for pos_coluna in range(len(grafo[0])):
		if grafo[pos_linha][pos_coluna] == 1: 
			L[pos_linha].append(pos_coluna) # adiciona os vertices que fazem ligacao com 1 vertice
		else:
			L[pos_linha]
print L
print "\n\n"

#converter matriz de adj para matriz de inc
w, h = qtAresta, qtVertice
grafo2 = [[0 for i in range(w)] for j in range(h)]
qt = 0
grafodiv = np.triu(grafo, k=0)#pega a matriz triangular superior
for pos_linha in range(len(grafo)):
  	for pos_coluna in range(len(grafo[0])):
  		if grafodiv[pos_linha][pos_coluna] == 1:
  			grafo2[qt][pos_coluna] = 1
  			grafo2[qt][pos_linha] = 1
  			qt+=1

print grafo2
print "\n\n"

arquivo.close()


