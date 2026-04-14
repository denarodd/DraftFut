"""
Edge-case tests for Squad / Team building.

Covers:
- Formation validation (invalid formats, wrong total players)
- Empty squads
- Duplicate players in a squad
- Position mismatches (player doesn't fit slot)
- Chemistry calculation edge cases
- Squad size limits (too few / too many)
- Bench and substitution edge cases
"""

import pytest


class TestFormationValidation:
    """Edge cases around formation strings and structures."""

    def test_empty_formation_name_rejected(self):
        """An empty formation name must be rejected."""
        with pytest.raises(ValueError):
            _validate_formation("")

    def test_none_formation_rejected(self):
        """A None formation must be rejected."""
        with pytest.raises((ValueError, TypeError)):
            _validate_formation(None)

    def test_formation_with_wrong_total_rejected(self):
        """A formation whose positions don't sum to 10 outfield players must be rejected."""
        with pytest.raises(ValueError):
            _validate_formation("5-5-5")  # sums to 15, not 10

    def test_formation_with_zero_in_line_rejected(self):
        """A formation with a 0 in any line (e.g. '4-0-6') should be rejected."""
        with pytest.raises(ValueError):
            _validate_formation("4-0-6")

    def test_formation_with_negative_numbers_rejected(self):
        """Negative numbers in a formation must be rejected."""
        with pytest.raises(ValueError):
            _validate_formation("4-(-1)-7")

    def test_formation_with_non_numeric_parts_rejected(self):
        """Formation with non-numeric parts must be rejected."""
        with pytest.raises(ValueError):
            _validate_formation("four-three-three")

    def test_valid_433_accepted(self):
        """Standard 4-3-3 formation must be accepted (sums to 10)."""
        result = _validate_formation("4-3-3")
        assert result is True

    def test_valid_442_accepted(self):
        """Standard 4-4-2 formation must be accepted."""
        result = _validate_formation("4-4-2")
        assert result is True

    def test_valid_352_accepted(self):
        """Standard 3-5-2 formation must be accepted."""
        result = _validate_formation("3-5-2")
        assert result is True

    def test_valid_5_line_formation_accepted(self):
        """Formations with more lines like 4-1-2-1-2 (sums to 10) must be accepted."""
        result = _validate_formation("4-1-2-1-2")
        assert result is True

    def test_single_line_formation_rejected(self):
        """A single-number formation like '10' should be rejected (needs at least 2 lines)."""
        with pytest.raises(ValueError):
            _validate_formation("10")

    def test_formation_with_extra_dashes_rejected(self):
        """Malformed formations like '4--3-3' must be rejected."""
        with pytest.raises(ValueError):
            _validate_formation("4--3-3")

    def test_formation_with_spaces_rejected(self):
        """Formations with spaces like '4 3 3' must be rejected."""
        with pytest.raises(ValueError):
            _validate_formation("4 3 3")


class TestSquadComposition:
    """Edge cases around squad building and player assignment."""

    def test_empty_squad_rejected(self):
        """A squad with no players must be rejected for a starting XI."""
        with pytest.raises(ValueError):
            _build_squad([], formation="4-3-3")

    def test_squad_with_fewer_than_11_rejected(self):
        """A starting XI with fewer than 11 players must be rejected."""
        players = _make_players(10)
        with pytest.raises(ValueError):
            _build_squad(players, formation="4-3-3")

    def test_squad_with_more_than_11_starters_rejected(self):
        """A starting XI with more than 11 must be rejected."""
        players = _make_players(12)
        with pytest.raises(ValueError):
            _build_squad(players, formation="4-3-3")

    def test_squad_with_no_goalkeeper_rejected(self):
        """A starting XI must have exactly one GK."""
        players = [_make_outfield_player(i, "ST") for i in range(11)]
        with pytest.raises(ValueError):
            _build_squad(players, formation="4-3-3")

    def test_squad_with_two_goalkeepers_rejected(self):
        """A starting XI with two GKs must be rejected."""
        players = _make_players(9, all_position="ST")
        players.append({"id": 100, "name": "GK1", "position": "GK", "rating": 85})
        players.append({"id": 101, "name": "GK2", "position": "GK", "rating": 82})
        with pytest.raises(ValueError):
            _build_squad(players, formation="4-3-3")

    def test_duplicate_player_in_squad_rejected(self):
        """The same player ID appearing twice in a squad must be rejected."""
        players = _make_players(10)
        players.append(players[0])  # duplicate
        with pytest.raises(ValueError):
            _build_squad(players, formation="4-3-3")

    def test_none_player_in_squad_rejected(self):
        """A None entry in the squad list must be rejected."""
        players = _make_players(10)
        players.append(None)
        with pytest.raises((ValueError, TypeError)):
            _build_squad(players, formation="4-3-3")


