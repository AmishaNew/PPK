"""
Utility Functions - Helper functions and constants for the city simulation

Contains commonly used functions, constants, and utility classes.
"""

import random
import math
from typing import List, Tuple, Dict, Any

# Game constants
GAME_CONSTANTS = {
    'MAX_POPULATION_PER_ZONE': 250,
    'MAX_JOBS_PER_COMMERCIAL': 150,
    'MAX_JOBS_PER_INDUSTRIAL': 200,
    'BASE_HAPPINESS': 50,
    'MAX_HAPPINESS': 100,
    'MIN_HAPPINESS': 0,
    'MAX_POLLUTION': 100,
    'MIN_POLLUTION': 0,
    'STARTING_MONEY': 100000,
    'POWER_PLANT_RADIUS': 10,
    'WATER_FACILITY_RADIUS': 8,
    'SCHOOL_RADIUS': 5,
    'HOSPITAL_RADIUS': 8,
    'POLICE_RADIUS': 12,
    'FIRE_RADIUS': 10,
    'PARK_RADIUS': 6
}

# Color palettes for different themes
COLOR_THEMES = {
    'default': {
        'empty': '#F5F5DC',      # Beige
        'residential': '#90EE90',  # Light green
        'commercial': '#87CEEB',   # Sky blue
        'industrial': '#F4A460',   # Sandy brown
        'road': '#696969',         # Dim gray
        'power': '#FFD700',        # Gold
        'water': '#00CED1',        # Dark turquoise
        'grid': '#CCCCCC',         # Light gray
        'border': '#000000'        # Black
    },
    'night': {
        'empty': '#2F2F2F',
        'residential': '#4F7F4F',
        'commercial': '#4F6F8F',
        'industrial': '#8F6F4F',
        'road': '#1F1F1F',
        'power': '#BFAF00',
        'water': '#007F8F',
        'grid': '#404040',
        'border': '#FFFFFF'
    },
    'colorblind': {
        'empty': '#F0F0F0',
        'residential': '#0072B2',
        'commercial': '#D55E00',
        'industrial': '#CC79A7',
        'road': '#999999',
        'power': '#F0E442',
        'water': '#56B4E9',
        'grid': '#DDDDDD',
        'border': '#000000'
    }
}

