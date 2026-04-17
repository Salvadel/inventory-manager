import inventory
from app import run_app

"""
main.py purpose:
Entry point of the application.
"""

def main() -> None:
    # 1. Initialize the database and ensure the default user exists
    # This ensures that even on a fresh install, 'LabTA' can log in immediately.
    inventory.startup()
    inventory.create_default_user("LabTA", "COMLab123!")
    
    # 2. Hand off control to the app engine
    run_app()

if __name__ == "__main__":
    main()