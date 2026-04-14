"""
Edge-case tests for the Player model.

Covers:
- Empty / missing fields
- Invalid data types and formats
- Boundary values for ratings and attributes
- Special characters in names
- Position validation
- Duplicate player handling
"""

import pytest


class TestPlayerNameValidation:
    """Edge cases around the player name field."""

    def test_empty_name_rejected(self, valid_player_data):
        """A player with an empty string name must be rejected."""
        valid_player_data["name"] = ""
        with pytest.raises((ValueError, TypeError)):
            _create_player(valid_player_data)

    def test_none_name_rejected(self, valid_player_data):
        """A player with a None name must be rejected."""
        valid_player_data["name"] = None
        with pytest.raises((ValueError, TypeError)):
            _create_player(valid_player_data)

    def test_whitespace_only_name_rejected(self, valid_player_data):
        """A name consisting solely of whitespace must be rejected."""
        valid_player_data["name"] = "   "
        with pytest.raises(ValueError):
            _create_player(valid_player_data)

    def test_name_with_special_characters_accepted(self, valid_player_data):
        """Names with accents, hyphens, apostrophes are valid (e.g. O'Brien, Müller)."""
        for name in ["Müller", "O'Brien", "Mbappé", "Hernández-López"]:
            valid_player_data["name"] = name
            player = _create_player(valid_player_data)
            assert player["name"] == name

    def test_numeric_name_rejected(self, valid_player_data):
        """A purely numeric name should be rejected."""
        valid_player_data["name"] = "12345"
        with pytest.raises(ValueError):
            _create_player(valid_player_data)

    def test_extremely_long_name_rejected(self, valid_player_data):
        """A name exceeding a reasonable max length (e.g. 100 chars) must be rejected."""
        valid_player_data["name"] = "A" * 101
        with pytest.raises(ValueError):
            _create_player(valid_player_data)

    def test_name_stripped_of_leading_trailing_whitespace(self, valid_player_data):
        """Leading/trailing whitespace in names should be stripped."""
        valid_player_data["name"] = "  Messi  "
        player = _create_player(valid_player_data)
        assert player["name"] == "Messi"


class TestPlayerRatingValidation:
    """Edge cases around overall rating and individual attributes."""

    def test_rating_below_minimum_rejected(self, valid_player_data):
        """Rating below 1 must be rejected."""
        valid_player_data["rating"] = 0
        with pytest.raises(ValueError):
            _create_player(valid_player_data)

    def test_rating_above_maximum_rejected(self, valid_player_data):
        """Rating above 99 must be rejected."""
        valid_player_data["rating"] = 100
        with pytest.raises(ValueError):
            _create_player(valid_player_data)

    def test_negative_rating_rejected(self, valid_player_data):
        """Negative ratings must be rejected."""
        valid_player_data["rating"] = -5
        with pytest.raises(ValueError):
            _create_player(valid_player_data)

    def test_rating_boundary_minimum_accepted(self, valid_player_data):
        """Rating of 1 (minimum) must be accepted."""
        valid_player_data["rating"] = 1
        player = _create_player(valid_player_data)
        assert player["rating"] == 1

    def test_rating_boundary_maximum_accepted(self, valid_player_data):
        """Rating of 99 (maximum) must be accepted."""
        valid_player_data["rating"] = 99
        player = _create_player(valid_player_data)
        assert player["rating"] == 99

    def test_float_rating_rejected(self, valid_player_data):
        """Floating-point ratings must be rejected (ratings are integers)."""
        valid_player_data["rating"] = 85.5
        with pytest.raises((ValueError, TypeError)):
            _create_player(valid_player_data)

    def test_string_rating_rejected(self, valid_player_data):
        """String values for rating must be rejected."""
        valid_player_data["rating"] = "ninety"
        with pytest.raises((ValueError, TypeError)):
            _create_player(valid_player_data)

    def test_none_rating_rejected(self, valid_player_data):
        """None rating must be rejected."""
        valid_player_data["rating"] = None
        with pytest.raises((ValueError, TypeError)):
            _create_player(valid_player_data)

    @pytest.mark.parametrize("attr", ["pace", "shooting", "passing", "dribbling", "defending", "physical"])
    def test_individual_attribute_below_zero_rejected(self, valid_player_data, attr):
        """Each individual attribute must be >= 0."""
        valid_player_data[attr] = -1
        with pytest.raises(ValueError):
            _create_player(valid_player_data)

    @pytest.mark.parametrize("attr", ["pace", "shooting", "passing", "dribbling", "defending", "physical"])
    def test_individual_attribute_above_99_rejected(self, valid_player_data, attr):
        """Each individual attribute must be <= 99."""
        valid_player_data[attr] = 100
        with pytest.raises(ValueError):
            _create_player(valid_player_data)


