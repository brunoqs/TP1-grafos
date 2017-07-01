#!/usr/bin/env python

import sys
import numpy as np #biblioteca usada para pegar a matriz triangular 
import copy 

class grafo:

	#construtor
	def __init__(self):
		self.nome_arq = sys.argv[1]
		self.arquivo = open(self.nome_arq, 'rw') #abrindo arquivo

		self.arquivo.readline() # pula a primeira linha
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
			if len(vertice) == 2: #entra quando tiver 2 conteudos em 1 linha do arquivo no caso 2 vertices
				vertice_x = int(vertice[0])
				vertice_y = int(vertice[1])
				self.ma[vertice_x][vertice_y] = 1
				if self.d[0] == "UNDIRECTED": #espelha a matriz se o grafo nao for direcionado
					self.ma[vertice_y][vertice_x] = 1

		self.arquivo.close()

	#funcao que converte matriz de adjacencia em lista de adjacencia
	def maTOla(self):
		la={} #criando dicionario
		la1=[] #criando lista
		for pos_linha in range(len(self.ma)):
			la1.append([]) # cria uma lista dentro da la1  
			for pos_coluna in range(len(self.ma[0])):
				if self.ma[pos_linha][pos_coluna] == 1: 
					la1[pos_linha].append(pos_coluna) # adiciona os vertices que fazem ligacao com 1 vertice
				else:
					la1[pos_linha]
			la[pos_linha] = la1[pos_linha] #adiciona as listas referente a cada vertice no dicionario
		return la

	#funcao que converte matriz de adjacencia em matriz de incidencia
	def maTOmi(self):
		if self.d[0] == "UNDIRECTED":
			w, h = self.qt_aresta, self.qt_vertice
			mi = [[0 for i in range(h)] for j in range(w)]
			ma_div = np.triu(self.ma, k=0) #pega a matriz triangular superior
		else:
			w, h = self.qt_aresta, self.qt_vertice
			mi = [[0 for i in range(h)] for j in range(w)]
			ma_div = self.ma

		aresta = 0
		for pos_linha in range(len(ma_div)):
		  	for pos_coluna in range(len(ma_div[0])):
		  		if ma_div[pos_linha][pos_coluna] == 1:
		  			if self.d[0] == "UNDIRECTED":
		  				mi[aresta][pos_coluna] = 1
		  				mi[aresta][pos_linha] = 1
		  			else:
		  				mi[aresta][pos_coluna] = -1
		  				mi[aresta][pos_linha] = 1
		  			aresta+=1
		return mi

	#funcao de busca em largura, que retorna o caminho apartir de um vertice inicial
	#https://stackoverflow.com/questions/24895564/python-dfs-optimised-algorithm
	#http://code.activestate.com/recipes/576723-dfs-and-bfs-graph-traversal/
	def bfs(self, start, grafo):
		path = [] #caminho percorrido
		Q = [start]
		while Q:
			v = Q.pop(0)
			if not v in path and grafo[v]:
				path.append(v)
				Q = Q + grafo[v] #empilha os vizinhos de 1 vertice

		return path

	#Existe um unico vertice que, se retirado, causaria uma desconexao no grafo?
	def P2(self, grafo):
		vertices_removidos = []
		backup = {}
		backup = copy.deepcopy(grafo) # faz um backup
		for chave in grafo.keys():
			del grafo[chave] # remove o vertice e suas arestas
			for a in grafo.values(): 
				if chave in a:
					a.remove(chave) # remove arestas que interligava o vertice que foi removido
			if chave == 0: 
				if self.desconexo() == "Desconexo":
					if len(self.bfs(1, grafo)) < self.qt_vertice-2: # testa bfs pra ver se o grafo ficou desconexo
						vertices_removidos.append(chave)
				else:
					if len(self.bfs(1, grafo)) < self.qt_vertice-1:
						vertices_removidos.append(chave)
			else:
				if self.desconexo() == "Desconexo":
					if len(self.bfs(0, grafo)) < self.qt_vertice-2:
						vertices_removidos.append(chave)
				else:
					if len(self.bfs(0, grafo)) < self.qt_vertice-1:
						vertices_removidos.append(chave)
			grafo = copy.deepcopy(backup) # copia backup para grafo
		return vertices_removidos

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
		ma = self.dfs_recursiva(grafo,0,caminho)
		#print ma
		G_T = self.grafo_transposto(self.ma)
		mb = self.dfs_recursiva(G_T,0,caminho)
		#print mb
		ma.sort() #Ordena a lista
		mb.sort()
		if ma != mb:
			return False
		else:
			return True

	#Partindo de um vertice qualquer, quantos outros vertices podemos alcancar no grafo?
	def P3(self, vert):
		return len(self.bfs(vert, self.maTOla()))

	def desconexo(self):
		for linha in self.ma:
			if linha.count(0) == self.qt_vertice: #se uma linha da matriz for 0, entao o grafo e desconexo
				conexao = "Desconexo"
				return conexao
			else:
				conexao = "indefinido"
				return conexao

	#O grafo e desconexo, (fracamente) conexo, semi-fortemente conexo ou fortemente conexo?
	def P5(self):
		if self.verifica_conexo_direcionado(self.maTOla()) == True:
			print "Fortemente conexo"
		elif self.desconexo() == "Desconexo":
			print "Desconexo"

	def visitado_lista(self,v,visited,grafo,visitados):
		visited[v] = True #Marca o vertice como visitado
		visitados.append(v)
		for i in grafo[v]:
			if visited[i] == False:          
				g.visitado_lista(i, visited,grafo,visitados)
		return visitados
                
	def DFS(self,v,grafo):
		visitados = []
		visited = [False]*(len(grafo))  # Cria uma lista com o numero total de vertices, todos os valores igual a False
		visitados = g.visitado_lista(v,visited,grafo,visitados)
		return visitados

	def ponte_busca(self,u,visitado,parentes,low,disc,grafo,Time):
		children = 0  
		visitado[u] = True #vertice de inicio marcado como visitado
		disc[u] = Time #vertice acima marcado com tempo 0
		low[u] = Time #vertice abaixo marcado com tempo 0
		Time += 1 # imcremento no tempo
		for v in grafo[u]: # executa ate o vertice de busca
			if visitado[v] == False:
				parentes[v] = u
				children+= 1
				g.ponte_busca(v,visitado,parentes,low,disc,grafo,Time) #BFS 
				low[u] = min(low[u], low[v])
				if low[v] > disc[u]:	
					print 'Ponte(s):', u,v
				else:
					return False
			elif v != parentes[u]:
				low[u] = min(low[u], disc[v])
				
	#Se for conexo, qual aresta que se retirada o torna desconexo? Existe apenas uma oumais arestas com essa peculiaridade?
	def P1(self,grafo,V):
		Time = 0 #Inicia o tempo com zero
		visitado = [False] * (len(grafo)) #lista com False/ lista com a mesma quantidade de vertices
		disc = [float("Inf")] * (len(grafo)) #lisca com tempo-Inf /lista com a mesma quantidade de vertices
		low = [float("Inf")] * (len(grafo)) #lista com tempo-Inf / lista com a mesma quantidade de vertices
		parentes = g.DFS(V,grafo)#lista com os vertices percorridos com uma DFS
		for i in range(len(grafo[V])):# for ate o numero de vertices
			if visitado[i] == False:# se o vertice nao foi visitado chama a funcao de busca de ponte
				res =  g.ponte_busca(i,visitado,parentes,low,disc,grafo,Time)
			if res == False:#se o retorno for igual a False o grafo nao tem pontes
				print "O grafo nao possui pontes"

