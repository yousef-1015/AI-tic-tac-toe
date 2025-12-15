import customtkinter as ctk
from board import Board, WIN_LINES
from alphabeta import alphabeta
from heuristic import classical_eval
from trainer import train
import random
import os
import time
import pygame
import sys

# Suppress Tkinter after-event errors on window close
class SuppressTkErrors:
    def __init__(self, stream):
        self.stream = stream
    def write(self, msg):
        if "invalid command name" not in msg:
            self.stream.write(msg)
    def flush(self):
        self.stream.flush()

sys.stderr = SuppressTkErrors(sys.stderr)

# Initialize pygame mixer for sounds
pygame.mixer.init()

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------- Theme Definitions ----------
THEMES = {
    "Dark": {
        "bg": "#0d1117",
        "panel": "#161b22",
        "board": "#21262d",
        "cell": "#30363d",
        "cell_hover": "#3d444d",
        "text": "#ffffff",
        "text_dim": "#8b949e",
        "x_color": "#58a6ff",
        "o_color": "#f78166",
        "win": "#7ee787",
        "lose": "#f85149",
        "draw": "#8b949e",
        "accent": "#238636",
        "accent_hover": "#2ea043",
        "win_highlight": "#3fb950",
    },
    "Light": {
        "bg": "#ffffff",
        "panel": "#f6f8fa",
        "board": "#e1e4e8",
        "cell": "#ffffff",
        "cell_hover": "#f3f4f6",
        "text": "#24292f",
        "text_dim": "#57606a",
        "x_color": "#0969da",
        "o_color": "#cf222e",
        "win": "#1a7f37",
        "lose": "#cf222e",
        "draw": "#57606a",
        "accent": "#2da44e",
        "accent_hover": "#3fb950",
        "win_highlight": "#2da44e",
    },
    "Purple": {
        "bg": "#1a1625",
        "panel": "#2d2640",
        "board": "#3d3555",
        "cell": "#4a4165",
        "cell_hover": "#5a5175",
        "text": "#ffffff",
        "text_dim": "#a89ec4",
        "x_color": "#c084fc",
        "o_color": "#fb7185",
        "win": "#86efac",
        "lose": "#fca5a5",
        "draw": "#a89ec4",
        "accent": "#8b5cf6",
        "accent_hover": "#a78bfa",
        "win_highlight": "#c084fc",
    },
    "Ocean": {
        "bg": "#0c1929",
        "panel": "#132f4c",
        "board": "#1e3a5f",
        "cell": "#2d4a6f",
        "cell_hover": "#3d5a7f",
        "text": "#ffffff",
        "text_dim": "#7eb8da",
        "x_color": "#5bc0eb",
        "o_color": "#fde74c",
        "win": "#9bc53d",
        "lose": "#e55934",
        "draw": "#7eb8da",
        "accent": "#00b4d8",
        "accent_hover": "#48cae4",
        "win_highlight": "#5bc0eb",
    },
}

