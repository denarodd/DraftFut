"""
Edge-case tests for the League / Tournament system.

Covers:
- Empty / invalid league names
- Team capacity limits
- Joining and leaving edge cases
- Draft type validation
- Scoring system validation
- Standings calculation edge cases
- League state transitions
"""

import pytest


class TestLeagueCreation:
    """Edge cases around creating a new league."""

    def test_empty_league_name_rejected(self, league_config):
        """A league with an empty name must be rejected."""
        league_config["name"] = ""
        with pytest.raises(ValueError):
            _create_league(league_config)

    def test_none_league_name_rejected(self, league_config):
        """A league with a None name must be rejected."""
        league_config["name"] = None
        with pytest.raises((ValueError, TypeError)):
            _create_league(league_config)

    def test_whitespace_only_league_name_rejected(self, league_config):
        """A league name of only whitespace must be rejected."""
        league_config["name"] = "   "
        with pytest.raises(ValueError):
            _create_league(league_config)

    def test_very_long_league_name_rejected(self, league_config):
        """A league name exceeding 50 characters must be rejected."""
        league_config["name"] = "A" * 51
        with pytest.raises(ValueError):
            _create_league(league_config)

    def test_max_teams_zero_rejected(self, league_config):
        """A league with zero max teams must be rejected."""
        league_config["max_teams"] = 0
        with pytest.raises(ValueError):
            _create_league(league_config)

    def test_max_teams_one_rejected(self, league_config):
        """A league with only 1 team max must be rejected (need at least 2)."""
        league_config["max_teams"] = 1
        with pytest.raises(ValueError):
            _create_league(league_config)

    def test_max_teams_negative_rejected(self, league_config):
        """Negative max teams must be rejected."""
        league_config["max_teams"] = -4
        with pytest.raises(ValueError):
            _create_league(league_config)

    def test_max_teams_exceeds_limit_rejected(self, league_config):
        """Max teams exceeding upper limit (e.g. 32) must be rejected."""
        league_config["max_teams"] = 33
        with pytest.raises(ValueError):
            _create_league(league_config)

    def test_invalid_draft_type_rejected(self, league_config):
        """An unrecognized draft type must be rejected."""
        league_config["draft_type"] = "random_chaos"
        with pytest.raises(ValueError):
            _create_league(league_config)

    def test_invalid_scoring_system_rejected(self, league_config):
        """An unrecognized scoring system must be rejected."""
        league_config["scoring_system"] = "made_up"
        with pytest.raises(ValueError):
            _create_league(league_config)

    def test_valid_league_creation(self, league_config):
        """A league with valid config should be created successfully."""
        league = _create_league(league_config)
        assert league["name"] == league_config["name"]
        assert league["max_teams"] == league_config["max_teams"]

    def test_missing_name_field_rejected(self):
        """A config missing the name field must be rejected."""
        with pytest.raises((ValueError, KeyError, TypeError)):
            _create_league({"max_teams": 8, "draft_type": "snake", "scoring_system": "standard"})


class TestLeagueMembership:
    """Edge cases around joining and leaving leagues."""

    def test_join_full_league_rejected(self, league_config):
        """Joining a league that has reached max_teams must be rejected."""
        league_config["max_teams"] = 2
        league = _create_league(league_config)
        _join_league(league, user_id=1)
        _join_league(league, user_id=2)
        with pytest.raises(ValueError):
            _join_league(league, user_id=3)

    def test_join_same_league_twice_rejected(self, league_config):
        """A user joining the same league twice must be rejected."""
        league = _create_league(league_config)
        _join_league(league, user_id=1)
        with pytest.raises(ValueError):
            _join_league(league, user_id=1)

    def test_leave_league_not_member_rejected(self, league_config):
        """A user leaving a league they never joined must be rejected."""
        league = _create_league(league_config)
        with pytest.raises(ValueError):
            _leave_league(league, user_id=99)

    def test_leave_league_after_draft_started_rejected(self, league_config):
        """A user cannot leave once the draft has started."""
        league = _create_league(league_config)
        _join_league(league, user_id=1)
        _join_league(league, user_id=2)
        league["status"] = "drafting"
        with pytest.raises(ValueError):
            _leave_league(league, user_id=1)

    def test_join_league_after_draft_started_rejected(self, league_config):
        """A user cannot join once the draft has started."""
        league = _create_league(league_config)
        _join_league(league, user_id=1)
        _join_league(league, user_id=2)
        league["status"] = "drafting"
        with pytest.raises(ValueError):
            _join_league(league, user_id=3)

    def test_join_with_none_user_id_rejected(self, league_config):
        """Joining with a None user ID must be rejected."""
        league = _create_league(league_config)
        with pytest.raises((ValueError, TypeError)):
            _join_league(league, user_id=None)

    def test_join_with_negative_user_id_rejected(self, league_config):
        """Joining with a negative user ID must be rejected."""
        league = _create_league(league_config)
        with pytest.raises(ValueError):
            _join_league(league, user_id=-1)


