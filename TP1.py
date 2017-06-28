#!/usr/bin/env python

import sys
import numpy as np #biblioteca usada para pegar a matriz triangular 

class grafo:

	#construtor
	def __init__(self):
		self.nomeArq = sys.argv[1]
		self.arquivo = open(self.nomeArq, 'rw') #abrindo arquivo

		self.arquivo.readline() # lendo a primeira linha
		self.d = self.arquivo.readline().split() #variavel para ver se o grafo e direcionado ou nao

		self.arquivo.readline() # pula uma linha
		self.qtVertice = self.arquivo.readline() #armazenando a quantidade de vertices em qtVertice
		self.qtVertice = int(self.qtVertice) #conversao int

		self.qtAresta = len(self.arquivo.readlines()) #armazenando a quantidade de aresta em qtAresta

		self.arquivo.close() #fechando arquivo

		#instanciando matriz de adjacencia com valor 0
		w, h = self.qtVertice, self.qtVertice
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
				if self.d[0] == "UNDIRECTED":
					self.ma[verticeY][verticeX] = 1

		self.arquivo.close()

	#funcao que converte matriz de adjacencia em lista de adjacencia
	def maTOla(self):
		la={} #criando dicionario
		la1=[] #criando lista
		for pos_linha in range(len(self.ma)):
			la1.append([]) # cria uma lista dentro de la1 para cada vertice 
			for pos_coluna in range(len(self.ma[0])):
				if self.ma[pos_linha][pos_coluna] == 1: 
					la1[pos_linha].append(pos_coluna) # adiciona os vertices que fazem ligacao com 1 vertice
				else:
					la1[pos_linha]
			la[pos_linha] = la1[pos_linha] #adiciona as lista no dicionario
		return la

	#funcao que converte matriz de adjacencia em matriz de incidencia
	def maTOmc(self):
		if self.d[0] == "UNDIRECTED":
			w, h = self.qtAresta, self.qtVertice
			mc = [[0 for i in range(w)] for j in range(h)]
			maDiv = np.triu(self.ma, k=0) #pega a matriz triangular superior
		else:
			w, h = self.qtAresta, self.qtVertice
			mc = [[0 for i in range(w)] for j in range(h)]
			maDiv = self.ma

		qt = 0
		for pos_linha in range(len(maDiv)):
			if qt > self.qtAresta:
		  		break
		  	for pos_coluna in range(len(maDiv[0])):
		  		if maDiv[pos_linha][pos_coluna] == 1:
		  			if self.d[0] == "UNDIRECTED":
		  				mc[qt][pos_coluna] = 1
		  				mc[qt][pos_linha] = 1
		  			else:
		  				mc[qt][pos_coluna] = -1
		  				mc[qt][pos_linha] = 1
		  			qt+=1
		  			print qt
		return mc

	#funcao de busca em largura, que retorna o caminho apartir de um vertice inicial
	#https://stackoverflow.com/questions/24895564/python-dfs-optimised-algorithm
	#http://code.activestate.com/recipes/576723-dfs-and-bfs-graph-traversal/
	def bfs(self, start, la):
		path = [] #caminho percorrido
		Q = [start]
		while Q:
			v = Q.pop(0)
			if not v in path:
				path.append(v)
				Q = Q + la[v]
		return path
	
#main
if __name__ == "__main__":
	g = grafo()
	g.lerArquivo()
	print np.matrix(g.ma)
	print g.maTOla()
	print np.matrix(g.maTOmc())
	la = g.maTOla()
	print g.bfs(0, la)