import inventory
from app import run_app

"""
main.py purpose:
Entry point of the application.
"""
# This file initializes the database and starts the application.
def main() -> None:

    inventory.startup()
    inventory.create_default_user("Admin", "ChangeMe123!")
    
    # Run the application (GUI)
    run_app()

# Run Main
if __name__ == "__main__":
    main()

# Backup code is Backup123!