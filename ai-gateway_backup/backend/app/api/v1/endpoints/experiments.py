from fastapi import APIRouter
from app.analytics.stats_engine import StatsEngine

router = APIRouter()

@router.get("")
async def get_experiments():
    return {"status": "implemented in backend"}

@router.post("")
async def create_experiment():
    return {"status": "implemented in backend"}

@router.get("/{experiment_id}/stats")
async def get_experiment_stats(experiment_id: str):
    """Run statistical evaluation for an experiment."""
    # Dummy data for demonstration
    group_a_latency = [200.0, 210.0, 195.0, 205.0]
    group_b_latency = [150.0, 155.0, 160.0, 152.0]
    t_test_res = StatsEngine.calculate_t_test(group_a_latency, group_b_latency)
    
    chi_sq_res = StatsEngine.calculate_chi_square(95, 100, 85, 100)
    
    return {
        "experiment_id": experiment_id,
        "latency_t_test": t_test_res,
        "success_rate_chi_square": chi_sq_res
    }
