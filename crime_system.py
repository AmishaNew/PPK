"""
Crime System - Simulates crime generation and police response

Calculates crime rates based on city conditions and police coverage.
"""

from typing import Dict, Tuple
from dataclasses import dataclass
from infrastructure import Infrastructure
from zone import Zone
import random

@dataclass
class CrimeData:
    """Crime statistics for a location."""
    crime_rate: float  # Crimes per 1000 residents per year
    crime_types: Dict[str, float]  # Breakdown by crime type
    police_response_time: float  # Minutes
    safety_index: float  # 0.0 to 1.0

class CrimeSystem:
    """
    Manages crime simulation and public safety.
    """
    
    def __init__(self, city):
        """Initialize the crime system."""
        self.city = city
        self.crime_data = {}  # Position -> CrimeData
        self.police_coverage = {}  # Position -> coverage strength
        self.base_crime_rate = 50  # Base crimes per 1000 residents per year
        
    def update_crime_system(self):
        """Update the crime system."""
        self._calculate_police_coverage()
        self._calculate_crime_rates()
        self._update_safety_indices()
    
    def _calculate_police_coverage(self):
        """Calculate police coverage across the city."""
        self.police_coverage = {}
        
        # Initialize all positions with no coverage
        for y in range(self.city.height):
            for x in range(self.city.width):
                self.police_coverage[(x, y)] = 0.0
        
        # Add coverage from police stations
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.get_cell(x, y)
                if isinstance(cell, Infrastructure) and cell.infrastructure_type == 'police_station':
                    coverage_radius = cell.properties.get('safety_range', 12)
                    self._add_police_coverage(x, y, coverage_radius)
    
    def _add_police_coverage(self, station_x: int, station_y: int, radius: int):
        """Add police coverage around a police station."""
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                distance = (dx * dx + dy * dy) ** 0.5
                if distance <= radius:
                    coverage_x = station_x + dx
                    coverage_y = station_y + dy
                    
                    if self.city.is_valid_position(coverage_x, coverage_y):
                        # Coverage strength decreases with distance
                        strength = max(0, 1.0 - (distance / radius))
                        current_coverage = self.police_coverage.get((coverage_x, coverage_y), 0.0)
                        # Multiple stations can overlap (additive up to 1.0)
                        self.police_coverage[(coverage_x, coverage_y)] = min(1.0, current_coverage + strength)
    
    def _calculate_crime_rates(self):
        """Calculate crime rates for all positions."""
        self.crime_data = {}
        
        for y in range(self.city.height):
            for x in range(self.city.width):
                crime_rate = self._calculate_base_crime_rate(x, y)
                crime_types = self._calculate_crime_breakdown(x, y, crime_rate)
                response_time = self._calculate_response_time(x, y)
                
                self.crime_data[(x, y)] = CrimeData(
                    crime_rate=crime_rate,
                    crime_types=crime_types,
                    police_response_time=response_time,
                    safety_index=0.0  # Will be calculated later
                )
    
    def _calculate_base_crime_rate(self, x: int, y: int) -> float:
        """Calculate base crime rate for a position."""
        crime_rate = self.base_crime_rate
        
        # Population density factor
        population_density = self._get_local_population_density(x, y)
        if population_density > 500:
            crime_rate *= 1.5  # High density increases crime
        elif population_density > 200:
            crime_rate *= 1.2
        elif population_density < 50:
            crime_rate *= 0.7  # Low density reduces crime
        
        # Economic factors
        unemployment_factor = self._get_local_unemployment_factor(x, y)
        crime_rate *= (1.0 + unemployment_factor)
        
        # Land value factor (higher value = lower crime)
        if hasattr(self.city, 'land_valuation'):
            land_value = self.city.land_valuation.get_land_value(x, y)
            base_value = self.city.land_valuation.base_value
            value_ratio = land_value / base_value
            
            if value_ratio > 1.5:
                crime_rate *= 0.6  # High-value areas have less crime
            elif value_ratio > 1.2:
                crime_rate *= 0.8
            elif value_ratio < 0.8:
                crime_rate *= 1.3  # Low-value areas have more crime
        
        # Police coverage factor
        police_coverage = self.police_coverage.get((x, y), 0.0)
        crime_reduction = police_coverage * 0.7  # Up to 70% reduction
        crime_rate *= (1.0 - crime_reduction)
        
        # Industrial areas have different crime patterns
        cell = self.city.get_cell(x, y)
        if isinstance(cell, Zone) and cell.zone_type == 'industrial':
            crime_rate *= 0.8  # Industrial areas typically have less street crime
        
        return max(5.0, crime_rate)  # Minimum crime rate
    
    def _get_local_population_density(self, x: int, y: int) -> int:
        """Get population density in the local area."""
        population = 0
        area_count = 0
        
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                nx, ny = x + dx, y + dy
                if self.city.is_valid_position(nx, ny):
                    cell = self.city.get_cell(nx, ny)
                    if isinstance(cell, Zone) and cell.zone_type == 'residential':
                        population += cell.development_level * 50
                    area_count += 1
        
        return population // max(1, area_count) if area_count > 0 else 0
    
    def _get_local_unemployment_factor(self, x: int, y: int) -> float:
        """Get local unemployment factor (0.0 to 1.0)."""
        # Simplified: areas far from commercial/industrial have higher unemployment
        min_job_distance = float('inf')
        
        for y2 in range(self.city.height):
            for x2 in range(self.city.width):
                cell = self.city.get_cell(x2, y2)
                if isinstance(cell, Zone) and cell.zone_type in ['commercial', 'industrial'] and cell.development_level > 0:
                    distance = ((x - x2) ** 2 + (y - y2) ** 2) ** 0.5
                    min_job_distance = min(min_job_distance, distance)
        
        if min_job_distance == float('inf'):
            return 0.5  # No jobs available
        elif min_job_distance > 15:
            return 0.4  # Far from jobs
        elif min_job_distance > 10:
            return 0.2
        else:
            return 0.0  # Close to jobs
    
    def _calculate_crime_breakdown(self, x: int, y: int, total_crime_rate: float) -> Dict[str, float]:
        """Calculate breakdown of crime types."""
        # Base distribution
        breakdown = {
            'theft': 0.4,
            'vandalism': 0.25,
            'assault': 0.15,
            'burglary': 0.12,
            'drug_related': 0.08
        }
        
        # Adjust based on area type
        cell = self.city.get_cell(x, y)
        if isinstance(cell, Zone):
            if cell.zone_type == 'commercial':
                breakdown['theft'] += 0.1
                breakdown['vandalism'] -= 0.05
                breakdown['burglary'] -= 0.05
            elif cell.zone_type == 'industrial':
                breakdown['vandalism'] += 0.1
                breakdown['theft'] -= 0.05
                breakdown['assault'] -= 0.05
        
        # Convert to actual numbers
        return {crime_type: total_crime_rate * ratio for crime_type, ratio in breakdown.items()}
    
    def _calculate_response_time(self, x: int, y: int) -> float:
        """Calculate police response time in minutes."""
        base_response_time = 15.0  # 15 minutes base
        
        # Find nearest police station
        min_distance = float('inf')
        for y2 in range(self.city.height):
            for x2 in range(self.city.width):
                cell = self.city.get_cell(x2, y2)
                if isinstance(cell, Infrastructure) and cell.infrastructure_type == 'police_station':
                    distance = ((x - x2) ** 2 + (y - y2) ** 2) ** 0.5
                    min_distance = min(min_distance, distance)
        
        if min_distance == float('inf'):
            return 60.0  # No police stations
        
        # Response time increases with distance
        response_time = base_response_time + (min_distance * 0.5)
        
        # Traffic affects response time
        if hasattr(self.city, 'traffic_manager'):
            # Simplified: high traffic areas have slower response
            traffic_data = self.city.traffic_manager.get_traffic_data(x, y)
            if traffic_data.congestion_level > 0.7:
                response_time *= 1.5
            elif traffic_data.congestion_level > 0.4:
                response_time *= 1.2
        
        return min(60.0, response_time)  # Cap at 60 minutes
    
    def _update_safety_indices(self):
        """Update safety indices for all positions."""
        for position, crime_data in self.crime_data.items():
            # Safety index based on crime rate and police response
            base_safety = max(0, 1.0 - (crime_data.crime_rate / 200.0))  # Normalize crime rate
            
            # Police coverage improves safety
            police_coverage = self.police_coverage.get(position, 0.0)
            safety_bonus = police_coverage * 0.3
            
            # Response time affects safety
            response_factor = max(0, 1.0 - (crime_data.police_response_time / 60.0))
            safety_bonus += response_factor * 0.2
            
            final_safety = min(1.0, base_safety + safety_bonus)
            crime_data.safety_index = final_safety
    
    def get_crime_rate(self, x: int, y: int) -> float:
        """Get crime rate at specific position."""
        crime_data = self.crime_data.get((x, y))
        return crime_data.crime_rate if crime_data else self.base_crime_rate
    
    def get_safety_level(self, x: int, y: int) -> float:
        """Get safety level at specific position (0.0 to 1.0)."""
        crime_data = self.crime_data.get((x, y))
        return crime_data.safety_index if crime_data else 0.5
    
    def get_police_coverage(self, x: int, y: int) -> float:
        """Get police coverage at specific position."""
        return self.police_coverage.get((x, y), 0.0)
    
    def get_crime_color(self, x: int, y: int) -> str:
        """Get color representing crime level."""
        safety = self.get_safety_level(x, y)
        
        if safety >= 0.8:
            return '#90EE90'  # Light green - very safe
        elif safety >= 0.6:
            return '#FFD700'  # Gold - moderately safe
        elif safety >= 0.4:
            return '#FFA500'  # Orange - some risk
        elif safety >= 0.2:
            return '#FF6347'  # Tomato - high risk
        else:
            return '#8B0000'  # Dark red - very dangerous
    
    def get_crime_statistics(self) -> Dict[str, float]:
        """Get overall crime statistics."""
        if not self.crime_data:
            return {'average_crime_rate': self.base_crime_rate, 'average_safety': 0.5, 'police_coverage': 0.0}
        
        total_crime = sum(data.crime_rate for data in self.crime_data.values())
        total_safety = sum(data.safety_index for data in self.crime_data.values())
        total_coverage = sum(self.police_coverage.values())
        
        num_positions = len(self.crime_data)
        
        return {
            'average_crime_rate': total_crime / num_positions,
            'average_safety': total_safety / num_positions,
            'police_coverage_percentage': (total_coverage / (self.city.width * self.city.height)) * 100,
            'total_positions': num_positions
        }