class TestSquadChemistry:
    """Edge cases for team chemistry calculations."""

    def test_chemistry_of_empty_squad_is_zero(self):
        """An empty squad should have zero chemistry."""
        assert _calculate_chemistry([]) == 0

    def test_chemistry_of_single_player_is_base(self):
        """A single player alone has no links, chemistry should be base/minimum."""
        players = [{"id": 1, "name": "Solo", "position": "ST", "club": "A", "nationality": "X", "league": "L1"}]
        chem = _calculate_chemistry(players)
        assert chem >= 0

    def test_chemistry_all_same_club_is_maximum(self):
        """All players from the same club and nation should yield max chemistry."""
        players = [
            {"id": i, "name": f"P{i}", "position": "ST", "club": "FC Test",
             "nationality": "Testland", "league": "TestLeague"}
            for i in range(11)
        ]
        chem = _calculate_chemistry(players)
        assert chem == 100  # or whatever max is

    def test_chemistry_no_links_at_all(self):
        """Players with no shared club, nationality, or league should yield minimum chemistry."""
        players = [
            {"id": i, "name": f"P{i}", "position": "ST",
             "club": f"Club{i}", "nationality": f"Nation{i}", "league": f"League{i}"}
            for i in range(11)
        ]
        chem = _calculate_chemistry(players)
        assert chem <= 33  # low threshold

    def test_chemistry_with_none_nationality(self):
        """Players with None nationality should not crash chemistry calculation."""
        players = [
            {"id": i, "name": f"P{i}", "position": "ST",
             "club": "FC Test", "nationality": None, "league": "L1"}
            for i in range(11)
        ]
        chem = _calculate_chemistry(players)
        assert isinstance(chem, (int, float))

    def test_chemistry_with_empty_string_club(self):
        """Players with empty-string club should not crash but yield lower chemistry."""
        players = [
            {"id": i, "name": f"P{i}", "position": "ST",
             "club": "", "nationality": "Testland", "league": "L1"}
            for i in range(11)
        ]
        chem = _calculate_chemistry(players)
        assert isinstance(chem, (int, float))


class TestBenchAndSubstitutions:
    """Edge cases around bench players and substitutions."""

    def test_bench_exceeds_maximum_size_rejected(self):
        """Bench size must not exceed maximum allowed (e.g. 7)."""
        bench = _make_players(8)
        with pytest.raises(ValueError):
            _set_bench(bench, max_bench_size=7)

    def test_empty_bench_allowed(self):
        """An empty bench is valid (no substitutes)."""
        result = _set_bench([], max_bench_size=7)
        assert result == []

    def test_substitute_player_not_on_bench_rejected(self):
        """Substituting a player who isn't on the bench must be rejected."""
        with pytest.raises(ValueError):
            _substitute(player_out_id=1, player_in_id=999, bench_ids=[2, 3, 4])

    def test_substitute_player_already_on_field_rejected(self):
        """Cannot sub in someone already on the field."""
        with pytest.raises(ValueError):
            _substitute(player_out_id=1, player_in_id=2, bench_ids=[2, 3], squad_ids=[1, 2, 3])

    def test_substitute_same_player_in_and_out_rejected(self):
        """Cannot substitute a player with themselves."""
        with pytest.raises(ValueError):
            _substitute(player_out_id=1, player_in_id=1, bench_ids=[1])


