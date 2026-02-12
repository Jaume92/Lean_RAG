import pytest
from app.services.calculator import LeanCalculator
from app.models.schemas import OEEInput

def test_oee_calculation():
    """Test OEE calculation"""
    calculator = LeanCalculator()
    
    input_data = OEEInput(
        availability=90.0,
        performance=95.0,
        quality=99.0
    )
    
    result = calculator.calculate_oee(input_data)
    
    # Expected OEE: 90 * 0.95 * 0.99 = 84.645
    assert abs(result.oee - 84.65) < 0.01
    assert result.world_class == False  # < 85%
    assert len(result.recommendations) > 0

def test_oee_world_class():
    """Test World Class OEE"""
    calculator = LeanCalculator()
    
    input_data = OEEInput(
        availability=95.0,
        performance=98.0,
        quality=99.5

    )
    
    result = calculator.calculate_oee(input_data)
    
    # Expected OEE: 95 * 0.98 * 0.995 = 92.6
    assert result.oee >= 85
    assert result.world_class == True

def test_takt_time_calculation():
    """Test Takt Time calculation"""
    calculator = LeanCalculator()
    
    result = calculator.calculate_takt_time(
        available_time_minutes=480,
        customer_demand_units=240
    )
    
    assert result["takt_time_minutes"] == 2.0
    assert result["takt_time_seconds"] == 120.0
    assert result["units_per_hour"] == 30.0

def test_lead_time_calculation():
    """Test Lead Time calculation"""
    calculator = LeanCalculator()
    
    process_steps = [
        {"name": "Step 1", "cycle_time": 5, "wait_time": 10},
        {"name": "Step 2", "cycle_time": 3, "wait_time": 15},
        {"name": "Step 3", "cycle_time": 7, "wait_time": 5},
    ]
    
    result = calculator.calculate_lead_time(process_steps)
    
    # Total cycle: 5 + 3 + 7 = 15
    # Total wait: 10 + 15 + 5 = 30
    # Total lead: 45
    assert result["total_cycle_time"] == 15
    assert result["total_wait_time"] == 30
    assert result["total_lead_time_minutes"] == 45
    
    # Value added ratio: 15/45 = 33.33%
    assert abs(result["value_added_ratio"] - 33.33) < 0.01
    assert result["waste_percentage"] == pytest.approx(66.67, rel=0.01)

def test_cycle_vs_takt():
    """Test cycle time vs takt time comparison"""
    calculator = LeanCalculator()
    
    # Cycle time faster than takt (good)
    result = calculator.calculate_cycle_time_vs_takt(
        cycle_time_minutes=1.5,
        takt_time_minutes=2.0
    )
    
    assert result["ratio"] < 1
    assert "suficiente" in result["status"].lower()
    
    # Cycle time slower than takt (bad)
    result = calculator.calculate_cycle_time_vs_takt(
        cycle_time_minutes=2.5,
        takt_time_minutes=2.0
    )
    
    assert result["ratio"] > 1
    assert "insuficiente" in result["status"].lower()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
