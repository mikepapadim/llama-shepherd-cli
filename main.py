import sys
import os
from tabulate import tabulate  # Import the tabulate module
import config

# Access the 'options' dictionary from the config module
llamas = config.options


def display_options(category=None):
    headers = ["#", "Language", "Name", "Github", "Author"]
    table_data = []
    global_index = 1  # Initialize a global index

    for cat, options in llamas.items():
        if category and cat.lower() != category.lower():
            continue

        category_rows = []
        for option in options:
            # Check if "author" key exists in the option dictionary
            author = option.get("author", "N/A")
            row = [f"{global_index}.", cat, option["name"], option["url"], author]
            category_rows.append(row)
            global_index += 1  # Increment the global index

        # Add an empty row as a separator between categories
        if table_data:
            table_data.append(["", "", "", "", ""])

        # Extend the main table with the rows of the current category
        table_data.extend(category_rows)

    # Use tabulate to format the table without grid lines
    table = tabulate(table_data, headers=headers, tablefmt="plain")

    # Print the formatted table
    print(table)


def choose_category():
    display_options()
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 0 <= choice <= len(llamas):
                return None if choice == 0 else list(llamas.keys())[choice - 1]
            else:
                print("Invalid choice. Please enter a number between 0 and", len(llamas))
        except ValueError:
            print("Invalid input. Please enter a number.")


def choose_option(category):
    category_options = llamas[category]
    print(f"\nChoose an option from the {category} category:")
    for i, option in enumerate(category_options, start=1):
        print(f"{i}. {option['name']} by {option['author']}")
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(category_options):
                return category_options[choice - 1]
            else:
                print("Invalid choice. Please enter a number between 1 and", len(category_options))
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    if len(sys.argv) == 1:
        # If no arguments are provided, display the full list
        display_options()
    elif len(sys.argv) == 3 and sys.argv[1].lower() == "list":
        # If the command is "list" and a category is provided, display options for that category
        category = sys.argv[2]
        display_options(category)
    else:
        print("Invalid command. Use 'list' to display options for a specific category.")


if __name__ == "__main__":
    main()
