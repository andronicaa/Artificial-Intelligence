# Andronic Alexandra - Grupa 231

import copy


# functie care calculeaza functia euristica folosind distanta manhattan
def functia_euristica(initial_matrix, final_matrix):
	h = 0
	for i in range(len(initial_matrix)):
		for j in range(len(initial_matrix[0])):
			for ii in range(len(final_matrix)):
				for jj in range(len(final_matrix[0])):
					if initial_matrix[i][j] == final_matrix[ii][jj]:
						h += (abs(i - ii) + abs(j - jj))
	return h

def matrice_egala(initial_matrix, final_matrix):
	for i in range(len(initial_matrix)):
		for j in range(len(initial_matrix[0])):
			if initial_matrix[i][j] != final_matrix[i][j]:
				return False
	return True
# am putea sa mai definim o functie care sa ne ajuta la test_scop atunci cand verificam daca o matrice initial_matrix a ajuns de forma final_matrix

# definirea problemei

class Nod:
	def __init__(self, info, h):
		self.info = info
		self.h = h

	def __str__ (self):
		return "({}, h={})".format(self.info, self.h)

	def __repr__ (self):
		return f"({self.info}, h={self.h})"


class Arc:
	def __init__(self, capat, varf, cost):
		self.capat = capat
		self.varf = varf
		self.cost = cost

# definim matricea initiala si cea finala 
initial_matrix = [
	['1', '2', '3'],
	['0', '4', '6'],
	['7', '5', '8']
]
final_matrix = [
	['1', '2', '3'],
	['4', '5', '6'],
	['7', '8', '0']
]
class Problema:
	def __init__(self):
		# este de tip nod, ne trebuie nodul de start dar si functia euristica
		self.nod_start = Nod(initial_matrix,
			functia_euristica(initial_matrix, final_matrix)
		)  # de tip Nod
		self.nod_scop = final_matrix  # doar info (fara h)




	def cauta_nod_nume(self, info):
		"""Stiind doar informatia "info" a unui nod,
		trebuie sa returnati fie obiectul de tip Nod care are acea informatie,
		fie None, daca nu exista niciun nod cu acea informatie."""
		### TO DO ... DONE
		for nod in self.noduri:
			if nod.info == info:
				return nod
		return None





""" Clase folosite in algoritmul A* """

class NodParcurgere:
	"""O clasa care cuprinde informatiile asociate unui nod din listele open/closed
		Cuprinde o referinta catre nodul in sine (din graf)
		dar are ca proprietati si valorile specifice algoritmului A* (f si g).
		Se presupune ca h este proprietate a nodului din graf

	"""

	problema = None	# atribut al clasei


	def __init__(self, nod_graf, parinte = None, g = 0, f = None):
		self.nod_graf = nod_graf  	# obiect de tip Nod
		self.parinte = parinte  	# obiect de tip Nod
		self.g = g  	# costul drumului de la radacina pana la nodul curent
		if f is None :
			self.f = self.g + self.nod_graf.h
		else:
			self.f = f


	def drum_arbore(self):
		"""
			Functie care calculeaza drumul asociat unui nod din arborele de cautare.
			Functia merge din parinte in parinte pana ajunge la radacina
		"""
		nod_c = self
		# lista cu drumul (nod_c) -> nod curent
		drum = [nod_c]
		while nod_c.parinte is not None :
			drum = [nod_c.parinte] + drum
			nod_c = nod_c.parinte
		return drum


	def contine_in_drum(self, nod):
		"""
			Functie care verifica daca nodul "nod" se afla in drumul dintre radacina si nodul curent (self).
			Verificarea se face mergand din parinte in parinte pana la radacina
			Se compara doar informatiile nodurilor (proprietatea info)
			Returnati True sau False.

			"nod" este obiect de tip Nod (are atributul "nod.info")
			"self" este obiect de tip NodParcurgere (are "self.nod_graf.info")
		"""
		### TO DO ... DONE
		nod_c = self
		while nod_c.parinte is not None :
			# aici trebuie sa vad daca nu cumva imi verifica adresele si nu matricile in sine
			if matrice_egala(nod.info, nod_c.nod_graf.info):
				return True
			nod_c = nod_c.parinte
		return False


	#se modifica in functie de problema
	def expandeaza(self):
		"""Pentru nodul curent (self) parinte, trebuie sa gasiti toti succesorii (fiii)
		si sa returnati o lista de tupluri (nod_fiu, cost_muchie_tata_fiu),
		sau lista vida, daca nu exista niciunul.
		(Fiecare tuplu contine un obiect de tip Nod si un numar.)
		"""
		l_succesori = []
		# eu pot muta in casuta libera (cea care contine 0) minim 2, maxim 4 numere diferite
		# fac un vectori de mutari
		# trebuie sa gasesc pozitia locului liber din matrice
		for i in range(len(self.nod_graf.info)):
			for j in range(len(self.nod_graf.info[0])):
				if self.nod_graf.info[i][j] == '0':
					i_liber = i
					j_liber = j
					
		mutari = [[-1, 0], [0, 1], [1, 0], [0, -1]]
		for m in mutari:
			# generam o mutare vedem -> daca este valida
			new_i = i_liber + m[0]
			new_j = j_liber + m[1]
			if 0 <= new_i < len(self.nod_graf.info) and 0 <= new_j < len(self.nod_graf.info[0]):

				succesor = copy.deepcopy(self.nod_graf.info)
				succesor[i_liber][j_liber], succesor[new_i][new_j] = succesor[new_i][new_j], succesor[i_liber][j_liber]
				l_succesori.append((Nod(succesor, functia_euristica(succesor, self.problema.nod_scop)), 1))

		return l_succesori



	#se modifica in functie de problema
	def test_scop(self):
		return matrice_egala(self.nod_graf.info, self.problema.nod_scop)


	def __str__ (self):
		parinte = self.parinte if self.parinte is None else self.parinte.nod_graf.info
		return f"({self.nod_graf}, parinte={parinte}, f={self.f}, g={self.g}\n)"



