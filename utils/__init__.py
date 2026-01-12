"""
Utils package initialization.
"""
from .antibot import AntiBot, ALL_USER_AGENTS
from .benchmark import BenchmarkEngine

__all__ = [
    'AntiBot',
    'ALL_USER_AGENTS',
    'BenchmarkEngine'
]