# https://stackoverflow.com/questions/15646307/algorithm-for-diameter-of-graph ideia para implementar o diametro

#http://ctr.wikia.com/wiki/Find_the_graph_diameter diametro
#http://www.inf.ufsc.br/grafos/definicoes/definicao.html conceitos grafos
#http://www3.ifrn.edu.br/~jurandy/fdp/doc/aprenda-python/index.html doc python br
#main
if __name__ == "__main__":
	g = grafo()
	g.lerArquivo()
	print np.matrix(g.ma)
	print g.maTOla()
	print np.matrix(g.maTOmi())
	print g.P3(0)
	la = g.maTOla()
	print g.P2(la)
	g.P5()
	la1 = g.maTOla()
	g.P1(la1,0)



#aparentemente o main do jeito que o mayron viado vai querer
#	if sys.argv[2] == "-p1":
#		if g.d[0] == "UNDIRECTED":
#			print "TODO"
#	if sys.argv[3] == "-p2":
#		if g.d[0] == "UNDIRECTED":
#			la = g.maTOla()
#			print g.P2(la)
#
#	if sys.argv[4] == "-p3" and sys.argv[5] != "-p4" or sys.argv[6] != "-p5":
#		if sys.argv[5] != "-p4":
#			print g.P3(int(sys.argv[5]))
#		if sys.argv[6] != "-p5":
#			print g.P3(int(sys.argv[6]))
#
#	if sys.argv[5] == "-p4":
#		print "TODO"
#	if sys.argv[6] == "-p5":
#		g.P5()
#	if sys.argv[7] == "-p6":
#		if g.d[0] == "DIRECTED":
#			print "TODO"