def calculate_distance(x1: int, y1: int, x2: int, y2: int) -> float:
    """
    Calculate Euclidean distance between two points.
    
    Args:
        x1, y1: First point coordinates
        x2, y2: Second point coordinates
    
    Returns:
        Distance as float
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def calculate_manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    """
    Calculate Manhattan distance between two points.
    
    Args:
        x1, y1: First point coordinates
        x2, y2: Second point coordinates
    
    Returns:
        Manhattan distance as integer
    """
    return abs(x2 - x1) + abs(y2 - y1)

def get_neighbors_in_radius(center_x: int, center_y: int, radius: int, 
                          width: int, height: int) -> List[Tuple[int, int]]:
    """
    Get all valid grid positions within a circular radius.
    
    Args:
        center_x, center_y: Center position
        radius: Search radius
        width, height: Grid bounds
    
    Returns:
        List of (x, y) coordinates within radius and bounds
    """
    neighbors = []
    
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            # Check if point is within circular radius
            if dx * dx + dy * dy <= radius * radius:
                x, y = center_x + dx, center_y + dy
                # Check if point is within grid bounds
                if 0 <= x < width and 0 <= y < height:
                    neighbors.append((x, y))
    
    return neighbors

def get_neighbors_in_square(center_x: int, center_y: int, radius: int,
                           width: int, height: int) -> List[Tuple[int, int]]:
    """
    Get all valid grid positions within a square radius.
    
    Args:
        center_x, center_y: Center position
        radius: Search radius (Manhattan distance)
        width, height: Grid bounds
    
    Returns:
        List of (x, y) coordinates within square radius and bounds
    """
    neighbors = []
    
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            x, y = center_x + dx, center_y + dy
            # Check if point is within grid bounds
            if 0 <= x < width and 0 <= y < height:
                neighbors.append((x, y))
    
    return neighbors

def interpolate_color(color1: str, color2: str, factor: float) -> str:
    """
    Interpolate between two hex colors.
    
    Args:
        color1: First color as hex string
        color2: Second color as hex string
        factor: Interpolation factor (0-1)
    
    Returns:
        Interpolated color as hex string
    """
    # Parse hex colors
    c1 = color1.lstrip('#')
    c2 = color2.lstrip('#')
    
    r1, g1, b1 = tuple(int(c1[i:i+2], 16) for i in (0, 2, 4))
    r2, g2, b2 = tuple(int(c2[i:i+2], 16) for i in (0, 2, 4))
    
    # Interpolate
    factor = max(0, min(1, factor))  # Clamp to 0-1
    r = int(r1 + (r2 - r1) * factor)
    g = int(g1 + (g2 - g1) * factor)
    b = int(b1 + (b2 - b1) * factor)
    
    return f"#{r:02x}{g:02x}{b:02x}"

def lighten_color(hex_color: str, factor: float) -> str:
    """
    Lighten a hex color by mixing with white.
    
    Args:
        hex_color: Color as hex string
        factor: Lightening factor (0-1)
    
    Returns:
        Lightened color as hex string
    """
    return interpolate_color(hex_color, '#FFFFFF', factor)

def darken_color(hex_color: str, factor: float) -> str:
    """
    Darken a hex color by mixing with black.
    
    Args:
        hex_color: Color as hex string
        factor: Darkening factor (0-1)
    
    Returns:
        Darkened color as hex string
    """
    return interpolate_color(hex_color, '#000000', factor)

def format_money(amount: int) -> str:
    """
    Format money amount with appropriate suffix.
    
    Args:
        amount: Money amount as integer
    
    Returns:
        Formatted string with K/M/B suffixes
    """
    if abs(amount) >= 1_000_000_000:
        return f"${amount / 1_000_000_000:.1f}B"
    elif abs(amount) >= 1_000_000:
        return f"${amount / 1_000_000:.1f}M"
    elif abs(amount) >= 1_000:
        return f"${amount / 1_000:.1f}K"
    else:
        return f"${amount:,}"

def format_percentage(value: float) -> str:
    """
    Format a percentage value.
    
    Args:
        value: Value as float (0-100)
    
    Returns:
        Formatted percentage string
    """
    return f"{value:.1f}%"

def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Clamp a value between min and max bounds.
    
    Args:
        value: Value to clamp
        min_value: Minimum bound
        max_value: Maximum bound
    
    Returns:
        Clamped value
    """
    return max(min_value, min(max_value, value))

def weighted_random_choice(choices: List[Tuple[Any, float]]) -> Any:
    """
    Make a weighted random choice from a list of (item, weight) tuples.
    
    Args:
        choices: List of (item, weight) tuples
    
    Returns:
        Randomly selected item based on weights
    """
    if not choices:
        return None
    
    total_weight = sum(weight for _, weight in choices)
    if total_weight <= 0:
        return random.choice([item for item, _ in choices])
    
    r = random.uniform(0, total_weight)
    cumulative_weight = 0
    
    for item, weight in choices:
        cumulative_weight += weight
        if r <= cumulative_weight:
            return item
    
    # Fallback to last item (shouldn't happen with proper weights)
    return choices[-1][0]

def smooth_transition(current: float, target: float, factor: float) -> float:
    """
    Create a smooth transition between current and target values.
    
    Args:
        current: Current value
        target: Target value
        factor: Transition factor (0-1, higher = faster transition)
    
    Returns:
        New value between current and target
    """
    return current + (target - current) * factor

def calculate_service_coverage(buildings: List[Tuple[int, int, int]], 
                             position: Tuple[int, int]) -> float:
    """
    Calculate service coverage at a position from multiple service buildings.
    
    Args:
        buildings: List of (x, y, radius) tuples for service buildings
        position: (x, y) position to check coverage
    
    Returns:
        Coverage strength (0-1)
    """
    if not buildings:
        return 0.0
    
    px, py = position
    total_coverage = 0.0
    
    for bx, by, radius in buildings:
        distance = calculate_distance(px, py, bx, by)
        if distance <= radius:
            # Linear falloff within radius
            strength = max(0, 1.0 - (distance / radius))
            total_coverage = min(1.0, total_coverage + strength)
    
    return total_coverage

