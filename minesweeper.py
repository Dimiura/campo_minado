import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import json
import os
from PIL import Image, ImageTk

class MinesweeperGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Campo Minado")
        self.root.configure(bg='#E6F3FF')
        
        # Configurações das dificuldades
        self.difficulties = {
            'Fácil': {'size': 8, 'mines': 10},
            'Médio': {'size': 12, 'mines': 30},
            'Difícil': {'size': 16, 'mines': 60}
        }
        
        self.high_scores = self.load_scores()
        self.create_main_menu()
        
    def load_scores(self):
        if os.path.exists('scores.json'):
            with open('scores.json', 'r') as f:
                return json.load(f)
        return {'Fácil': float('inf'), 'Médio': float('inf'), 'Difícil': float('inf')}
    
    def save_scores(self):
        with open('scores.json', 'w') as f:
            json.dump(self.high_scores, f)
    
    def create_main_menu(self):
        # Título
        title = tk.Label(self.root, text="Campo Minado", font=('Arial', 24, 'bold'),
                        bg='#E6F3FF', fg='#003366')
        title.pack(pady=20)
        
        # Frame para os botões
        button_frame = tk.Frame(self.root, bg='#E6F3FF')
        button_frame.pack(pady=10)
        
        # Mostrar recordes
        scores_frame = tk.Frame(self.root, bg='#E6F3FF')
        scores_frame.pack(pady=20)
        
        tk.Label(scores_frame, text="Recordes:", font=('Arial', 16, 'bold'),
                bg='#E6F3FF', fg='#003366').pack()
        
        for diff in self.difficulties:
            score = self.high_scores[diff]
            score_text = f"{diff}: {'Sem recorde' if score == float('inf') else f'{score:.1f}s'}"
            tk.Label(scores_frame, text=score_text, font=('Arial', 12),
                    bg='#E6F3FF', fg='#003366').pack()
        
        # Botões de dificuldade
        for diff in self.difficulties:
            btn = tk.Button(button_frame, text=diff,
                          command=lambda d=diff: self.start_game(d),
                          font=('Arial', 12),
                          width=15,
                          bg='#003366',
                          fg='white',
                          activebackground='#004C99')
            btn.pack(pady=5)
    
    def start_game(self, difficulty):
        game_window = tk.Toplevel(self.root)
        game_window.title(f"Campo Minado - {difficulty}")
        game_window.configure(bg='#E6F3FF')
        
        size = self.difficulties[difficulty]['size']
        mines = self.difficulties[difficulty]['mines']
        
        self.current_game = GameBoard(game_window, size, mines, difficulty, self)
        
class GameBoard:
    def __init__(self, window, size, mines, difficulty, main_game):
        self.window = window
        self.size = size
        self.mines = mines
        self.difficulty = difficulty
        self.main_game = main_game
        self.buttons = []
        self.board = []
        self.game_started = False
        self.start_time = None
        
        self.create_board()
        self.create_timer()
    
    def create_timer(self):
        self.timer_label = tk.Label(self.window, text="Tempo: 0.0s",
                                  font=('Arial', 12), bg='#E6F3FF', fg='#003366')
        self.timer_label.grid(row=self.size + 1, column=0, columnspan=self.size, pady=10)
        self.update_timer()
    
    def update_timer(self):
        if self.game_started and not hasattr(self, 'game_over'):
            elapsed = time.time() - self.start_time
            self.timer_label.config(text=f"Tempo: {elapsed:.1f}s")
            self.window.after(100, self.update_timer)
    
    def create_board(self):
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.buttons = []
        
        # Criar grade de botões
        for i in range(self.size):
            row = []
            for j in range(self.size):
                btn = tk.Button(self.window, width=2, height=1,
                              command=lambda r=i, c=j: self.click(r, c),
                              bg='#FFFFFF')
                btn.grid(row=i, column=j)
                btn.bind('<Button-3>', lambda e, r=i, c=j: self.right_click(r, c))
                row.append(btn)
            self.buttons.append(row)
    
    def place_mines(self, first_row, first_col):
        positions = [(r, c) for r in range(self.size) for c in range(self.size)
                    if (r, c) != (first_row, first_col)]
        mine_positions = random.sample(positions, self.mines)
        
        for row, col in mine_positions:
            self.board[row][col] = 'X'
            
        # Calcular números
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] != 'X':
                    mines = sum(1 for r in range(max(0, row-1), min(self.size, row+2))
                              for c in range(max(0, col-1), min(self.size, col+2))
                              if self.board[r][c] == 'X')
                    self.board[row][col] = mines
    
    def click(self, row, col):
        if not self.game_started:
            self.game_started = True
            self.start_time = time.time()
            self.place_mines(row, col)
        
        if self.board[row][col] == 'X':
            self.game_over()
            return
        
        self.reveal(row, col)
        if self.check_win():
            self.win_game()
    
    def reveal(self, row, col):
        if not (0 <= row < self.size and 0 <= col < self.size):
            return
        
        btn = self.buttons[row][col]
        if btn['state'] == 'disabled':
            return
        
        btn['state'] = 'disabled'
        value = self.board[row][col]
        
        if value == 0:
            btn['bg'] = '#E6F3FF'
            for r in range(max(0, row-1), min(self.size, row+2)):
                for c in range(max(0, col-1), min(self.size, col+2)):
                    self.reveal(r, c)
        else:
            btn['bg'] = '#E6F3FF'
            btn['text'] = value
            colors = {1: 'blue', 2: 'green', 3: 'red', 4: 'purple',
                     5: 'maroon', 6: 'turquoise', 7: 'black', 8: 'gray'}
            btn['fg'] = colors.get(value, 'black')
    
    def right_click(self, row, col):
        btn = self.buttons[row][col]
        if btn['state'] != 'disabled':
            if btn['text'] == '🚩':
                btn['text'] = ''
            else:
                btn['text'] = '🚩'
    
    def check_win(self):
        for i in range(self.size):
            for j in range(self.size):
                btn = self.buttons[i][j]
                if self.board[i][j] != 'X' and btn['state'] != 'disabled':
                    return False
        return True
    
    def win_game(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time < self.main_game.high_scores[self.difficulty]:
            self.main_game.high_scores[self.difficulty] = elapsed_time
            self.main_game.save_scores()
        
        messagebox.showinfo("Parabéns!", 
                          f"Você venceu!\nTempo: {elapsed_time:.1f} segundos")
        self.window.destroy()
    
    def game_over(self):
        self.game_over = True
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 'X':
                    self.buttons[i][j]['text'] = '💣'
                    self.buttons[i][j]['bg'] = 'red'
        
        messagebox.showinfo("Game Over", "Você perdeu!")
        self.window.destroy()

if __name__ == "__main__":
    game = MinesweeperGame()
    game.root.mainloop()