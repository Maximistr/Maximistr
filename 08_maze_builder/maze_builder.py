"""
Maze Builder - Generátor a Vizualizér Bludišť
Aplikace pro automatické generování náhodných bludišť pomocí algoritmu
rekurzivního prohledávání a hledání cesty pomocí BFS.
"""

import random
import json
import time
from collections import deque
from pathlib import Path


class MazeBuilder:
    """
    Třída pro generování a správu bludišť.
    Používá algoritmus rekurzivního prohledávání (Recursive Backtracking)
    pro vytvoření náhodného bludiště.
    """

    def __init__(self, width, height):
        """
        Inicializace generátoru bludiště.
        
        Args:
            width (int): Šířka bludiště (počet buněk)
            height (int): Výška bludiště (počet buněk)
        """
        # Zajistíme, aby byly rozměry liché (požadavek algoritmu)
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
        
        # Vytvoříme matici - True znamená stěna, False znamená chodba
        self.maze = [[True for _ in range(self.width)] for _ in range(self.height)]
        
        # Počáteční a cílová pozice
        self.start = (1, 1)
        self.end = (self.height - 2, self.width - 2)

    def generate(self):
        """
        Generuje bludiště pomocí algoritmu rekurzivního prohledávání.
        Algoritmus náhodně procházíá bludiště a vytváří chodby.
        """
        # Počáteční buňka je chodba
        start_x, start_y = self.start
        self.maze[start_x][start_y] = False
        
        # Pomocné směry pro pohyb (nahoru, dolů, doleva, doprava)
        # Pohybujeme se po 2 buňkách, abychom zachovali stěny mezi chodbami
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        
        # Pomocná funkce pro rekurzivní prohledávání
        def carve_path(x, y):
            """Rekurzivně vytváří chodby v bludišti."""
            # Zamícháme směry pro náhodnost
            random.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                # Ověříme, zda je nová pozice v rámci bludiště
                # a zda je to dosud nenavštívená stěna
                if 0 < nx < self.height and 0 < ny < self.width:
                    if self.maze[nx][ny]:  # Pokud je to stěna
                        # Vytvoříme chodbu v nové pozici
                        self.maze[nx][ny] = False
                        
                        # Vytvoříme průjezd mezi starým a novým místem
                        wall_x = (x + nx) // 2
                        wall_y = (y + ny) // 2
                        self.maze[wall_x][wall_y] = False
                        
                        # Rekurzivně pokračujeme z nové pozice
                        carve_path(nx, ny)
        
        # Spustíme generování z počáteční pozice
        carve_path(start_x, start_y)

    def display(self):
        """
        Zobrazí bludiště v terminálu.
        # představuje stěnu, space představuje chodbu,
        S je start, E je cíl.
        """
        for i, row in enumerate(self.maze):
            for j, cell in enumerate(row):
                if (i, j) == self.start:
                    print("S", end=" ")
                elif (i, j) == self.end:
                    print("E", end=" ")
                elif cell:
                    print("█", end=" ")  # Stěna
                else:
                    print(" ", end=" ")  # Chodba
            print()

    def find_path(self):
        """
        Hledá cestu z počátku do cíle pomocí algoritmu BFS.
        Vrací seznam pozic tvořících cestu nebo None, pokud cesta neexistuje.
        
        Returns:
            list: Seznam (x, y) souřadnic cesty, nebo None
        """
        # BFS algoritmus - prohledávání do šířky
        queue = deque([(self.start, [self.start])])
        visited = {self.start}
        
        while queue:
            (x, y), path = queue.popleft()
            
            # Ověříme, zda jsme dosáhli cíle
            if (x, y) == self.end:
                return path
            
            # Zkontrolujeme všechny čtyři směry
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                
                # Ověříme hranice a zda jsme tam již byli
                if (0 <= nx < self.height and 
                    0 <= ny < self.width and 
                    not self.maze[nx][ny] and  # Chodba, ne stěna
                    (nx, ny) not in visited):
                    
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))
        
        return None  # Cesta neexistuje

    def display_with_solution(self, path):
        """
        Zobrazí bludiště s vyznačenou cestou.
        
        Args:
            path (list): Seznam pozic tvořících cestu
        """
        # Vytvoříme sadu pozic na cestě pro rychlejší vyhledávání
        path_set = set(path)
        
        for i, row in enumerate(self.maze):
            for j, cell in enumerate(row):
                if (i, j) == self.start:
                    print("S", end=" ")
                elif (i, j) == self.end:
                    print("E", end=" ")
                elif (i, j) in path_set and (i, j) != self.start:
                    print("·", end=" ")  # Bod na cestě
                elif cell:
                    print("█", end=" ")  # Stěna
                else:
                    print(" ", end=" ")  # Chodba
            print()

    def save_to_file(self, filename):
        """
        Uloží bludiště do JSON souboru.
        
        Args:
            filename (str): Jméno souboru pro uložení
        """
        data = {
            "width": self.width,
            "height": self.height,
            "start": self.start,
            "end": self.end,
            "maze": self.maze
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Bludiště uloženo do souboru: {filename}")

    @staticmethod
    def load_from_file(filename):
        """
        Načte bludiště z JSON souboru.
        
        Args:
            filename (str): Jméno souboru pro načtení
            
        Returns:
            MazeBuilder: Objekt bludiště s načtenými daty
        """
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        maze = MazeBuilder(data["width"], data["height"])
        maze.maze = data["maze"]
        maze.start = tuple(data["start"])
        maze.end = tuple(data["end"])
        print(f"Bludiště načteno ze souboru: {filename}")
        return maze


def main():
    """Hlavní funkce programu - interaktivní menu."""
    print("=" * 50)
    print("Vítejte v Maze Builder - Generátoru Bludišť")
    print("=" * 50)
    
    maze = None
    
    while True:
        print("\nVyberte akci:")
        print("1 - Generovat nové bludiště")
        print("2 - Zobrazit bludiště")
        print("3 - Najít cestu z bludiště")
        print("4 - Uložit bludiště")
        print("5 - Načíst bludiště")
        print("6 - Konec")
        
        choice = input("\nVaše volba (1-6): ").strip()
        
        if choice == "1":
            # Generování nového bludiště
            try:
                width = int(input("Zadejte šířku bludiště (doporučeno 11-51): "))
                height = int(input("Zadejte výšku bludiště (doporučeno 11-51): "))
                
                print("\nGeneruji bludiště...")
                start_time = time.time()
                
                maze = MazeBuilder(width, height)
                maze.generate()
                
                elapsed = time.time() - start_time
                print(f"Bludiště vygenerováno za {elapsed:.3f} sekund!")
                
            except ValueError:
                print("Chyba: Zadejte prosím čísla!")
        
        elif choice == "2":
            # Zobrazení bludiště
            if maze:
                print("\nBludiště (S = start, E = cíl):\n")
                maze.display()
            else:
                print("Nejdříve vygenerujte bludiště!")
        
        elif choice == "3":
            # Hledání cesty
            if maze:
                print("\nHledám cestu...")
                start_time = time.time()
                
                path = maze.find_path()
                
                elapsed = time.time() - start_time
                
                if path:
                    print(f"Cesta nalezena za {elapsed:.3f} sekund!")
                    print(f"Délka cesty: {len(path)} buněk\n")
                    maze.display_with_solution(path)
                else:
                    print("Cesta neexistuje!")
            else:
                print("Nejdříve vygenerujte bludiště!")
        
        elif choice == "4":
            # Uložení bludiště
            if maze:
                filename = input("Zadejte jméno souboru (bez přípony): ").strip()
                maze.save_to_file(f"{filename}.json")
            else:
                print("Nejdříve vygenerujte bludiště!")
        
        elif choice == "5":
            # Načtení bludiště
            filename = input("Zadejte jméno souboru (bez přípony): ").strip()
            try:
                maze = MazeBuilder.load_from_file(f"{filename}.json")
            except FileNotFoundError:
                print(f"Soubor '{filename}.json' nenalezen!")
        
        elif choice == "6":
            print("\nDěkuji za použití Maze Builder!")
            break
        
        else:
            print("Neplatná volba!")


if __name__ == "__main__":
    main()
