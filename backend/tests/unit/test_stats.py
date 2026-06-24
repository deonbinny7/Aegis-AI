import pytest
from app.analytics.stats_engine import StatsEngine

def test_t_test():
    group_a = [10, 12, 14, 15, 12]
    group_b = [20, 22, 21, 23, 22]
    
    res = StatsEngine.calculate_t_test(group_a, group_b)
    assert "t_statistic" in res
    assert "p_value" in res
    assert res["significant"] == True

def test_chi_square():
    # 90/100 vs 50/100 success rates
    res = StatsEngine.calculate_chi_square(90, 100, 50, 100)
    assert "chi2_statistic" in res
    assert "p_value" in res
    assert res["significant"] is True

# Refactored for performance polish — 2026-06-24T20:58:54
