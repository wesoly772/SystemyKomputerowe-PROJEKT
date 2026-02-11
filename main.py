from cpuschedule import round_robin,sjf,generate_processes
from pagereplacement import fifo,lfu,lru,generate_pages
from functools import partial
from graphs import  makegraph_cpu, makegraph_page
import os
import shutil
from numpy import random

def simulation_cpu_schedulding(algorithms,processes): # Przeprowadzamy symulacje dla każdego algorytmu planowania procesora
    average_times = {} # Przechowanie wyników do analizy dla każdego z algorytmów
    for name, alg in algorithms.items():  
        schedulded_list, times = alg(processes)  # Uruchomienie symulacji
        average_times[name] = times # Pobieramy czasy realizacji i oczekiwania procesów
        with open(f"{name}.txt",'w') as file: # Zapisujemy do pliku wyniki działania algorytmów
            file.write("PID;START;END\n")
            for process in schedulded_list:
                out=f"{process[0]};{process[1]};{process[2]}\n"  # Dla każdego procesu w kolejce wypisujemy jego PID, czas rozpoczecia i zakończenia/odebrania czasu procesora
                file.write(out)
    return average_times


def run_cpu_tests(settings_cpu, t,seed):  #Funkcja obsługująca dany test dla algorytmów planowania


    cpu_algorithms = {
        "Shortest Job First": sjf,
        "Round Robin": partial(round_robin,quantum=settings_cpu["Quantum"][t])
    }

    processes = generate_processes(     # Generowanie procesów uzależnionych od ustawień dla konkretnego testu
        settings_cpu["Number Of Processes"][t],
        settings_cpu["Arrival Range"][t],
        settings_cpu["Burst Range"][t],
        seed
        )

    results_cpu = simulation_cpu_schedulding(cpu_algorithms,processes) # Zwrot wyników symulacji do dalszej analizy 

    return results_cpu


def simulation_pages_replacement(algorithms, pages,size_of_buffor): # Przeprowadzamy symulacje dla każdego algorytmu zamieniania stron

    faults = {} # Przechowanie wyników do analizy dla każdego z algorytmów
    for name, alg in algorithms.items():
        results = alg(pages,size_of_buffor) #Uruchomienie symulacji
        faults[name] = results
        with open(f"{name}.txt", "w") as file: # Zapisanie wyników do plików
            file.write(f"{name} algorithm results: {results} faults")
    return faults




def run_page_replacement_test(settings_page,page_algorithms,t,seed): # Funkcja obsługująca dany test dla algorytmów zastępowania strn

    pages = generate_pages(                     # Generowanie stron uzależnionych od ustawień dla konkretnego testu
        settings_page["Number of pages"][t],
        settings_page["Page range"][t],
        seed
        )

    results_page = simulation_pages_replacement(page_algorithms,pages,settings_page["Buffor size"][t]) # Zwrot wyników do dalszej analizys

    return results_page



def main():

    #Ustawienia randomizacji procesów oraz stron
    seed = 124

    #Ustawienia symulacji kolejkowania procesów
    settings_cpu = {  
        "Number Of Processes": [25,75,125],
        "Arrival Range": [(0,100) for i in range(3)],           # Ustawienia generowania procesów
        "Burst Range": [(5,6) for i in range(3)],
        "Quantum": [3 for i in range(3)]
    } 
    test_number = 3  # Liczba testów
    test_dir="CPUTests" # Folder do zapisu wyników poszczególnych testów
    

    #Tworzymy główny folder
    os.makedirs(test_dir,exist_ok=True)  
    os.chdir(test_dir)

    #Zapisanie skumulowanych wyników
    with open("Merged.txt","w") as file:
        file.write("LiczbaProcesow;Algorytm;ATT;AWT\n")

    for t in range(test_number):
        if os.path.exists(f"test{t}"):     # Dla każdego testu tworzymy osobny folder
            shutil.rmtree(f"test{t}")
        os.makedirs(f"test{t}", )
        os.chdir(f"test{t}")

        results_cpu = run_cpu_tests(settings_cpu,t,seed)  # Zwrot wyników testu
        makegraph_cpu(results_cpu,t) # Stworzenie wykresu dla pary algorytmów
        os.chdir("..")

        with open("Merged.txt", "a") as file: #Tworzymy zbiorczy plik ze wszystkimi wynikami
            for key, value in results_cpu.items():
                file.write(f"{settings_cpu["Number Of Processes"][t]};{key};{value[0]};{value[1]}\n".replace(".",","))
            
    

    #Symulacja kolejkowania stron
    settings_page = {
        "Number of pages": [100 for _ in range(4)],       # Ustawienia generowania stron
        "Page range": [(1,10),(1,50),(1,100),(1,200)],
        "Buffor size": [4 for i in range(4)]
    }
    page_algorithms = {
        "First In First Out": fifo,
        "Least Frequently Used": lfu,
        "Least Recently Used": lru
    }
    test_number = 4
    test_dir = "PageTests" 
    os.chdir("../")
    os.makedirs(test_dir,exist_ok=True)
    os.chdir(test_dir)

    

    with open("Merged.txt", "w") as file:
        file.write("LiczbaStron;Algorytm;PageFaults\n")

    for t in range(test_number):
        if os.path.exists(f"test{t}"):
            shutil.rmtree(f"test{t}")
        os.makedirs(f"test{t}", )
        os.chdir(f"test{t}")

        results_page = run_page_replacement_test(settings_page,page_algorithms,t,seed) # Zwrot wyników testu
        makegraph_page(results_page,t) # Utworzenie wykresu dla algorytmów

        os.chdir("..")
        
        with open("Merged.txt", "a") as file: #Tworzymy zbiorczy plik ze wszystkimi wynikami
            for key, value in results_page.items():
                file.write(f"{settings_page['Number of pages'][t]};{key};{value}\n")

        


if __name__ == "__main__":
    main()

