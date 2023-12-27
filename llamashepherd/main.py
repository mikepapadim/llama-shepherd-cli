#!/usr/bin/env python3

import sys
import os
import subprocess
import argparse
from tabulate import tabulate
import config

# Access the 'options' dictionary from the config module
llamas = config.options


def display_options(category=None, language=None):
    headers = ["#", "Language", "Name", "Github", "Author"]
    table_data = []
    global_index = 1  # Initialize a global index

    for cat, options in llamas.items():
        if category and cat.lower() != category.lower():
            continue

        category_rows = []
        for option in options:
            if language and option['name'].lower() != language.lower():
                continue

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
    table = tabulate(table_data, headers=headers, tablefmt="pipe")

    # Print the formatted table
    print_table(table)


def print_table(table):
    print("\n" + "-" * 121 + "\n")
    print(table)
    print("\n" + "-" * 121 + "\n")


def choose_implemenation():
    display_options()
    while True:
        try:
            choice = int(input("Enter the number of your choice (0 to exit): "))
            if 0 <= choice <= len(llamas):
                return None if choice == 0 else list(llamas.keys())[choice - 1]
            else:
                print("Invalid choice. Please enter a number between 0 and", len(llamas))
        except ValueError:
            print("Invalid input. Please enter a number.")


def choose_option(category):
    category_options = llamas[category]
    print(f"\nChoose an option from the {category} category (0 to go back):")
    for i, option in enumerate(category_options, start=1):
        name = option.get('name', 'N/A')
        author = option.get('author', 'N/A')
        print(f"{i}. {name} by {author}")
    while True:
        try:
            choice = int(input("Enter the number of your choice (0 to go back): "))
            if 0 <= choice <= len(category_options):
                return None if choice == 0 else category_options[choice - 1]
            else:
                print(f"Invalid choice. Please enter a number between 0 and {len(category_options)}")
        except ValueError:
            print("Invalid input. Please enter a number.")


def clone_repository(url, destination):
    try:
        subprocess.run(["git", "clone", url, destination], check=True)
        print(f"Repository cloned successfully to {destination}")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")


def list_action(language=None):
    display_options(language)


def interactive_action(default_llama_shepherd_path):
    while True:
        category = choose_implemenation()
        if category is None:
            break  # Exit the program if the user chooses to exit

        selected_option = choose_option(category)
        if selected_option is None:
            continue  # Go back to category selection if the user chooses to go back

        default_path = os.path.join(default_llama_shepherd_path, category, selected_option['name'])
        destination = input(f"Enter the destination directory (default: {default_path}): ").strip() or default_path

        # Create the destination directory if it doesn't exist
        os.makedirs(destination, exist_ok=True)

        clone_repository(selected_option['url'], destination)

        # Ask whether to initialize or exit
        while True:
            user_input = input(
                "Do you want to download and config Tokenizer and/or TinyLLama models? (y/n, 0 to exit): ").lower()
            if user_input == 'y':
                initialize_action()
                break
            elif user_input == 'n':
                sys.exit()
            else:
                print("Invalid input. Please enter 'y', 'n', or '0'.")


def initialize_action():
    # Add initialization logic here
    print("Initializing models...")


def main():
    home_directory = os.path.expanduser("~")
    default_llama_shepherd_path = os.path.join(home_directory, "llama-shepherd")

    parser = argparse.ArgumentParser(
        description="Llama Shepherd CLI: Manage your llama-related projects.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter  # Show default values in the help menu
    )
    parser.add_argument(
        "action",
        nargs="?",
        default="--help",  # Set default action to "--help"
        choices=["list", "interactive", "initialize", "--help"],
        help="Action to perform"
    )

    parser.add_argument(
        "language",
        nargs="?",  # Make language optional
        default=None,
        help="Specify the language for the 'list' action"
    )

    args = parser.parse_args()

    if args.action == "list":
        list_action(args.language)  # Pass the language argument
    elif args.action == "interactive":
        interactive_action(default_llama_shepherd_path)
    elif args.action == "initialize":
        initialize_action()
    elif args.action == "--help":
        parser.print_help()


if __name__ == "__main__":
    main()
