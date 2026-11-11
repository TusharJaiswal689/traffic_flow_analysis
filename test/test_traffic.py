from src.traffic import TrafficAnalyzer

def test_traffic_delay_ratio_for_no_road_closure():
    ratio, category = TrafficAnalyzer.traffic_delay_ratio(3, 4, False)
    assert ratio == 0.75
    assert category == "Normal"

def test_traffic_delay_ratio_for_road_closure():
    ratio, closure = TrafficAnalyzer.traffic_delay_ratio(3, 4, True)
    assert ratio == -1
    assert closure == True

def test_traffic_delay_ratio_for_negative_values():
    ratio, category = TrafficAnalyzer.traffic_delay_ratio(-3, 4, False)
    assert ratio == -1
    assert category == "Invalid"