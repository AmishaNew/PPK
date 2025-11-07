"""
Supply Chain System - Manages industrial logistics and cargo flow

Handles supply chains, cargo routing, and external connections.
"""

from typing import Dict, Set, Tuple, List
from dataclasses import dataclass
import random
from infrastructure import Infrastructure
from zone import Zone

@dataclass
class Commodity:
    """Represents a type of industrial commodity."""
    name: str
    production_rate: int  # Units per month per facility
    consumption_rate: int  # Units per month per facility
    transport_cost: float  # Cost per unit per distance

@dataclass
class SupplyRoute:
    """Represents a cargo route between facilities."""
    origin: Tuple[int, int]
    destination: Tuple[int, int]
    commodity: str
    volume: int  # Units per month
    transport_mode: str  # 'road', 'rail'

@dataclass
class ExternalConnection:
    """Represents connection to neighboring cities."""
    x: int
    y: int
    connection_type: str  # 'road', 'rail'
    import_capacity: int
    export_capacity: int

class SupplyChainSystem:
    """
    Manages industrial supply chains and cargo logistics.
    """
    
    def __init__(self, city):
        """Initialize the supply chain system."""
        self.city = city
        self.commodities = self._initialize_commodities()
        self.supply_routes = []
        self.external_connections = []
        self.cargo_traffic = {}  # Cargo volume on roads/rails
        
    def _initialize_commodities(self) -> Dict[str, Commodity]:
        """Initialize commodity types."""
        return {
            'raw_materials': Commodity('raw_materials', 100, 0, 2.0),
            'manufactured_goods': Commodity('manufactured_goods', 0, 80, 3.0),
            'consumer_goods': Commodity('consumer_goods', 50, 60, 1.5),
            'food': Commodity('food', 30, 40, 2.5)
        }
    
    def update_supply_chain(self):
        """Update the supply chain system."""
        self._find_external_connections()
        self._calculate_supply_demand()
        self._route_cargo()
        self._update_cargo_traffic()
    
    def _find_external_connections(self):
        """Find external connections at city edges."""
        self.external_connections = []
        
        # Check city edges for highways and rail connections
        for x in range(self.city.width):
            # Top and bottom edges
            for y in [0, self.city.height - 1]:
                cell = self.city.get_cell(x, y)
                if isinstance(cell, Infrastructure):
                    if cell.infrastructure_type == 'highway':
                        connection = ExternalConnection(
                            x=x, y=y, connection_type='road',
                            import_capacity=1000, export_capacity=1000
                        )
                        self.external_connections.append(connection)
        
        for y in range(self.city.height):
            # Left and right edges
            for x in [0, self.city.width - 1]:
                cell = self.city.get_cell(x, y)
                if isinstance(cell, Infrastructure):
                    if cell.infrastructure_type == 'highway':
                        connection = ExternalConnection(
                            x=x, y=y, connection_type='road',
                            import_capacity=1000, export_capacity=1000
                        )
                        self.external_connections.append(connection)
    
    def _calculate_supply_demand(self) -> Dict[str, Dict[str, int]]:
        """Calculate supply and demand for each commodity."""
        supply_demand = {}
        
        for commodity_name in self.commodities:
            supply_demand[commodity_name] = {'supply': 0, 'demand': 0, 'facilities': []}
        
        # Calculate from industrial zones
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.get_cell(x, y)
                if isinstance(cell, Zone) and cell.zone_type == 'industrial' and cell.development_level > 0:
                    # Different industrial zones produce/consume different commodities
                    facility_type = self._get_facility_type(x, y)
                    
                    if facility_type == 'raw_producer':
                        supply_demand['raw_materials']['supply'] += 100 * cell.development_level
                        supply_demand['raw_materials']['facilities'].append((x, y, 'producer'))
                    elif facility_type == 'manufacturer':
                        supply_demand['raw_materials']['demand'] += 80 * cell.development_level
                        supply_demand['manufactured_goods']['supply'] += 60 * cell.development_level
                        supply_demand['manufactured_goods']['facilities'].append((x, y, 'producer'))
                    elif facility_type == 'food_processor':
                        supply_demand['food']['supply'] += 50 * cell.development_level
                        supply_demand['food']['facilities'].append((x, y, 'producer'))
        
        # Calculate demand from commercial zones
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.get_cell(x, y)
                if isinstance(cell, Zone) and cell.zone_type == 'commercial' and cell.development_level > 0:
                    supply_demand['manufactured_goods']['demand'] += 40 * cell.development_level
                    supply_demand['consumer_goods']['demand'] += 30 * cell.development_level
                    supply_demand['food']['demand'] += 20 * cell.development_level
        
        return supply_demand
    
    def _get_facility_type(self, x: int, y: int) -> str:
        """Determine facility type based on location."""
        # Simple heuristic based on position
        if x < self.city.width // 3:
            return 'raw_producer'
        elif x < 2 * self.city.width // 3:
            return 'manufacturer'
        else:
            return 'food_processor'
    
    def _route_cargo(self):
        """Route cargo between supply and demand points."""
        self.supply_routes = []
        supply_demand = self._calculate_supply_demand()
        
        for commodity_name, data in supply_demand.items():
            producers = [f for f in data['facilities'] if f[2] == 'producer']
            
            # Route to internal demand (simplified)
            if data['demand'] > 0 and producers:
                for producer in producers:
                    # Find nearby commercial zones for delivery
                    commercial_zones = self._find_nearby_commercial(producer[0], producer[1])
                    
                    for com_x, com_y in commercial_zones[:2]:  # Limit to 2 destinations
                        route = SupplyRoute(
                            origin=(producer[0], producer[1]),
                            destination=(com_x, com_y),
                            commodity=commodity_name,
                            volume=min(50, data['supply'] // len(producers)),
                            transport_mode='road'
                        )
                        self.supply_routes.append(route)
            
            # Route to external connections for export
            if data['supply'] > data['demand'] and self.external_connections:
                surplus = data['supply'] - data['demand']
                for producer in producers:
                    if surplus > 0:
                        # Find nearest external connection
                        nearest_connection = self._find_nearest_connection(producer[0], producer[1])
                        if nearest_connection:
                            export_volume = min(surplus // len(producers), nearest_connection.export_capacity)
                            route = SupplyRoute(
                                origin=(producer[0], producer[1]),
                                destination=(nearest_connection.x, nearest_connection.y),
                                commodity=commodity_name,
                                volume=export_volume,
                                transport_mode=nearest_connection.connection_type
                            )
                            self.supply_routes.append(route)
                            surplus -= export_volume
    
    def _find_nearby_commercial(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Find commercial zones near an industrial facility."""
        commercial_zones = []
        
        for y2 in range(self.city.height):
            for x2 in range(self.city.width):
                cell = self.city.get_cell(x2, y2)
                if isinstance(cell, Zone) and cell.zone_type == 'commercial' and cell.development_level > 0:
                    distance = ((x - x2) ** 2 + (y - y2) ** 2) ** 0.5
                    if distance <= 10:  # Within reasonable distance
                        commercial_zones.append((x2, y2))
        
        # Sort by distance
        commercial_zones.sort(key=lambda pos: ((x - pos[0]) ** 2 + (y - pos[1]) ** 2) ** 0.5)
        return commercial_zones
    
    def _find_nearest_connection(self, x: int, y: int) -> ExternalConnection:
        """Find the nearest external connection."""
        if not self.external_connections:
            return None
        
        min_distance = float('inf')
        nearest = None
        
        for connection in self.external_connections:
            distance = ((x - connection.x) ** 2 + (y - connection.y) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                nearest = connection
        
        return nearest
    
    def _update_cargo_traffic(self):
        """Update cargo traffic on roads and rails."""
        self.cargo_traffic = {}
        
        for route in self.supply_routes:
            # Simple pathfinding for cargo routes
            path = self._find_cargo_path(route.origin, route.destination)
            
            for road_pos in path:
                if road_pos not in self.cargo_traffic:
                    self.cargo_traffic[road_pos] = 0
                
                # Convert monthly volume to hourly traffic
                hourly_volume = route.volume // (30 * 24)  # Monthly to hourly
                self.cargo_traffic[road_pos] += hourly_volume
    
    def _find_cargo_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Find path for cargo routing (simplified)."""
        # Use the traffic manager's road network if available
        if hasattr(self.city, 'traffic_manager'):
            return self.city.traffic_manager._find_shortest_path(start, end)
        
        # Fallback: direct line approximation
        path = []
        x1, y1 = start
        x2, y2 = end
        
        # Simple line drawing algorithm
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        x, y = x1, y1
        
        x_inc = 1 if x1 < x2 else -1
        y_inc = 1 if y1 < y2 else -1
        
        error = dx - dy
        
        while True:
            # Check if current position has a road
            cell = self.city.get_cell(x, y)
            if isinstance(cell, Infrastructure) and cell.infrastructure_type in ['road', 'highway']:
                path.append((x, y))
            
            if x == x2 and y == y2:
                break
            
            e2 = 2 * error
            if e2 > -dy:
                error -= dy
                x += x_inc
            if e2 < dx:
                error += dx
                y += y_inc
        
        return path
    
    def get_cargo_volume(self, x: int, y: int) -> int:
        """Get cargo volume at a specific position."""
        return self.cargo_traffic.get((x, y), 0)
    
    def get_supply_chain_efficiency(self) -> float:
        """Calculate overall supply chain efficiency."""
        if not self.supply_routes:
            return 0.0
        
        total_routes = len(self.supply_routes)
        successful_routes = sum(1 for route in self.supply_routes if route.volume > 0)
        
        return successful_routes / total_routes if total_routes > 0 else 0.0
    
    def get_supply_chain_statistics(self) -> Dict[str, any]:
        """Get supply chain statistics."""
        supply_demand = self._calculate_supply_demand()
        
        return {
            'total_routes': len(self.supply_routes),
            'external_connections': len(self.external_connections),
            'efficiency': self.get_supply_chain_efficiency(),
            'cargo_volume': sum(self.cargo_traffic.values()),
            'commodities': supply_demand
        }