""" Algoritmul A* """


def str_info_noduri(l):
	"""
		o functie folosita strict in afisari - poate fi modificata in functie de problema
	"""
	sir = "["
	for x in l:
		sir += str(x) + "  "
	sir += "]"
	return sir


def afis_succesori_cost(l):
	"""
		o functie folosita strict in afisari - poate fi modificata in functie de problema
	"""
	sir = ""
	for (x, cost) in l:
		sir += "\nnod: "+str(x)+", cost arc:"+ str(cost)
	return sir


def in_lista(l, nod):
	"""
		lista "l" contine obiecte de tip NodParcurgere
		"nod" este de tip Nod
	"""
	for i in range(len(l)):
		if l[i].nod_graf.info == nod.info:
			return l[i]
	return None


def a_star():
	"""
		Functia care implementeaza algoritmul A-star
	"""
	### TO DO ... DONE
	
	rad_arbore = NodParcurgere(NodParcurgere.problema.nod_start)
	# mai intai se va pune in lista open nodul de start iar lista closed va fi vida
	open = [rad_arbore]  # open va contine elemente de tip NodParcurgere
	closed = []  # closed va contine elemente de tip NodParcurgere
	# cat timp lista open va fi nevida si nu s-a ajung inca la nodul scop
	while len(open) > 0 :

		
		print("Open=" + str_info_noduri(open))	# afisam lista open
		print("Closed= " + str_info_noduri(closed)) # afisam lista closed
		nod_curent = open.pop(0)	# scoatem primul element din lista open
		closed.append(nod_curent)	# si il adaugam la finalul listei closed

		#testez daca nodul extras din lista open este nod scop (si daca da, ies din bucla while)
		if nod_curent.test_scop():
			break
		
		l_succesori = nod_curent.expandeaza()
		for (nod_succesor, cost_succesor) in l_succesori:
			# "nod_curent" este tatal, "nod_succesor" este fiul curent

			# daca fiul nu e in drumul dintre radacina si tatal sau (adica nu se creeaza un circuit)
			if (not nod_curent.contine_in_drum(nod_succesor)):

				# calculez valorile g si f pentru "nod_succesor" (fiul)
				g_succesor = nod_curent.g + cost_succesor # g-ul tatalui + cost muchie(tata, fiu)
				f_succesor = g_succesor + nod_succesor.h # g-ul fiului + h-ul fiului

				#verific daca "nod_succesor" se afla in closed
				# (si il si sterg, returnand nodul sters in nod_parcg_vechi
				nod_parcg_vechi = in_lista(closed, nod_succesor)

				if nod_parcg_vechi is not None:	# "nod_succesor" e in closed
					# daca f-ul calculat pentru drumul actual este mai bun (mai mic) decat
					# 	   f-ul pentru drumul gasit anterior (f-ul nodului aflat in lista closed)
					# atunci actualizez parintele, g si f
					# si apoi voi adauga "nod_nou" in lista open
					
					if (f_succesor < nod_parcg_vechi.f):
						closed.remove(nod_parcg_vechi)	# scot nodul din lista closed
						nod_parcg_vechi.parinte = nod_curent # actualizez parintele
						nod_parcg_vechi.g = g_succesor	# actualizez g
						nod_parcg_vechi.f = f_succesor	# actualizez f
						nod_nou = nod_parcg_vechi	# setez "nod_nou", care va fi adaugat apoi in open

				else :
					# daca nu e in closed, verific daca "nod_succesor" se afla in open
					nod_parcg_vechi = in_lista(open, nod_succesor)

					if nod_parcg_vechi is not None:	# "nod_succesor" e in open
						# daca f-ul calculat pentru drumul actual este mai bun (mai mic) decat
						# 	   f-ul pentru drumul gasit anterior (f-ul nodului aflat in lista open)
						# atunci scot nodul din lista open
						# 		(pentru ca modificarea valorilor f si g imi va strica sortarea listei open)
						# actualizez parintele, g si f
						# si apoi voi adauga "nod_nou" in lista open (la noua pozitie corecta in sortare)
						if (f_succesor < nod_parcg_vechi.f):
							open.remove(nod_parcg_vechi)
							nod_parcg_vechi.parinte = nod_curent
							nod_parcg_vechi.g = g_succesor
							nod_parcg_vechi.f = f_succesor
							nod_nou = nod_parcg_vechi

					else: # cand "nod_succesor" nu e nici in closed, nici in open
						nod_nou = NodParcurgere(nod_graf=nod_succesor, parinte=nod_curent, g=g_succesor)
						# se calculeaza f automat in constructor

				if nod_nou:
					# inserare in lista sortata crescator dupa f
					# (si pentru f-uri egale descrescator dupa g)
					i=0
					while i < len(open):
						if open[i].f < nod_nou.f:
							i += 1
						else:
							while i < len(open) and open[i].f == nod_nou.f and open[i].g > nod_nou.g:
								i += 1
							break

					open.insert(i, nod_nou)


	print("\n------------------ Concluzie -----------------------")
	if len(open) == 0:
		print("Lista open e vida, nu avem drum de la nodul start la nodul scop")
	else:
		print("Drum de cost minim: " +"\n" +  str_info_noduri(nod_curent.drum_arbore()))





if __name__ == "__main__":
	problema = Problema()
	NodParcurgere.problema = problema
	a_star()
	