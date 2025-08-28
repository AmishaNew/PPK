# City Simulation Game

## Overview

This is a comprehensive city simulation game built with Python and tkinter. The game allows players to build and manage a virtual city by placing zones (residential, commercial, industrial), constructing buildings (schools, hospitals, shops), and developing infrastructure (roads, power plants, water facilities). The simulation includes time progression, economic management, population dynamics, and city statistics tracking.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Game Architecture
The application follows a modular object-oriented design with clear separation of concerns:

- **Model-View-Controller Pattern**: The `City` class serves as the core data model, `CitySimulationUI` handles the view layer, and `Simulation` manages the game logic controller
- **Grid-Based World**: Uses a 2D grid system (default 50x50) where each cell can contain zones, buildings, or infrastructure
- **Component-Based Design**: Separate classes for different game elements (Zone, Building, Infrastructure) with type-specific characteristics

### Frontend Architecture
- **GUI Framework**: Built entirely with tkinter for cross-platform desktop compatibility
- **Canvas-Based Rendering**: Uses tkinter Canvas for the main city view with zoom and scroll capabilities
- **Real-Time Updates**: UI updates are driven by simulation callbacks to maintain synchronization
- **Tool-Based Interaction**: Users select tools (inspect, zone, build, infrastructure) to interact with the city grid

### Game Logic System
- **Time Progression**: Real-time simulation with configurable speed (0.1x to 10x)
- **Resource Management**: Tracks money, population, happiness, pollution, and employment
- **Development Mechanics**: Zones automatically develop over time based on city conditions
- **Service Coverage**: Infrastructure provides area-of-effect coverage (power, water, education, health)

### Data Management
- **In-Memory State**: All game state stored in Python objects during gameplay
- **Save/Load System**: Uses JSON for human-readable saves and pickle for binary saves
- **Statistics Tracking**: Comprehensive tracking of city metrics and performance indicators

### Simulation Engine
- **Event-Driven Updates**: Monthly and yearly simulation cycles for economic updates
- **Dependency System**: Buildings and zones require infrastructure (power, water, roads) to function
- **Dynamic Calculations**: Real-time calculation of happiness, pollution, employment, and tax revenue

## External Dependencies

### Core Dependencies
- **tkinter**: Built-in Python GUI framework for all user interface elements
- **Standard Library**: Uses json, pickle, time, random, math, and typing modules

### Development Libraries
- **typing**: Provides type hints for better code maintainability and IDE support

### Runtime Requirements
- **Python 3.6+**: Required for type hints and modern Python features
- **Cross-Platform**: Designed to run on Windows, macOS, and Linux through tkinter

The application is designed to be self-contained with minimal external dependencies, relying primarily on Python's standard library for maximum compatibility and ease of deployment.