"""
Traffic Manager - Handles traffic flow and transportation

Calculates traffic based on commuting patterns and leisure activities.
"""

from typing import Dict, Set, Tuple, List
from dataclasses import dataclass
import random
from infrastructure import Infrastructure
from zone import Zone

@dataclass
class TrafficData:
    """Traffic information for a road segment."""
    volume: int  # Vehicles per hour
    capacity: int  # Maximum vehicles per hour
    congestion_level: float  # 0.0 to 1.0
    average_speed: float  # km/h

@dataclass
class TripGenerator:
    """Represents a source of trips in the city."""
    origin: Tuple[int, int]
    destination: Tuple[int, int]
    trip_type: str  # 'commute', 'leisure', 'cargo'
    volume: int  # Trips per day

class TrafficManager:
    """
    Manages traffic flow calculation and road network analysis.
    """
    
    def __init__(self, city):
        """Initialize the traffic manager."""
        self.city = city
        self.road_network = {}  # Graph of road connections
        self.traffic_data = {}  # Traffic data for each road segment
        self.trip_generators = []  # Sources of traffic
        
    def update_traffic_system(self):
        """Update the entire traffic system."""
        self._build_road_network()
        self._generate_trips()
        self._calculate_traffic_flow()
        self._update_congestion()
    
    def _build_road_network(self):
        """Build a graph of connected roads."""
        self.road_network = {}
        
        # Find all roads and highways
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.get_cell(x, y)
                if isinstance(cell, Infrastructure):
                    if cell.infrastructure_type in ['road', 'highway']:
                        self.road_network[(x, y)] = {
                            'connections': [],
                            'capacity': self._get_road_capacity(cell),
                            'type': cell.infrastructure_type
                        }
        
        # Connect adjacent roads
        for pos in list(self.road_network.keys()):
            x, y = pos
            # Check 4 adjacent positions
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) in self.road_network:
                    self.road_network[pos]['connections'].append((nx, ny))
    
    def _get_road_capacity(self, road: Infrastructure) -> int:
        """Get the traffic capacity of a road."""
        if road.infrastructure_type == 'highway':
            return road.properties.get('traffic_capacity', 2000)
        else:  # regular road
            return 500  # Default capacity for regular roads
    
    def _generate_trips(self):
        """Generate trip patterns based on city zones."""
        self.trip_generators = []
        
        # Find residential zones (trip origins)
        residential_zones = []
        commercial_zones = []
        industrial_zones = []
        
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.get_cell(x, y)
                if isinstance(cell, Zone) and cell.development_level > 0:
                    if cell.zone_type == 'residential':
                        residential_zones.append((x, y, cell.development_level))
                    elif cell.zone_type == 'commercial':
                        commercial_zones.append((x, y, cell.development_level))
                    elif cell.zone_type == 'industrial':
                        industrial_zones.append((x, y, cell.development_level))
        
        # Generate commuting trips (residential to commercial/industrial)
        for res_x, res_y, res_level in residential_zones:
            population = res_level * 50  # 50 people per development level
            working_population = int(population * 0.6)  # 60% work
            
            # Distribute workers to nearby commercial and industrial zones
            job_zones = commercial_zones + industrial_zones
            if job_zones:
                for _ in range(working_population // 10):  # Group trips
                    # Find nearby job zone
                    job_zone = self._find_nearest_zone((res_x, res_y), job_zones)
                    if job_zone:
                        job_x, job_y, _ = job_zone
                        self.trip_generators.append(TripGenerator(
                            origin=(res_x, res_y),
                            destination=(job_x, job_y),
                            trip_type='commute',
                            volume=10  # 10 trips per generator
                        ))
        
        # Generate leisure trips (residential to commercial)
        for res_x, res_y, res_level in residential_zones:
            population = res_level * 50
            leisure_trips = int(population * 0.3)  # 30% make leisure trips
            
            if commercial_zones:
                for _ in range(leisure_trips // 15):  # Group leisure trips
                    # Random commercial destination
                    com_zone = random.choice(commercial_zones)
                    com_x, com_y, _ = com_zone
                    self.trip_generators.append(TripGenerator(
                        origin=(res_x, res_y),
                        destination=(com_x, com_y),
                        trip_type='leisure',
                        volume=15  # 15 trips per generator
                    ))
    
    def _find_nearest_zone(self, origin: Tuple[int, int], zones: List[Tuple[int, int, int]]) -> Tuple[int, int, int]:
        """Find the nearest zone to the origin."""
        if not zones:
            return None
        
        ox, oy = origin
        min_distance = float('inf')
        nearest_zone = None
        
        for zx, zy, level in zones:
            distance = ((ox - zx) ** 2 + (oy - zy) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                nearest_zone = (zx, zy, level)
        
        return nearest_zone
    
    def _calculate_traffic_flow(self):
        """Calculate traffic flow on road network."""
        # Initialize traffic data
        for pos in self.road_network:
            self.traffic_data[pos] = TrafficData(
                volume=0,
                capacity=self.road_network[pos]['capacity'],
                congestion_level=0.0,
                average_speed=50.0  # Default speed km/h
            )
        
        # Route trips through road network
        for trip in self.trip_generators:
            path = self._find_shortest_path(trip.origin, trip.destination)
            if path:
                # Add traffic volume to each road segment in path
                for road_pos in path:
                    if road_pos in self.traffic_data:
                        self.traffic_data[road_pos].volume += trip.volume
    
    def _find_shortest_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Find shortest path through road network using simple pathfinding."""
        # Find nearest road to start and end
        start_road = self._find_nearest_road(start)
        end_road = self._find_nearest_road(end)
        
        if not start_road or not end_road:
            return []
        
        # Simple BFS pathfinding
        queue = [(start_road, [start_road])]
        visited = set()
        
        while queue:
            current, path = queue.pop(0)
            
            if current == end_road:
                return path
            
            if current in visited:
                continue
            
            visited.add(current)
            
            if current in self.road_network:
                for neighbor in self.road_network[current]['connections']:
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))
        
        return []
    
    def _find_nearest_road(self, position: Tuple[int, int]) -> Tuple[int, int]:
        """Find the nearest road to a position."""
        px, py = position
        min_distance = float('inf')
        nearest_road = None
        
        for road_pos in self.road_network:
            rx, ry = road_pos
            distance = ((px - rx) ** 2 + (py - ry) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                nearest_road = road_pos
        
        return nearest_road
    
    def _update_congestion(self):
        """Update congestion levels and speeds based on traffic volume."""
        for pos, traffic in self.traffic_data.items():
            if traffic.capacity > 0:
                traffic.congestion_level = min(1.0, traffic.volume / traffic.capacity)
                
                # Speed decreases with congestion
                if traffic.congestion_level < 0.5:
                    traffic.average_speed = 50.0  # Free flow
                elif traffic.congestion_level < 0.8:
                    traffic.average_speed = 30.0  # Moderate congestion
                else:
                    traffic.average_speed = 15.0  # Heavy congestion
    
    def get_traffic_data(self, x: int, y: int) -> TrafficData:
        """Get traffic data for a specific position."""
        return self.traffic_data.get((x, y), TrafficData(0, 0, 0.0, 0.0))
    
    def get_congestion_color(self, x: int, y: int) -> str:
        """Get color representing traffic congestion level."""
        traffic = self.get_traffic_data(x, y)
        
        if traffic.congestion_level < 0.3:
            return '#90EE90'  # Light green - free flow
        elif traffic.congestion_level < 0.6:
            return '#FFD700'  # Yellow - moderate traffic
        elif traffic.congestion_level < 0.8:
            return '#FFA500'  # Orange - heavy traffic
        else:
            return '#FF4500'  # Red - severe congestion
    
    def get_traffic_statistics(self) -> Dict[str, float]:
        """Get overall traffic statistics."""
        if not self.traffic_data:
            return {'total_volume': 0, 'average_congestion': 0, 'total_roads': 0}
        
        total_volume = sum(traffic.volume for traffic in self.traffic_data.values())
        average_congestion = sum(traffic.congestion_level for traffic in self.traffic_data.values()) / len(self.traffic_data)
        
        return {
            'total_volume': total_volume,
            'average_congestion': average_congestion,
            'total_roads': len(self.traffic_data)
        }