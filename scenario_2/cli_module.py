# this module contains items to be displayed for the CLI


def display_results(result_df):
    """
    displays formatted carpark details to the user
    """
    print("\nCarpark Availability Details\n")
    for index, row in result_df.iterrows():
        print(f"Carpark Number: {row['car_park_no']}")
        print(f"Address: {row['address']}")
        print(f"Coordinates: X {row['x_coord']}, Y {row['y_coord']}")
        print(f"Type: {row['car_park_type']}")
        print(f"Parking System: {row['type_of_parking_system']}")
        print(f"Short-Term Parking: {row['short_term_parking']}")
        print(f"Night Parking: {row['night_parking']}")
        print(f"Updated On: {row['update_datetime']}\n")

        # display lot availability per type, hardcoded since lot_types previously found
        lot_types = ["C", "M", "L", "S", "H", "Y"]
        for lot in lot_types:
            capacity_col = f"capacity_{lot}_lots"
            available_col = f"available_{lot}_lots"
            if capacity_col in row and available_col in row:
                # only display lot types where total capacity >0
                if row[capacity_col] != "0":
                    print(
                        f"  {lot} Lots - Capacity: {row[capacity_col]}, Available: {row[available_col]}")

        print("\n" + "-" * 50 + "\n")


def display_menu():
    """
    displays the main menu options to the user
    """
    print("\nCarpark Search System")
    print("1. Search by Carpark Number")
    print("2. Search by Address")
    print("3. Exit")
