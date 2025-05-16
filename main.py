# Entry point for the app

import sys

from smart_rockhound.data_lookup import lookup_data
from smart_rockhound.input_handler import get_user_input


def main() -> int:
    user_data: dict = get_user_input()
    print(f"Input received: {user_data}")
    lookup_result: str = lookup_data(user_data['value'])
    print(f"Lookup result: {lookup_result}")
    print("Welcome to Smart Rockhounding!")
    # TODO: Implement CLI or GUI logic
    return 0


if __name__ == "__main__":
    sys.exit(main())