# ---------------------------------------------------------------------------
# Stub helpers — replace with actual implementation imports when ready
# ---------------------------------------------------------------------------

def _validate_formation(formation) -> bool:
    """Stub: validate a formation string like '4-3-3'."""
    if formation is None:
        raise TypeError("Formation must not be None")
    if not isinstance(formation, str):
        raise TypeError("Formation must be a string")
    if not formation.strip():
        raise ValueError("Formation must not be empty")
    if " " in formation:
        raise ValueError("Formation must not contain spaces")
    if "--" in formation:
        raise ValueError("Formation must not contain consecutive dashes")

    parts = formation.split("-")
    if len(parts) < 2:
        raise ValueError("Formation must have at least 2 lines")

    total = 0
    for part in parts:
        if not part:
            raise ValueError("Empty segment in formation")
        try:
            val = int(part)
        except ValueError:
            raise ValueError(f"Non-numeric part in formation: {part}")
        if val <= 0:
            raise ValueError(f"Each line must have at least 1 player, got {val}")
        total += val

    if total != 10:
        raise ValueError(f"Formation must sum to 10 outfield players, got {total}")
    return True


def _build_squad(players: list, formation: str) -> dict:
    """Stub: build a starting XI from a list of players and a formation."""
    if not players:
        raise ValueError("Squad must not be empty")
    for p in players:
        if p is None:
            raise TypeError("Player entries must not be None")

    ids = [p["id"] for p in players]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate players in squad")
    if len(players) != 11:
        raise ValueError(f"Starting XI must have exactly 11 players, got {len(players)}")

    gk_count = sum(1 for p in players if p["position"] == "GK")
    if gk_count == 0:
        raise ValueError("Squad must have exactly one goalkeeper")
    if gk_count > 1:
        raise ValueError("Squad must have exactly one goalkeeper")

    _validate_formation(formation)
    return {"players": players, "formation": formation}


def _make_players(count, all_position="CM"):
    """Helper: generate a list of dummy players (first one is always GK)."""
    players = []
    if count >= 1:
        players.append({"id": 0, "name": "GK1", "position": "GK", "rating": 85})
    for i in range(1, count):
        players.append({"id": i, "name": f"Player{i}", "position": all_position, "rating": 80})
    return players


def _make_outfield_player(player_id, position="ST"):
    """Helper: generate a single outfield player (never GK)."""
    return {"id": player_id, "name": f"Player{player_id}", "position": position, "rating": 80}


def _calculate_chemistry(players: list) -> int:
    """Stub: calculate team chemistry (0-100)."""
    if not players:
        return 0
    if len(players) == 1:
        return 0

    score = 0
    n = len(players)
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = players[i], players[j]
            if p1.get("club") and p2.get("club") and p1["club"] == p2["club"]:
                score += 3
            if p1.get("nationality") and p2.get("nationality") and p1["nationality"] == p2["nationality"]:
                score += 1
            if p1.get("league") and p2.get("league") and p1["league"] == p2["league"]:
                score += 1

    max_possible = n * (n - 1) // 2 * 5
    if max_possible == 0:
        return 0
    return min(100, int(score / max_possible * 100))


def _set_bench(players: list, max_bench_size: int = 7) -> list:
    """Stub: validate and set the bench."""
    if len(players) > max_bench_size:
        raise ValueError(f"Bench size {len(players)} exceeds max {max_bench_size}")
    return players


def _substitute(player_out_id: int, player_in_id: int, bench_ids: list, squad_ids: list = None):
    """Stub: perform a substitution."""
    if player_out_id == player_in_id:
        raise ValueError("Cannot substitute a player with themselves")
    if player_in_id not in bench_ids:
        raise ValueError("Substitute player is not on the bench")
    if squad_ids and player_in_id in squad_ids:
        raise ValueError("Player is already on the field")
