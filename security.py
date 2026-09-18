from config import OWNER_KEY, OWNER_NAME


# ============================================================
# RUDRA OWNER SECURITY
# ============================================================

_owner_authenticated = False


# ============================================================
# OWNER ACCESS HEADER
# ============================================================

def _header():

    print()
    print("+" + "-" * 52 + "+")
    print("|" + " RUDRA OWNER ACCESS ".center(52) + "|")
    print("+" + "-" * 52 + "+")
    print()


# ============================================================
# AUTHENTICATE OWNER
# ============================================================

def authenticate():

    global _owner_authenticated

    _header()

    key = input("  Enter owner key: ").strip()

    if key == OWNER_KEY:

        _owner_authenticated = True

        print()
        print("  [OK] OWNER ACCESS GRANTED")
        print(f"  Owner: {OWNER_NAME}")
        print("  [OK] OWNER SESSION AUTHENTICATED")
        print()

        return True

    _owner_authenticated = False

    print()
    print("  [X] ACCESS DENIED")
    print()

    return False


# ============================================================
# VERIFY OWNER
# ============================================================

def verify_owner():

    global _owner_authenticated

    if _owner_authenticated:
        return True

    return authenticate()


# ============================================================
# CHECK OWNER AUTHENTICATION
# ============================================================

def is_owner_authenticated():

    return _owner_authenticated


# ============================================================
# OWNER LOGOUT
# ============================================================

def logout_owner():

    global _owner_authenticated

    _owner_authenticated = False

    print()
    print("  [OK] OWNER SESSION LOCKED")
    print()


# ============================================================
# OWNER REQUIRED MESSAGE
# ============================================================

def owner_required():

    print()
    print("  [!] OWNER AUTHENTICATION REQUIRED")
    print("  This command is restricted to the system owner.")
    print()


# ============================================================
# SECURITY STATUS
# ============================================================

def security_status():

    return {
        "owner": OWNER_NAME,
        "authenticated": _owner_authenticated,
        "status": (
            "OWNER AUTHENTICATED"
            if _owner_authenticated
            else "LOCKED"
        )
    }


# ============================================================
# DIRECT SECURITY TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 50)
    print("             RUDRA SECURITY TEST")
    print("=" * 50)
    print()

    if authenticate():

        print("  Security test       : PASS")

        print()
        print("  Testing persistent authentication...")

        if verify_owner():

            print("  Persistent session  : PASS")

        else:

            print("  Persistent session  : FAILED")

    else:

        print("  Security test       : FAILED")

    print()
    print("=" * 50)
    print()