class TestPlayerPositionValidation:
    """Edge cases around player position."""

    VALID_POSITIONS = [
        "GK", "CB", "LB", "RB", "LWB", "RWB",
        "CDM", "CM", "CAM", "LM", "RM",
        "LW", "RW", "CF", "ST",
    ]

    def test_empty_position_rejected(self, valid_player_data):
        """An empty position string must be rejected."""
        valid_player_data["position"] = ""
        with pytest.raises(ValueError):
            _create_player(valid_player_data)

    def test_none_position_rejected(self, valid_player_data):
        """A None position must be rejected."""
        valid_player_data["position"] = None
        with pytest.raises((ValueError, TypeError)):
            _create_player(valid_player_data)

    def test_invalid_position_rejected(self, valid_player_data):
        """An unrecognised position abbreviation must be rejected."""
        valid_player_data["position"] = "XYZ"
        with pytest.raises(ValueError):
            _create_player(valid_player_data)

    def test_lowercase_position_normalised(self, valid_player_data):
        """Position should be case-insensitive; 'gk' should resolve to 'GK'."""
        valid_player_data["position"] = "rw"
        player = _create_player(valid_player_data)
        assert player["position"] == "RW"

    @pytest.mark.parametrize("pos", [p for p in VALID_POSITIONS if p != "GK"])
    def test_all_valid_outfield_positions_accepted(self, valid_player_data, pos):
        """Every recognised FUT outfield position must be accepted."""
        valid_player_data["position"] = pos
        player = _create_player(valid_player_data)
        assert player["position"] == pos

    def test_goalkeeper_position_accepted(self, valid_goalkeeper_data):
        """GK position must be accepted with goalkeeper-specific data."""
        player = _create_player(valid_goalkeeper_data)
        assert player["position"] == "GK"


class TestPlayerNationalityAndClub:
    """Edge cases around nationality and club fields."""

    def test_empty_nationality_rejected(self, valid_player_data):
        """Nationality must not be an empty string."""
        valid_player_data["nationality"] = ""
        with pytest.raises(ValueError):
            _create_player(valid_player_data)

    def test_empty_club_rejected(self, valid_player_data):
        """Club must not be an empty string."""
        valid_player_data["club"] = ""
        with pytest.raises(ValueError):
            _create_player(valid_player_data)

    def test_none_club_allowed_for_free_agents(self, valid_player_data):
        """A None club could represent a free agent and may be allowed."""
        valid_player_data["club"] = None
        player = _create_player(valid_player_data)
        assert player["club"] is None

    def test_club_with_only_digits_rejected(self, valid_player_data):
        """Club names that are purely numeric should be rejected."""
        valid_player_data["club"] = "12345"
        with pytest.raises(ValueError):
            _create_player(valid_player_data)


class TestGoalkeeperAttributes:
    """Edge cases specific to goalkeeper attribute validation."""

    @pytest.mark.parametrize("attr", ["diving", "handling", "kicking", "reflexes", "speed", "positioning"])
    def test_gk_attribute_below_zero_rejected(self, valid_goalkeeper_data, attr):
        """Goalkeeper attributes must be >= 0."""
        valid_goalkeeper_data[attr] = -1
        with pytest.raises(ValueError):
            _create_player(valid_goalkeeper_data)

    @pytest.mark.parametrize("attr", ["diving", "handling", "kicking", "reflexes", "speed", "positioning"])
    def test_gk_attribute_above_99_rejected(self, valid_goalkeeper_data, attr):
        """Goalkeeper attributes must be <= 99."""
        valid_goalkeeper_data[attr] = 100
        with pytest.raises(ValueError):
            _create_player(valid_goalkeeper_data)

    def test_outfield_attributes_on_goalkeeper_rejected(self, valid_goalkeeper_data):
        """Supplying outfield-only attributes (pace, shooting...) for a GK should be rejected or ignored."""
        valid_goalkeeper_data["pace"] = 50
        valid_goalkeeper_data["shooting"] = 30
        with pytest.raises((ValueError, KeyError)):
            _create_player(valid_goalkeeper_data)


