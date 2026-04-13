import numpy as np
from scipy import stats
import structlog

logger = structlog.get_logger(__name__)

class StatsEngine:
    @staticmethod
    def calculate_t_test(group_a: list[float], group_b: list[float]) -> dict:
        """
        Calculate Independent t-Test for two groups (e.g. latency, cost).
        """
        if not group_a or not group_b:
            return {"error": "Insufficient data"}
            
        try:
            t_stat, p_val = stats.ttest_ind(group_a, group_b, equal_var=False)
            return {
                "t_statistic": round(float(t_stat), 4),
                "p_value": round(float(p_val), 4),
                "significant": p_val < 0.05
            }
        except Exception as e:
            logger.error("StatsEngine: t-test failed", error=str(e))
            return {"error": str(e)}

    @staticmethod
    def calculate_chi_square(successes_a: int, trials_a: int, successes_b: int, trials_b: int) -> dict:
        """
        Calculate Chi-Square test for two groups of proportions (e.g. success rate).
        """
        if trials_a == 0 or trials_b == 0:
            return {"error": "Insufficient data"}
            
        try:
            # Contingency table
            # [ [success_a, fail_a], [success_b, fail_b] ]
            table = [
                [successes_a, trials_a - successes_a],
                [successes_b, trials_b - successes_b]
            ]
            chi2, p_val, dof, expected = stats.chi2_contingency(table)
            
            return {
                "chi2_statistic": round(float(chi2), 4),
                "p_value": round(float(p_val), 4),
                "significant": p_val < 0.05
            }
        except Exception as e:
            logger.error("StatsEngine: chi-square failed", error=str(e))
            return {"error": str(e)}
