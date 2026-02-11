from copy import copy
from random import randint
from numpy import random

class Process(): # Klasa Process posłuży do efektywniejszego zarządzania

    def __init__(self, pid, burst_time, arrival_time):
        self.pid = pid
        self.burst_time = burst_time  # Czas wykonania
        self.arrival_time = arrival_time # Czas przyjścia
        self.time_left = burst_time # Pozostały czas do wykonania procesu
        self.waiting_time = None # Czas oczekiwania
        self.turnaround_time = None # Czas realizacji
    

    def setturnaround_time(self,current_time): # Metoda, która ustala, w jakim momencie proces się zakończył
        self.turnaround_time = current_time - self.arrival_time

    def setwaiting_time(self): # 
        self.waiting_time = self.turnaround_time - self.burst_time
        
    
    def __str__(self): # Reprezentacja klasy
        return f"PID: {self.pid}, BT: {self.burst_time}, AT: {self.arrival_time}"

#Algorytmy kolejkowania procesów

def sjf(processes):
    processes_copy = copy(processes) # Tworzymy kopie procesów, aby nie ingerować w oryginalną liste
    n = len(processes_copy) # Ilość procesów 
    average_waiting_time = 0 # Przechowanie średniego czasu oczekiwania
    average_turnaround_time = 0 # Przechowanie średniego czasu realizacji
    current_time = 0 # Czas od poczatku dzialania algorytmu
    schedulded_list = [] # Gotowa kolejka procesów
    queue = [] # Procesy, które już nadeszły

    while processes_copy or queue: # Wykonujemy algorytm do momentu kiedy nie będzie oczekiwał żaden proces
        while processes_copy and processes_copy[0].arrival_time <= current_time:
            queue.append(processes_copy[0])         # Dodajemy do kolejki procesy, które nadeszły
            processes_copy.pop(0)                   # Usuwamy te procesy z listy 
        
        queue.sort(key=lambda x: x.burst_time) # Sortujemy naszą kolejkę według czasu wykonania co ułatwmi nam wybór kolejnego procesu

        if queue: # Obsługujemy kolejkę 
            process = queue.pop(0) # Ściągamy nasz proces z kolejki
            schedulded_list.append((process.pid, current_time, current_time + process.burst_time)) # Dodajemy do szeregu 
            current_time += process.burst_time # Zwiększamy czas algorytmu o długość wykonania danego procesu
            process.setturnaround_time(current_time) # Ustawiamy jego czas realizacji
            process.setwaiting_time() # Ustawiamy czas oczekiwania 
            average_turnaround_time += process.turnaround_time 
            average_waiting_time += process.waiting_time 
        else:
            current_time = processes_copy[0].arrival_time  # Jeśli kolejka jest pusta, to przechodzimy do momentu nadejścia kolejnego procesu
    
    average_waiting_time /= n # Obliczamy średni czas oczekiwania dla wszystkich procesów
    average_turnaround_time /= n # Obliczamy średni czas realizacji dla wszysktkich procesów
    return schedulded_list, (average_turnaround_time,average_waiting_time) # Zwracamy wyniki


def round_robin(processes, quantum):
    processes_copy = copy(processes)
    n = len(processes_copy)
    average_waiting_time = 0
    average_turnaround_time = 0
    current_time = 0 
    queue = [] 
    schedulded_list = []

    while processes_copy or queue: 
        if queue:
            process = queue.pop(0)
            execute = min(process.time_left, quantum)  # Jako czas trwania wybieramy najmniejszą opcję
            schedulded_list.append((process.pid, current_time, current_time + execute )) # Dodajemy proces do szeregu
            current_time += execute # Zwiększamy czas o wykonanie procesu
            process.time_left -= execute # Ustalamy pozostały czas dla procesu

            while processes_copy and processes_copy[0].arrival_time <= current_time:  # Sprawdzamy czy w między czasie nie przyszły jakieś procesu
                queue.append(processes_copy.pop(0)) #Dodajemy do kolejki
            
            if process.time_left > 0:  # Jeśli procesowi pozostał czas to dodajemy go na  koniec kolejki
                queue.append(process)
            else: #Jeśli proces się wykonał
                process.setturnaround_time(current_time) #Ustawiamy czas realizacji
                process.setwaiting_time() #Ustawiamy czas oczekiwania
                average_turnaround_time += process.turnaround_time
                average_waiting_time += process.waiting_time
        else: #Obsługujemy resztę procesów, które jeszcze nie nadeszły
            next_process = processes_copy.pop(0) 
            current_time = next_process.arrival_time
            queue.append(next_process)

    average_waiting_time /= n # Obliczamy średni czas oczekiwania 
    average_turnaround_time /= n #Obliczamy średni czas realizacji
    return schedulded_list, (average_turnaround_time, average_waiting_time) # Zwracamy wyniki 


def generate_processes(num,arrival_range=(0,1),burst_range=(0,1),seed=None): # Generator procesów
    random.seed(seed)
    return sorted([Process(pid=i, arrival_time=random.randint(arrival_range[0], arrival_range[1]), burst_time=random.randint(burst_range[0], burst_range[1])) for i in range(num)],key=lambda x: x.arrival_time)






