import sys
import os

# Import the config module
import config
from tabulate import tabulate  # Import the tabulate module


# Access the 'options' dictionary from the config module
llamas = config.options


# def display_options():
#     print("Choose a category:")
#     for i, category in enumerate(llamas.keys(), start=1):
#         print(f"{i}. {category}")

# def display_options():
#     headers = ["Category", "Name", "URL", "Author"]  # Define headers for the table
#     table_data = []  # Initialize an empty list to store table rows
#
#     for category, options in llamas.items():
#         for option in options:
#             row = [category, option["name"], option["url"], option["author"]]
#             table_data.append(row)
#
#     # Use tabulate to format the table
#     table = tabulate(table_data, headers=headers, tablefmt="grid")
#
#     # Print the formatted table
#     print(table)

# def choose_category():
#     display_options()
#     while True:
#         try:
#             choice = int(input("Enter the number of your choice: "))
#             if 1 <= choice <= len(llamas):
#                 return list(llamas.keys())[choice - 1]
#             else:
#                 print("Invalid choice. Please enter a number between 1 and", len(llamas))
#         except ValueError:
#             print("Invalid input. Please enter a number.")

def display_options(category=None):
    headers = ["#", "Category", "Name", "URL", "Author"]
    table_data = []

    for cat, options in llamas.items():
        if category and cat.lower() != category.lower():
            continue

        category_rows = []
        for idx, option in enumerate(options, start=1):
            # Check if "author" key exists in the option dictionary
            author = option.get("author", "N/A")
            row = [f"{idx}.", cat, option["name"], option["url"], author]
            category_rows.append(row)

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

# def main():
#     selected_category = choose_category()
#     selected_option = choose_option(selected_category)
#
#     print("\nYou selected:")
#     print(f"Name: {selected_option['name']}")
#     print(f"URL: {selected_option['url']}")
#     print(f"Author: {selected_option['author']}")
#
# if __name__ == "__main__":
#     main()

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