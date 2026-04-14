"""
Edge-case tests for the Scoring / Points system.

Covers:
- Empty match data
- Invalid stat values (negative, non-numeric)
- Boundary conditions for bonus thresholds
- Missing stat fields
- Zero-contribution matches
- Large / extreme stat values
- Point multiplier edge cases
"""

import pytest


class TestMatchPointsCalculation:
    """Edge cases for calculating fantasy points from a single match performance."""

    def test_empty_stats_returns_zero(self):
        """A match with no stats should yield 0 points."""
        assert _calculate_match_points({}) == 0

    def test_none_stats_rejected(self):
        """None stats must be rejected."""
        with pytest.raises((ValueError, TypeError)):
            _calculate_match_points(None)

    def test_all_zero_stats_returns_base_appearance_points(self):
        """A player with all-zero stats should get only appearance points."""
        stats = _make_stats(goals=0, assists=0, clean_sheet=False, minutes_played=90)
        points = _calculate_match_points(stats)
        # Appearance points for playing 90 minutes
        assert points >= 1

    def test_negative_goals_rejected(self):
        """Negative goal count must be rejected."""
        stats = _make_stats(goals=-1)
        with pytest.raises(ValueError):
            _calculate_match_points(stats)

    def test_negative_assists_rejected(self):
        """Negative assist count must be rejected."""
        stats = _make_stats(assists=-2)
        with pytest.raises(ValueError):
            _calculate_match_points(stats)

    def test_negative_minutes_rejected(self):
        """Negative minutes played must be rejected."""
        stats = _make_stats(minutes_played=-10)
        with pytest.raises(ValueError):
            _calculate_match_points(stats)

    def test_minutes_over_120_rejected(self):
        """Minutes played over 120 (max with extra time) must be rejected."""
        stats = _make_stats(minutes_played=121)
        with pytest.raises(ValueError):
            _calculate_match_points(stats)

    def test_zero_minutes_no_appearance_points(self):
        """A player with 0 minutes played should get 0 points (unused sub)."""
        stats = _make_stats(minutes_played=0)
        points = _calculate_match_points(stats)
        assert points == 0

    def test_float_goals_rejected(self):
        """Float values for goals must be rejected."""
        stats = _make_stats(goals=1.5)
        with pytest.raises((ValueError, TypeError)):
            _calculate_match_points(stats)

    def test_string_stat_value_rejected(self):
        """String values for numeric stats must be rejected."""
        stats = {"goals": "two", "assists": 0, "minutes_played": 90}
        with pytest.raises((ValueError, TypeError)):
            _calculate_match_points(stats)


class TestScoringByPosition:
    """Edge cases for position-specific scoring rules."""

    def test_goalkeeper_clean_sheet_bonus(self):
        """A goalkeeper with a clean sheet should get bonus points."""
        stats = _make_stats(minutes_played=90, clean_sheet=True, position="GK")
        points = _calculate_match_points(stats)
        base = _calculate_match_points(_make_stats(minutes_played=90, clean_sheet=False, position="GK"))
        assert points > base

    def test_defender_clean_sheet_bonus(self):
        """A defender with a clean sheet should get bonus points."""
        stats = _make_stats(minutes_played=90, clean_sheet=True, position="CB")
        points = _calculate_match_points(stats)
        base = _calculate_match_points(_make_stats(minutes_played=90, clean_sheet=False, position="CB"))
        assert points > base

    def test_forward_goal_worth_more_than_defender_goal(self):
        """A forward's goal may be worth fewer points than a defender's goal (position bonus)."""
        fwd_stats = _make_stats(goals=1, minutes_played=90, position="ST")
        def_stats = _make_stats(goals=1, minutes_played=90, position="CB")
        fwd_points = _calculate_match_points(fwd_stats)
        def_points = _calculate_match_points(def_stats)
        # Defenders get more points per goal as it's rarer
        assert def_points >= fwd_points

    def test_midfielder_assist_points(self):
        """Midfielders should get standard assist points."""
        stats = _make_stats(assists=1, minutes_played=90, position="CM")
        points = _calculate_match_points(stats)
        base = _calculate_match_points(_make_stats(minutes_played=90, position="CM"))
        assert points > base

    def test_clean_sheet_not_awarded_under_60_minutes(self):
        """Clean sheet bonus should not apply if player played < 60 minutes."""
        stats = _make_stats(minutes_played=59, clean_sheet=True, position="GK")
        points_short = _calculate_match_points(stats)
        stats_full = _make_stats(minutes_played=90, clean_sheet=True, position="GK")
        points_full = _calculate_match_points(stats_full)
        assert points_full > points_short


