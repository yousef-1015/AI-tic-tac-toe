# 🎮 Tic-Tac-Toe AI

An intelligent Tic-Tac-Toe game powered by **Alpha-Beta pruning** with two evaluation strategies: classical heuristics and machine learning.
<img width="1061" height="649" alt="image" src="https://github.com/user-attachments/assets/dd980ec6-b578-455d-aefd-413196600225" />


## ✨ Features

- **Smart AI** - Uses Alpha-Beta pruning for optimal move selection
- **Dual Evaluation** - Choose between classical heuristic or ML-based evaluation
- **Three Difficulty Levels** - Easy, Normal, and Hard (unbeatable)
- **Real-time Analysis** - Watch the AI evaluate each possible move
- **Clean Interface** - Simple, modern GUI built with Tkinter

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.7+
pip install customtkinter pandas pygame
```

### Run the Game
```bash
python main.py
```

## 🎯 How It Works

### Alpha-Beta Pruning
Optimized minimax algorithm that prunes unnecessary branches in the game tree, making the AI faster while maintaining perfect play at high difficulty.

### Classical Heuristic
Hand-crafted evaluation considering:
- Immediate wins and blocks (highest priority)
- Two-in-a-row threats
- Center and corner control

### Machine Learning
Linear regression model trained on 2000+ game positions with features like piece counts, near-win states, and strategic positions.

## 🎲 Difficulty Levels

| Level  | Search Depth | Random Moves | Strength      |
|--------|--------------|--------------|---------------|
| Easy   | 2            | 35%          | Beatable      |
| Normal | 4            | 15%          | Challenging   |
| Hard   | 9            | 0%           | Unbeatable    |

## 📁 Project Structure

```
├── main.py                  # GUI and game controller
├── board.py                 # Board logic and rules
├── alphabeta.py             # Search algorithm
├── heuristic.py             # Classical evaluation
├── ml_model.py              # Linear regression model
├── trainer.py               # Model training script
├── tictactoe_dataset.csv    # Training data (2015 samples)
└── README.md
```

## 🛠️ Built With

- **Python** - Core language
- **Tkinter** - GUI framework
- **Pandas** - CSV data handling
- **Custom ML** - Linear regression implemented from scratch

## 📝 Notes

All AI components (Alpha-Beta, evaluation functions, ML model) are implemented from scratch without external AI libraries like scikit-learn or TensorFlow.


---

**Enjoy the game! 🎉**
