from app.services.matching import build_location_filter


def test_single_location():
    sql, params = build_location_filter("Janakpuri")
    assert "%janakpuri%" in params

def test_partial_match():
    sql, params = build_location_filter("Janak")
    assert "%janak%" in params

def test_multiple_locations():
    sql, params = build_location_filter("Janak Puri or Tilak Nagar")
    assert "%janakpuri%" in params
    assert "%tilaknagar%" in params
    assert "OR" in sql


def test_empty_location():
    sql, params = build_location_filter("")
    assert sql == ""
    assert params == []


if __name__ == "__main__":
    print("Running tests...\n")

    test_single_location()
    print("✓ test_single_location passed")

    test_multiple_locations()
    print("✓ test_multiple_locations passed")

    test_empty_location()
    print("✓ test_empty_location passed")

    test_partial_match()
    print("✓ test_partial_match passed")

    print("\nAll tests passed.")