# ---------- Splash Screen with Loading Bar ----------
def show_splash():
    ctk.set_appearance_mode("dark")
    
    splash = ctk.CTk()
    splash.title("Loading...")
    splash.geometry("400x200")
    splash.resizable(False, False)
    splash.configure(fg_color="#0d1117")
    
    # Center the window
    splash.update_idletasks()
    x = (splash.winfo_screenwidth() - 400) // 2
    y = (splash.winfo_screenheight() - 200) // 2
    splash.geometry(f"400x200+{x}+{y}")
    
    # Keep on top
    splash.attributes("-topmost", True)
    splash.lift()
    splash.focus_force()
    
    # Title
    title = ctk.CTkLabel(splash, text="🎮 Tic-Tac-Toe AI", 
                         font=("Arial", 24, "bold"), text_color="#ffffff")
    title.pack(pady=(40, 10))
    
    # Status label
    status = ctk.CTkLabel(splash, text="Initializing...", 
                          font=("Arial", 12), text_color="#8b949e")
    status.pack(pady=(5, 15))
    
    # Progress bar
    progress = ctk.CTkProgressBar(splash, width=300, height=15, 
                                   corner_radius=8, fg_color="#21262d",
                                   progress_color="#238636")
    progress.pack(pady=10)
    progress.set(0)
    
    model = None
    
    # Step 1: Initialize (0-30%)
    status.configure(text="Loading components...")
    for i in range(30):
        progress.set(i / 100)
        splash.update()
        time.sleep(0.01)
    
    # Step 2: Train model (30-80%)
    status.configure(text="Training ML model...")
    splash.update()
    
    try:
        dataset_path = os.path.join(SCRIPT_DIR, "tictactoe_dataset.csv")
        if os.path.exists(dataset_path):
            model = train(silent=True)
            for i in range(30, 80):
                progress.set(i / 100)
                splash.update()
                time.sleep(0.008)
        else:
            status.configure(text="Dataset not found, using classical only...")
            splash.update()
            for i in range(30, 80):
                progress.set(i / 100)
                splash.update()
                time.sleep(0.01)
    except Exception as e:
        status.configure(text=f"ML training failed...")
        splash.update()
        time.sleep(0.3)
    
    # Step 3: Finalize (80-100%)
    status.configure(text="Starting game...")
    for i in range(80, 101):
        progress.set(i / 100)
        splash.update()
        time.sleep(0.01)
    
    time.sleep(0.2)
    
    # Suppress Tkinter errors on close
    try:
        splash.destroy()
    except:
        pass
    
    return model

# ---------- Train model with splash screen ----------
import sys
import io

# Suppress pygame welcome message
sys.stdout = io.StringIO()
pygame.init()
sys.stdout = sys.__stdout__

model = show_splash()

# ---------- ML evaluation ----------
def extract_features(board):
    X = board.cells.count('X')
    O = board.cells.count('O')
    X_almost = 0
    O_almost = 0
    for line in WIN_LINES:
        xs = sum(board.cells[i] == 'X' for i in line)
        os = sum(board.cells[i] == 'O' for i in line)
        if xs == 2 and os == 0:
            X_almost += 1
        if os == 2 and xs == 0:
            O_almost += 1
    X_center = 1 if board.cells[4] == 'X' else 0
    X_corners = sum(board.cells[i] == 'X' for i in [0, 2, 6, 8])
    return [X, O, X_almost, O_almost, X_center, X_corners]

def ml_eval(board, player):
    if model is None:
        return classical_eval(board, player)
    score = model.predict_from_features(extract_features(board))
    return score if player == 'X' else -score

# ---------- Difficulty ----------
DIFFICULTY = {
    "Easy":   {"depth": 1, "mistake": 0.50, "noise": 5.0},   # Very shallow, lots of mistakes
    "Normal": {"depth": 3, "mistake": 0.20, "noise": 1.5},   # Moderate depth, some mistakes
    "Hard":   {"depth": 9, "mistake": 0.0,  "noise": 0.0}    # Perfect play
}

def noisy_eval(board, player, eval_fn, noise):
    base = eval_fn(board, player)
    return base + random.uniform(-noise, noise) if noise > 0 else base


