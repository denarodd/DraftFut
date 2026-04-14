"""
Edge-case tests for User management.

Covers:
- Registration with empty / invalid inputs
- Email format validation
- Password strength edge cases
- Username constraints (length, characters, uniqueness)
- Authentication edge cases (wrong password, locked accounts)
- Profile update edge cases
"""

import pytest


class TestUserRegistrationUsername:
    """Edge cases around username during registration."""

    def test_empty_username_rejected(self, valid_user_data):
        """An empty username must be rejected."""
        valid_user_data["username"] = ""
        with pytest.raises(ValueError):
            _register_user(valid_user_data)

    def test_none_username_rejected(self, valid_user_data):
        """A None username must be rejected."""
        valid_user_data["username"] = None
        with pytest.raises((ValueError, TypeError)):
            _register_user(valid_user_data)

    def test_whitespace_only_username_rejected(self, valid_user_data):
        """A username consisting only of whitespace must be rejected."""
        valid_user_data["username"] = "   "
        with pytest.raises(ValueError):
            _register_user(valid_user_data)

    def test_username_too_short_rejected(self, valid_user_data):
        """A username shorter than 3 characters must be rejected."""
        valid_user_data["username"] = "ab"
        with pytest.raises(ValueError):
            _register_user(valid_user_data)

    def test_username_too_long_rejected(self, valid_user_data):
        """A username longer than 30 characters must be rejected."""
        valid_user_data["username"] = "a" * 31
        with pytest.raises(ValueError):
            _register_user(valid_user_data)

    def test_username_with_spaces_rejected(self, valid_user_data):
        """Usernames must not contain spaces."""
        valid_user_data["username"] = "user name"
        with pytest.raises(ValueError):
            _register_user(valid_user_data)

    def test_username_with_special_chars_rejected(self, valid_user_data):
        """Usernames must only contain alphanumeric characters and underscores."""
        valid_user_data["username"] = "user@name!"
        with pytest.raises(ValueError):
            _register_user(valid_user_data)

    def test_username_with_underscore_accepted(self, valid_user_data):
        """Usernames with underscores are valid."""
        valid_user_data["username"] = "draft_king_99"
        user = _register_user(valid_user_data)
        assert user["username"] == "draft_king_99"

    def test_duplicate_username_rejected(self, valid_user_data):
        """Registering with an already-taken username must be rejected."""
        _register_user(valid_user_data)
        with pytest.raises(ValueError):
            _register_user(valid_user_data)

    def test_username_case_insensitive_duplicate_rejected(self, valid_user_data):
        """Usernames should be case-insensitive for uniqueness."""
        _register_user(valid_user_data)
        valid_user_data["username"] = valid_user_data["username"].upper()
        valid_user_data["email"] = "other@example.com"
        with pytest.raises(ValueError):
            _register_user(valid_user_data)


class TestUserRegistrationEmail:
    """Edge cases around email during registration."""

    def test_empty_email_rejected(self, valid_user_data):
        """An empty email must be rejected."""
        valid_user_data["email"] = ""
        with pytest.raises(ValueError):
            _register_user(valid_user_data)

    def test_none_email_rejected(self, valid_user_data):
        """A None email must be rejected."""
        valid_user_data["email"] = None
        with pytest.raises((ValueError, TypeError)):
            _register_user(valid_user_data)

    def test_email_without_at_sign_rejected(self, valid_user_data):
        """An email missing the @ symbol must be rejected."""
        valid_user_data["email"] = "userexample.com"
        with pytest.raises(ValueError):
            _register_user(valid_user_data)

    def test_email_without_domain_rejected(self, valid_user_data):
        """An email missing the domain part must be rejected."""
        valid_user_data["email"] = "user@"
        with pytest.raises(ValueError):
            _register_user(valid_user_data)

    def test_email_without_local_part_rejected(self, valid_user_data):
        """An email missing the local part must be rejected."""
        valid_user_data["email"] = "@example.com"
        with pytest.raises(ValueError):
            _register_user(valid_user_data)

    def test_email_with_multiple_at_signs_rejected(self, valid_user_data):
        """An email with multiple @ symbols must be rejected."""
        valid_user_data["email"] = "user@@example.com"
        with pytest.raises(ValueError):
            _register_user(valid_user_data)

    def test_email_with_spaces_rejected(self, valid_user_data):
        """An email containing spaces must be rejected."""
        valid_user_data["email"] = "user @example.com"
        with pytest.raises(ValueError):
            _register_user(valid_user_data)

    def test_duplicate_email_rejected(self, valid_user_data):
        """Registering with an already-used email must be rejected."""
        _register_user(valid_user_data)
        valid_user_data["username"] = "another_user"
        with pytest.raises(ValueError):
            _register_user(valid_user_data)

    def test_email_normalised_to_lowercase(self, valid_user_data):
        """Emails should be stored in lowercase."""
        valid_user_data["email"] = "Fan@EXAMPLE.COM"
        user = _register_user(valid_user_data)
        assert user["email"] == "fan@example.com"


