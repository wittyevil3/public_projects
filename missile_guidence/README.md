# Files
## Included files
- README.md
- missile.py
## Required python libraries
- numpy
- random
- matplotlib.pyplot
- time

# Running Instructions
Just run the program to have the missile follow the enemy missile and plot the output
## Options in the last part of code (`if __name__ == '__main__':`)
- un-comment `missile.graphaccuracy(10, 1, 2)` to graph the accurraccy fall off of the missile
- `misle.velocity` is how fast your missile goes
- `enemy.position` is where the enemy starts
- `enemy.set_facing` is the angle the enemy starts looking at
- `enemy.velocity` is how fast the enemy is going
- `metadata` is the offset, sence angle, strength, and resistance of the missile (more info in the `missile.one_strength` function)
