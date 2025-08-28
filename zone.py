"""
Zone Class - Represents zoned areas in the city

Handles residential, commercial, and industrial zones with development progression.
"""

from typing import Dict, Any
import random

class Zone:
    """
    Represents a zoned area that can develop over time based on city conditions.
    """
    
    # Zone types and their characteristics
    ZONE_TYPES = {
        'residential': {
            'color': '#90EE90',  # Light green
            'max_development': 5,
            'population_per_level': 50,
            'power_required': True,
            'water_required': True
        },
        'commercial': {
            'color': '#87CEEB',  # Sky blue
            'max_development': 4,
            'jobs_per_level': 30,
            'power_required': True,
            'water_required': False
        },
        'industrial': {
            'color': '#F4A460',  # Sandy brown
            'max_development': 4,
            'jobs_per_level': 40,
            'pollution_per_level': 5,
            'power_required': True,
            'water_required': False
        }
    }
    
    def __init__(self, x: int, y: int, zone_type: str):
        """
        Initialize a new zone.
        
        Args:
            x, y: Grid coordinates
            zone_type: 'residential', 'commercial', or 'industrial'
        """
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.development_level = 0  # 0 = undeveloped, max varies by type
        self.last_growth_check = 0  # Game time when last checked for growth
        
        # Validate zone type
        if zone_type not in self.ZONE_TYPES:
            raise ValueError(f"Invalid zone type: {zone_type}")
        
        self.properties = self.ZONE_TYPES[zone_type].copy()
    
    def get_color(self) -> str:
        """Get the display color for this zone type."""
        if self.development_level == 0:
            # Undeveloped zones are lighter
            base_color = self.properties['color']
            return self._lighten_color(base_color, 0.5)
        return self.properties['color']
    
    def _lighten_color(self, hex_color: str, factor: float) -> str:
        """Lighten a hex color by the given factor (0-1)."""
        # Simple color lightening - mix with white
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Mix with white
        r = int(r + (255 - r) * factor)
        g = int(g + (255 - g) * factor)
        b = int(b + (255 - b) * factor)
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def can_develop(self, city) -> bool:
        """
        Check if this zone can develop further.
        
        Args:
            city: City instance to check requirements against
        
        Returns:
            True if zone can develop
        """
        # Check if already at max development
        if self.development_level >= self.properties['max_development']:
            return False
        
        # Check power requirement
        if self.properties.get('power_required', False):
            if (self.x, self.y) not in city.power_coverage:
                return False
        
        # Check water requirement
        if self.properties.get('water_required', False):
            if (self.x, self.y) not in city.water_coverage:
                return False
        
        # Check for road access (zones need road connection)
        has_road_access = False
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = self.x + dx, self.y + dy
            if (nx, ny) in city.road_network:
                has_road_access = True
                break
        
        if not has_road_access:
            return False
        
        # Zone-specific requirements
        if self.zone_type == 'residential':
            # Residential needs low pollution and some commercial nearby
            return self._check_residential_requirements(city)
        elif self.zone_type == 'commercial':
            # Commercial needs population nearby
            return self._check_commercial_requirements(city)
        elif self.zone_type == 'industrial':
            # Industrial just needs basic infrastructure
            return True
        
        return False
    
    def _check_residential_requirements(self, city) -> bool:
        """Check specific requirements for residential development."""
        # Check local pollution level
        local_pollution = 0
        neighbors = city.get_neighbors(self.x, self.y, radius=3)
        
        for nx, ny, cell in neighbors:
            if hasattr(cell, 'zone_type') and cell.zone_type == 'industrial':
                local_pollution += cell.development_level * 2
        
        if local_pollution > 10:  # Too much pollution
            return False
        
        # Check for commercial zones nearby (for jobs/shopping)
        commercial_nearby = 0
        for nx, ny, cell in neighbors:
            if hasattr(cell, 'zone_type') and cell.zone_type == 'commercial':
                commercial_nearby += 1
        
        # Need at least some commercial development or be in early game
        return commercial_nearby > 0 or city.population < 1000
    
    def _check_commercial_requirements(self, city) -> bool:
        """Check specific requirements for commercial development."""
        # Commercial needs population nearby to serve
        population_nearby = 0
        neighbors = city.get_neighbors(self.x, self.y, radius=5)
        
        for nx, ny, cell in neighbors:
            if hasattr(cell, 'zone_type') and cell.zone_type == 'residential':
                population_nearby += cell.development_level * 50
        
        # Need at least 200 people in the area to support development
        return population_nearby >= 200
    
    def attempt_development(self, city, growth_rate: float = 0.1) -> bool:
        """
        Attempt to develop this zone based on current conditions.
        
        Args:
            city: City instance
            growth_rate: Base probability of growth per attempt
        
        Returns:
            True if zone developed this turn
        """
        if not self.can_develop(city):
            return False
        
        # Calculate actual growth probability based on conditions
        actual_rate = growth_rate
        
        # Happiness affects growth rate
        happiness_modifier = (city.happiness - 50) / 100  # -0.5 to +0.5
        actual_rate += happiness_modifier * 0.05
        
        # Employment affects residential growth
        if self.zone_type == 'residential':
            employment_modifier = (city.employment_rate - 0.5) * 0.1
            actual_rate += employment_modifier
        
        # Money affects all growth (wealthy cities grow faster)
        if city.money > 50000:
            actual_rate += 0.02
        elif city.money < 10000:
            actual_rate -= 0.02
        
        # Random development check
        if random.random() < actual_rate:
            self.development_level += 1
            return True
        
        return False
    
    def get_info(self) -> Dict[str, Any]:
        """Get detailed information about this zone."""
        info = {
            'type': 'zone',
            'zone_type': self.zone_type,
            'development_level': self.development_level,
            'max_development': self.properties['max_development'],
            'position': (self.x, self.y)
        }
        
        # Add zone-specific info
        if self.zone_type == 'residential':
            info['population'] = self.development_level * self.properties['population_per_level']
        elif self.zone_type in ['commercial', 'industrial']:
            info['jobs'] = self.development_level * self.properties['jobs_per_level']
        
        if self.zone_type == 'industrial':
            info['pollution'] = self.development_level * self.properties['pollution_per_level']
        
        return info
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert zone to dictionary for saving."""
        return {
            'type': 'zone',
            'zone_type': self.zone_type,
            'development_level': self.development_level,
            'x': self.x,
            'y': self.y
        }
    
    def __str__(self) -> str:
        """String representation of the zone."""
        return f"{self.zone_type.capitalize()} Zone (Level {self.development_level})"