class Game:
    def __init__(self):
        # Window
        self.root = ctk.CTk()
        self.root.title("Tic-Tac-Toe AI")
        self.root.geometry("850x650")
        self.root.minsize(850, 650)
        
        # Theme & Sound
        self.current_theme = "Dark"
        self.theme = THEMES[self.current_theme]
        self.sounds_enabled = True
        self.load_sounds()
        
        # Score tracking
        self.scores = {"player": 0, "ai": 0, "draw": 0}
        
        # Move history
        self.move_history = []
        
        # State
        self.board = Board()
        self.player = "X"
        self.difficulty = "Normal"
        self.eval_mode = "Classical"
        self.waiting = False
        self.winning_line = None
        
        self.apply_theme()
        self.build_ui()
        self.root.mainloop()

    def load_sounds(self):
        """Load sound effects"""
        self.sounds = {}
        sound_dir = os.path.join(SCRIPT_DIR, "sounds")
        try:
            self.sounds["click"] = pygame.mixer.Sound(os.path.join(sound_dir, "click.wav"))
            self.sounds["win"] = pygame.mixer.Sound(os.path.join(sound_dir, "win.wav"))
            self.sounds["lose"] = pygame.mixer.Sound(os.path.join(sound_dir, "lose.wav"))
            self.sounds["draw"] = pygame.mixer.Sound(os.path.join(sound_dir, "draw.wav"))
        except:
            self.sounds_enabled = False

    def play_sound(self, name):
        """Play a sound effect if enabled"""
        if self.sounds_enabled and name in self.sounds:
            try:
                self.sounds[name].play()
            except:
                pass

    def apply_theme(self):
        """Apply the current theme to the window"""
        self.theme = THEMES[self.current_theme]
        self.root.configure(fg_color=self.theme["bg"])

    def build_ui(self):
        # Top bar
        top = ctk.CTkFrame(self.root, fg_color="transparent")
        top.pack(fill="x", padx=30, pady=(20, 10))
        
        title = ctk.CTkLabel(top, text="🎮 Tic-Tac-Toe AI", font=("Arial", 28, "bold"), 
                             text_color=self.theme["text"])
        title.pack(side="left")
        
        # Score display
        self.score_frame = ctk.CTkFrame(top, fg_color=self.theme["panel"], corner_radius=8)
        self.score_frame.pack(side="right", padx=10)
        
        self.score_label = ctk.CTkLabel(self.score_frame, font=("Arial", 12, "bold"),
                                        text_color=self.theme["text_dim"])
        self.score_label.pack(padx=15, pady=8)
        self.update_score_display()
        
        self.status = ctk.CTkLabel(top, text="Your turn", font=("Arial", 16), 
                                   text_color=self.theme["win"])
        self.status.pack(side="right", padx=20)
        
        # Main content
        content = ctk.CTkFrame(self.root, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30)
        
        # Left - Board + Controls
        left = ctk.CTkFrame(content, fg_color="transparent")
        left.pack(side="left", fill="y", padx=(0, 20))
        
        self.build_board(left)
        self.build_controls(left)
        
        # Right panel - Analysis + History
        right = ctk.CTkFrame(content, fg_color=self.theme["panel"], corner_radius=12, width=320)
        right.pack(side="left", fill="both", expand=True)
        right.pack_propagate(False)
        
        # Analysis section
        header = ctk.CTkLabel(right, text="📊 AI Analysis", font=("Arial", 14, "bold"), 
                              text_color=self.theme["text_dim"])
        header.pack(anchor="w", padx=15, pady=(15, 5))
        
        self.log = ctk.CTkTextbox(right, font=("Consolas", 11), fg_color=self.theme["bg"], 
                                   text_color=self.theme["text"], corner_radius=8, height=150)
        self.log.pack(fill="x", padx=15, pady=(0, 10))
        self.log.insert("1.0", "Waiting for moves...")
        
        # Move History section
        history_header = ctk.CTkLabel(right, text="📜 Move History", font=("Arial", 14, "bold"), 
                                      text_color=self.theme["text_dim"])
        history_header.pack(anchor="w", padx=15, pady=(10, 5))
        
        self.history_box = ctk.CTkTextbox(right, font=("Consolas", 11), fg_color=self.theme["bg"], 
                                          text_color=self.theme["text"], corner_radius=8, height=120)
        self.history_box.pack(fill="x", padx=15, pady=(0, 10))
        self.history_box.insert("1.0", "Game not started...")
        
        # Theme & Sound controls
        bottom_controls = ctk.CTkFrame(right, fg_color="transparent")
        bottom_controls.pack(fill="x", padx=15, pady=(5, 15))
        
        ctk.CTkLabel(bottom_controls, text="🎨 Theme", font=("Arial", 12), 
                     text_color=self.theme["text_dim"]).pack(side="left")
        
        self.theme_btn = ctk.CTkSegmentedButton(bottom_controls, 
                                                 values=list(THEMES.keys()),
                                                 command=self.change_theme, width=180)
        self.theme_btn.set(self.current_theme)
        self.theme_btn.pack(side="left", padx=(8, 15))
        
        self.sound_btn = ctk.CTkButton(bottom_controls, text="🔊", width=40, height=32,
                                       fg_color=self.theme["accent"], 
                                       hover_color=self.theme["accent_hover"],
                                       command=self.toggle_sound)
        self.sound_btn.pack(side="right")

    def build_board(self, parent):
        self.board_frame = ctk.CTkFrame(parent, fg_color=self.theme["board"], corner_radius=12)
        self.board_frame.pack(pady=(0, 15))
        
        self.btns = []
        for i in range(9):
            btn = ctk.CTkButton(
                self.board_frame, text="", width=100, height=100,
                font=("Arial", 44, "bold"),
                fg_color=self.theme["cell"], hover_color=self.theme["cell_hover"],
                text_color=self.theme["text"], corner_radius=10,
                command=lambda x=i: self.click(x)
            )
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.btns.append(btn)

    def build_controls(self, parent):
        frame = ctk.CTkFrame(parent, fg_color=self.theme["panel"], corner_radius=12)
        frame.pack(fill="x")
        
        # Row 1 - Player & Difficulty
        row1 = ctk.CTkFrame(frame, fg_color="transparent")
        row1.pack(fill="x", padx=12, pady=(12, 6))
        
        ctk.CTkLabel(row1, text="Play as", font=("Arial", 12), 
                     text_color=self.theme["text_dim"]).pack(side="left")
        self.player_btn = ctk.CTkSegmentedButton(row1, values=["X", "O"], 
                                                  command=self.set_player, width=100)
        self.player_btn.set("X")
        self.player_btn.pack(side="left", padx=(8, 20))
        
        ctk.CTkLabel(row1, text="Difficulty", font=("Arial", 12), 
                     text_color=self.theme["text_dim"]).pack(side="left")
        self.diff_btn = ctk.CTkSegmentedButton(row1, values=["Easy", "Normal", "Hard"],
                                                command=self.set_diff, width=180)
        self.diff_btn.set("Normal")
        self.diff_btn.pack(side="left", padx=8)
        
        # Row 2 - Eval & Reset
        row2 = ctk.CTkFrame(frame, fg_color="transparent")
        row2.pack(fill="x", padx=12, pady=(6, 12))
        
        ctk.CTkLabel(row2, text="Eval", font=("Arial", 12), 
                     text_color=self.theme["text_dim"]).pack(side="left")
        self.eval_btn = ctk.CTkSegmentedButton(row2, values=["Classical", "ML"],
                                                command=self.set_eval, width=140)
        self.eval_btn.set("Classical")
        self.eval_btn.pack(side="left", padx=(8, 20))
        
        reset = ctk.CTkButton(row2, text="🔄 New Game", width=110, height=32,
                              fg_color=self.theme["accent"], hover_color=self.theme["accent_hover"],
                              command=self.reset)
        reset.pack(side="right")

    def update_score_display(self):
        """Update the score display"""
        text = f"👤 {self.scores['player']}  |  🤖 {self.scores['ai']}  |  🤝 {self.scores['draw']}"
        self.score_label.configure(text=text)

    def change_theme(self, theme_name):
        """Change the application theme"""
        self.current_theme = theme_name
        self.theme = THEMES[theme_name]
        
        # Update appearance mode for light theme
        if theme_name == "Light":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")
        
        # Recreate UI with new theme
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.apply_theme()
        self.build_ui()
        self.draw()
        self.update_score_display()

    def toggle_sound(self):
        """Toggle sound effects on/off"""
        self.sounds_enabled = not self.sounds_enabled
        self.sound_btn.configure(text="🔊" if self.sounds_enabled else "🔇")

    def add_to_history(self, player, cell):
        """Add a move to the history"""
        move_num = len(self.move_history) + 1
        row, col = cell // 3 + 1, cell % 3 + 1
        self.move_history.append(f"{move_num}. {player} → Row {row}, Col {col}")
        
        history_text = "\n".join(self.move_history[-10:])  # Show last 10 moves
        self.history_box.delete("1.0", "end")
        self.history_box.insert("1.0", history_text)

    def highlight_winning_line(self):
        """Highlight the winning cells with animation"""
        if self.winning_line is None:
            return
        
        # Determine highlight color based on winner
        winner = self.board.winner()
        if winner == self.player:
            highlight_color = self.theme["win_highlight"]  # Green for player win
        else:
            highlight_color = self.theme["lose"]  # Red for AI win
        
        # Flash the winning cells
        for _ in range(3):
            for i in self.winning_line:
                self.btns[i].configure(fg_color=highlight_color)
            self.root.update()
            time.sleep(0.15)
            for i in self.winning_line:
                self.btns[i].configure(fg_color=self.theme["cell"])
            self.root.update()
            time.sleep(0.1)
        
        # Keep highlighted
        for i in self.winning_line:
            self.btns[i].configure(fg_color=highlight_color)

    def find_winning_line(self):
        """Find which line won"""
        for line in WIN_LINES:
            cells = [self.board.cells[i] for i in line]
            if cells[0] != '-' and cells[0] == cells[1] == cells[2]:
                return line
        return None

    def set_player(self, v):
        if not self.waiting and self.is_fresh():
            self.player = v

    def set_diff(self, v):
        if not self.waiting and self.is_fresh():
            self.difficulty = v

    def set_eval(self, v):
        if not self.waiting and self.is_fresh():
            self.eval_mode = v

    def is_fresh(self):
        return self.board.cells.count('-') == 9

    def click(self, i):
        # Can't click if waiting for AI or cell taken or game over
        if self.waiting or self.board.cells[i] != '-' or self.board.is_terminal():
            return
        
        # Play click sound
        self.play_sound("click")
        
        # Human move
        self.board.make_move(i, self.player)
        self.add_to_history(self.player, i)
        self.draw()
        
        if self.board.is_terminal():
            self.end()
            return
        
        # AI turn
        self.waiting = True
        self.status.configure(text="AI thinking...", text_color=self.theme["text_dim"])
        self.root.update()
        self.root.after(200, self.ai_turn)

    def ai_turn(self):
        ai = "O" if self.player == "X" else "X"
        cfg = DIFFICULTY[self.difficulty]
        depth, mistake, noise = cfg["depth"], cfg["mistake"], cfg["noise"]
        
        base_eval = classical_eval if self.eval_mode == "Classical" else ml_eval
        def eval_fn(b, p): return noisy_eval(b, p, base_eval, noise)
        
        moves = self.board.legal_moves()
        
        # Opening move handling based on difficulty
        if len(moves) == 9:
            if self.difficulty == "Hard":
                # Optimal: center or corners only
                best = random.choice([4, 0, 2, 6, 8])
            elif self.difficulty == "Normal":
                # Usually good moves, occasionally an edge
                if random.random() < 0.2:
                    best = random.choice([1, 3, 5, 7])  # Sometimes pick edge
                else:
                    best = random.choice([4, 0, 2, 6, 8])
            else:  # Easy
                # Any position is fair game
                best = random.choice(moves)
            self.write_log(f"Opening move: Cell {best}")
        # Random mistake
        elif random.random() < mistake and len(moves) > 1:
            best = random.choice(moves)
            self.write_log(f"[Mistake] Random pick: Cell {best}")
        else:
            # Calculate
            lines = []
            lines.append(f"Difficulty: {self.difficulty} | Depth: {depth}")
            lines.append(f"Evaluation: {self.eval_mode}\n")
            lines.append("Raw Scores:")
            
            for m in moves:
                b = self.board.copy()
                b.make_move(m, ai)
                raw = base_eval(b, ai)
                lines.append(f"  Cell {m}: {raw:+.1f}")
            
            lines.append("\nSearch Scores:")
            scores = []
            for m in moves:
                b = self.board.copy()
                b.make_move(m, ai)
                s = alphabeta(b, depth, -9999, 9999, False, ai, eval_fn)
                scores.append((m, s))
                lines.append(f"  Cell {m}: {s:+.1f}")
            
            # Find best score and randomly pick among ties
            best_score = max(s for m, s in scores)
            best_moves = [m for m, s in scores if s == best_score]
            best = random.choice(best_moves)  # Random among equally good moves
            
            # Sometimes pick suboptimal
            if len(scores) > 1 and random.random() < mistake * 0.5:
                scores.sort(key=lambda x: x[1], reverse=True)
                best = random.choice(scores[:3])[0]
                lines.append("\n(Picked suboptimal)")
            
            lines.append(f"\nChosen: Cell {best}")
            self.write_log("\n".join(lines))
        
        self.board.make_move(best, ai)
        self.add_to_history(ai, best)
        self.play_sound("click")
        self.draw()
        
        if self.board.is_terminal():
            self.end()
        else:
            self.waiting = False
            self.status.configure(text="Your turn", text_color=self.theme["win"])

    def draw(self):
        colors = {"X": self.theme["x_color"], "O": self.theme["o_color"], "-": self.theme["text"]}
        for i, c in enumerate(self.board.cells):
            txt = "" if c == "-" else c
            self.btns[i].configure(text=txt, text_color=colors[c], fg_color=self.theme["cell"])

    def write_log(self, text):
        self.log.delete("1.0", "end")
        self.log.insert("1.0", text)

    def end(self):
        w = self.board.winner()
        self.winning_line = self.find_winning_line()
        
        if w == "D":
            self.status.configure(text="🤝 Draw!", text_color=self.theme["draw"])
            self.scores["draw"] += 1
            self.play_sound("draw")
        elif w == self.player:
            self.status.configure(text="🎉 You win!", text_color=self.theme["win"])
            self.scores["player"] += 1
            self.play_sound("win")
        else:
            self.status.configure(text="🤖 AI wins!", text_color=self.theme["lose"])
            self.scores["ai"] += 1
            self.play_sound("lose")
        
        self.update_score_display()
        
        # Highlight winning line with animation
        if self.winning_line:
            self.root.after(100, self.highlight_winning_line)
        
        self.waiting = True  # Prevent further clicks

    def reset(self):
        self.board = Board()
        self.waiting = False
        self.player = self.player_btn.get()
        self.difficulty = self.diff_btn.get()
        self.eval_mode = self.eval_btn.get()
        self.winning_line = None
        self.move_history = []
        
        for btn in self.btns:
            btn.configure(text="", text_color=self.theme["text"], fg_color=self.theme["cell"])
        
        self.log.delete("1.0", "end")
        self.log.insert("1.0", "Waiting for moves...")
        self.history_box.delete("1.0", "end")
        self.history_box.insert("1.0", "Game started!")
        self.status.configure(text="Your turn", text_color=self.theme["win"])
        
        # If playing O, AI goes first
        if self.player == "O":
            self.waiting = True
            self.status.configure(text="AI thinking...", text_color=self.theme["text_dim"])
            self.root.after(300, self.ai_turn)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    Game()
