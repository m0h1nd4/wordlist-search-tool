#!/usr/bin/env python3
import argparse
import os
import json
from tqdm import tqdm

def TOTAL():
    """
    Main function to search a large text file for an exact word or a fragment.
    Processes the file line by line (UTF-8, errors ignored) to avoid memory issues,
    and optionally shows a progress bar.
    """
    parser = argparse.ArgumentParser(
        description="Search a large txt file (one word per line) for a word or a fragment."
    )
    parser.add_argument(
        "file", help="Path to the txt file containing words (one per line)."
    )
    parser.add_argument(
        "search_term", help="The word or fragment to search for."
    )
    parser.add_argument(
        "--mode",
        choices=["exact", "fragment"],
        default="exact",
        help="Search mode: 'exact' (default) for full word match or 'fragment' for substring search."
    )
    parser.add_argument(
        "--case-sensitive",
        action="store_true",
        help="Enable case-sensitive search. (Default is case-insensitive)"
    )
    parser.add_argument(
        "--progress",
        action="store_true",
        help="Display a real-time progress indicator using tqdm."
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save the JSON output to a file. The file will be named <search_term>.json (or with a counter if it exists)."
    )
    args = parser.parse_args()

    file_path = args.file
    search_term = args.search_term
    mode = args.mode
    case_sensitive = args.case_sensitive
    show_progress = args.progress
    save_output = args.save

    # Prepare the search term based on case sensitivity.
    search_term_to_use = search_term if case_sensitive else search_term.lower()

    # Initialize counters/results.
    if mode == "exact":
        count = 0
    else:  # fragment mode
        fragment_results = {}

    # Attempt to get the total file size for progress indicator.
    try:
        total_size = os.path.getsize(file_path)
    except Exception as e:
        print(f"Error: Unable to get size of file '{file_path}': {e}")
        return

    try:
        with open(file_path, "rb") as f:
            if show_progress:
                progress_bar = tqdm(total=total_size, unit="B", unit_scale=True, desc="Processing")
            while True:
                line_bytes = f.readline()
                if not line_bytes:
                    break
                if show_progress:
                    progress_bar.update(len(line_bytes))
                # Decode the line using utf-8 and ignore errors.
                try:
                    line = line_bytes.decode("utf-8", errors="ignore").strip()
                except Exception:
                    continue  # Skip lines that cause decoding issues.
                if not line:
                    continue

                # For matching, consider case sensitivity.
                word = line if case_sensitive else line.lower()

                if mode == "exact":
                    if word == search_term_to_use:
                        count += 1
                else:  # fragment mode
                    if search_term_to_use in word:
                        # Store the original line as the key.
                        fragment_results[line] = fragment_results.get(line, 0) + 1

            if show_progress:
                progress_bar.close()
    except Exception as e:
        print(f"Error while processing file: {e}")
        return

    # Build the result JSON structure.
    if mode == "exact":
        result = {search_term: count}
    else:
        result = {search_term: fragment_results}

    output_json = json.dumps(result, ensure_ascii=False, indent=4)
    print(output_json)

    # Save output to a file if requested.
    if save_output:
        output_file = f"{search_term}.json"
        counter = 1
        # If a file already exists, append a counter to the file name.
        while os.path.exists(output_file):
            output_file = f"{search_term}{counter}.json"
            counter += 1
        try:
            with open(output_file, "w", encoding="utf-8") as outf:
                outf.write(output_json)
            print(f"Output saved to {output_file}")
        except Exception as e:
            print(f"Error while writing output file: {e}")

if __name__ == '__main__':
    TOTAL()