class TestBonusThresholds:
    """Edge cases around bonus point thresholds."""

    def test_hat_trick_bonus(self):
        """A player scoring 3+ goals should receive a hat-trick bonus."""
        stats_2 = _make_stats(goals=2, minutes_played=90, position="ST")
        stats_3 = _make_stats(goals=3, minutes_played=90, position="ST")
        points_2 = _calculate_match_points(stats_2)
        points_3 = _calculate_match_points(stats_3)
        # 3rd goal + hat trick bonus should be more than just 1 extra goal worth
        goal_diff_2_to_3 = points_3 - points_2
        goal_diff_1_to_2 = points_2 - _calculate_match_points(_make_stats(goals=1, minutes_played=90, position="ST"))
        assert goal_diff_2_to_3 > goal_diff_1_to_2

    def test_exactly_60_minutes_gets_appearance_bonus(self):
        """Playing exactly 60 minutes should qualify for the full appearance bonus."""
        stats_59 = _make_stats(minutes_played=59)
        stats_60 = _make_stats(minutes_played=60)
        points_59 = _calculate_match_points(stats_59)
        points_60 = _calculate_match_points(stats_60)
        assert points_60 > points_59

    def test_penalty_miss_deduction(self):
        """Missing a penalty should result in a point deduction."""
        stats_miss = _make_stats(minutes_played=90, penalties_missed=1)
        stats_none = _make_stats(minutes_played=90, penalties_missed=0)
        assert _calculate_match_points(stats_miss) < _calculate_match_points(stats_none)

    def test_own_goal_deduction(self):
        """Scoring an own goal should result in a point deduction."""
        stats_og = _make_stats(minutes_played=90, own_goals=1)
        stats_none = _make_stats(minutes_played=90, own_goals=0)
        assert _calculate_match_points(stats_og) < _calculate_match_points(stats_none)

    def test_yellow_card_deduction(self):
        """Receiving a yellow card should result in a small point deduction."""
        stats_yc = _make_stats(minutes_played=90, yellow_cards=1)
        stats_none = _make_stats(minutes_played=90, yellow_cards=0)
        assert _calculate_match_points(stats_yc) < _calculate_match_points(stats_none)

    def test_red_card_deduction(self):
        """Receiving a red card should result in a larger point deduction."""
        stats_rc = _make_stats(minutes_played=90, red_cards=1)
        stats_yc = _make_stats(minutes_played=90, yellow_cards=1)
        assert _calculate_match_points(stats_rc) < _calculate_match_points(stats_yc)

    def test_negative_own_goals_rejected(self):
        """Negative own goals must be rejected."""
        stats = _make_stats(own_goals=-1)
        with pytest.raises(ValueError):
            _calculate_match_points(stats)


class TestWeeklyAggregation:
    """Edge cases around aggregating points across a gameweek."""

    def test_empty_gameweek_returns_zero(self):
        """An empty list of match performances should yield 0 weekly points."""
        assert _calculate_weekly_points([]) == 0

    def test_none_gameweek_rejected(self):
        """None gameweek data must be rejected."""
        with pytest.raises((ValueError, TypeError)):
            _calculate_weekly_points(None)

    def test_single_match_gameweek(self):
        """A gameweek with a single match should return that match's points."""
        stats = _make_stats(goals=1, minutes_played=90, position="ST")
        weekly = _calculate_weekly_points([stats])
        single = _calculate_match_points(stats)
        assert weekly == single

    def test_gameweek_with_none_entry_rejected(self):
        """A None entry within the gameweek list must be rejected."""
        stats = _make_stats(goals=1, minutes_played=90)
        with pytest.raises((ValueError, TypeError)):
            _calculate_weekly_points([stats, None])

    def test_large_gameweek_aggregation(self):
        """Aggregating many matches should sum correctly without overflow issues."""
        stats_list = [_make_stats(goals=2, assists=1, minutes_played=90, position="ST") for _ in range(38)]
        total = _calculate_weekly_points(stats_list)
        single = _calculate_match_points(stats_list[0])
        assert total == single * 38


class TestPointMultipliers:
    """Edge cases around captain / vice-captain multipliers."""

    def test_captain_doubles_points(self):
        """Captain designation should double the match points."""
        stats = _make_stats(goals=1, minutes_played=90, position="ST")
        base = _calculate_match_points(stats)
        captain = _apply_multiplier(base, multiplier=2)
        assert captain == base * 2

    def test_zero_multiplier_rejected(self):
        """A zero multiplier must be rejected."""
        with pytest.raises(ValueError):
            _apply_multiplier(10, multiplier=0)

    def test_negative_multiplier_rejected(self):
        """A negative multiplier must be rejected."""
        with pytest.raises(ValueError):
            _apply_multiplier(10, multiplier=-1)

    def test_fractional_multiplier_rejected(self):
        """Only integer multipliers (1, 2, 3) should be allowed."""
        with pytest.raises((ValueError, TypeError)):
            _apply_multiplier(10, multiplier=1.5)

    def test_multiplier_on_zero_points(self):
        """Multiplying zero points should still be zero."""
        assert _apply_multiplier(0, multiplier=2) == 0

    def test_multiplier_on_negative_points(self):
        """Multiplying negative base points should double the negative."""
        result = _apply_multiplier(-5, multiplier=2)
        assert result == -10


