from backend.utils.hashing import hash_password, verify_password

def test_hash_differs_from_plain():
    # Hash must not equal the original password
    assert hash_password("pass123") != "pass123"

def test_correct_password_verifies():
    # Correct password should verify against its hash
    h = hash_password("mypassword")
    assert verify_password("mypassword", h) is True

def test_wrong_password_fails():
    # Wrong password must not verify
    h = hash_password("mypassword")
    assert verify_password("wrong", h) is False

def test_two_hashes_differ():
    # bcrypt salts mean same input produces different hashes
    assert hash_password("same") != hash_password("same")
