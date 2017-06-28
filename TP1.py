#!/usr/bin/env python

import sys
import numpy as np #biblioteca usada para pegar a matriz triangular 

class grafo:

	#construtor
	def __init__(self):
		self.nome_arq = sys.argv[1]
		self.arquivo = open(self.nome_arq, 'rw') #abrindo arquivo

		self.arquivo.readline() # lendo a primeira linha
		self.d = self.arquivo.readline().split() #variavel para ver se o grafo e direcionado ou nao

		self.arquivo.readline() # pula uma linha
		self.qt_vertice = self.arquivo.readline() #armazenando a quantidade de vertices em qt_vertice
		self.qt_vertice = int(self.qt_vertice) #conversao int

		self.qt_aresta = len(self.arquivo.readlines()) #armazenando a quantidade de aresta em qt_aresta

		self.arquivo.close() #fechando arquivo

		#instanciando matriz de adjacencia com valor 0
		w, h = self.qt_vertice, self.qt_vertice
		self.ma = [[0 for i in range(w)] for j in range(h)]

	#funcao que le o arquivo e armazena o grafo em uma matriz de adjacencia
	def lerArquivo(self):
		self.arquivo = open(self.nome_arq, 'rw')
		for linha in self.arquivo:
			vertice = linha.split() #pega cada linha do arquivo e separa o conteudo
			if len(vertice) == 2: #entra quando tiver 2 conteudos em 1 linha no caso 2 arestas
				vertice_x = int(vertice[0])
				vertice_y = int(vertice[1])
				self.ma[vertice_x][vertice_y] = 1
				if self.d[0] == "UNDIRECTED":
					self.ma[vertice_y][vertice_x] = 1

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
			w, h = self.qt_aresta, self.qt_vertice
			mc = [[0 for i in range(h)] for j in range(w)]
			ma_div = np.triu(self.ma, k=0) #pega a matriz triangular superior
		else:
			w, h = self.qt_aresta, self.qt_vertice
			mc = [[0 for i in range(h)] for j in range(w)]
			ma_div = self.ma

		qt = 0
		for pos_linha in range(len(ma_div)):
		  	for pos_coluna in range(len(ma_div[0])):
		  		if ma_div[pos_linha][pos_coluna] == 1:
		  			if self.d[0] == "UNDIRECTED":
		  				mc[qt][pos_coluna] = 1
		  				mc[qt][pos_linha] = 1
		  			else:
		  				mc[qt][pos_coluna] = -1
		  				mc[qt][pos_linha] = 1
		  			qt+=1
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

	#Realiza a busca em profundidade no grafo e retorna o caminho        
	def dfs_recursiva(self, grafo, start, caminho):
		caminho = caminho + [start]
		for node in grafo[start]:
			if not node in caminho:
				caminho = self.dfs_recursiva(grafo, node, caminho)
		return caminho                              

	#pega um grafo representado em matriz de adj e calcula o grafo transposto
	def grafo_transposto(self,grafo):
		grafo_transp = []
		for j in range(len(grafo[0])):
			linha = []
			for i in range(len(grafo)):
				linha.append(grafo[i][j])
				grafo_transp.append(linha)
		return grafo_transp
        

	def verifica_conexo_direcionado(self,grafo):
		caminho = []
		ma = g.dfs_recursiva(la,0,caminho)
		print ma
		G_T = g.grafo_transposto(g.ma)
		mb = g.dfs_recursiva(G_T,0,caminho)
		print mb
		ma.sort() #Ordena a lista
		mb.sort()
		if ma != mb:
			return False
		else:
			return True

	#Existe um unico vertice que, se retirado, causaria uma desconexao no grafo?
	def P2(self, la):
		backup = []
		backup2 = {}
		tamLa = len(la)
		for a, vertice in la.iteritems():
			backup = vertice
			print "bk1", backup
			del la[a]
			backup2 = la
			print "bk2",backup2
			for vertice2, aresta in la.iteritems(): # pega a lista de arestas referente a cada vertice
				if aresta.count(a) == 1: # verifica se existe aresta do vertice removido na lista, se tiver ela e removida
					aresta.remove(a)
			if tamLa-1 > a:
				print "a",la
				print self.bfs(a+1 % tamLa, la)
				la = backup2
				la[a] = backup
			else:
				break

	#Partindo de um vErtice qualquer, quantos outros vErtices podemos alcanCar no grafo?
	def P3(self, vert):
		return len(self.bfs(vert, self.maTOla()))

#http://www3.ifrn.edu.br/~jurandy/fdp/doc/aprenda-python/index.html doc python br
#main
if __name__ == "__main__":
	g = grafo()
	g.lerArquivo()
	print np.matrix(g.ma)
	print g.maTOla()
	print np.matrix(g.maTOmc())
	la = g.maTOla()
	#print g.bfs(0, la)
	#print g.P2(la)
	#print g.P3(0)
	res = g.verifica_conexo_direcionado(g.ma)
	print 'Grafo conexo:',res