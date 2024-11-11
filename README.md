<div align="center">

# Flappy Bird AI

<img
  src="img/explanations/start_view.png"
  alt="Start View"
  width="600"
  style="max-width: 100%;">
</div>

A Python implementation of Flappy Bird featuring AI gameplay using the NEAT
(NeuroEvolution of Augmenting Topologies) genetic algorithm.

## ✨ Features
- **Multiple Game Modes**: Play solo, compete against AI, train new AI models,
or watch AI gameplay
- **NEAT Implementation**: Neural network/genetic algorithm using the NEAT
library
- **Customizable Parameters**: Adjust generation count and population size
- **Performance Tracking**: Real-time display of alive birds, current score,
and generation number
- **Interactive UI**: Easy navigation between different modes with intuitive
controls

## 🎮 Game Modes

### 1. Solo Play
Classic Flappy Bird gameplay with score tracking and instant replay option.

![Play view](img/explanations/play_view.gif)

### 2. AI Competition
Play as an **Orange** Flappy Bird against the AI's **Blue** Flappy Bird. Test
your skills against the trained neural network!

![Play Against AI view](img/explanations/play_against_ai_view.gif)

### 3. AI Training
Run the genetic algorithm to create new AI models. Watch multiple birds learn
simultaneously with real-time performance metrics.

![Train AI view](img/explanations/train_ai_view.gif)

#### Training Process
- Fixed number of generations (default: 10)
- Each generation has multiple birds (default: 15)
- Best performers are selected to create the next generation
- Full algorithm details in [NEAT paper](http://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf)

### 4. AI Exhibition
Watch the best-performing AI play the game. This is the same model used in
Competition mode.

![Test AI view](img/explanations/test_ai_view.gif)

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/flappy-bird-ai.git
cd flappy-bird-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Launch the game:
```bash
python run.py
```

## ⚙️ Configuration

### Training Parameters
1. Modify generation count:
   - Edit `./config/neat/neat_config`
   - Update `GENERATIONS_NUMBER` value

2. Adjust population size:
   - Edit `./config/neat/network_config.txt`
   - Update `pop_size` value

### Training View Information
During training, you'll see:
- Number of birds still alive
- Current score
- Generation number

**Note:** Please allow the training to complete before returning to the start
view.

## 🧠 NEAT Algorithm Overview
The genetic algorithm follows these steps:
1. Initialize population with random neural networks
2. For each generation:
   - All birds play simultaneously
   - Evaluate
