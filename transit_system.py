"""
Public Transit System - Manages trains, subways, and public transportation

Handles transit stations, lines, and passenger routing.
"""

from typing import Dict, Set, Tuple, List
from dataclasses import dataclass
from infrastructure import Infrastructure
from zone import Zone

@dataclass
class TransitStation:
    """Represents a transit station."""
    x: int
    y: int
    station_type: str  # 'train_station', 'subway_station'
    capacity: int
    coverage_radius: int
    
@dataclass
class TransitLine:
    """Represents a transit line connecting stations."""
    stations: List[TransitStation]
    line_type: str  # 'train', 'subway'
    frequency: int  # Trains per hour

class TransitSystem:
    """
    Manages the city's public transportation network.
    """
    
    def __init__(self, city):
        """Initialize the transit system."""
        self.city = city
        self.stations = []
        self.transit_lines = []
        self.coverage_areas = set()
        self.passenger_capacity = 0
        
    def update_transit_system(self):
        """Update the transit system."""
        self._find_stations()
        self._create_transit_lines()
        self._calculate_coverage()
        self._update_capacity()
    
    def _find_stations(self):
        """Find all transit stations in the city."""
        self.stations = []
        
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.get_cell(x, y)
                if isinstance(cell, Infrastructure):
                    if cell.infrastructure_type in ['train_station', 'subway_station']:
                        capacity = cell.properties.get('transit_capacity', 1000)
                        radius = cell.properties.get('coverage_radius', 5)
                        
                        station = TransitStation(
                            x=x, y=y,
                            station_type=cell.infrastructure_type,
                            capacity=capacity,
                            coverage_radius=radius
                        )
                        self.stations.append(station)
    
    def _create_transit_lines(self):
        """Create transit lines connecting nearby stations."""
        self.transit_lines = []
        
        # Group stations by type
        train_stations = [s for s in self.stations if s.station_type == 'train_station']
        subway_stations = [s for s in self.stations if s.station_type == 'subway_station']
        
        # Create train lines
        if len(train_stations) >= 2:
            # Connect stations that are reasonably close
            connected_stations = []
            for station in train_stations:
                if not connected_stations:
                    connected_stations.append(station)
                else:
                    # Find closest connected station
                    closest_dist = float('inf')
                    for connected in connected_stations:
                        dist = ((station.x - connected.x) ** 2 + (station.y - connected.y) ** 2) ** 0.5
                        if dist < closest_dist and dist <= 15:  # Max connection distance
                            closest_dist = dist
                    
                    if closest_dist <= 15:
                        connected_stations.append(station)
            
            if len(connected_stations) >= 2:
                line = TransitLine(
                    stations=connected_stations,
                    line_type='train',
                    frequency=6  # 6 trains per hour
                )
                self.transit_lines.append(line)
        
        # Create subway lines
        if len(subway_stations) >= 2:
            connected_stations = []
            for station in subway_stations:
                if not connected_stations:
                    connected_stations.append(station)
                else:
                    closest_dist = float('inf')
                    for connected in connected_stations:
                        dist = ((station.x - connected.x) ** 2 + (station.y - connected.y) ** 2) ** 0.5
                        if dist < closest_dist and dist <= 10:  # Shorter max distance for subway
                            closest_dist = dist
                    
                    if closest_dist <= 10:
                        connected_stations.append(station)
            
            if len(connected_stations) >= 2:
                line = TransitLine(
                    stations=connected_stations,
                    line_type='subway',
                    frequency=12  # 12 trains per hour
                )
                self.transit_lines.append(line)
    
    def _calculate_coverage(self):
        """Calculate transit coverage areas."""
        self.coverage_areas = set()
        
        for station in self.stations:
            # Add coverage around each station
            for dy in range(-station.coverage_radius, station.coverage_radius + 1):
                for dx in range(-station.coverage_radius, station.coverage_radius + 1):
                    if dx * dx + dy * dy <= station.coverage_radius * station.coverage_radius:
                        coverage_x = station.x + dx
                        coverage_y = station.y + dy
                        if self.city.is_valid_position(coverage_x, coverage_y):
                            self.coverage_areas.add((coverage_x, coverage_y))
    
    def _update_capacity(self):
        """Update total passenger capacity."""
        self.passenger_capacity = sum(station.capacity for station in self.stations)
    
    def has_transit_access(self, x: int, y: int) -> bool:
        """Check if a position has transit access."""
        return (x, y) in self.coverage_areas
    
    def get_transit_reduction_factor(self, x: int, y: int) -> float:
        """Get traffic reduction factor due to transit access."""
        if self.has_transit_access(x, y):
            # Find nearest station
            min_distance = float('inf')
            for station in self.stations:
                dist = ((x - station.x) ** 2 + (y - station.y) ** 2) ** 0.5
                min_distance = min(min_distance, dist)
            
            # Closer to station = more traffic reduction
            if min_distance <= 2:
                return 0.4  # 40% traffic reduction
            elif min_distance <= 4:
                return 0.25  # 25% traffic reduction
            else:
                return 0.1  # 10% traffic reduction
        
        return 0.0  # No reduction
    
    def get_coverage_statistics(self) -> Dict[str, float]:
        """Get transit coverage statistics."""
        total_area = self.city.width * self.city.height
        coverage_percentage = len(self.coverage_areas) / total_area * 100
        
        return {
            'stations': len(self.stations),
            'lines': len(self.transit_lines),
            'coverage_percentage': coverage_percentage,
            'passenger_capacity': self.passenger_capacity
        }