"""
Smart Study Planner

A console-based Python programme that helps a student log, review and
analyse their study sessions across different subjects the course of a
semester and continues to work correctly across multiple runs by
saving its data to a file.

"""
import os

DATA_FILE = "/Users/user/My Drive/Personal/Victoria University/Course Work/ProgrammingFundamentals/study_log.txt"
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


def save_sessions(sessions):
    """
    Docstring: The function save every logged session to DATA_FILE, one session per line.
    Fields are separated by FIELD_SEP so they can be split back out on load.
    """
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            for session in sessions:
                line = FIELD_SEP.join([
                    session["subject"],
                    session["topic"],
                    session["date"],
                    str(session["duration"]),
                ])
                f.write(line + "\n")
        print(f"Saved {len(sessions)} session(s) to '{DATA_FILE}'.")
    except OSError as e:
        # If the file can't be written for some reason, don't crash -
        # just warn the user so they know their data wasn't persisted.
        print(f"Warning: could not save sessions ({e}).")


def load_sessions():
    """
    Docstring: Function loads sessions from DATA_FILE if it exists. Returns a list of session
    dictionaries. If the file doesn't exist (e.g. first run ever), or a
    line is malformed, that is handled gracefully rather than crashing.
    """
    sessions = []
    if not os.path.exists(DATA_FILE):
        # First run - there's simply nothing to load yet.
        return sessions
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for line_number, raw_line in enumerate(f, start=1):
                line = raw_line.strip()
                if not line:
                    continue  # skip blank lines

                parts = line.split(FIELD_SEP)
                if len(parts) != 4:
                    # Malformed line - skip it but let the user know.
                    print(f"Skipping malformed line {line_number} in {DATA_FILE}.")
                    continue
                subject, topic, date, duration_str = parts
                try:
                    duration = float(duration_str)
                except ValueError:
                    print(f"Skipping line {line_number} - invalid duration.")
                    continue
                sessions.append({"subject": subject, "topic": topic, "date": date, "duration": duration,})
    except OSError as e:
        print(f"Warning: could not read '{DATA_FILE}' ({e}). Starting with no sessions.")

    return sessions


def add_session(sessions):
    """
    Docstring: Function prompts the user for the details of a new study session and append it
    to the sessions list as a dictionary.
    """
    subject = input("Subject: ").strip()
    topic = input("Topic covered: ").strip()
    date = input("Date / day label (e.g. 2026-08-31 or 'Monday'): ").strip()

    # Keep re-prompting until a valid positive number is given for duration.
    duration = None
    while duration is None:
        duration_str = input("Duration in minutes: ").strip()
        try:
            value = float(duration_str)
            if value <= 0:
                print("Duration must be a positive number. Please try again.")
                continue
            duration = value
        except ValueError:
            print("Please enter a valid number for duration.")

    session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration,
    }
    sessions.append(session)
    print("Session added successfully!\n")


def view_sessions(sessions):
    """
    Docstring: Function displays every logged session in a neatly formatted table, including
    each session's Short/Medium/Long classification.
    """
    if not sessions:
        print("No sessions have been logged yet.\n")
        return

    header = f"{'#':<3} {'Subject':<15} {'Topic':<20} {'Date':<15} {'Duration (min)':<15} {'Type':<8}"
    print(header)
    print("-" * len(header))

    for index, session in enumerate(sessions, start=1):
        session_type = classify_session(session["duration"])
        print(f"{index:<3} {session['subject']:<15} {session['topic']:<20} "
              f"{session['date']:<15} {session['duration']:<15.1f} {session_type:<8}")
    print()


def search_by_subject(sessions):
    """
    Docstring: Function asks the user for a subject name (case-insensitive match) and display
    only the sessions recorded for that subject, plus the total time
    spent on it. Shows a clear message if none are found.
    """
    query = input("Enter subject to search for: ").strip()
    matches = [s for s in sessions if s["subject"].lower() == query.lower()]

    if not matches:
        print(f"No sessions found for subject '{query}'.\n")
        return

    header = f"{'#':<3} {'Topic':<20} {'Date':<15} {'Duration (min)':<15} {'Type':<8}"
    print(header)
    print("-" * len(header))

    total_minutes = 0
    for index, session in enumerate(matches, start=1):
        session_type = classify_session(session["duration"])
        print(f"{index:<3} {session['topic']:<20} {session['date']:<15} "
              f"{session['duration']:<15.1f} {session_type:<8}")
        total_minutes += session["duration"]

    print(f"\nTotal time spent on '{query}': {total_minutes:.1f} minutes "
          f"({total_minutes / 60:.2f} hours)\n")


def study_statistics(sessions):
    """
    Docstring: Function computes and displays:
      - total hours studied overall
      - total hours studied per subject
      - the subject with the least total study time (weakest area)
      - the single longest session recorded
    """
    if not sessions:
        print("No sessions have been logged yet, so no statistics are available.\n")
        return

    # Build a subject -> total minutes mapping.
    totals_by_subject = {}
    for session in sessions:
        subject = session["subject"]
        totals_by_subject[subject] = totals_by_subject.get(subject, 0) + session["duration"]
    total_minutes_overall = sum(totals_by_subject.values())

    print(f"Total hours studied overall: {total_minutes_overall / 60:.2f} hours\n")

    print("Hours studied per subject:")
    for subject, minutes in totals_by_subject.items():
        print(f"  - {subject}: {minutes / 60:.2f} hours")

    # Weakest area = subject with the least total study time.
    weakest_subject = min(totals_by_subject, key=totals_by_subject.get)
    print(f"\nWeakest area (least total study time): {weakest_subject} "
          f"({totals_by_subject[weakest_subject] / 60:.2f} hours)")

    # Longest single session recorded.
    longest_session = max(sessions, key=lambda s: s["duration"])
    print(f"Longest single session: {longest_session['subject']} - "
          f"'{longest_session['topic']}' on {longest_session['date']} "
          f"({longest_session['duration']:.1f} minutes, "
          f"{classify_session(longest_session['duration'])})\n")


def display_menu():
    """Docstring: Function prints the main menu options."""
    print("=" * 40)
    print("       SMART STUDY PLANNER")
    print("=" * 40)
    print("1. Add a study session")
    print("2. View all sessions")
    print("3. Search sessions by subject")
    print("4. View statistics")
    print("5. Save and exit")
    print("-" * 40)


def main():
    """
    Docstring: This function returns the main programme loop: loads existing sessions, display the menu
    repeatedly, and route the user's choice to the right function until
    they choose to save and exit.
    """
    sessions = load_sessions()
    if sessions:
        print(f"Loaded {len(sessions)} existing session(s) from '{DATA_FILE}'.\n")

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_session(sessions)
        elif choice == "2":
            view_sessions(sessions)
        elif choice == "3":
            search_by_subject(sessions)
        elif choice == "4":
            study_statistics(sessions)
        elif choice == "5":
            save_sessions(sessions)
            print("Goodbye! Keep up the good study habits.")
            break
        else:
            # Reject invalid choices without crashing the programme.
            print("Invalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()