class TestLeagueStandings:
    """Edge cases around league standings calculations."""

    def test_standings_with_no_teams_returns_empty(self, league_config):
        """Standings for a league with no teams should be empty."""
        league = _create_league(league_config)
        standings = _get_standings(league)
        assert standings == []

    def test_standings_with_one_team(self, league_config):
        """Standings with a single team should return that team at rank 1."""
        league = _create_league(league_config)
        _join_league(league, user_id=1)
        league["scores"] = {1: 0}
        standings = _get_standings(league)
        assert len(standings) == 1
        assert standings[0]["user_id"] == 1

    def test_standings_with_tied_scores(self, league_config):
        """When two teams have the same score, standings should handle ties."""
        league = _create_league(league_config)
        _join_league(league, user_id=1)
        _join_league(league, user_id=2)
        league["scores"] = {1: 50, 2: 50}
        standings = _get_standings(league)
        assert len(standings) == 2
        # Both should share the same rank
        assert standings[0]["points"] == standings[1]["points"]

    def test_standings_all_zero_scores(self, league_config):
        """All teams at 0 points should still return valid standings."""
        league = _create_league(league_config)
        for uid in range(1, 5):
            _join_league(league, user_id=uid)
        league["scores"] = {uid: 0 for uid in range(1, 5)}
        standings = _get_standings(league)
        assert len(standings) == 4
        assert all(s["points"] == 0 for s in standings)

    def test_standings_with_negative_scores(self, league_config):
        """If the scoring system allows negative points, standings should still work."""
        league = _create_league(league_config)
        _join_league(league, user_id=1)
        _join_league(league, user_id=2)
        league["scores"] = {1: -10, 2: 5}
        standings = _get_standings(league)
        assert standings[0]["user_id"] == 2
        assert standings[1]["user_id"] == 1


class TestLeagueStateTransitions:
    """Edge cases around league lifecycle states."""

    def test_start_draft_with_less_than_two_teams_rejected(self, league_config):
        """Cannot start a draft with fewer than 2 teams."""
        league = _create_league(league_config)
        _join_league(league, user_id=1)
        with pytest.raises(ValueError):
            _start_league_draft(league)

    def test_start_draft_when_already_drafting_rejected(self, league_config):
        """Cannot start a draft that is already in progress."""
        league = _create_league(league_config)
        _join_league(league, user_id=1)
        _join_league(league, user_id=2)
        _start_league_draft(league)
        with pytest.raises(ValueError):
            _start_league_draft(league)

    def test_start_draft_when_league_completed_rejected(self, league_config):
        """Cannot start a draft for a completed league."""
        league = _create_league(league_config)
        league["status"] = "completed"
        with pytest.raises(ValueError):
            _start_league_draft(league)


# ---------------------------------------------------------------------------
# Stub helpers — replace with actual implementation imports when ready
# ---------------------------------------------------------------------------

VALID_DRAFT_TYPES = {"snake", "linear", "auction"}
VALID_SCORING_SYSTEMS = {"standard", "points_per_reception", "head_to_head"}


def _create_league(config: dict) -> dict:
    name = config.get("name")
    if name is None:
        raise TypeError("League name is required")
    if not isinstance(name, str):
        raise TypeError("League name must be a string")
    name = name.strip()
    if not name:
        raise ValueError("League name must not be empty")
    if len(name) > 50:
        raise ValueError("League name must not exceed 50 characters")

    max_teams = config.get("max_teams")
    if max_teams is None:
        raise KeyError("max_teams is required")
    if not isinstance(max_teams, int):
        raise TypeError("max_teams must be an integer")
    if max_teams < 2:
        raise ValueError("max_teams must be at least 2")
    if max_teams > 32:
        raise ValueError("max_teams must not exceed 32")

    draft_type = config.get("draft_type", "snake")
    if draft_type not in VALID_DRAFT_TYPES:
        raise ValueError(f"Invalid draft type: {draft_type}")

    scoring = config.get("scoring_system", "standard")
    if scoring not in VALID_SCORING_SYSTEMS:
        raise ValueError(f"Invalid scoring system: {scoring}")

    return {
        "name": name,
        "max_teams": max_teams,
        "draft_type": draft_type,
        "scoring_system": scoring,
        "members": [],
        "status": "open",
        "scores": {},
    }


def _join_league(league: dict, user_id) -> dict:
    if user_id is None:
        raise TypeError("user_id must not be None")
    if not isinstance(user_id, int) or user_id < 0:
        raise ValueError("user_id must be a non-negative integer")
    if league["status"] != "open":
        raise ValueError("Cannot join a league that is not open")
    if len(league["members"]) >= league["max_teams"]:
        raise ValueError("League is full")
    if user_id in league["members"]:
        raise ValueError("User already in league")
    league["members"].append(user_id)
    return league


def _leave_league(league: dict, user_id: int) -> dict:
    if league["status"] != "open":
        raise ValueError("Cannot leave a league that is not open")
    if user_id not in league["members"]:
        raise ValueError("User is not a member of this league")
    league["members"].remove(user_id)
    return league


def _get_standings(league: dict) -> list:
    scores = league.get("scores", {})
    standings = [{"user_id": uid, "points": pts} for uid, pts in scores.items()]
    standings.sort(key=lambda x: x["points"], reverse=True)
    return standings


def _start_league_draft(league: dict) -> dict:
    if league["status"] == "completed":
        raise ValueError("League is already completed")
    if league["status"] == "drafting":
        raise ValueError("Draft is already in progress")
    if len(league["members"]) < 2:
        raise ValueError("Need at least 2 teams to start a draft")
    league["status"] = "drafting"
    return league
