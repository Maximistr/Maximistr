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
import tkinter as tk
from tkinter import messagebox, filedialog


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


class MazeGUI:
    """
    Grafické uživatelské rozhraní pro Maze Builder.
    Zobrazuje bludiště v okně a umožňuje interakci přes tlačítka.
    """
    
    def __init__(self, root):
        """Inicializace GUI okna."""
        self.root = root
        self.root.title("Maze Builder - Generátor Bludišť")
        self.root.geometry("900x750")
        self.root.resizable(False, False)
        
        self.maze = None
        self.path = None
        self.cell_size = 10
        self.player_pos = None
        self.game_won = False
        
        # Keyboard controls
        self.root.bind("<Up>", lambda e: self.move_player(-1, 0))
        self.root.bind("<Down>", lambda e: self.move_player(1, 0))
        self.root.bind("<Left>", lambda e: self.move_player(0, -1))
        self.root.bind("<Right>", lambda e: self.move_player(0, 1))
        self.root.bind("<w>", lambda e: self.move_player(-1, 0))
        self.root.bind("<a>", lambda e: self.move_player(0, -1))
        self.root.bind("<s>", lambda e: self.move_player(1, 0))
        self.root.bind("<d>", lambda e: self.move_player(0, 1))
        self.root.bind("<r>", lambda e: self.reset_game())
        
        # Panel s tlačítky
        self.button_frame = tk.Frame(root, bg="#f0f0f0", height=60)
        self.button_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Tlačítka
        tk.Button(self.button_frame, text="Generovat", command=self.generate_maze, 
                  bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Najít cestu", command=self.find_path_btn, 
                  bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Vyčistit", command=self.clear_path, 
                  bg="#FF9800", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Resetovat hru", command=self.reset_game, 
                  bg="#FF5722", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Uložit", command=self.save_maze, 
                  bg="#9C27B0", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Načíst", command=self.load_maze, 
                  bg="#673AB7", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Canvas pro kreslení bludiště
        self.canvas = tk.Canvas(root, bg="white", highlightthickness=1, highlightbackground="black")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panel se statistikami
        self.status_frame = tk.Frame(root, bg="#f0f0f0", height=40)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        self.status_label = tk.Label(self.status_frame, 
                                     text="Ovládání: WASD/Šipky = Pohyb | R = Reset | Připraveno. Klikněte na 'Generovat'.", 
                                     bg="#f0f0f0", font=("Arial", 9))
        self.status_label.pack(side=tk.LEFT, padx=5)
    
    def generate_maze(self):
        """Generuje nové bludiště."""
        try:
            dialog = tk.Toplevel(self.root)
            dialog.title("Parametry bludiště")
            dialog.geometry("300x150")
            dialog.transient(self.root)
            dialog.grab_set()
            
            tk.Label(dialog, text="Šířka (doporučeno 11-51):").pack(pady=5)
            width_entry = tk.Entry(dialog, width=10)
            width_entry.insert(0, "21")
            width_entry.pack()
            
            tk.Label(dialog, text="Výška (doporučeno 11-51):").pack(pady=5)
            height_entry = tk.Entry(dialog, width=10)
            height_entry.insert(0, "21")
            height_entry.pack()
            
            def create():
                try:
                    width = int(width_entry.get())
                    height = int(height_entry.get())
                    
                    self.status_label.config(text="Generuji bludiště...")
                    self.root.update()
                    
                    start_time = time.time()
                    self.maze = MazeBuilder(width, height)
                    self.maze.generate()
                    elapsed = time.time() - start_time
                    
                    self.player_pos = self.maze.start
                    self.path = None
                    self.game_won = False
                    self.draw_maze()
                    self.status_label.config(text=f"Bludiště vygenerováno za {elapsed:.3f} sekund! Velikost: {width}x{height} | Pohybuj se pomocí WASD/Šipek na konec (červené políčko)")
                    dialog.destroy()
                except ValueError:
                    messagebox.showerror("Chyba", "Zadejte prosím platná čísla!")
            
            tk.Button(dialog, text="Vytvořit", command=create, bg="#4CAF50", fg="white").pack(pady=10)
        
        except Exception as e:
            messagebox.showerror("Chyba", f"Chyba při generování: {str(e)}")
    
    def draw_maze(self):
        """Kreslí bludiště na canvas."""
        if not self.maze:
            return
        
        self.canvas.delete("all")
        
        for i, row in enumerate(self.maze.maze):
            for j, cell in enumerate(row):
                x0 = j * self.cell_size
                y0 = i * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                
                # Určení barvy
                if (i, j) == self.player_pos:
                    color = "#00BCD4"  # Cyan - hráč
                elif (i, j) == self.maze.start:
                    color = "#4CAF50"  # Zelená
                elif (i, j) == self.maze.end:
                    color = "#F44336"  # Červená
                elif self.path and (i, j) in set(self.path) and (i, j) != self.maze.start:
                    color = "#FFC107"  # Žlutá
                elif cell:  # Stěna
                    color = "#333333"  # Tmavě šedá
                else:  # Chodba
                    color = "white"
                
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=color)
    
    def find_path_btn(self):
        """Hledá cestu v bludišti."""
        if not self.maze:
            messagebox.showwarning("Upozornění", "Nejdříve vygenerujte bludiště!")
            return
        
        self.status_label.config(text="Hledám cestu...")
        self.root.update()
        
        start_time = time.time()
        self.path = self.maze.find_path()
        elapsed = time.time() - start_time
        
        if self.path:
            self.draw_maze()
            self.status_label.config(text=f"Cesta nalezena za {elapsed:.3f} sekund! Délka: {len(self.path)} buněk")
        else:
            messagebox.showinfo("Výsledek", "Cesta neexistuje!")
            self.status_label.config(text="Cesta neexistuje!")
    
    def move_player(self, dx, dy):
        """Pohybuje hráčem v bludišti s detekcí kolizí."""
        if not self.maze or not self.player_pos:
            return
        
        if self.game_won:
            messagebox.showinfo("Gratuluji!", "Už jste vyhrál! Vygenerujte nové bludiště.")
            return
        
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        
        # Ověříme hranice
        if 0 <= new_x < self.maze.height and 0 <= new_y < self.maze.width:
            # Ověříme kolizi se stěnou
            if not self.maze.maze[new_x][new_y]:  # False = chodba, můžeme se pohybovat
                self.player_pos = (new_x, new_y)
                
                # Ověříme, zda jsme dosáhli cíle
                if self.player_pos == self.maze.end:
                    self.game_won = True
                    self.draw_maze()
                    messagebox.showinfo("VYHRÁL JSI!", "Gratulujeme! Dosáhli jste cíle!")
                    self.status_label.config(text="🎉 GRATULUJI! Dosáhli jste cíle! Stiskněte R pro novou hru nebo 'Generovat' pro nové bludiště.")
                    return
                
                self.draw_maze()
                self.status_label.config(text=f"Pozice: {self.player_pos} | Cíl: {self.maze.end}")
            else:
                # Do zdi!
                self.status_label.config(text="BUMP! Narazili jste do zdi!")
    
    def reset_game(self):
        """Resetuje pozici hráče na start."""
        if self.maze:
            self.player_pos = self.maze.start
            self.game_won = False
            self.draw_maze()
            self.status_label.config(text=f"Hra resetována. Pozice: {self.player_pos} | Cíl: {self.maze.end}")
    
    def clear_path(self):
        """Vyčistí zobrazení cesty."""
        self.path = None
        self.draw_maze()
        self.status_label.config(text="Cesta vyčištěna.")
    
    def save_maze(self):
        """Uloží bludiště do souboru."""
        if not self.maze:
            messagebox.showwarning("Upozornění", "Nejdříve vygenerujte bludiště!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir=".",
            initialfile="maze.json"
        )
        
        if filename:
            try:
                self.maze.save_to_file(filename)
                self.status_label.config(text=f"Bludiště uloženo: {filename}")
                messagebox.showinfo("Úspěch", "Bludiště uloženo!")
            except Exception as e:
                messagebox.showerror("Chyba", f"Chyba při ukládání: {str(e)}")
    
    def load_maze(self):
        """Načte bludiště ze souboru."""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir="."
        )
        
        if filename:
            try:
                self.maze = MazeBuilder.load_from_file(filename)
                self.player_pos = self.maze.start
                self.path = None
                self.game_won = False
                self.draw_maze()
                self.status_label.config(text=f"Bludiště načteno: {filename}")
            except Exception as e:
                messagebox.showerror("Chyba", f"Chyba při načítání: {str(e)}")


def main():
    """Hlavní funkce programu - spuští grafické rozhraní."""
    root = tk.Tk()
    gui = MazeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
