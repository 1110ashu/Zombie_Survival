A grid-based Zombie Survival Game developed using Python and the Pygame, focused on demonstrating the practical application of the Breadth-First Search (BFS) algorithm.

In this game, zombies spread across the grid using a BFS-inspired approach, and the player must reach a safe zone while avoiding them within a limited time.

🎮 Gameplay Overview
The player starts at one corner of the grid
Zombies spawn randomly and spread level-by-level
The player must reach the safe zone
If the player is caught or time runs out → Game Over
✨ Features
🧠 BFS-based zombie spreading algorithm
🎮 Grid-based player movement
⏱️ Timer-based survival challenge
📈 Level progression with increasing difficulty
🏆 Score tracking system
🎵 Background music and sound effects
🎨 Improved UI with glow effects
🎥 Camera shake effect on game over
🔁 Restart system
🧠 Algorithm Used
Breadth-First Search (BFS)

The zombie spreading logic is based on BFS principles:

Each zombie spreads to its adjacent cells
Expansion happens level-by-level
Simulates real-world spreading (like infection propagation)
🛠️ Tech Stack
Language: Python 3.x
Library: Pygame
Concepts:
BFS Algorithm
Game Loop
Event Handling
Collision Detection

📂 Project Structure

zombie.py
bg_music.wav
move.wav
win.wav
lose.wav