def generate_city_name() -> str:
    """
    Generate a random city name.
    
    Returns:
        Random city name as string
    """
    prefixes = [
        "New", "Old", "North", "South", "East", "West", "Upper", "Lower",
        "Great", "Little", "Big", "Small", "High", "Deep", "Broad", "Long"
    ]
    
    roots = [
        "Spring", "River", "Hill", "Valley", "Lake", "Creek", "Ridge", "Grove",
        "Field", "Wood", "Stone", "Gold", "Silver", "Green", "Blue", "Red",
        "White", "Black", "Sun", "Moon", "Star", "Dawn", "Dusk", "Harbor",
        "Bay", "Port", "Bridge", "Cross", "Gate", "Peak", "Mesa", "Falls"
    ]
    
    suffixes = [
        "ville", "town", "city", "burg", "ford", "ham", "ton", "field",
        "wood", "haven", "port", "dale", "glen", "brook", "mount", "view",
        "side", "land", "shire", "worth"
    ]
    
    # Choose components
    use_prefix = random.random() < 0.4
    
    if use_prefix:
        prefix = random.choice(prefixes)
        root = random.choice(roots)
        suffix = random.choice(suffixes) if random.random() < 0.7 else ""
        
        if suffix:
            return f"{prefix} {root}{suffix}"
        else:
            return f"{prefix} {root}"
    else:
        root = random.choice(roots)
        suffix = random.choice(suffixes)
        return f"{root}{suffix}"

class EventLogger:
    """
    Simple event logging system for tracking game events.
    """
    
    def __init__(self, max_events: int = 100):
        """
        Initialize event logger.
        
        Args:
            max_events: Maximum number of events to keep
        """
        self.events = []
        self.max_events = max_events
    
    def log_event(self, event_type: str, message: str, data: Dict[str, Any] = None):
        """
        Log a game event.
        
        Args:
            event_type: Type of event (e.g., 'construction', 'disaster', 'economic')
            message: Human-readable message
            data: Additional event data
        """
        event = {
            'type': event_type,
            'message': message,
            'data': data or {},
            'timestamp': len(self.events)  # Simple timestamp
        }
        
        self.events.append(event)
        
        # Remove old events if we exceed the limit
        if len(self.events) > self.max_events:
            self.events.pop(0)
    
    def get_recent_events(self, count: int = 10) -> List[Dict[str, Any]]:
        """
        Get the most recent events.
        
        Args:
            count: Number of events to return
        
        Returns:
            List of recent events
        """
        return self.events[-count:] if self.events else []
    
    def get_events_by_type(self, event_type: str) -> List[Dict[str, Any]]:
        """
        Get all events of a specific type.
        
        Args:
            event_type: Type of event to filter by
        
        Returns:
            List of matching events
        """
        return [event for event in self.events if event['type'] == event_type]
    
    def clear_events(self):
        """Clear all logged events."""
        self.events.clear()

class PerformanceMonitor:
    """
    Simple performance monitoring for the simulation.
    """
    
    def __init__(self):
        """Initialize performance monitor."""
        self.metrics = {}
        self.start_times = {}
    
    def start_timer(self, name: str):
        """
        Start a named timer.
        
        Args:
            name: Timer name
        """
        import time
        self.start_times[name] = time.time()
    
    def end_timer(self, name: str):
        """
        End a named timer and record the elapsed time.
        
        Args:
            name: Timer name
        """
        if name in self.start_times:
            import time
            elapsed = time.time() - self.start_times[name]
            
            if name not in self.metrics:
                self.metrics[name] = []
            
            self.metrics[name].append(elapsed)
            
            # Keep only recent measurements
            if len(self.metrics[name]) > 100:
                self.metrics[name].pop(0)
            
            del self.start_times[name]
    
    def get_average_time(self, name: str) -> float:
        """
        Get average time for a named timer.
        
        Args:
            name: Timer name
        
        Returns:
            Average time in seconds
        """
        if name in self.metrics and self.metrics[name]:
            return sum(self.metrics[name]) / len(self.metrics[name])
        return 0.0
    
    def get_performance_report(self) -> str:
        """
        Get a formatted performance report.
        
        Returns:
            Performance report as string
        """
        if not self.metrics:
            return "No performance data available."
        
        report = "Performance Report:\n"
        report += "=" * 20 + "\n"
        
        for name, times in self.metrics.items():
            if times:
                avg_time = sum(times) / len(times)
                max_time = max(times)
                min_time = min(times)
                
                report += f"{name}:\n"
                report += f"  Average: {avg_time * 1000:.2f} ms\n"
                report += f"  Min: {min_time * 1000:.2f} ms\n"
                report += f"  Max: {max_time * 1000:.2f} ms\n"
                report += f"  Samples: {len(times)}\n\n"
        
        return report
