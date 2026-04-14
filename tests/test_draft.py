"""
Edge-case tests for the Draft system.

Covers:
- Empty player pool
- Invalid draft configurations (zero rounds, negative timers)
- Out-of-turn picks
- Drafting already-drafted players
- Drafting from an exhausted pool
- Snake draft order edge cases
- Timer expiration behaviour
- Single-player and maximum-player drafts
"""

import pytest


class TestDraftConfiguration:
    """Edge cases around draft setup / configuration."""

    def test_zero_rounds_rejected(self, draft_config):
        """A draft with zero rounds must be rejected."""
        draft_config["num_rounds"] = 0
        with pytest.raises(ValueError):
            _create_draft(draft_config, num_players=4)

    def test_negative_rounds_rejected(self, draft_config):
        """Negative round count must be rejected."""
        draft_config["num_rounds"] = -3
        with pytest.raises(ValueError):
            _create_draft(draft_config, num_players=4)

    def test_zero_time_per_pick_rejected(self, draft_config):
        """A draft with zero seconds per pick must be rejected."""
        draft_config["time_per_pick_seconds"] = 0
        with pytest.raises(ValueError):
            _create_draft(draft_config, num_players=4)

    def test_negative_time_per_pick_rejected(self, draft_config):
        """Negative time per pick must be rejected."""
        draft_config["time_per_pick_seconds"] = -10
        with pytest.raises(ValueError):
            _create_draft(draft_config, num_players=4)

    def test_max_players_less_than_two_rejected(self, draft_config):
        """A draft needs at least 2 participants."""
        draft_config["max_players"] = 1
        with pytest.raises(ValueError):
            _create_draft(draft_config, num_players=1)

    def test_max_players_zero_rejected(self, draft_config):
        """Zero max players must be rejected."""
        draft_config["max_players"] = 0
        with pytest.raises(ValueError):
            _create_draft(draft_config, num_players=0)

    def test_non_integer_rounds_rejected(self, draft_config):
        """Float or string round count must be rejected."""
        draft_config["num_rounds"] = 5.5
        with pytest.raises((ValueError, TypeError)):
            _create_draft(draft_config, num_players=4)

    def test_extremely_large_rounds_rejected(self, draft_config):
        """Unreasonably large round counts (>100) should be rejected."""
        draft_config["num_rounds"] = 500
        with pytest.raises(ValueError):
            _create_draft(draft_config, num_players=4)

    def test_missing_config_key_rejected(self):
        """An incomplete config dict missing required keys must be rejected."""
        incomplete = {"num_rounds": 10}
        with pytest.raises((ValueError, KeyError)):
            _create_draft(incomplete, num_players=4)


class TestDraftPlayerPool:
    """Edge cases around the available player pool."""

    def test_empty_player_pool_rejected(self, draft_config):
        """Starting a draft with an empty player pool must be rejected."""
        draft = _create_draft(draft_config, num_players=4)
        with pytest.raises(ValueError):
            _start_draft(draft, player_pool=[])

    def test_player_pool_smaller_than_total_picks(self, draft_config):
        """If pool has fewer players than total required picks, draft must be rejected."""
        draft_config["num_rounds"] = 10
        draft = _create_draft(draft_config, num_players=4)
        tiny_pool = [{"id": i, "name": f"P{i}", "position": "ST", "rating": 80} for i in range(5)]
        # 4 players * 10 rounds = 40 picks needed, but only 5 available
        with pytest.raises(ValueError):
            _start_draft(draft, player_pool=tiny_pool)

    def test_duplicate_player_ids_in_pool_rejected(self, draft_config):
        """Player pool must not contain duplicate player IDs."""
        draft = _create_draft(draft_config, num_players=4)
        dup_pool = [
            {"id": 1, "name": "Player A", "position": "ST", "rating": 90},
            {"id": 1, "name": "Player A Copy", "position": "ST", "rating": 90},
        ]
        with pytest.raises(ValueError):
            _start_draft(draft, player_pool=dup_pool)

    def test_player_pool_with_none_entry_rejected(self, draft_config):
        """A None entry in the player pool must be rejected."""
        draft = _create_draft(draft_config, num_players=2)
        pool = [
            {"id": 1, "name": "Player A", "position": "ST", "rating": 90},
            None,
        ]
        with pytest.raises((ValueError, TypeError)):
            _start_draft(draft, player_pool=pool)


