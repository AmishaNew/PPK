"""
Land Valuation System - Calculates dynamic property values

Determines land values based on proximity to services, transportation, and amenities.
"""

from typing import Dict, Tuple
from dataclasses import dataclass
from infrastructure import Infrastructure
from zone import Zone
import math

@dataclass
class ValuationFactors:
    """Factors affecting land valuation."""
    transportation_access: float  # 0.0 to 1.0
    service_proximity: float  # 0.0 to 1.0
    safety_level: float  # 0.0 to 1.0
    environmental_quality: float  # 0.0 to 1.0
    economic_activity: float  # 0.0 to 1.0

class LandValuationSystem:
    """
    Manages dynamic land valuation based on city conditions.
    """
    
    def __init__(self, city):
        """Initialize the land valuation system."""
        self.city = city
        self.land_values = {}  # Position -> value
        self.base_value = 1000  # Base land value per tile
        
    def calculate_land_values(self):
        """Calculate land values for all positions."""
        self.land_values = {}
        
        for y in range(self.city.height):
            for x in range(self.city.width):
                factors = self._calculate_valuation_factors(x, y)
                value = self._calculate_property_value(factors)
                self.land_values[(x, y)] = value
    
    def _calculate_valuation_factors(self, x: int, y: int) -> ValuationFactors:
        """Calculate all factors affecting land value at a position."""
        
        # Transportation access factor
        transport_factor = self._calculate_transportation_factor(x, y)
        
        # Service proximity factor
        service_factor = self._calculate_service_factor(x, y)
        
        # Safety level factor
        safety_factor = self._calculate_safety_factor(x, y)
        
        # Environmental quality factor
        environment_factor = self._calculate_environment_factor(x, y)
        
        # Economic activity factor
        economic_factor = self._calculate_economic_factor(x, y)
        
        return ValuationFactors(
            transportation_access=transport_factor,
            service_proximity=service_factor,
            safety_level=safety_factor,
            environmental_quality=environment_factor,
            economic_activity=economic_factor
        )
    
    def _calculate_transportation_factor(self, x: int, y: int) -> float:
        """Calculate transportation access factor."""
        score = 0.0
        
        # Road access
        road_distance = self._find_nearest_infrastructure_distance(x, y, ['road', 'highway'])
        if road_distance <= 2:
            score += 0.3
        elif road_distance <= 5:
            score += 0.2
        elif road_distance <= 10:
            score += 0.1
        
        # Transit access
        if hasattr(self.city, 'transit_system'):
            if self.city.transit_system.has_transit_access(x, y):
                score += 0.4
        
        # Highway access bonus
        highway_distance = self._find_nearest_infrastructure_distance(x, y, ['highway'])
        if highway_distance <= 3:
            score += 0.3
        
        return min(1.0, score)
    
    def _calculate_service_factor(self, x: int, y: int) -> float:
        """Calculate proximity to services factor."""
        score = 0.0
        
        # Schools
        school_distance = self._find_nearest_infrastructure_distance(x, y, ['school'])
        if school_distance <= 5:
            score += 0.25
        elif school_distance <= 10:
            score += 0.15
        
        # Hospitals
        hospital_distance = self._find_nearest_infrastructure_distance(x, y, ['hospital'])
        if hospital_distance <= 8:
            score += 0.25
        elif hospital_distance <= 15:
            score += 0.15
        
        # Parks
        park_distance = self._find_nearest_infrastructure_distance(x, y, ['park'])
        if park_distance <= 3:
            score += 0.2
        elif park_distance <= 6:
            score += 0.1
        
        # Commercial zones
        commercial_distance = self._find_nearest_zone_distance(x, y, 'commercial')
        if commercial_distance <= 5:
            score += 0.3
        elif commercial_distance <= 10:
            score += 0.2
        
        return min(1.0, score)
    
    def _calculate_safety_factor(self, x: int, y: int) -> float:
        """Calculate safety level factor."""
        # Base safety level
        safety = 0.5
        
        # Police station proximity
        police_distance = self._find_nearest_infrastructure_distance(x, y, ['police_station'])
        if police_distance <= 5:
            safety += 0.4
        elif police_distance <= 10:
            safety += 0.2
        elif police_distance <= 15:
            safety += 0.1
        
        # Fire station proximity
        fire_distance = self._find_nearest_infrastructure_distance(x, y, ['fire_station'])
        if fire_distance <= 8:
            safety += 0.1
        
        return min(1.0, safety)
    
    def _calculate_environment_factor(self, x: int, y: int) -> float:
        """Calculate environmental quality factor."""
        score = 0.8  # Base environmental score
        
        # Pollution from industrial zones
        industrial_pollution = 0
        for dy in range(-5, 6):
            for dx in range(-5, 6):
                nx, ny = x + dx, y + dy
                if self.city.is_valid_position(nx, ny):
                    cell = self.city.get_cell(nx, ny)
                    if isinstance(cell, Zone) and cell.zone_type == 'industrial':
                        distance = (dx * dx + dy * dy) ** 0.5
                        if distance > 0:
                            pollution_impact = cell.development_level / distance
                            industrial_pollution += pollution_impact
        
        # Reduce score based on pollution
        score -= min(0.6, industrial_pollution * 0.1)
        
        # Parks improve environment
        park_distance = self._find_nearest_infrastructure_distance(x, y, ['park'])
        if park_distance <= 3:
            score += 0.2
        elif park_distance <= 6:
            score += 0.1
        
        return max(0.0, min(1.0, score))
    
    def _calculate_economic_factor(self, x: int, y: int) -> float:
        """Calculate economic activity factor."""
        score = 0.0
        
        # Nearby commercial activity
        commercial_activity = 0
        for dy in range(-8, 9):
            for dx in range(-8, 9):
                nx, ny = x + dx, y + dy
                if self.city.is_valid_position(nx, ny):
                    cell = self.city.get_cell(nx, ny)
                    if isinstance(cell, Zone) and cell.zone_type == 'commercial':
                        distance = max(1, (dx * dx + dy * dy) ** 0.5)
                        activity = cell.development_level / distance
                        commercial_activity += activity
        
        score += min(0.6, commercial_activity * 0.1)
        
        # Employment opportunities (industrial zones)
        industrial_jobs = 0
        for dy in range(-10, 11):
            for dx in range(-10, 11):
                nx, ny = x + dx, y + dy
                if self.city.is_valid_position(nx, ny):
                    cell = self.city.get_cell(nx, ny)
                    if isinstance(cell, Zone) and cell.zone_type == 'industrial':
                        distance = max(1, (dx * dx + dy * dy) ** 0.5)
                        jobs = cell.development_level / distance
                        industrial_jobs += jobs
        
        score += min(0.4, industrial_jobs * 0.05)
        
        return min(1.0, score)
    
    def _find_nearest_infrastructure_distance(self, x: int, y: int, infrastructure_types: list) -> float:
        """Find distance to nearest infrastructure of given types."""
        min_distance = float('inf')
        
        for y2 in range(self.city.height):
            for x2 in range(self.city.width):
                cell = self.city.get_cell(x2, y2)
                if isinstance(cell, Infrastructure) and cell.infrastructure_type in infrastructure_types:
                    distance = ((x - x2) ** 2 + (y - y2) ** 2) ** 0.5
                    min_distance = min(min_distance, distance)
        
        return min_distance if min_distance != float('inf') else 999
    
    def _find_nearest_zone_distance(self, x: int, y: int, zone_type: str) -> float:
        """Find distance to nearest zone of given type."""
        min_distance = float('inf')
        
        for y2 in range(self.city.height):
            for x2 in range(self.city.width):
                cell = self.city.get_cell(x2, y2)
                if isinstance(cell, Zone) and cell.zone_type == zone_type and cell.development_level > 0:
                    distance = ((x - x2) ** 2 + (y - y2) ** 2) ** 0.5
                    min_distance = min(min_distance, distance)
        
        return min_distance if min_distance != float('inf') else 999
    
    def _calculate_property_value(self, factors: ValuationFactors) -> float:
        """Calculate final property value based on factors."""
        # Weighted combination of factors
        weights = {
            'transportation': 0.25,
            'services': 0.20,
            'safety': 0.20,
            'environment': 0.20,
            'economic': 0.15
        }
        
        weighted_score = (
            factors.transportation_access * weights['transportation'] +
            factors.service_proximity * weights['services'] +
            factors.safety_level * weights['safety'] +
            factors.environmental_quality * weights['environment'] +
            factors.economic_activity * weights['economic']
        )
        
        # Apply multiplier to base value
        multiplier = 0.5 + (weighted_score * 2.0)  # Range: 0.5x to 2.5x base value
        return self.base_value * multiplier
    
    def get_land_value(self, x: int, y: int) -> float:
        """Get land value at specific position."""
        return self.land_values.get((x, y), self.base_value)
    
    def get_tax_multiplier(self, x: int, y: int) -> float:
        """Get tax multiplier based on land value."""
        value = self.get_land_value(x, y)
        base_multiplier = value / self.base_value
        return max(0.5, min(3.0, base_multiplier))  # Clamp between 0.5x and 3.0x
    
    def get_development_probability_modifier(self, x: int, y: int) -> float:
        """Get development probability modifier based on land value."""
        value = self.get_land_value(x, y)
        if value > self.base_value * 1.5:
            return 1.5  # High-value areas develop faster
        elif value > self.base_value * 1.2:
            return 1.2
        elif value < self.base_value * 0.8:
            return 0.7  # Low-value areas develop slower
        else:
            return 1.0
    
    def get_value_color(self, x: int, y: int) -> str:
        """Get color representing land value."""
        value = self.get_land_value(x, y)
        ratio = value / self.base_value
        
        if ratio >= 2.0:
            return '#8B0000'  # Dark red - very high value
        elif ratio >= 1.5:
            return '#FF4500'  # Orange red - high value
        elif ratio >= 1.2:
            return '#FFD700'  # Gold - above average
        elif ratio >= 0.8:
            return '#90EE90'  # Light green - average
        else:
            return '#87CEEB'  # Sky blue - below average
    
    def get_valuation_statistics(self) -> Dict[str, float]:
        """Get land valuation statistics."""
        if not self.land_values:
            return {'average_value': self.base_value, 'min_value': self.base_value, 'max_value': self.base_value}
        
        values = list(self.land_values.values())
        return {
            'average_value': sum(values) / len(values),
            'min_value': min(values),
            'max_value': max(values),
            'total_positions': len(values)
        }