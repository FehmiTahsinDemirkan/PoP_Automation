import os
import random

def create_output_folder(folder_path):
    """Create the output folder if it doesn't exist."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def select_random_emails(messages, count):
    """Select random emails from the fetched messages."""
    return random.sample(messages, min(len(messages), count))