class TestDraftPicking:
    """Edge cases around the pick mechanism."""

    def test_pick_already_drafted_player_rejected(self):
        """Picking a player that has already been drafted must be rejected."""
        draft = _make_active_draft(num_players=2, pool_size=10)
        _make_pick(draft, player_id=1, drafter_index=0)
        with pytest.raises(ValueError):
            _make_pick(draft, player_id=1, drafter_index=1)

    def test_pick_player_not_in_pool_rejected(self):
        """Picking a player ID that doesn't exist in the pool must be rejected."""
        draft = _make_active_draft(num_players=2, pool_size=20)
        with pytest.raises(ValueError):
            _make_pick(draft, player_id=999, drafter_index=0)

    def test_out_of_turn_pick_rejected(self):
        """A participant picking out of turn must be rejected."""
        draft = _make_active_draft(num_players=2, pool_size=10)
        # It's drafter 0's turn first
        with pytest.raises(ValueError):
            _make_pick(draft, player_id=1, drafter_index=1)

    def test_pick_with_negative_player_id_rejected(self):
        """A negative player ID is invalid."""
        draft = _make_active_draft(num_players=2, pool_size=10)
        with pytest.raises(ValueError):
            _make_pick(draft, player_id=-1, drafter_index=0)

    def test_pick_with_none_player_id_rejected(self):
        """A None player ID must be rejected."""
        draft = _make_active_draft(num_players=2, pool_size=10)
        with pytest.raises((ValueError, TypeError)):
            _make_pick(draft, player_id=None, drafter_index=0)

    def test_pick_after_draft_completed_rejected(self):
        """No picks allowed after all rounds are exhausted."""
        draft = _make_active_draft(num_players=2, pool_size=20, num_rounds=1)
        _make_pick(draft, player_id=1, drafter_index=0)
        _make_pick(draft, player_id=2, drafter_index=1)
        with pytest.raises(ValueError):
            _make_pick(draft, player_id=3, drafter_index=0)


class TestSnakeDraftOrder:
    """Edge cases around snake-draft turn order."""

    def test_snake_draft_reverses_on_even_rounds(self):
        """In a snake draft with 3 players, round 2 goes 2→1→0."""
        draft = _make_active_draft(num_players=3, pool_size=30, num_rounds=2, snake=True)
        expected_order = [0, 1, 2, 2, 1, 0]
        for i, expected_drafter in enumerate(expected_order):
            assert _current_drafter(draft) == expected_drafter, f"Pick {i}: expected drafter {expected_drafter}"
            _make_pick(draft, player_id=i + 1, drafter_index=expected_drafter)

    def test_non_snake_draft_same_order_every_round(self):
        """In a non-snake draft, order stays 0→1→2 every round."""
        draft = _make_active_draft(num_players=3, pool_size=30, num_rounds=2, snake=False)
        expected_order = [0, 1, 2, 0, 1, 2]
        for i, expected_drafter in enumerate(expected_order):
            assert _current_drafter(draft) == expected_drafter, f"Pick {i}: expected drafter {expected_drafter}"
            _make_pick(draft, player_id=i + 1, drafter_index=expected_drafter)

    def test_two_player_snake_draft(self):
        """Smallest snake draft: 2 players alternate 0,1,1,0,0,1,..."""
        draft = _make_active_draft(num_players=2, pool_size=20, num_rounds=3, snake=True)
        expected_order = [0, 1, 1, 0, 0, 1]
        for i, expected_drafter in enumerate(expected_order):
            assert _current_drafter(draft) == expected_drafter
            _make_pick(draft, player_id=i + 1, drafter_index=expected_drafter)


class TestDraftTimerEdgeCases:
    """Edge cases around the pick timer."""

    def test_pick_at_exact_time_limit_accepted(self):
        """A pick made exactly at the deadline should still be valid."""
        draft = _make_active_draft(num_players=2, pool_size=10, time_per_pick=60)
        # Simulate pick at t=60s (boundary)
        result = _make_pick(draft, player_id=1, drafter_index=0, elapsed_seconds=60)
        assert result["accepted"] is True

    def test_pick_after_time_limit_triggers_auto_pick_or_skip(self):
        """A pick arriving after the deadline must be rejected or trigger auto-pick."""
        draft = _make_active_draft(num_players=2, pool_size=10, time_per_pick=60)
        with pytest.raises(ValueError):
            _make_pick(draft, player_id=1, drafter_index=0, elapsed_seconds=61)


