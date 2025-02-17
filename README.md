# Search Script

## Overview

This Python script searches a very large text file for either an exact word match or for a fragment (substring) match. The file is assumed to contain one word (or phrase) per line. To handle very large files, the script processes the file line by line using UTF-8 encoding with `errors="ignore"`.

In addition to counting the occurrences:
- **Exact Mode:** The script counts how many lines exactly match the search term.
- **Fragment Mode:** The script identifies all lines that contain the search term as a substring and counts the occurrences for each matching line.

The result is output as a JSON object:
- **Exact Mode Example:**
  ```json
  {"door": 5}

Fragment Mode Example:

{
    "door": {
        "garden door": 1,
        "room door": 1,
        "house door": 1
    }
}


Optionally, the script can display a real-time progress indicator (using tqdm) based on the file’s byte size, and the JSON result can be saved to a file. If a file with the intended name already exists, a counter is appended to the filename.

Features

Two Search Modes:

Exact Mode: Counts only full-line (exact) matches.

Fragment Mode: Finds and counts any word (line) that contains the search term as a substring.


Case Sensitivity:
The user can choose between case-sensitive or case-insensitive search.

Progress Indicator:
An optional progress bar (using tqdm) shows the processing progress in real time.

Output Saving:
Optionally save the JSON output to a file. If <search_term>.json exists, a counter (e.g. door1.json) is appended to create a unique filename.

Performance:
Processes the file line by line to manage memory usage for very large files.

Error Handling:
Handles file access errors, reading/decoding errors, and issues during output writing.


Requirements

Python 3.x

tqdm


To install tqdm, run:

pip install tqdm

Usage

Run the script from the command line as follows:

python search_script.py <file> <search_term> [--mode {exact,fragment}] [--case-sensitive] [--progress] [--save]

Positional Arguments:

<file>: Path to the text file containing words (one per line).

<search_term>: The word or fragment to search for.


Optional Arguments:

--mode {exact,fragment}:
Select the search mode. Default is exact.

--case-sensitive:
Enable case-sensitive search. By default, the search is case-insensitive.

--progress:
Display a progress bar showing how many bytes of the file have been processed.

--save:
Save the JSON output to a file named <search_term>.json. If such a file exists, a counter is appended (e.g., door1.json, door2.json, etc.).


Example Commands

Exact Match, Case-Insensitive (default):

python search_script.py wordlist.txt door

Exact Match, Case-Sensitive, with Progress Bar:

python search_script.py wordlist.txt Door --case-sensitive --progress

Fragment Search, Case-Insensitive, Save Output:

python search_script.py wordlist.txt door --mode fragment --save


Code Structure

TOTAL Function:
The entire search logic is encapsulated in a function named TOTAL(), which is called when the script is executed.

File Reading:
The file is read in binary mode to accurately update the progress bar (based on byte count). Each line is decoded with UTF-8 using errors="ignore".

Error Handling:
The script gracefully handles file access errors, decoding errors, and issues encountered during output writing.



---

This script provides a robust, modular, and performance-optimized solution for searching large text files with options for both exact and fragment matching.
