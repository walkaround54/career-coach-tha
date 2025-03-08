import user_input_handling_module as user_input_handling

# run this to run the app for scenario 2, excludes static data processing module


def main():
    """
    runs scenario 2 pipeline
    """
    print("Starting Carpark Search System...\n")

    # calls user_input_handling module to begin user interaction
    user_input_handling.handle_user_input()


if __name__ == "__main__":
    main()
