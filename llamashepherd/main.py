#!/usr/bin/env python3

import sys
import os
import subprocess
import argparse
import wget
from tabulate import tabulate
import config
import model_config

# Access the 'options' dictionary from the config module
llamas = config.options


def display_options(category=None, language=None):
    """Display llama options in a tabular format.

    Args:
        category (str, optional): Filter options by category. Defaults to None.
        language (str, optional): Filter options by language. Defaults to None.
    """
    headers = ["#", "Language", "Name", "Github", "Author"]
    table_data = []
    global_index = 1  # Initialize a global index

    for cat, options in llamas.items():
        if category and cat.lower() != category.lower():
            continue

        category_rows = []
        for option in options:
            if language and option["name"].lower() != language.lower():
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
    """Print a formatted table.

    Args:
        table (str): Formatted table to print.
    """
    print("\n" + "-" * 121 + "\n")
    print(table)
    print("\n" + "-" * 121 + "\n")


def clone_repository(url, destination):
    """Clone a Git repository.

    Args:
        url (str): URL of the Git repository.
        destination (str): Destination directory for cloning.
    """
    try:
        subprocess.run(["git", "clone", url, destination], check=True)
        print(f"Repository cloned successfully to {destination}")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")


def list_action(language=None):
    """List llama options based on the specified language.

    Args:
        language (str, optional): Language to filter llama options. Defaults to None.
    """
    display_options(language)


def choose_option():
    """Prompt the user to choose a llama option.

    Returns:
        dict or None: The selected llama option or None if the user chose to go back.
    """
    all_options = [option for options in llamas.values() for option in options]
    total_options = len(all_options)

    print("Choose an option (0 to go back):")

    while True:
        try:
            choice = int(input(f"Enter the number of your choice (0 to go back): "))
            if 0 <= choice <= total_options:
                return None if choice == 0 else all_options[choice - 1]
            else:
                print(
                    f"Invalid choice. Please enter a number between 0 and {total_options}"
                )
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_language_for_option(options_dict, selected_option):
    """Get the language associated with a selected llama option.

    Args:
        options_dict (dict): Dictionary of llama options.
        selected_option (dict): Selected llama option.

    Returns:
        str or None: Language associated with the selected option or None if not found.
    """
    for language, options_list in options_dict.items():
        for option in options_list:
            if option == selected_option:
                return language
    return None  # Return None if the selected option is not found in any language category


def interactive_action(default_llama_shepherd_path):
    """Perform interactive actions for choosing and cloning llama options.

    Args:
        default_llama_shepherd_path (str): Default path for llama shepherd.
    """
    display_options()
    while True:
        selected_option = choose_option()
        selected_category = get_language_for_option(llamas, selected_option)

        default_path = os.path.join(
            default_llama_shepherd_path, selected_category, selected_option["name"]
        )
        destination = (
            input(
                f"Enter the destination directory (default: {default_path}): "
            ).strip()
            or default_path
        )

        # Create the destination directory if it doesn't exist
        os.makedirs(destination, exist_ok=True)

        clone_repository(selected_option["url"], destination)

        # Ask whether to initialize or exit
        while True:
            user_input = input(
                "Do you want to download and config Tokenizer and/or TinyLLama models? (y/n, 0 to exit): "
            ).lower()
            if user_input == "y":
                initialize_action(default_llama_shepherd_path)
                break
            elif user_input == "n":
                sys.exit()
            else:
                print("Invalid input. Please enter 'y', 'n', or '0.'")


def initialize_action(default_llama_shepherd_path):
    """Initialize llama models based on user input.

    Args:
        default_llama_shepherd_path (str): Default path for llama shepherd.
    """
    print("Initializing models...")

    while True:
        user_input = input(
            "Do you want to download and config Tokenizer and/or TinyLLama models? (y/n, 0 to exit): "
        ).lower()

        if user_input == "y":
            # Ask whether to download Tokenizer
            download_tokenizer = input(
                f"Do you want to download the Tokenizer model? (y/n): "
            ).lower()
            if download_tokenizer == "y":
                # Add logic to download and configure the Tokenizer model
                download_and_configure_model(
                    "Tokenizer",
                    model_config.urls["tokenizer"],
                    default_llama_shepherd_path,
                )

            # Ask whether to download stories models
            download_stories = input(
                f"Do you want to download the stories models? (y/n): "
            ).lower()
            if download_stories == "y":
                # Add logic to download and configure stories models
                download_and_configure_model(
                    "Stories15M",
                    model_config.urls["stories15M"],
                    default_llama_shepherd_path,
                )
                download_and_configure_model(
                    "Stories42M",
                    model_config.urls["stories42M"],
                    default_llama_shepherd_path,
                )
                download_and_configure_model(
                    "Stories110M",
                    model_config.urls["stories110M"],
                    default_llama_shepherd_path,
                )

            break
        elif user_input == "n":
            sys.exit()
        else:
            print("Invalid input. Please enter 'y', 'n', or '0'.")


def download_and_configure_model(model_name, model_url, destination_directory):
    """Download and configure a llama model.

    Args:
        model_name (str): Name of the llama model.
        model_url (str): URL of the llama model.
        destination_directory (str): Destination directory for the llama model.
    """
    print(f"Downloading and configuring {model_name} model from: {model_url}")

    # Ensure the models directory exists
    models_directory = os.path.join(destination_directory, "models")
    os.makedirs(models_directory, exist_ok=True)

    # Specify the destination file path
    destination_path = os.path.join(models_directory, f"{model_name}.bin")

    try:
        # Download the model using wget
        wget.download(model_url, out=destination_path)
        print(f"\n{model_name} model downloaded successfully to {destination_path}")

        # Add logic to configure the model if needed

    except Exception as e:
        print(f"Error downloading {model_name} model: {e}")


def main():
    """Main function to handle llama shepherd CLI operations."""
    home_directory = os.path.expanduser("~")
    default_llama_shepherd_path = os.path.join(home_directory, "llama-shepherd")

    parser = argparse.ArgumentParser(
        description="Llama Shepherd CLI: Manage your llama-related projects.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,  # Show default values in the help menu
    )
    parser.add_argument(
        "action",
        nargs="?",
        default="--help",  # Set default action to "--help"
        choices=["list", "install", "models", "--help"],
        help="Action to perform",
    )

    parser.add_argument(
        "language",
        nargs="?",  # Make language optional
        default=None,
        help="Specify the language for the 'list' action",
    )

    args = parser.parse_args()

    if args.action == "list":
        list_action(args.language)  # Pass the language argument
    elif args.action == "install":
        interactive_action(default_llama_shepherd_path)
    elif args.action == "models":
        initialize_action(default_llama_shepherd_path)
    elif args.action == "--help":
        parser.print_help()


if __name__ == "__main__":
    main()
