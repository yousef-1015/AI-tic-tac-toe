# Tic-Tac-Toe AI with Alpha-Beta Pruning and Machine Learning

An intelligent Tic-Tac-Toe game featuring AI that uses Alpha-Beta pruning with two evaluation methods: classical heuristic and machine learning.

## Features

### ✅ Complete Implementation

1. **Game Environment**
   - 3×3 Tic-Tac-Toe board
   - Legal move generation
   - Terminal state detection (win/loss/draw)

2. **Alpha-Beta Search**
   - Minimax with Alpha-Beta pruning optimization
   - Configurable search depth
   - Supports custom evaluation functions

3. **Two Evaluation Functions**
   - **Classical Heuristic**: Hand-coded evaluation considering:
     - Immediate wins and blocks (high priority)
     - Potential winning lines
     - Center control bonus
     - Corner control bonus
   
   - **Machine Learning**: Linear regression model trained on dataset with features:
     - X and O piece counts
     - Near-win positions (2-in-a-row)
     - Center occupation
     - Corner occupation
     - Labels: +1 for X wins, -1 for O wins

4. **Difficulty Levels**
   - **Easy**: Depth 2, 35% random moves
   - **Normal**: Depth 4, 15% random moves
   - **Hard**: Depth 9 (perfect play), no mistakes

5. **User Interface**
   - Clean, modern GUI using Tkinter
   - Choose to play as X or O
   - Select difficulty level
   - Choose evaluation function (Classical or ML)
   - Real-time AI analysis display showing:
     - Raw evaluation scores for each move
     - Alpha-Beta search scores
     - Chosen move and reasoning

## Files

- `main.py` - Main GUI application and game loop
- `board.py` - Board representation and game logic
- `alphabeta.py` - Alpha-Beta pruning implementation
- `heuristic.py` - Classical evaluation function
- `ml_model.py` - Linear regression model (from scratch)
- `trainer.py` - ML model training script
- `tictactoe_dataset.csv` - Training dataset (2015 samples)

## Requirements

```
Python 3.7+
pandas
tkinter (usually included with Python)
```

## Installation

1. Install Python dependencies:
```bash
pip install pandas
```

2. Run the game:
```bash
python main.py
```

## How to Play

1. **Select your settings**:
   - Choose your piece (X or O)
   - Select difficulty (Easy/Normal/Hard)
   - Choose evaluation method (Classical/ML)

2. **Play the game**:
   - Click any empty cell to make your move
   - Watch the AI analyze its options
   - See evaluation scores in the analysis panel

3. **AI Analysis Panel** shows:
   - Raw evaluation scores for each possible move
   - Alpha-Beta search scores (looking ahead)
   - Which move the AI selected and why

## AI Implementation Details

### Alpha-Beta Pruning
- Optimizes minimax search by pruning branches
- Returns higher scores for faster wins
- Terminal states: +1000 for win, -1000 for loss, 0 for draw

### Classical Heuristic
- Prioritizes immediate wins (score: +50)
- Blocks opponent near-wins (score: -40)
- Values center position (+3) and corners (+2)

### Machine Learning Model
- Custom linear regression (no AI libraries)
- Trained with gradient descent
- 200 epochs, learning rate 0.01
- 6 features extracted from board state

## Project Structure

```
AI project/
├── main.py              # GUI and game controller
├── board.py             # Board logic
├── alphabeta.py         # Search algorithm
├── heuristic.py         # Classical evaluation
├── ml_model.py          # ML model class
├── trainer.py           # Model training
├── tictactoe_dataset.csv # Training data
└── README.md           # This file
```

## Notes

- All AI components (Alpha-Beta, heuristic, ML model) are implemented from scratch
- No external AI libraries used (scikit-learn, tensorflow, etc.)
- Only pandas is used for CSV reading (allowed non-AI library)
- Hard difficulty provides perfect play (unbeatable when going first)

## Author

Created as a university AI project demonstrating:
- Game tree search algorithms
- Evaluation function design
- Machine learning from scratch
- GUI development
