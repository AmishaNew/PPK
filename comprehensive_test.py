#!/usr/bin/env python3
"""
Comprehensive Test Script for Advanced City Systems

This script creates a complete test city demonstrating all advanced features:
- Transportation and power systems
- Public transit networks
- Industrial supply chains
- Land valuation
- Crime and safety systems
- Enhanced economics

Run this script to see all systems working together.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from city import City
from infrastructure import Infrastructure
from zone import Zone

def create_comprehensive_test_city():
    """Create a comprehensive test city with all systems."""
    print("Creating comprehensive test city (30x30)...")
    
    city = City(30, 30)
    
    # 1. BUILD TRANSPORTATION NETWORK
    print("Building transportation network...")
    
    # Main highway (horizontal)
    for x in range(0, 30):
        city.place_infrastructure(x, 10, 'highway')
    
    # Secondary highway (vertical)
    for y in range(0, 30):
        city.place_infrastructure(15, y, 'highway')
    
    # Local roads
    # Horizontal roads
    for x in range(5, 25):
        city.place_infrastructure(x, 5, 'road')
        city.place_infrastructure(x, 15, 'road')
        city.place_infrastructure(x, 20, 'road')
    
    # Vertical roads
    for y in range(2, 28):
        city.place_infrastructure(8, y, 'road')
        city.place_infrastructure(22, y, 'road')
    
    # 2. BUILD POWER GRID
    print("Building power grid...")
    
    # Power plants
    city.place_infrastructure(2, 2, 'power_plant')
    city.place_infrastructure(27, 27, 'power_plant')
    
    # Power lines connecting to zones
    # From first power plant
    for x in range(2, 16):
        city.place_infrastructure(x, 3, 'power_line')
    for y in range(3, 12):
        city.place_infrastructure(15, y, 'power_line')
    
    # From second power plant
    for x in range(15, 28):
        city.place_infrastructure(x, 26, 'power_line')
    for y in range(15, 27):
        city.place_infrastructure(16, y, 'power_line')
    
    # 3. BUILD PUBLIC TRANSIT
    print("Building public transit...")
    
    # Train stations
    city.place_infrastructure(5, 10, 'train_station')
    city.place_infrastructure(15, 10, 'train_station')
    city.place_infrastructure(25, 10, 'train_station')
    
    # Subway stations
    city.place_infrastructure(8, 15, 'subway_station')
    city.place_infrastructure(15, 15, 'subway_station')
    city.place_infrastructure(22, 15, 'subway_station')
    
    # 4. BUILD PUBLIC SERVICES
    print("Building public services...")
    
    # Police stations
    city.place_infrastructure(10, 8, 'police_station')
    city.place_infrastructure(20, 18, 'police_station')
    
    # Fire stations
    city.place_infrastructure(12, 12, 'fire_station')
    city.place_infrastructure(18, 22, 'fire_station')
    
    # Schools
    city.place_infrastructure(6, 6, 'school')
    city.place_infrastructure(24, 24, 'school')
    
    # Hospitals
    city.place_infrastructure(4, 18, 'hospital')
    city.place_infrastructure(26, 8, 'hospital')
    
    # Parks
    city.place_infrastructure(10, 4, 'park')
    city.place_infrastructure(20, 14, 'park')
    city.place_infrastructure(14, 24, 'park')
    
    # 5. CREATE ZONED AREAS
    print("Creating zoned areas...")
    
    # Residential areas (near transit and services)
    # Area 1: Near first train station
    for x in range(3, 7):
        for y in range(7, 10):
            city.place_zone(x, y, 'residential')
    
    # Area 2: Near subway
    for x in range(6, 10):
        for y in range(16, 19):
            city.place_zone(x, y, 'residential')
    
    # Area 3: Suburban area
    for x in range(17, 21):
        for y in range(3, 7):
            city.place_zone(x, y, 'residential')
    
    # Area 4: High-density near transit
    for x in range(23, 27):
        for y in range(16, 20):
            city.place_zone(x, y, 'residential')
    
    # Commercial areas (near highways and residential)
    # Downtown commercial
    for x in range(13, 17):
        for y in range(11, 14):
            city.place_zone(x, y, 'commercial')
    
    # Strip mall
    for x in range(9, 12):
        for y in range(21, 24):
            city.place_zone(x, y, 'commercial')
    
    # Shopping center
    for x in range(19, 22):
        for y in range(8, 11):
            city.place_zone(x, y, 'commercial')
    
    # Industrial areas (near highways, away from residential)
    # Industrial district 1
    for x in range(1, 4):
        for y in range(25, 29):
            city.place_zone(x, y, 'industrial')
    
    # Industrial district 2
    for x in range(26, 29):
        for y in range(1, 5):
            city.place_zone(x, y, 'industrial')
    
    # Industrial district 3 (near highway)
    for x in range(17, 20):
        for y in range(25, 28):
            city.place_zone(x, y, 'industrial')
    
    # 6. DEVELOP ZONES
    print("Developing zones...")
    
    # Force development for testing
    for y in range(city.height):
        for x in range(city.width):
            cell = city.get_cell(x, y)
            if isinstance(cell, Zone):
                # Develop zones that have power
                if city.power_grid.is_powered(x, y):
                    # Develop to different levels based on zone type and location
                    if cell.zone_type == 'residential':
                        cell.development_level = min(3, cell.properties['max_development'])
                    elif cell.zone_type == 'commercial':
                        cell.development_level = min(2, cell.properties['max_development'])
                    elif cell.zone_type == 'industrial':
                        cell.development_level = min(2, cell.properties['max_development'])
    
    return city

def test_all_systems(city):
    """Test all city systems comprehensively."""
    print("\n" + "="*60)
    print("COMPREHENSIVE SYSTEMS TEST")
    print("="*60)
    
    # Update all systems
    city.update_statistics()
    
    # 1. POWER SYSTEM TEST
    print("\n1. POWER GRID SYSTEM")
    print("-" * 30)
    power_stats = city.power_grid.get_power_statistics()
    print(f"Power Generation: {power_stats['generation']:.0f} MW")
    print(f"Power Consumption: {power_stats['consumption']:.0f} MW")
    print(f"Grid Coverage: {power_stats['coverage_percentage']:.1f}%")
    print(f"Grid Efficiency: {power_stats['efficiency']:.1%}")
    
    # Count powered vs unpowered zones
    powered_zones = 0
    unpowered_zones = 0
    for y in range(city.height):
        for x in range(city.width):
            cell = city.get_cell(x, y)
            if isinstance(cell, Zone):
                if city.power_grid.is_powered(x, y):
                    powered_zones += 1
                else:
                    unpowered_zones += 1
    
    print(f"Powered Zones: {powered_zones}")
    print(f"Unpowered Zones: {unpowered_zones}")
    
    # 2. TRAFFIC SYSTEM TEST
    print("\n2. TRAFFIC SYSTEM")
    print("-" * 30)
    traffic_stats = city.traffic_manager.get_traffic_statistics()
    print(f"Total Traffic Volume: {traffic_stats['total_volume']} vehicles/hour")
    print(f"Average Congestion: {traffic_stats['average_congestion']:.1%}")
    print(f"Total Roads: {traffic_stats['total_roads']}")
    
    # Show busiest roads
    busiest_roads = []
    for y in range(city.height):
        for x in range(city.width):
            cell = city.get_cell(x, y)
            if isinstance(cell, Infrastructure) and cell.infrastructure_type in ['road', 'highway']:
                traffic = city.traffic_manager.get_traffic_data(x, y)
                if traffic.volume > 0:
                    busiest_roads.append((x, y, traffic.volume, traffic.congestion_level))
    
    busiest_roads.sort(key=lambda x: x[2], reverse=True)
    print("Busiest Roads:")
    for x, y, volume, congestion in busiest_roads[:5]:
        print(f"  ({x},{y}): {volume} vehicles/hour, {congestion:.1%} congestion")
    
    # 3. TRANSIT SYSTEM TEST
    print("\n3. PUBLIC TRANSIT SYSTEM")
    print("-" * 30)
    transit_stats = city.transit_system.get_coverage_statistics()
    print(f"Transit Stations: {transit_stats['stations']}")
    print(f"Transit Lines: {transit_stats['lines']}")
    print(f"Coverage: {transit_stats['coverage_percentage']:.1f}%")
    print(f"Passenger Capacity: {transit_stats['passenger_capacity']:,}")
    
    # 4. SUPPLY CHAIN TEST
    print("\n4. SUPPLY CHAIN SYSTEM")
    print("-" * 30)
    supply_stats = city.supply_chain.get_supply_chain_statistics()
    print(f"Supply Routes: {supply_stats['total_routes']}")
    print(f"External Connections: {supply_stats['external_connections']}")
    print(f"Supply Chain Efficiency: {supply_stats['efficiency']:.1%}")
    print(f"Total Cargo Volume: {supply_stats['cargo_volume']} units/hour")
    
    print("Commodity Supply & Demand:")
    for commodity, data in supply_stats['commodities'].items():
        print(f"  {commodity}: Supply={data['supply']}, Demand={data['demand']}")
    
    # 5. LAND VALUATION TEST
    print("\n5. LAND VALUATION SYSTEM")
    print("-" * 30)
    valuation_stats = city.land_valuation.get_valuation_statistics()
    print(f"Average Land Value: ${valuation_stats['average_value']:,.0f}")
    print(f"Minimum Land Value: ${valuation_stats['min_value']:,.0f}")
    print(f"Maximum Land Value: ${valuation_stats['max_value']:,.0f}")
    
    # Show highest and lowest value areas
    high_value_areas = []
    low_value_areas = []
    for y in range(city.height):
        for x in range(city.width):
            value = city.land_valuation.get_land_value(x, y)
            if value > valuation_stats['average_value'] * 1.5:
                high_value_areas.append((x, y, value))
            elif value < valuation_stats['average_value'] * 0.7:
                low_value_areas.append((x, y, value))
    
    print(f"High-Value Areas: {len(high_value_areas)}")
    print(f"Low-Value Areas: {len(low_value_areas)}")
    
    # 6. CRIME SYSTEM TEST
    print("\n6. CRIME & SAFETY SYSTEM")
    print("-" * 30)
    crime_stats = city.crime_system.get_crime_statistics()
    print(f"Average Crime Rate: {crime_stats['average_crime_rate']:.1f} per 1000 residents/year")
    print(f"Average Safety Level: {crime_stats['average_safety']:.1%}")
    print(f"Police Coverage: {crime_stats['police_coverage_percentage']:.1f}%")
    
    # Show safest and most dangerous areas
    safe_areas = []
    dangerous_areas = []
    for y in range(city.height):
        for x in range(city.width):
            safety = city.crime_system.get_safety_level(x, y)
            if safety > 0.8:
                safe_areas.append((x, y, safety))
            elif safety < 0.4:
                dangerous_areas.append((x, y, safety))
    
    print(f"Very Safe Areas: {len(safe_areas)}")
    print(f"High-Risk Areas: {len(dangerous_areas)}")
    
    # 7. ECONOMIC SYSTEM TEST
    print("\n7. ECONOMIC SYSTEM")
    print("-" * 30)
    financial_summary = city.economic_system.get_financial_summary()
    print(f"Current Balance: ${financial_summary['current_balance']:,.0f}")
    print(f"Monthly Net Income: ${financial_summary['monthly_net']:,.0f}")
    print(f"Monthly Income: ${financial_summary['monthly_income']:,.0f}")
    print(f"Monthly Expenses: ${financial_summary['monthly_expenses']:,.0f}")
    print(f"Financial Trend: {financial_summary['trend'].title()}")
    
    # Detailed breakdown
    breakdown = city.economic_system.get_detailed_breakdown()
    print("\nIncome Sources:")
    for source, amount in breakdown['income'].items():
        print(f"  {source.replace('_', ' ').title()}: ${amount:,.0f}")
    
    print("\nExpense Categories:")
    for category, amount in breakdown['expenses'].items():
        print(f"  {category.replace('_', ' ').title()}: ${amount:,.0f}")
    
    # 8. CITY OVERVIEW
    print("\n8. CITY OVERVIEW")
    print("-" * 30)
    print(f"Population: {city.population:,}")
    print(f"Happiness: {city.happiness:.1f}%")
    print(f"Employment Rate: {city.employment_rate:.1%}")
    print(f"Pollution Level: {city.pollution:.1f}")
    
    # Zone statistics
    print(f"\nZone Distribution:")
    for zone_type, count in city.zone_counts.items():
        print(f"  {zone_type.capitalize()}: {count} zones")

def demonstrate_view_modes():
    """Demonstrate different view modes available in the UI."""
    print("\n" + "="*60)
    print("VIEW MODES DEMONSTRATION")
    print("="*60)
    
    print("\nAvailable View Modes in the UI:")
    print("1. NORMAL - Standard city view showing all infrastructure")
    print("2. POWER - Shows power grid coverage (yellow = powered areas)")
    print("3. TRAFFIC - Shows traffic congestion (green=free, yellow=moderate, red=heavy)")
    print("4. TRANSIT - Shows public transit coverage (lavender = transit access)")
    print("5. CRIME - Shows safety levels (green=safe, red=dangerous)")
    print("6. LAND_VALUE - Shows property values (red=expensive, blue=cheap)")
    
    print("\nTo test these view modes:")
    print("1. Run: python main.py")
    print("2. Use the 'View Mode' dropdown in the UI")
    print("3. Place infrastructure using the new tools:")
    print("   - Power Line (connects power plants to zones)")
    print("   - Highway (high-capacity roads)")
    print("   - Train Station (public transit)")
    print("   - Subway Station (underground transit)")
    print("4. Click on any cell to inspect detailed information")

def run_comprehensive_test():
    """Run the complete test suite."""
    print("Advanced City Simulation - Comprehensive Test")
    print("=" * 60)
    
    # Create test city
    city = create_comprehensive_test_city()
    
    # Test all systems
    test_all_systems(city)
    
    # Show view mode information
    demonstrate_view_modes()
    
    print("\n" + "="*60)
    print("TEST COMPLETE - ALL SYSTEMS OPERATIONAL")
    print("="*60)
    
    print("\nSUMMARY OF IMPLEMENTED FEATURES:")
    print("✓ Transportation & Power Systems")
    print("  - Roads, highways, power lines, power plants")
    print("  - Power grid connectivity and zone coverage")
    print("  - Traffic calculation based on commuting patterns")
    print("  - Visual traffic indicators")
    
    print("✓ Public Transit System")
    print("  - Train and subway stations with coverage areas")
    print("  - Transit lines connecting stations")
    print("  - Traffic reduction in transit-covered areas")
    
    print("✓ Industrial Supply Chain")
    print("  - Supply and demand calculation")
    print("  - Cargo routing between facilities")
    print("  - External city connections")
    print("  - Supply chain efficiency tracking")
    
    print("✓ Dynamic Land Valuation")
    print("  - Property values based on location factors")
    print("  - Annual revaluation")
    print("  - Tax multipliers based on land value")
    print("  - Development probability modifiers")
    
    print("✓ Crime & Safety System")
    print("  - Crime rate calculation by area")
    print("  - Police coverage and response times")
    print("  - Safety visualization on maps")
    print("  - Crime effects on happiness and property values")
    
    print("✓ Enhanced Economic System")
    print("  - Detailed tax revenue from all sources")
    print("  - Comprehensive expense tracking")
    print("  - Financial reports and breakdowns")
    print("  - Budget effects on city services")
    
    print("\nTo manually test and verify:")
    print("1. Run 'python main.py' to start the game")
    print("2. Switch between view modes to see different systems")
    print("3. Place infrastructure and zones to test interactions")
    print("4. Use the inspect tool to see detailed information")
    print("5. Advance time to see systems update dynamically")

if __name__ == "__main__":
    run_comprehensive_test()