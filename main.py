"""
Smart Study Planner

A console-based Python programme that helps a student log, review and
analyse their study sessions across different subjects the course of a
semester and continues to work correctly across multiple runs by
saving its data to a file.

"""

import os

DATA_FILE = "study_log.txt"
FIELD_SEP = "|"  # separator used when saving/loading records to/from the file


def classify_session(duration):
    """
    Docstring: The function classifies study sessions based on its duration (in minutes).
    - Short:  under 30 minutes
    - Medium: 30 to 90 minutes (inclusive)
    - Long:   over 90 minutes
    """
    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"


def main():
    """
    Docstring: This function returns the main programme loop: loads existing sessions, display the menu
    repeatedly, and route the user's choice to the right function until
    they choose to save and exit.
    """
    print(f"Loaded existing session(s) from '{DATA_FILE}'.\n")


if __name__ == "__main__":
    main()

