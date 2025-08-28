"""
City Class - Core city management and data structure

Manages the overall city state, grid layout, and coordinates between different systems.
"""

import json
import pickle
from typing import Dict, List, Tuple, Optional
from zone import Zone
from building import Building
from infrastructure import Infrastructure

class City:
    """
    Main city class that manages the grid, zones, buildings, and overall city state.
    """
    
    def __init__(self, width: int = 50, height: int = 50):
        """
        Initialize a new city with given dimensions.
        
        Args:
            width: Grid width in tiles
            height: Grid height in tiles
        """
        self.width = width
        self.height = height
        
        # Initialize grid - each cell can contain a zone, building, or infrastructure
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        
        # City resources and statistics
        self.money = 100000  # Starting money
        self.population = 0
        self.happiness = 50.0  # Scale 0-100
        self.pollution = 0.0   # Scale 0-100
        
        # Economic indicators
        self.tax_revenue = 0
        self.maintenance_cost = 0
        self.employment_rate = 0.0
        
        # Infrastructure coverage tracking
        self.power_coverage = set()  # Grid positions with power
        self.water_coverage = set()  # Grid positions with water
        self.road_network = set()    # Grid positions with roads
        
        # Zone counts for statistics
        self.zone_counts = {
            'residential': 0,
            'commercial': 0,
            'industrial': 0
        }
        
        # Building counts
        self.building_counts = {
            'houses': 0,
            'shops': 0,
            'factories': 0,
            'schools': 0,
            'hospitals': 0,
            'power_plants': 0,
            'water_facilities': 0
        }
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if the given position is within city bounds."""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get_cell(self, x: int, y: int) -> Optional[object]:
        """Get the object at the specified grid position."""
        if self.is_valid_position(x, y):
            return self.grid[y][x]
        return None
    
    def set_cell(self, x: int, y: int, obj: object) -> bool:
        """
        Set an object at the specified grid position.
        
        Returns:
            True if successful, False if position is invalid or occupied
        """
        if not self.is_valid_position(x, y):
            return False
        
        if self.grid[y][x] is not None:
            return False  # Position already occupied
        
        self.grid[y][x] = obj
        return True
    
    def remove_cell(self, x: int, y: int) -> bool:
        """Remove an object from the specified grid position."""
        if not self.is_valid_position(x, y):
            return False
        
        obj = self.grid[y][x]
        if obj is None:
            return False
        
        # Update counts based on object type
        if isinstance(obj, Zone):
            self.zone_counts[obj.zone_type] -= 1
        elif isinstance(obj, Building):
            if obj.building_type in self.building_counts:
                self.building_counts[obj.building_type] -= 1
        
        self.grid[y][x] = None
        return True
    
    def place_zone(self, x: int, y: int, zone_type: str) -> bool:
        """
        Place a zone at the specified position.
        
        Args:
            x, y: Grid coordinates
            zone_type: 'residential', 'commercial', or 'industrial'
        
        Returns:
            True if placement successful
        """
        if not self.is_valid_position(x, y) or self.grid[y][x] is not None:
            return False
        
        zone = Zone(x, y, zone_type)
        self.grid[y][x] = zone
        self.zone_counts[zone_type] += 1
        return True
    
    def place_infrastructure(self, x: int, y: int, infra_type: str) -> bool:
        """
        Place infrastructure at the specified position.
        
        Args:
            x, y: Grid coordinates
            infra_type: Type of infrastructure to place
        
        Returns:
            True if placement successful
        """
        if not self.is_valid_position(x, y) or self.grid[y][x] is not None:
            return False
        
        infrastructure = Infrastructure(x, y, infra_type)
        cost = infrastructure.get_cost()
        
        if self.money < cost:
            return False  # Not enough money
        
        self.grid[y][x] = infrastructure
        self.money -= cost
        
        # Update coverage maps
        if infra_type == 'power_plant':
            self.update_power_coverage(x, y)
            self.building_counts['power_plants'] += 1
        elif infra_type == 'water_facility':
            self.update_water_coverage(x, y)
            self.building_counts['water_facilities'] += 1
        elif infra_type == 'road':
            self.road_network.add((x, y))
        elif infra_type in ['school', 'hospital']:
            self.building_counts[infra_type + 's'] += 1
        
        return True
    
    def update_power_coverage(self, power_x: int, power_y: int, radius: int = 10):
        """Update power coverage around a power plant."""
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy <= radius * radius:
                    pos_x, pos_y = power_x + dx, power_y + dy
                    if self.is_valid_position(pos_x, pos_y):
                        self.power_coverage.add((pos_x, pos_y))
    
    def update_water_coverage(self, water_x: int, water_y: int, radius: int = 8):
        """Update water coverage around a water facility."""
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy <= radius * radius:
                    pos_x, pos_y = water_x + dx, water_y + dy
                    if self.is_valid_position(pos_x, pos_y):
                        self.water_coverage.add((pos_x, pos_y))
    
    def get_neighbors(self, x: int, y: int, radius: int = 1) -> List[Tuple[int, int, object]]:
        """Get all neighbors within the specified radius."""
        neighbors = []
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if self.is_valid_position(nx, ny):
                    neighbors.append((nx, ny, self.grid[ny][nx]))
        return neighbors
    
    def calculate_happiness(self) -> float:
        """
        Calculate overall city happiness based on various factors.
        
        Returns:
            Happiness value between 0-100
        """
        if self.population == 0:
            return 50.0
        
        happiness_factors = []
        
        # Employment factor (0-25 points)
        employment_happiness = min(25, self.employment_rate * 25)
        happiness_factors.append(employment_happiness)
        
        # Pollution factor (0-25 points, inverse)
        pollution_happiness = max(0, 25 - (self.pollution / 4))
        happiness_factors.append(pollution_happiness)
        
        # Infrastructure coverage factor (0-25 points)
        total_zones = sum(self.zone_counts.values())
        if total_zones > 0:
            power_coverage_ratio = len(self.power_coverage) / (self.width * self.height)
            water_coverage_ratio = len(self.water_coverage) / (self.width * self.height)
            infrastructure_happiness = (power_coverage_ratio + water_coverage_ratio) * 12.5
        else:
            infrastructure_happiness = 0
        happiness_factors.append(infrastructure_happiness)
        
        # Services factor (0-25 points)
        schools = self.building_counts.get('schools', 0)
        hospitals = self.building_counts.get('hospitals', 0)
        service_ratio = min(1.0, (schools + hospitals) / max(1, self.population / 1000))
        services_happiness = service_ratio * 25
        happiness_factors.append(services_happiness)
        
        total_happiness = sum(happiness_factors)
        self.happiness = max(0, min(100, total_happiness))
        return self.happiness
    
    def update_statistics(self):
        """Update all city statistics."""
        # Reset counters
        self.population = 0
        self.tax_revenue = 0
        self.maintenance_cost = 0
        total_jobs = 0
        employed = 0
        self.pollution = 0
        
        # Calculate based on grid contents
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                if isinstance(cell, Zone):
                    if cell.zone_type == 'residential' and cell.development_level > 0:
                        # Each development level adds population
                        residents = cell.development_level * 50
                        self.population += residents
                        self.tax_revenue += residents * 10  # $10 per resident
                    
                    elif cell.zone_type == 'commercial' and cell.development_level > 0:
                        # Commercial zones provide jobs and tax revenue
                        jobs = cell.development_level * 30
                        total_jobs += jobs
                        self.tax_revenue += cell.development_level * 500
                    
                    elif cell.zone_type == 'industrial' and cell.development_level > 0:
                        # Industrial zones provide jobs but create pollution
                        jobs = cell.development_level * 40
                        total_jobs += jobs
                        self.tax_revenue += cell.development_level * 300
                        self.pollution += cell.development_level * 5
                
                elif isinstance(cell, Infrastructure):
                    # Infrastructure has maintenance costs
                    self.maintenance_cost += cell.get_maintenance_cost()
        
        # Calculate employment rate
        if self.population > 0:
            working_population = self.population * 0.6  # 60% of population can work
            employed = min(working_population, total_jobs)
            self.employment_rate = employed / working_population if working_population > 0 else 0
        
        # Update happiness
        self.calculate_happiness()
    
    def save_to_file(self, filename: str) -> bool:
        """
        Save the current city state to a file.
        
        Args:
            filename: Path to save file
        
        Returns:
            True if save successful
        """
        try:
            save_data = {
                'width': self.width,
                'height': self.height,
                'money': self.money,
                'population': self.population,
                'happiness': self.happiness,
                'pollution': self.pollution,
                'zone_counts': self.zone_counts,
                'building_counts': self.building_counts,
                'grid_data': []
            }
            
            # Serialize grid data
            for y in range(self.height):
                row = []
                for x in range(self.width):
                    cell = self.grid[y][x]
                    if cell is None:
                        row.append(None)
                    else:
                        row.append(cell.to_dict())
                save_data['grid_data'].append(row)
            
            with open(filename, 'wb') as f:
                pickle.dump(save_data, f)
            return True
        except Exception as e:
            print(f"Error saving city: {e}")
            return False
    
    def load_from_file(self, filename: str) -> bool:
        """
        Load city state from a file.
        
        Args:
            filename: Path to save file
        
        Returns:
            True if load successful
        """
        try:
            with open(filename, 'rb') as f:
                save_data = pickle.load(f)
            
            # Restore basic properties
            self.width = save_data['width']
            self.height = save_data['height']
            self.money = save_data['money']
            self.population = save_data['population']
            self.happiness = save_data['happiness']
            self.pollution = save_data['pollution']
            self.zone_counts = save_data['zone_counts']
            self.building_counts = save_data['building_counts']
            
            # Recreate grid
            self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
            
            for y, row in enumerate(save_data['grid_data']):
                for x, cell_data in enumerate(row):
                    if cell_data is not None:
                        # Recreate objects from saved data
                        obj_type = cell_data['type']
                        if obj_type == 'zone':
                            zone = Zone(x, y, cell_data['zone_type'])
                            zone.development_level = cell_data['development_level']
                            self.grid[y][x] = zone
                        elif obj_type == 'infrastructure':
                            infra = Infrastructure(x, y, cell_data['infrastructure_type'])
                            self.grid[y][x] = infra
                        elif obj_type == 'building':
                            building = Building(x, y, cell_data['building_type'])
                            self.grid[y][x] = building
            
            # Rebuild coverage maps
            self.power_coverage = set()
            self.water_coverage = set()
            self.road_network = set()
            
            for y in range(self.height):
                for x in range(self.width):
                    cell = self.grid[y][x]
                    if isinstance(cell, Infrastructure):
                        if cell.infrastructure_type == 'power_plant':
                            self.update_power_coverage(x, y)
                        elif cell.infrastructure_type == 'water_facility':
                            self.update_water_coverage(x, y)
                        elif cell.infrastructure_type == 'road':
                            self.road_network.add((x, y))
            
            return True
        except Exception as e:
            print(f"Error loading city: {e}")
            return False