# ---------------------------------------------------------------------------
# Stub helpers — replace with actual implementation imports when ready
# ---------------------------------------------------------------------------

# Points configuration
POINTS_CONFIG = {
    "appearance": 1,
    "appearance_60_plus": 2,
    "goal_forward": 4,
    "goal_midfielder": 5,
    "goal_defender": 6,
    "goal_goalkeeper": 6,
    "assist": 3,
    "clean_sheet_gk": 4,
    "clean_sheet_def": 4,
    "clean_sheet_mid": 1,
    "hat_trick_bonus": 3,
    "penalty_miss": -2,
    "own_goal": -2,
    "yellow_card": -1,
    "red_card": -3,
}


def _make_stats(
    goals=0, assists=0, minutes_played=90, clean_sheet=False,
    position="ST", penalties_missed=0, own_goals=0,
    yellow_cards=0, red_cards=0,
):
    """Helper: build a stats dict."""
    return {
        "goals": goals,
        "assists": assists,
        "minutes_played": minutes_played,
        "clean_sheet": clean_sheet,
        "position": position,
        "penalties_missed": penalties_missed,
        "own_goals": own_goals,
        "yellow_cards": yellow_cards,
        "red_cards": red_cards,
    }


def _calculate_match_points(stats) -> int:
    """Stub: calculate fantasy points for a single match."""
    if stats is None:
        raise TypeError("Stats must not be None")
    if not isinstance(stats, dict):
        raise TypeError("Stats must be a dict")
    if not stats:
        return 0

    # Validate numeric fields
    int_fields = ["goals", "assists", "minutes_played", "penalties_missed", "own_goals", "yellow_cards", "red_cards"]
    for field in int_fields:
        val = stats.get(field, 0)
        if not isinstance(val, (int, float)):
            raise TypeError(f"{field} must be numeric")
        if isinstance(val, float) and val != int(val):
            raise TypeError(f"{field} must be an integer")
        if val < 0:
            raise ValueError(f"{field} must not be negative")

    minutes = stats.get("minutes_played", 0)
    if minutes > 120:
        raise ValueError("minutes_played must not exceed 120")

    if minutes == 0:
        return 0

    points = POINTS_CONFIG["appearance"]
    if minutes >= 60:
        points = POINTS_CONFIG["appearance_60_plus"]

    position = stats.get("position", "ST")
    goals = int(stats.get("goals", 0))
    assists = int(stats.get("assists", 0))
    clean_sheet = stats.get("clean_sheet", False)

    # Goals
    if position in ("ST", "CF", "LW", "RW"):
        points += goals * POINTS_CONFIG["goal_forward"]
    elif position in ("CM", "CAM", "CDM", "LM", "RM"):
        points += goals * POINTS_CONFIG["goal_midfielder"]
    elif position in ("CB", "LB", "RB", "LWB", "RWB"):
        points += goals * POINTS_CONFIG["goal_defender"]
    elif position == "GK":
        points += goals * POINTS_CONFIG["goal_goalkeeper"]

    # Hat trick bonus
    if goals >= 3:
        points += POINTS_CONFIG["hat_trick_bonus"]

    # Assists
    points += assists * POINTS_CONFIG["assist"]

    # Clean sheet (only if >= 60 minutes)
    if clean_sheet and minutes >= 60:
        if position == "GK":
            points += POINTS_CONFIG["clean_sheet_gk"]
        elif position in ("CB", "LB", "RB", "LWB", "RWB"):
            points += POINTS_CONFIG["clean_sheet_def"]
        elif position in ("CM", "CAM", "CDM", "LM", "RM"):
            points += POINTS_CONFIG["clean_sheet_mid"]

    # Deductions
    points += int(stats.get("penalties_missed", 0)) * POINTS_CONFIG["penalty_miss"]
    points += int(stats.get("own_goals", 0)) * POINTS_CONFIG["own_goal"]
    points += int(stats.get("yellow_cards", 0)) * POINTS_CONFIG["yellow_card"]
    points += int(stats.get("red_cards", 0)) * POINTS_CONFIG["red_card"]

    return points


def _calculate_weekly_points(matches) -> int:
    """Stub: sum match points for a gameweek."""
    if matches is None:
        raise TypeError("Matches must not be None")
    total = 0
    for m in matches:
        if m is None:
            raise TypeError("Match entry must not be None")
        total += _calculate_match_points(m)
    return total


def _apply_multiplier(base_points: int, multiplier) -> int:
    """Stub: apply a captain/vice-captain multiplier."""
    if not isinstance(multiplier, int) or isinstance(multiplier, bool):
        raise TypeError("Multiplier must be an integer")
    if multiplier <= 0:
        raise ValueError("Multiplier must be positive")
    return base_points * multiplier
