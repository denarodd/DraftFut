"""
Shared fixtures and helpers for DraftFut test suite.

These fixtures provide reusable test data for player attributes,
draft configurations, squad setups, user profiles, and league settings.
"""

import pytest


# ---------------------------------------------------------------------------
# Player fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def valid_player_data():
    """Minimal valid player data dictionary."""
    return {
        "name": "Lionel Messi",
        "position": "RW",
        "rating": 93,
        "nationality": "Argentina",
        "club": "Inter Miami",
        "pace": 80,
        "shooting": 90,
        "passing": 88,
        "dribbling": 94,
        "defending": 35,
        "physical": 65,
    }


@pytest.fixture
def valid_goalkeeper_data():
    """Valid goalkeeper-specific player data."""
    return {
        "name": "Thibaut Courtois",
        "position": "GK",
        "rating": 90,
        "nationality": "Belgium",
        "club": "Real Madrid",
        "diving": 88,
        "handling": 85,
        "kicking": 75,
        "reflexes": 90,
        "speed": 50,
        "positioning": 89,
    }


# ---------------------------------------------------------------------------
# Draft fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def draft_config():
    """Default draft configuration."""
    return {
        "num_rounds": 15,
        "time_per_pick_seconds": 60,
        "max_players": 8,
        "snake_draft": True,
    }


@pytest.fixture
def sample_player_pool():
    """A small pool of players available for drafting."""
    return [
        {"id": 1, "name": "Player A", "position": "ST", "rating": 90},
        {"id": 2, "name": "Player B", "position": "CM", "rating": 85},
        {"id": 3, "name": "Player C", "position": "CB", "rating": 88},
        {"id": 4, "name": "Player D", "position": "GK", "rating": 87},
        {"id": 5, "name": "Player E", "position": "LW", "rating": 82},
    ]


# ---------------------------------------------------------------------------
# Squad / team fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def valid_formation():
    """A standard 4-3-3 formation."""
    return {
        "name": "4-3-3",
        "positions": {
            "GK": 1,
            "CB": 2,
            "LB": 1,
            "RB": 1,
            "CM": 3,
            "LW": 1,
            "RW": 1,
            "ST": 1,
        },
    }


@pytest.fixture
def full_squad_player_ids():
    """A list of 11 player IDs representing a full starting squad."""
    return list(range(1, 12))


# ---------------------------------------------------------------------------
# User fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def valid_user_data():
    """Minimal valid user registration data."""
    return {
        "username": "footballer99",
        "email": "fan@example.com",
        "password": "Str0ng!Pass",
    }


# ---------------------------------------------------------------------------
# League fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def league_config():
    """Default league configuration."""
    return {
        "name": "Premier Draft League",
        "max_teams": 8,
        "draft_type": "snake",
        "scoring_system": "standard",
    }