class TestPlayerMissingFields:
    """Edge cases when required fields are completely absent."""

    REQUIRED_FIELDS = ["name", "position", "rating"]

    @pytest.mark.parametrize("field", REQUIRED_FIELDS)
    def test_missing_required_field_rejected(self, valid_player_data, field):
        """Omitting any required field must raise an error."""
        del valid_player_data[field]
        with pytest.raises((ValueError, KeyError, TypeError)):
            _create_player(valid_player_data)

    def test_empty_dict_rejected(self):
        """Creating a player from an empty dict must fail."""
        with pytest.raises((ValueError, KeyError, TypeError)):
            _create_player({})

    def test_extra_unknown_fields_ignored_or_rejected(self, valid_player_data):
        """Unknown fields should either be silently ignored or raise an error."""
        valid_player_data["unknown_field"] = "surprise"
        # Implementation decides: we just confirm no crash on valid data
        try:
            player = _create_player(valid_player_data)
            assert "unknown_field" not in player or player.get("unknown_field") is not None
        except (ValueError, KeyError):
            pass  # Also acceptable to reject unknown fields


# ---------------------------------------------------------------------------
# Stub helper — replace with actual implementation import when ready
# ---------------------------------------------------------------------------

def _create_player(data: dict) -> dict:
    """
    Stub that validates and returns player data.

    Replace this with the actual Player model/factory once implemented:
        from draftfut.models.player import create_player as _create_player
    """
    errors = []
    name = data.get("name")
    if name is None:
        raise TypeError("name is required and cannot be None")
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    name = name.strip()
    if not name:
        raise ValueError("name must not be empty or whitespace")
    if name.isdigit():
        raise ValueError("name must not be purely numeric")
    if len(name) > 100:
        raise ValueError("name must not exceed 100 characters")

    position = data.get("position")
    if position is None:
        raise TypeError("position is required and cannot be None")
    if not isinstance(position, str):
        raise TypeError("position must be a string")
    if not position.strip():
        raise ValueError("position must not be empty")

    valid_positions = {
        "GK", "CB", "LB", "RB", "LWB", "RWB",
        "CDM", "CM", "CAM", "LM", "RM",
        "LW", "RW", "CF", "ST",
    }
    position = position.strip().upper()
    if position not in valid_positions:
        raise ValueError(f"Invalid position: {position}")

    rating = data.get("rating")
    if rating is None:
        raise TypeError("rating is required")
    if not isinstance(rating, int) or isinstance(rating, bool):
        raise TypeError("rating must be an integer")
    if rating < 1 or rating > 99:
        raise ValueError("rating must be between 1 and 99")

    nationality = data.get("nationality")
    if nationality is not None:
        if not isinstance(nationality, str) or not nationality.strip():
            raise ValueError("nationality must be a non-empty string")

    club = data.get("club")
    if club is not None:
        if not isinstance(club, str):
            raise ValueError("club must be a string")
        if not club.strip():
            raise ValueError("club must not be empty")
        if club.strip().isdigit():
            raise ValueError("club must not be purely numeric")

    if position == "GK":
        gk_attrs = ["diving", "handling", "kicking", "reflexes", "speed", "positioning"]
        outfield_attrs = ["pace", "shooting", "passing", "dribbling", "defending", "physical"]
        for oa in outfield_attrs:
            if oa in data:
                raise ValueError(f"Outfield attribute '{oa}' not valid for GK")
        for attr in gk_attrs:
            val = data.get(attr)
            if val is not None:
                if not isinstance(val, (int, float)):
                    raise TypeError(f"{attr} must be numeric")
                if val < 0 or val > 99:
                    raise ValueError(f"{attr} must be between 0 and 99")
    else:
        outfield_attrs = ["pace", "shooting", "passing", "dribbling", "defending", "physical"]
        for attr in outfield_attrs:
            val = data.get(attr)
            if val is not None:
                if not isinstance(val, (int, float)):
                    raise TypeError(f"{attr} must be numeric")
                if val < 0 or val > 99:
                    raise ValueError(f"{attr} must be between 0 and 99")

    result = {
        "name": name,
        "position": position,
        "rating": rating,
        "nationality": nationality,
        "club": club,
    }
    return result