class TestUserRegistrationPassword:
    """Edge cases around password during registration."""

    def test_empty_password_rejected(self, valid_user_data):
        """An empty password must be rejected."""
        valid_user_data["password"] = ""
        with pytest.raises(ValueError):
            _register_user(valid_user_data)

    def test_none_password_rejected(self, valid_user_data):
        """A None password must be rejected."""
        valid_user_data["password"] = None
        with pytest.raises((ValueError, TypeError)):
            _register_user(valid_user_data)

    def test_password_too_short_rejected(self, valid_user_data):
        """A password shorter than 8 characters must be rejected."""
        valid_user_data["password"] = "Ab1!xyz"
        with pytest.raises(ValueError):
            _register_user(valid_user_data)

    def test_password_without_uppercase_rejected(self, valid_user_data):
        """A password without any uppercase letter must be rejected."""
        valid_user_data["password"] = "alllower1!"
        with pytest.raises(ValueError):
            _register_user(valid_user_data)

    def test_password_without_lowercase_rejected(self, valid_user_data):
        """A password without any lowercase letter must be rejected."""
        valid_user_data["password"] = "ALLUPPER1!"
        with pytest.raises(ValueError):
            _register_user(valid_user_data)

    def test_password_without_digit_rejected(self, valid_user_data):
        """A password without any digit must be rejected."""
        valid_user_data["password"] = "NoDigits!!"
        with pytest.raises(ValueError):
            _register_user(valid_user_data)

    def test_password_without_special_char_rejected(self, valid_user_data):
        """A password without any special character must be rejected."""
        valid_user_data["password"] = "NoSpecial1"
        with pytest.raises(ValueError):
            _register_user(valid_user_data)

    def test_very_long_password_accepted(self, valid_user_data):
        """A very long password (128 chars) should be accepted."""
        valid_user_data["password"] = "Aa1!" + "x" * 124
        user = _register_user(valid_user_data)
        assert user["username"] == valid_user_data["username"]

    def test_password_exceeding_max_length_rejected(self, valid_user_data):
        """A password exceeding 256 characters must be rejected."""
        valid_user_data["password"] = "Aa1!" + "x" * 253
        with pytest.raises(ValueError):
            _register_user(valid_user_data)


class TestUserRegistrationMissingFields:
    """Edge cases for completely missing registration fields."""

    def test_missing_username_rejected(self, valid_user_data):
        del valid_user_data["username"]
        with pytest.raises((ValueError, KeyError, TypeError)):
            _register_user(valid_user_data)

    def test_missing_email_rejected(self, valid_user_data):
        del valid_user_data["email"]
        with pytest.raises((ValueError, KeyError, TypeError)):
            _register_user(valid_user_data)

    def test_missing_password_rejected(self, valid_user_data):
        del valid_user_data["password"]
        with pytest.raises((ValueError, KeyError, TypeError)):
            _register_user(valid_user_data)

    def test_empty_dict_rejected(self):
        with pytest.raises((ValueError, KeyError, TypeError)):
            _register_user({})


class TestUserAuthentication:
    """Edge cases around login / authentication."""

    def test_login_with_correct_credentials_succeeds(self, valid_user_data):
        """Login with valid credentials should succeed."""
        _register_user(valid_user_data)
        result = _login(valid_user_data["email"], valid_user_data["password"])
        assert result["authenticated"] is True

    def test_login_with_wrong_password_rejected(self, valid_user_data):
        """Login with incorrect password must be rejected."""
        _register_user(valid_user_data)
        with pytest.raises(ValueError):
            _login(valid_user_data["email"], "WrongPassword1!")

    def test_login_with_nonexistent_email_rejected(self):
        """Login with an email not in the system must be rejected."""
        with pytest.raises(ValueError):
            _login("nobody@example.com", "Password1!")

    def test_login_with_empty_email_rejected(self):
        """Login with an empty email must be rejected."""
        with pytest.raises(ValueError):
            _login("", "Password1!")

    def test_login_with_empty_password_rejected(self, valid_user_data):
        """Login with an empty password must be rejected."""
        _register_user(valid_user_data)
        with pytest.raises(ValueError):
            _login(valid_user_data["email"], "")

    def test_login_with_none_credentials_rejected(self):
        """Login with None email or password must be rejected."""
        with pytest.raises((ValueError, TypeError)):
            _login(None, "Password1!")
        with pytest.raises((ValueError, TypeError)):
            _login("user@example.com", None)


