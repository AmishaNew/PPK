"""
Enhanced Economic System - Comprehensive financial management

Handles detailed tax revenues, expenses, and economic indicators.
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from infrastructure import Infrastructure
from zone import Zone

@dataclass
class FinancialReport:
    """Monthly financial report."""
    total_income: float
    total_expenses: float
    net_income: float
    income_breakdown: Dict[str, float]
    expense_breakdown: Dict[str, float]

class EconomicSystem:
    """
    Manages comprehensive city economics and finances.
    """
    
    def __init__(self, city):
        """Initialize the economic system."""
        self.city = city
        self.monthly_reports = []
        self.tax_rates = {
            'residential': 0.02,  # 2% of land value per month
            'commercial': 0.03,   # 3% of land value per month
            'industrial': 0.025   # 2.5% of land value per month
        }
        
    def calculate_monthly_finances(self) -> FinancialReport:
        """Calculate comprehensive monthly finances."""
        income_breakdown = {}
        expense_breakdown = {}
        
        # Calculate all income sources
        income_breakdown['property_tax'] = self._calculate_property_tax()
        income_breakdown['business_tax'] = self._calculate_business_tax()
        income_breakdown['industrial_tax'] = self._calculate_industrial_tax()
        income_breakdown['transit_revenue'] = self._calculate_transit_revenue()
        income_breakdown['utility_fees'] = self._calculate_utility_fees()
        
        # Calculate all expenses
        expense_breakdown['infrastructure_maintenance'] = self._calculate_infrastructure_maintenance()
        expense_breakdown['public_services'] = self._calculate_public_services()
        expense_breakdown['transit_operations'] = self._calculate_transit_operations()
        expense_breakdown['police_operations'] = self._calculate_police_operations()
        expense_breakdown['utility_operations'] = self._calculate_utility_operations()
        expense_breakdown['administration'] = self._calculate_administration_costs()
        
        total_income = sum(income_breakdown.values())
        total_expenses = sum(expense_breakdown.values())
        net_income = total_income - total_expenses
        
        report = FinancialReport(
            total_income=total_income,
            total_expenses=total_expenses,
            net_income=net_income,
            income_breakdown=income_breakdown,
            expense_breakdown=expense_breakdown
        )
        
        self.monthly_reports.append(report)
        return report
    
    def _calculate_property_tax(self) -> float:
        """Calculate property tax from all zones."""
        total_tax = 0.0
        
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.get_cell(x, y)
                if isinstance(cell, Zone) and cell.development_level > 0:
                    # Base tax calculation
                    base_tax = cell.development_level * 100  # $100 per development level
                    
                    # Apply land value multiplier if available
                    if hasattr(self.city, 'land_valuation'):
                        multiplier = self.city.land_valuation.get_tax_multiplier(x, y)
                        base_tax *= multiplier
                    
                    # Apply zone-specific tax rate
                    tax_rate = self.tax_rates.get(cell.zone_type, 0.02)
                    zone_tax = base_tax * tax_rate
                    
                    total_tax += zone_tax
        
        return total_tax
    
    def _calculate_business_tax(self) -> float:
        """Calculate business tax from commercial zones."""
        total_tax = 0.0
        
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.get_cell(x, y)
                if isinstance(cell, Zone) and cell.zone_type == 'commercial' and cell.development_level > 0:
                    # Business tax based on development and location
                    business_tax = cell.development_level * 200
                    
                    # High-value locations generate more business tax
                    if hasattr(self.city, 'land_valuation'):
                        land_value = self.city.land_valuation.get_land_value(x, y)
                        base_value = self.city.land_valuation.base_value
                        if land_value > base_value * 1.5:
                            business_tax *= 1.5
                    
                    total_tax += business_tax
        
        return total_tax
    
    def _calculate_industrial_tax(self) -> float:
        """Calculate industrial tax and export revenues."""
        total_tax = 0.0
        
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.get_cell(x, y)
                if isinstance(cell, Zone) and cell.zone_type == 'industrial' and cell.development_level > 0:
                    # Base industrial tax
                    industrial_tax = cell.development_level * 150
                    
                    # Supply chain efficiency bonus
                    if hasattr(self.city, 'supply_chain'):
                        efficiency = self.city.supply_chain.get_supply_chain_efficiency()
                        industrial_tax *= (1.0 + efficiency * 0.5)
                    
                    total_tax += industrial_tax
        
        return total_tax
    
    def _calculate_transit_revenue(self) -> float:
        """Calculate revenue from public transit."""
        if not hasattr(self.city, 'transit_system'):
            return 0.0
        
        stats = self.city.transit_system.get_coverage_statistics()
        # Revenue based on passenger capacity and coverage
        base_revenue = stats['passenger_capacity'] * 0.1  # $0.10 per passenger capacity
        coverage_bonus = stats['coverage_percentage'] * 10  # Bonus for good coverage
        
        return base_revenue + coverage_bonus
    
    def _calculate_utility_fees(self) -> float:
        """Calculate utility fees from powered zones."""
        if not hasattr(self.city, 'power_grid'):
            return 0.0
        
        powered_zones = 0
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.get_cell(x, y)
                if isinstance(cell, Zone) and cell.development_level > 0:
                    if self.city.power_grid.is_powered(x, y):
                        powered_zones += cell.development_level
        
        return powered_zones * 25  # $25 per powered development level
    
    def _calculate_infrastructure_maintenance(self) -> float:
        """Calculate infrastructure maintenance costs."""
        total_cost = 0.0
        
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.get_cell(x, y)
                if isinstance(cell, Infrastructure):
                    maintenance = cell.get_maintenance_cost()
                    
                    # Poor city finances increase maintenance costs
                    if self.city.money < 10000:
                        maintenance *= 1.5  # Deferred maintenance is more expensive
                    elif self.city.money < 50000:
                        maintenance *= 1.2
                    
                    total_cost += maintenance
        
        return total_cost
    
    def _calculate_public_services(self) -> float:
        """Calculate public service costs."""
        population = self.city.population
        
        # Base services cost per capita
        base_cost_per_capita = 15
        
        # Scale with population
        if population > 50000:
            base_cost_per_capita *= 1.3  # Larger cities have higher per-capita costs
        elif population > 20000:
            base_cost_per_capita *= 1.1
        
        return population * base_cost_per_capita
    
    def _calculate_transit_operations(self) -> float:
        """Calculate transit system operational costs."""
        if not hasattr(self.city, 'transit_system'):
            return 0.0
        
        stats = self.city.transit_system.get_coverage_statistics()
        
        # Operational costs based on stations and lines
        station_costs = stats['stations'] * 500  # $500 per station per month
        line_costs = stats['lines'] * 1000      # $1000 per line per month
        
        return station_costs + line_costs
    
    def _calculate_police_operations(self) -> float:
        """Calculate police operational costs."""
        if not hasattr(self.city, 'crime_system'):
            return self.city.population * 5  # Basic police cost
        
        # Count police stations
        police_stations = 0
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.get_cell(x, y)
                if isinstance(cell, Infrastructure) and cell.infrastructure_type == 'police_station':
                    police_stations += 1
        
        # Base cost per station plus population-based patrol costs
        station_costs = police_stations * 2000  # $2000 per station per month
        patrol_costs = self.city.population * 3  # $3 per capita for patrols
        
        # High crime areas require more resources
        crime_stats = self.city.crime_system.get_crime_statistics()
        if crime_stats['average_crime_rate'] > 100:
            patrol_costs *= 1.5
        elif crime_stats['average_crime_rate'] > 75:
            patrol_costs *= 1.2
        
        return station_costs + patrol_costs
    
    def _calculate_utility_operations(self) -> float:
        """Calculate utility operational costs."""
        if not hasattr(self.city, 'power_grid'):
            return 0.0
        
        power_stats = self.city.power_grid.get_power_statistics()
        
        # Operational costs based on power generation and consumption
        generation_costs = power_stats['generation'] * 0.5  # $0.50 per MW generated
        grid_maintenance = power_stats['consumption'] * 0.2  # Grid maintenance costs
        
        return generation_costs + grid_maintenance
    
    def _calculate_administration_costs(self) -> float:
        """Calculate administrative overhead costs."""
        # Base administrative costs scale with city size and complexity
        base_admin = 5000  # Base monthly admin cost
        
        # Scale with population
        population_factor = self.city.population * 0.5
        
        # Scale with city infrastructure complexity
        infrastructure_count = 0
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.get_cell(x, y)
                if isinstance(cell, Infrastructure):
                    infrastructure_count += 1
        
        complexity_factor = infrastructure_count * 10
        
        return base_admin + population_factor + complexity_factor
    
    def apply_financial_effects(self, report: FinancialReport):
        """Apply financial effects to city services."""
        # Update city money
        self.city.money += report.net_income
        
        # Financial crisis effects
        if self.city.money < 0:
            self._apply_financial_crisis_effects()
        elif self.city.money < 10000:
            self._apply_budget_constraints()
    
    def _apply_financial_crisis_effects(self):
        """Apply effects of financial crisis."""
        # Reduce service quality
        if hasattr(self.city, 'crime_system'):
            # Crime increases due to reduced police funding
            for position in self.city.crime_system.crime_data:
                crime_data = self.city.crime_system.crime_data[position]
                crime_data.crime_rate *= 1.2  # 20% increase in crime
        
        # Infrastructure degrades faster
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.get_cell(x, y)
                if isinstance(cell, Infrastructure):
                    cell.condition = max(0, cell.condition - 2)  # Accelerated degradation
    
    def _apply_budget_constraints(self):
        """Apply effects of tight budget."""
        # Slower infrastructure maintenance
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.get_cell(x, y)
                if isinstance(cell, Infrastructure):
                    cell.condition = max(0, cell.condition - 0.5)  # Slower maintenance
    
    def get_financial_summary(self) -> Dict[str, float]:
        """Get summary of financial status."""
        if not self.monthly_reports:
            return {'current_balance': self.city.money, 'monthly_net': 0, 'trend': 'stable'}
        
        latest_report = self.monthly_reports[-1]
        
        # Calculate trend
        trend = 'stable'
        if len(self.monthly_reports) >= 2:
            previous_net = self.monthly_reports[-2].net_income
            current_net = latest_report.net_income
            
            if current_net > previous_net * 1.1:
                trend = 'improving'
            elif current_net < previous_net * 0.9:
                trend = 'declining'
        
        return {
            'current_balance': self.city.money,
            'monthly_net': latest_report.net_income,
            'monthly_income': latest_report.total_income,
            'monthly_expenses': latest_report.total_expenses,
            'trend': trend
        }
    
    def get_detailed_breakdown(self) -> Dict[str, Dict[str, float]]:
        """Get detailed financial breakdown."""
        if not self.monthly_reports:
            return {'income': {}, 'expenses': {}}
        
        latest_report = self.monthly_reports[-1]
        return {
            'income': latest_report.income_breakdown,
            'expenses': latest_report.expense_breakdown
        }