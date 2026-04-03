"""
tests/unit/test_prompts.py — Unit tests for Jinja2 prompt rendering (no DB/Redis needed)
"""
import pytest
from jinja2 import Environment, BaseLoader

# Test the rendering logic inline (unit test, no async/db needed)
_jinja_env = Environment(loader=BaseLoader(), autoescape=False)


class TestJinjaRendering:
    def test_simple_variable_injection(self):
        template = "Hello, {{ user_name }}! How can I help you?"
        rendered = _jinja_env.from_string(template).render(user_name="Alice")
        assert rendered == "Hello, Alice! How can I help you?"

    def test_conditional_rendering(self):
        template = (
            "{% if language == 'fr' %}Bonjour{% else %}Hello{% endif %}, {{ name }}!"
        )
        rendered = _jinja_env.from_string(template).render(language="fr", name="Alice")
        assert rendered == "Bonjour, Alice!"

    def test_loop_rendering(self):
        template = "Items: {% for item in items %}{{ item }}{% if not loop.last %}, {% endif %}{% endfor %}"
        rendered = _jinja_env.from_string(template).render(items=["a", "b", "c"])
        assert rendered == "Items: a, b, c"

    def test_missing_variable_renders_empty(self):
        template = "Hello, {{ user_name | default('stranger') }}!"
        rendered = _jinja_env.from_string(template).render()
        assert rendered == "Hello, stranger!"
