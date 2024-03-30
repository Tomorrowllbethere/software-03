'''
Софт для сортування файлів за їхніми розширеннями
'''
from pathlib import Path
import logging, shutil
from time import time
from threading import Thread

timer = time()



class Path_work():
    def __init__(self, dest_1):
        self.directory_1 = Path(f"./{dest_1}")# Створення об'єкту Path для директорії
        self.folders = []
    
    def get_folders(self): # Виведення переліку всіх файлів та піддиректорій в список
        for item in self.directory_1.iterdir():
            if item.is_file():
                self.folders.append(item) 
            elif item.is_dir():
                 self.get_folders_recursive(self.directory_1)
        logging.info('I\'m trying to unpack your folders')
                
    def get_folders_recursive(self, directory): #   рекурсивна історія для розпаковки subfolders
        for item in directory.iterdir():
            if item.is_file():
                self.folders.append(item) 
            elif item.is_dir():
                self.get_folders_recursive(item)    

class Move_to(): #отримання нового шляху
    def __init__(self) -> None:
        pass

    def get_new_folder(self, dest_2): #виклик функції для отримання шляху чи його створення
        direct = Path(dest_2)
        if  direct.is_dir() and direct.exists():  
            self.directory_2 = direct
        else:
            directory = Path(f'./{dest_2}')
            directory.mkdir(parents=True, exist_ok=True)
            self.directory_2 = directory
        

        
class Worker(Path_work, Move_to): # клас для роботи з шляхами і списком файлів. 
    def sorted(self):
        for el in self.folders:
            if el.is_file():
                d = el.suffix
                final_folder = d[1:]
                destination = Path(f"{self.directory_2}/{final_folder}")
                if not destination.exists():
                    destination.mkdir(parents=True, exist_ok=True)
                # shutil.move(el, destination)
                shutil.copy2(el, destination)
                logging.info(f"From {el} to {destination} moved")
    def __call__(self, *args, **kwds):
        return super().__call__(*args, **kwds)
   


if __name__ == '__main__':

    folder_from = "dist"
    folder_to = "desk_new"

    # folder_to = "dist"
    # folder_from = "desk_new"

    worker = Worker(folder_from)
    worker.get_new_folder(folder_to)
    logging.basicConfig(level=logging.INFO, format='%(threadName)s %(message)s')
    thread = Thread(target = worker.get_folders())
    thread_2 = Thread(target = worker.sorted())
    logging.info('Moving') 
    thread.start()
    thread_2.start()
    
    logging.info(f'___It takes about {time()-timer}')