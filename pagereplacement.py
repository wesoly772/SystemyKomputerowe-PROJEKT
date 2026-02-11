from numpy import random

#Algorytmy zamieniania stron
def fifo(pages, size):
    ram = [] # Strony w pamięci
    faults = 0 # Ilość wymuszonej zamiany stron

    for page in pages:
        if page not in ram:
            faults += 1
            if len(ram) == size:  # Jeśli pamięć jest zapełniona
                ram.pop(0) # Usuwamy najstarszą stronę
            ram.append(page) # Dodajemy stronę do pamięci

    return faults

def lru(pages,size):
    ram = []
    faults = 0

    for page in pages:
        if page not in ram:
            faults += 1
            if len(ram) == size:
                ram.pop(0) # Usuwamy strone z początku - ta która była najmniej używana
            ram.append(page) # Dodajemy strone do pamięci
        else:
            ram.append(ram.pop(ram.index(page))) # Jeśli strona już istnieje w pamięci, to dodajemy ją na koniec kolejki - w ten sposób zachowujemy kolejność 
    return faults

def lfu(pages,size):
    ram = []
    frequency = dict() # Przechowujemy liczbe wystapien kazdej strony.
    faults = 0
    for page in pages:
        if page not in ram:
            faults +=1 
            if len(ram) == size:
                least=min(frequency,key=frequency.get) # wyszukujemy najmniejszą wartość w słowniku
                del frequency[least] # Usuwamy pierwsze wystąpienie tej wartości 
                ram.pop(ram.index(least)) # Usuwamy strone z pamięci
            ram.append(page)
            frequency[page] = 1 # Przypisujemy nowa strone 
        else:
            frequency[page] = frequency[page] + 1 # Jeśli strona została użyta to zwiększamy jej częstotliwość

    return faults

def generate_pages(num,p_range=(1,10),seed=None):
    random.seed(seed)
    return [random.randint(p_range[0],p_range[1]) for i in range(num) ]

