"""
City Simulation Game - Main Entry Point

A comprehensive city simulation game built with Python and tkinter.
Features zoning, infrastructure building, time progression, and city management.
"""

import tkinter as tk
from ui import CitySimulationUI

def main():
    """Main entry point for the city simulation game."""
    # Create the main tkinter window
    root = tk.Tk()
    root.title("City Simulation Game")
    root.geometry("1200x800")
    root.resizable(True, True)
    
    # Set minimum window size
    root.minsize(800, 600)
    
    # Create and start the game UI
    game_ui = CitySimulationUI(root)
    
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()
