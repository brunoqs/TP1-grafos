#!/usr/bin/env python

import sys
import numpy as np #biblioteca usada para pegar a matriz triangular 
sys.setrecursionlimit(10000) #pilha de recursao aumentada para 10000

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

	#funcao busca em profundidade
	def DFS(self,v,grafo,flag = []):
		if flag == []:
			visitados = []
			visited = [False]*len(grafo)  # Cria uma lista com o numero total de vertices, todos os valores igual a False
			visitados = self.visitado_lista(v,visited,grafo,visitados)
			return visitados
		else:
			visitados = []
			visited = [False]*len(grafo)
			for a,valor in enumerate(grafo):
				if a == flag:
					visited[a]=True
		        visitados = self.visitado_lista(v,visited,grafo,visitados)
		return visitados 

	def visitado_lista(self,v,visited,grafo,visitados):
		visited[v] = True #Marca o vertice como visitado
		visitados.append(v)
		for i in grafo[v]:
			if visited[i] == False:          
				self.visitado_lista(i, visited,grafo,visitados)
		return visitados                       

	#Se for conexo, qual aresta que se retirada o torna desconexo? Existe apenas uma oumais arestas com essa peculiaridade?
	def P1(self,grafo,V):
		a = []
		parentes = g.DFS(V,grafo)
		tempo = 0 #Inicia o tempo com zero
		visitado = [False] * (len(grafo)) #lista com False/ lista com a mesma quantidade de vertices
		prox = [float("Inf")] * (len(grafo)) #lisca com tempo-Inf /lista com a mesma quantidade de vertices
		ant = [float("Inf")] * (len(grafo)) #lista com tempo-Inf / lista com a mesma quantidade de vertices
		for i in range(len(grafo[V])):# for ate o numero de vertices
			if visitado[i] == False:# se o vertice nao foi visitado chama a funcao de busca de ponte
				res =  self.ponte_busca(i,visitado,ant,prox,grafo,tempo,parentes,a)
		return res

	def ponte_busca(self,u,visitado,ant,prox,grafo,tempo,parentes,a,total_pontes = []):
		visitado[u] = True #vertice de inicio marcado como visitado
		prox[u] = tempo #vertice acima marcado com tempo 0
		ant[u] = tempo #vertice abaixo marcado com tempo 0
		tempo += 1 # imcremento no tempo
		for v in grafo[u]: # executa ate o vertice de busca
			if visitado[v] == False:
				parentes[v] = u
				parentes.append([])
				self.ponte_busca(v,visitado,ant,prox,grafo,tempo,parentes,a,total_pontes)  
				ant[u] = min(ant[u], ant[v])
				if ant[v] > prox[u]:	
					print 'P1 = Ponte(s):', u,v
					a.append('Inf')
					total_pontes.append(u)#Pra ser usado na P2 
					total_pontes.append(v)
			elif v != parentes[u]:
				ant[u] = min(ant[u], prox[v])
		return list(set(total_pontes))

	#Existe um unico vertice que, se retirado, causaria uma desconexao no grafo?
	def P2(self, grafo,total_pontes):
		#Os vertices cadidatos a gerarem desconexao no grafo, sao os vertices que possuem arestas de ponte
		vertices_removidos = []
		for chave in total_pontes:
			val = g.DFS(min(total_pontes),grafo,chave)
			if len(val) < len(grafo) - 1:
				vertices_removidos.append(chave)        
		return list(set(vertices_removidos))

	#Partindo de um vertice qualquer, quantos outros vertices podemos alcancar no grafo?
	def P3(self, vertice):
		return len(self.DFS(vertice, self.maTOla()))-1

	#diametro do grafo
	def P4(self,grafo):
		d = self.floyd_warshall(grafo)
		print "P4: ",d
	
	def matriz_floydwarshall(self,grafo):
		INF = 99999999
		matriz = [0]*len(grafo)
		for i in range(len(grafo)):      
			matriz[i] = [0]*len(grafo)
			
		for i,val in enumerate(grafo):
			for j, valor in enumerate(val):
				if grafo[i][j] == 0:
					grafo[i][j] = INF
                                    
		return grafo

            
	def floyd_warshall(self,grafo):
		caminho = self.matriz_floydwarshall(grafo)
		size = len(caminho)
		d = 0
		for k in range(size):
			for i in range(size):
				for j in range(size):
					menor = min(caminho[i][j],caminho[i][k] + caminho[k][j])
					if menor != caminho[i][j]:
						caminho[i][j] = menor
						if menor > d:
							d = menor
		return d

	#O grafo e desconexo, (fracamente) conexo, semi-fortemente conexo ou fortemente conexo?
	def P5(self):
		if self.verifica_fortemente_conexo(self.maTOla()) == True:
			print "P5: Fortemente conexo"
		elif self.desconexo() == True and self.d == "UNDIRECTED":
			print "P5: Desconexo"

	#Funcao recebe uma grafo como lista   
	def verifica_fortemente_conexo(self,grafo):
		caminho = []
		ma = self.DFS(0, grafo) #Faz a busca em profundidade e retorna uma lista 
		grafo_transp = self.grafo_transposto(self.ma) #calcula a matriz transposta do grafo/ MAS RETORNA O GRAFO COMO LISTA DE ADJ
		mb = self.DFS(0,grafo_transp) #faz a busca em profundidade no grafo como lista
		ma.sort() #Ordena a lista
		mb.sort()
		if ma != mb:
			return False
		else:
			return True

	def grafo_transposto(self,grafo):
		matriz = [0]*len(grafo)
		for i in range(len(grafo)):      
			matriz[i] = [0]*len(grafo)
		for i,val in enumerate(grafo):
			for j, valor in enumerate(val):
				matriz[i][j] = grafo[j][i]
                
		la={} #criando dicionario
		la1=[] #criando lista
		for pos_linha in range(len(matriz)):
			la1.append([]) # cria uma lista dentro da la1  
			for pos_coluna in range(len(matriz[0])):
				if matriz[pos_linha][pos_coluna] == 1: 
					la1[pos_linha].append(pos_coluna) # adiciona os vertices que fazem ligacao com 1 vertice
				else:
					la1[pos_linha]
			la[pos_linha] = la1[pos_linha] #adiciona as listas referente a cada vertice no dicionario
		return la

	def desconexo(self):
		for linha in self.ma:
			if linha.count(0) == self.qt_vertice: #se uma linha da matriz for 0, entao o grafo e desconexo
				conexao = True
				return conexao
			else:
				conexao = False
		return conexao

