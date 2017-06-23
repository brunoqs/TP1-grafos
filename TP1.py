#!/usr/bin/env python

import sys
import numpy as np #biblioteca usada para pegar a matriz triangular 

class grafo:

	#construtor
	def __init__(self):
		#abrindo arquivo
		self.nomeArq = sys.argv[1]
		self.arquivo = open(self.nomeArq, 'rw')

		#lendo a primeira linha do arquivo e separando o conteudo
		self.qtVertice = self.arquivo.readline().split() #armazenando a quantidade de vertices em qtVertice
		self.qtVertice = int(self.qtVertice[0]) #conversao int

		self.d = self.arquivo.readline(3).split() #variavel para ver se o grafo e direcionado ou nao

		self.qtAresta = len(self.arquivo.readlines())#armazenando a quantidade de aresta em qtAresta

		#fechando arquivo
		self.arquivo.close()

		#instanciando matriz de adjacencia com valor 0
		w, h = self.qtVertice, self.qtVertice;
		self.ma = [[0 for i in range(w)] for j in range(h)]

	#funcao que le o arquivo e armazena o grafo em uma matriz de adjacencia
	def lerArquivo(self):
		self.arquivo = open(self.nomeArq, 'rw')
		for linha in self.arquivo:
			vertice = linha.split() #pega cada linha do arquivo e separa o conteudo
			if len(vertice) == 2: #entra quando tiver 2 conteudos em 1 linha no caso 2 arestas
				verticeX = int(vertice[0])
				verticeY = int(vertice[1])
				self.ma[verticeX][verticeY] = 1
		self.arquivo.close()

	#funcao que converte matriz de adjacencia em lista de adjacencia
	def maTOla(self):
		la=[]
		for pos_linha in range(len(self.ma)):
			la.append([]) # cria uma lista dentro de L para cada vertice 
			for pos_coluna in range(len(self.ma[0])):
				if self.ma[pos_linha][pos_coluna] == 1: 
					la[pos_linha].append(pos_coluna) # adiciona os vertices que fazem ligacao com 1 vertice
				else:
					la[pos_linha]
		return la

	#funcao que converte matriz de adjacencia em matriz de incidencia
	def maTOmc(self):
		if self.d[0] == "ND":
			w, h = self.qtAresta/2, self.qtVertice
			mc = [[0 for i in range(w)] for j in range(h)]
			maDiv = np.triu(self.ma, k=0)#pega a matriz triangular superior
		else:
			w, h = self.qtAresta, self.qtVertice
			mc = [[0 for i in range(w)] for j in range(h)]
			maDiv = self.ma

		qt = 0
		for pos_linha in range(len(self.ma)):
		  	for pos_coluna in range(len(self.ma[0])):
		  		if maDiv[pos_linha][pos_coluna] == 1:
		  			if self.d[0] == "ND":
		  				mc[qt][pos_coluna] = 1
		  				mc[qt][pos_linha] = 1
		  			else:
		  				mc[qt][pos_coluna] = -1
		  				mc[qt][pos_linha] = 1
		  			qt+=1
		return mc

#main
if __name__ == "__main__":
    g = grafo()
    g.lerArquivo()
    print g.ma
    print g.maTOla()
    print g.maTOmc()