# ---------------------------------------------------------------------------
# Stub helpers — replace with actual implementation imports when ready
# ---------------------------------------------------------------------------

def _create_draft(config: dict, num_players: int) -> dict:
    """Stub: validate and create a draft from config."""
    rounds = config.get("num_rounds")
    if rounds is None:
        raise KeyError("num_rounds is required")
    if not isinstance(rounds, int) or isinstance(rounds, bool):
        raise TypeError("num_rounds must be an integer")
    if rounds <= 0:
        raise ValueError("num_rounds must be positive")
    if rounds > 100:
        raise ValueError("num_rounds must be <= 100")

    time_pp = config.get("time_per_pick_seconds")
    if time_pp is None:
        raise KeyError("time_per_pick_seconds is required")
    if time_pp <= 0:
        raise ValueError("time_per_pick_seconds must be positive")

    max_p = config.get("max_players")
    if max_p is None:
        raise KeyError("max_players is required")
    if max_p < 2:
        raise ValueError("max_players must be at least 2")
    if num_players < 2:
        raise ValueError("Need at least 2 participants")

    snake = config.get("snake_draft", True)

    return {
        "config": config,
        "num_players": num_players,
        "snake": snake,
        "picks": [],
        "current_round": 0,
        "current_pick_in_round": 0,
        "started": False,
        "completed": False,
        "player_pool": [],
    }


def _start_draft(draft: dict, player_pool: list) -> dict:
    """Stub: start the draft with a given player pool."""
    if not player_pool:
        raise ValueError("Player pool must not be empty")
    for entry in player_pool:
        if entry is None:
            raise TypeError("Player pool entries must not be None")
    ids = [p["id"] for p in player_pool]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate player IDs in pool")
    total_picks = draft["config"]["num_rounds"] * draft["num_players"]
    if len(player_pool) < total_picks:
        raise ValueError("Player pool too small for the number of picks required")
    draft["player_pool"] = player_pool
    draft["started"] = True
    return draft


def _make_active_draft(num_players=2, pool_size=10, num_rounds=5, snake=True, time_per_pick=60):
    """Helper: create and start a draft ready for picks."""
    config = {
        "num_rounds": num_rounds,
        "time_per_pick_seconds": time_per_pick,
        "max_players": max(num_players, 2),
        "snake_draft": snake,
    }
    draft = _create_draft(config, num_players)
    pool = [{"id": i, "name": f"Player {i}", "position": "ST", "rating": 80} for i in range(1, pool_size + 1)]
    _start_draft(draft, pool)
    return draft


def _current_drafter(draft: dict) -> int:
    """Return the index of the participant whose turn it is."""
    n = draft["num_players"]
    rnd = draft["current_round"]
    pick = draft["current_pick_in_round"]
    if draft["snake"] and rnd % 2 == 1:
        return n - 1 - pick
    return pick


def _make_pick(draft: dict, player_id, drafter_index: int, elapsed_seconds: int = 0) -> dict:
    """Stub: execute a draft pick."""
    if draft["completed"]:
        raise ValueError("Draft is already completed")
    if player_id is None:
        raise TypeError("player_id must not be None")
    if not isinstance(player_id, int):
        raise TypeError("player_id must be an integer")
    if player_id < 0:
        raise ValueError("player_id must be non-negative")

    time_limit = draft["config"]["time_per_pick_seconds"]
    if elapsed_seconds > time_limit:
        raise ValueError("Pick time expired")

    expected = _current_drafter(draft)
    if drafter_index != expected:
        raise ValueError(f"Not your turn. Expected drafter {expected}, got {drafter_index}")

    pool_ids = {p["id"] for p in draft["player_pool"]}
    drafted_ids = {p["player_id"] for p in draft["picks"]}
    if player_id not in pool_ids:
        raise ValueError(f"Player {player_id} not in pool")
    if player_id in drafted_ids:
        raise ValueError(f"Player {player_id} already drafted")

    draft["picks"].append({"player_id": player_id, "drafter": drafter_index, "round": draft["current_round"]})
    draft["current_pick_in_round"] += 1
    if draft["current_pick_in_round"] >= draft["num_players"]:
        draft["current_pick_in_round"] = 0
        draft["current_round"] += 1
        if draft["current_round"] >= draft["config"]["num_rounds"]:
            draft["completed"] = True

    return {"accepted": True}
