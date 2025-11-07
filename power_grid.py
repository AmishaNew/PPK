"""
Power Grid System - Manages electrical power distribution

Handles power generation, transmission through power lines, and zone coverage.
"""

from typing import Dict, Set, Tuple, List, Optional
from infrastructure import Infrastructure
from zone import Zone

class PowerGrid:
    """
    Manages the city's electrical power distribution system.
    """
    
    def __init__(self, city):
        """Initialize the power grid system."""
        self.city = city
        self.power_network = {}  # Graph of connected power infrastructure
        self.powered_zones = set()  # Zones that have power
        self.power_generation = 0
        self.power_consumption = 0
        
    def update_power_network(self):
        """Update the power network connectivity and coverage."""
        self._build_power_network()
        self._calculate_power_coverage()
        self._update_power_statistics()
    
    def _build_power_network(self):
        """Build a graph of connected power infrastructure."""
        self.power_network = {}
        
        # Find all power infrastructure
        power_plants = []
        power_lines = []
        
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.get_cell(x, y)
                if isinstance(cell, Infrastructure):
                    if cell.infrastructure_type == 'power_plant':
                        power_plants.append((x, y))
                        self.power_network[(x, y)] = []
                    elif cell.infrastructure_type == 'power_line':
                        power_lines.append((x, y))
                        self.power_network[(x, y)] = []
        
        # Connect adjacent power infrastructure
        for pos in list(self.power_network.keys()):
            x, y = pos
            # Check 4 adjacent positions
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) in self.power_network:
                    self.power_network[pos].append((nx, ny))
    
    def _calculate_power_coverage(self):
        """Calculate which zones have power access."""
        self.powered_zones = set()
        
        # Find all power plants
        power_plants = []
        for pos in self.power_network:
            x, y = pos
            cell = self.city.get_cell(x, y)
            if isinstance(cell, Infrastructure) and cell.infrastructure_type == 'power_plant':
                power_plants.append(pos)
        
        # For each power plant, find connected network
        for plant_pos in power_plants:
            connected_network = self._get_connected_network(plant_pos)
            
            # Add coverage around each connected infrastructure
            for net_pos in connected_network:
                self._add_coverage_around_position(net_pos)
    
    def _get_connected_network(self, start_pos: Tuple[int, int]) -> Set[Tuple[int, int]]:
        """Get all power infrastructure connected to the starting position."""
        visited = set()
        to_visit = [start_pos]
        
        while to_visit:
            current = to_visit.pop()
            if current in visited:
                continue
                
            visited.add(current)
            
            # Add connected neighbors
            if current in self.power_network:
                for neighbor in self.power_network[current]:
                    if neighbor not in visited:
                        to_visit.append(neighbor)
        
        return visited
    
    def _add_coverage_around_position(self, pos: Tuple[int, int], radius: int = 3):
        """Add power coverage around a power infrastructure position."""
        x, y = pos
        
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy <= radius * radius:
                    zone_x, zone_y = x + dx, y + dy
                    if self.city.is_valid_position(zone_x, zone_y):
                        self.powered_zones.add((zone_x, zone_y))
    
    def _update_power_statistics(self):
        """Update power generation and consumption statistics."""
        self.power_generation = 0
        self.power_consumption = 0
        
        # Calculate generation from power plants
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.get_cell(x, y)
                if isinstance(cell, Infrastructure) and cell.infrastructure_type == 'power_plant':
                    self.power_generation += cell.get_output('power')
        
        # Calculate consumption from zones
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.get_cell(x, y)
                if isinstance(cell, Zone) and cell.development_level > 0:
                    # Power consumption based on zone type and development
                    base_consumption = {
                        'residential': 10,
                        'commercial': 15,
                        'industrial': 25
                    }
                    consumption = base_consumption.get(cell.zone_type, 0) * cell.development_level
                    self.power_consumption += consumption
    
    def is_powered(self, x: int, y: int) -> bool:
        """Check if a position has power access."""
        return (x, y) in self.powered_zones
    
    def get_power_coverage(self) -> Set[Tuple[int, int]]:
        """Get all positions with power coverage."""
        return self.powered_zones.copy()
    
    def get_power_statistics(self) -> Dict[str, float]:
        """Get power system statistics."""
        return {
            'generation': self.power_generation,
            'consumption': self.power_consumption,
            'coverage_percentage': len(self.powered_zones) / (self.city.width * self.city.height) * 100,
            'efficiency': min(1.0, self.power_generation / max(1, self.power_consumption))
        }