class TestUserProfileUpdate:
    """Edge cases around profile updates."""

    def test_update_username_to_empty_rejected(self, valid_user_data):
        """Changing username to empty string must be rejected."""
        user = _register_user(valid_user_data)
        with pytest.raises(ValueError):
            _update_profile(user["id"], {"username": ""})

    def test_update_email_to_invalid_format_rejected(self, valid_user_data):
        """Changing email to an invalid format must be rejected."""
        user = _register_user(valid_user_data)
        with pytest.raises(ValueError):
            _update_profile(user["id"], {"email": "not-an-email"})

    def test_update_nonexistent_user_rejected(self):
        """Updating a user that doesn't exist must be rejected."""
        with pytest.raises(ValueError):
            _update_profile(user_id=99999, updates={"username": "new_name"})

    def test_update_with_empty_dict_is_noop(self, valid_user_data):
        """Updating with an empty dict should be a no-op (no crash)."""
        user = _register_user(valid_user_data)
        result = _update_profile(user["id"], {})
        assert result["username"] == valid_user_data["username"]


# ---------------------------------------------------------------------------
# Stub helpers — replace with actual implementation imports when ready
# ---------------------------------------------------------------------------

_user_store = []
_next_id = 1


def _reset_store():
    global _user_store, _next_id
    _user_store = []
    _next_id = 1


@pytest.fixture(autouse=True)
def _clear_users():
    """Reset user store before each test."""
    _reset_store()


def _validate_email(email):
    if not email or not isinstance(email, str):
        raise ValueError("Email is required")
    email = email.strip()
    if " " in email:
        raise ValueError("Email must not contain spaces")
    if email.count("@") != 1:
        raise ValueError("Email must contain exactly one @")
    local, domain = email.split("@")
    if not local:
        raise ValueError("Email must have a local part")
    if not domain or "." not in domain:
        raise ValueError("Email must have a valid domain")
    return email.lower()


def _validate_password(password):
    if password is None:
        raise TypeError("Password must not be None")
    if not isinstance(password, str):
        raise TypeError("Password must be a string")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    if len(password) > 256:
        raise ValueError("Password must not exceed 256 characters")
    if not any(c.isupper() for c in password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not any(c.islower() for c in password):
        raise ValueError("Password must contain at least one lowercase letter")
    if not any(c.isdigit() for c in password):
        raise ValueError("Password must contain at least one digit")
    if all(c.isalnum() for c in password):
        raise ValueError("Password must contain at least one special character")


def _validate_username(username):
    if username is None:
        raise TypeError("Username must not be None")
    if not isinstance(username, str):
        raise TypeError("Username must be a string")
    username = username.strip()
    if not username:
        raise ValueError("Username must not be empty")
    if len(username) < 3:
        raise ValueError("Username must be at least 3 characters")
    if len(username) > 30:
        raise ValueError("Username must not exceed 30 characters")
    if " " in username:
        raise ValueError("Username must not contain spaces")
    import re
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValueError("Username must be alphanumeric (underscores allowed)")
    return username


def _register_user(data: dict) -> dict:
    global _next_id
    username = _validate_username(data.get("username"))
    email = _validate_email(data.get("email"))
    password = data.get("password")
    _validate_password(password)

    for u in _user_store:
        if u["username"].lower() == username.lower():
            raise ValueError("Username already taken")
        if u["email"] == email:
            raise ValueError("Email already registered")

    user = {"id": _next_id, "username": username, "email": email, "password": password}
    _user_store.append(user)
    _next_id += 1
    return {"id": user["id"], "username": user["username"], "email": user["email"]}


def _login(email, password) -> dict:
    if email is None:
        raise TypeError("Email must not be None")
    if password is None:
        raise TypeError("Password must not be None")
    if not email:
        raise ValueError("Email must not be empty")
    if not password:
        raise ValueError("Password must not be empty")
    email = email.lower().strip()
    for u in _user_store:
        if u["email"] == email:
            if u["password"] != password:
                raise ValueError("Invalid credentials")
            return {"authenticated": True, "user_id": u["id"]}
    raise ValueError("Invalid credentials")


def _update_profile(user_id: int, updates: dict) -> dict:
    user = None
    for u in _user_store:
        if u["id"] == user_id:
            user = u
            break
    if not user:
        raise ValueError("User not found")

    if "username" in updates:
        username = _validate_username(updates["username"])
        user["username"] = username
    if "email" in updates:
        email = _validate_email(updates["email"])
        user["email"] = email

    return user
