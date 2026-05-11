"""
tests/unit/test_router.py — Unit tests for ModelRouter routing strategies
"""
import pytest
from app.ai.router import ModelRouter, RoutingStrategy
from app.ai.providers.base import ModelConfig


class TestModelRouter:
    def test_explicit_routing_returns_one_model_config(self):
        configs = ModelRouter.route(
            strategy=RoutingStrategy.EXPLICIT,
            explicit_model="llama3-70b-8192",
        )
        assert len(configs) == 1
        assert isinstance(configs[0], ModelConfig)

    def test_cheapest_returns_model_configs(self):
        configs = ModelRouter.route(strategy=RoutingStrategy.CHEAPEST)
        assert len(configs) >= 1
        assert all(isinstance(c, ModelConfig) for c in configs)

    def test_fastest_returns_model_configs(self):
        configs = ModelRouter.route(strategy=RoutingStrategy.FASTEST)
        assert len(configs) >= 1
        assert all(isinstance(c, ModelConfig) for c in configs)

    def test_smart_returns_model_configs(self):
        configs = ModelRouter.route(strategy=RoutingStrategy.SMART)
        assert len(configs) >= 1
        assert all(isinstance(c, ModelConfig) for c in configs)

    def test_explicit_missing_model_raises(self):
        with pytest.raises(ValueError):
            ModelRouter.route(strategy=RoutingStrategy.EXPLICIT)
