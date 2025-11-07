#!/usr/bin/env python3
"""
Test script for transportation and power systems

This script creates a test city and demonstrates the new features:
- Power grid with power plants and power lines
- Traffic calculation based on commuting patterns
- Visual indicators for power coverage and traffic flow
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from city import City
from infrastructure import Infrastructure
from zone import Zone

def create_test_city():
    """Create a test city with transportation and power infrastructure."""
    print("Creating test city...")
    
    # Create a smaller city for testing
    city = City(20, 20)
    
    # Build a basic road network
    print("Building road network...")
    # Horizontal road
    for x in range(5, 15):
        city.place_infrastructure(x, 10, 'road')
    
    # Vertical road
    for y in range(5, 15):
        city.place_infrastructure(10, y, 'road')
    
    # Add a highway
    for x in range(0, 20):
        city.place_infrastructure(x, 5, 'highway')
    
    # Build power infrastructure
    print("Building power infrastructure...")
    # Power plant
    city.place_infrastructure(2, 2, 'power_plant')
    
    # Power lines connecting to zones
    for x in range(2, 8):
        city.place_infrastructure(x, 3, 'power_line')
    for y in range(3, 8):
        city.place_infrastructure(7, y, 'power_line')
    
    # Add some zones
    print("Adding zones...")
    # Residential area (connected to power)
    for x in range(8, 12):
        for y in range(6, 9):
            city.place_zone(x, y, 'residential')
    
    # Commercial area (connected to power)
    for x in range(12, 15):
        for y in range(8, 11):
            city.place_zone(x, y, 'commercial')
    
    # Industrial area (no power connection initially)
    for x in range(15, 18):
        for y in range(12, 15):
            city.place_zone(x, y, 'industrial')
    
    # Develop some zones
    print("Developing zones...")
    for y in range(city.height):
        for x in range(city.width):
            cell = city.get_cell(x, y)
            if isinstance(cell, Zone):
                # Force some development for testing
                if cell.can_develop(city):
                    cell.development_level = min(2, cell.properties['max_development'])
    
    return city

def test_power_system(city):
    """Test the power grid system."""
    print("\n=== POWER SYSTEM TEST ===")
    
    # Update power grid
    city.power_grid.update_power_network()
    
    # Get power statistics
    stats = city.power_grid.get_power_statistics()
    print(f"Power Generation: {stats['generation']} MW")
    print(f"Power Consumption: {stats['consumption']} MW")
    print(f"Power Coverage: {stats['coverage_percentage']:.1f}%")
    print(f"Grid Efficiency: {stats['efficiency']:.1%}")
    
    # Check specific zones
    print("\nZone Power Status:")
    for y in range(city.height):
        for x in range(city.width):
            cell = city.get_cell(x, y)
            if isinstance(cell, Zone):
                powered = city.power_grid.is_powered(x, y)
                print(f"  {cell.zone_type.capitalize()} at ({x},{y}): {'Powered' if powered else 'No Power'}")

def test_traffic_system(city):
    """Test the traffic management system."""
    print("\n=== TRAFFIC SYSTEM TEST ===")
    
    # Update traffic system
    city.traffic_manager.update_traffic_system()
    
    # Get traffic statistics
    stats = city.traffic_manager.get_traffic_statistics()
    print(f"Total Traffic Volume: {stats['total_volume']} vehicles/hour")
    print(f"Average Congestion: {stats['average_congestion']:.1%}")
    print(f"Total Roads: {stats['total_roads']}")
    
    # Show traffic on specific roads
    print("\nRoad Traffic Status:")
    for y in range(city.height):
        for x in range(city.width):
            cell = city.get_cell(x, y)
            if isinstance(cell, Infrastructure) and cell.infrastructure_type in ['road', 'highway']:
                traffic = city.traffic_manager.get_traffic_data(x, y)
                if traffic.volume > 0:
                    print(f"  {cell.infrastructure_type.capitalize()} at ({x},{y}): {traffic.volume} vehicles/hour, {traffic.congestion_level:.1%} congestion")

def test_integration(city):
    """Test integration between systems."""
    print("\n=== INTEGRATION TEST ===")
    
    # Update city statistics (this should update all systems)
    city.update_statistics()
    
    print(f"City Population: {city.population}")
    print(f"City Money: ${city.money:,}")
    print(f"Tax Revenue: ${city.tax_revenue:,}/month")
    print(f"Maintenance Cost: ${city.maintenance_cost:,}/month")
    
    # Test zone development with power requirements
    print("\nTesting zone development with power requirements...")
    unpowered_zones = []
    for y in range(city.height):
        for x in range(city.width):
            cell = city.get_cell(x, y)
            if isinstance(cell, Zone) and not city.power_grid.is_powered(x, y):
                unpowered_zones.append((x, y, cell))
    
    if unpowered_zones:
        print(f"Found {len(unpowered_zones)} unpowered zones that cannot develop:")
        for x, y, zone in unpowered_zones[:3]:  # Show first 3
            can_develop = zone.can_develop(city)
            print(f"  {zone.zone_type.capitalize()} at ({x},{y}): Can develop = {can_develop}")

def run_tests():
    """Run all tests."""
    print("Transportation and Power Systems Test")
    print("=" * 40)
    
    # Create test city
    city = create_test_city()
    
    # Run tests
    test_power_system(city)
    test_traffic_system(city)
    test_integration(city)
    
    print("\n=== TEST COMPLETE ===")
    print("To see visual results:")
    print("1. Run: python main.py")
    print("2. Use the new 'Power Line' and 'Highway' infrastructure tools")
    print("3. Switch view modes to 'power' or 'traffic' to see coverage and congestion")
    print("4. Click on zones and roads to inspect power and traffic information")

if __name__ == "__main__":
    run_tests()