if __name__ == "__main__":

	g = grafo()
	g.lerArquivo()
	#print np.matrix(g.ma)
	#print g.maTOla()
	#print np.matrix(g.maTOmi())
	#la1 = g.maTOla()
	#la3 = g.P1(la1,0)
	#la2 = g.maTOla()
	#print "P2: ", g.P2(la2,la3)
	#print "P3: ", g.P3(0)
	#g.P4(g.ma)
	#g.P5()

	if sys.argv[2] == "-p1":
		if g.d[0] == "UNDIRECTED":
			la = g.maTOla()
			flag = g.P1(la, 0)
			if flag ==[]:
				print "P1: O grafo nao possui pontes"

	if sys.argv[3] == "-p2":
		if g.d[0] == "UNDIRECTED":
			la = g.maTOla()
			la1 = g.P1(la,0)
			la2 = g.maTOla()
			print 'P2: ',g.P2(la2,la1)

	if sys.argv[4] == "-p3" and sys.argv[5] != "-p4" or sys.argv[6] != "-p5":
		if sys.argv[5] != "-p4":
			print g.P3(int(sys.argv[5]))
		if sys.argv[6] != "-p5":
			print g.P3(int(sys.argv[6]))
	else:
		print "P3: ", g.P3(0)

	if sys.argv[5] == "-p4":
		g.P4(g.ma)

	if sys.argv[6] == "-p5":
		g.P5()

	if sys.argv[7] == "-p6":
		if g.d[0] == "DIRECTED":
			print "TODO"
