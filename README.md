# 2D Self-Driving Car Simulation

This is a simple 2D self-driving car simulation built using **Python** and **Pygame**. The car uses basic AI logic to navigate a track with obstacles while avoiding collisions.

---

## Features

- **Autonomous Navigation:** The car drives itself using a simple AI algorithm.
- **Sensors:** Forward, left, and right ray-casting sensors detect obstacles.
- **Dynamic Steering:** Adjusts speed and steering based on proximity to obstacles.
- **Distance Tracking:** Measures and displays the total distance traveled.
- **Obstacle Avoidance:** Handles both outer walls and inner obstacles.
- **Visual Feedback:** Sensor lines change color based on distance:
  - Green: Path clear
  - Yellow: Medium distance
  - Red: Very close

---


## 🛠 Installation & Run

### Prerequisites
- **Python 3.8+** installed on your system.
- **pip** (Python package manager).
- Python libraries:
  - `pygame`
  - `math` 

### Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/NJ-DEV-616/2D-Self-Driving-Car-simulation.git
   cd 2D-Self-Driving-Car-simulation
2. **Install Dependencies**
    ```bash
    pip install pygame
3. **Run the Program**
    ```bash
    python main.py
---
## 🧾 License
This project is licensed under the [MIT License](LICENSE).
---
