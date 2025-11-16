#!/usr/bin/python3
# ===============================================================================
# FASTQ to FASTA Converter (Python Implementation)
#
# Description:
#   Converts one or more FASTQ files to FASTA format with comprehensive
#   validation and error handling. This Python implementation provides
#   cross-platform compatibility and robust file processing.
#
# Usage:
#   python3 fastq2fasta.py file1.fastq [file2.fastq ...]
#
# Arguments:
#   One or more FASTQ files (.fastq or .fq extension, case-insensitive)
#
# Output:
#   Creates corresponding .fasta files in the same directory as input files
#   (e.g., sample.fastq → sample.fasta)
#
# FASTQ Format (4 lines per record):
#   Line 1: @ followed by sequence identifier
#   Line 2: Raw sequence (A, C, G, T, N)
#   Line 3: + (optionally followed by identifier)
#   Line 4: Quality scores (same length as sequence)
#
# FASTA Format (2 lines per record):
#   Line 1: > followed by sequence identifier
#   Line 2: Raw sequence
#
# Requirements:
#   - Python 3.x
#   - Standard library modules: sys, os, re
#
# Exit Codes:
#   0 - Success
#   1 - Error (validation failed, file not found, permission denied, etc.)
# ===============================================================================

import sys
import os
import re

# ===============================================================================
# COMMAND-LINE ARGUMENT PARSING
# ===============================================================================

# Extract all command-line arguments except the script name (argv[0])
# These should be paths to FASTQ files to be converted
files = sys.argv[1:]

# ===============================================================================
# INPUT VALIDATION FUNCTIONS
# ===============================================================================


def argument_check(files):
    """
    Validates all command-line arguments and input files.

    Performs comprehensive validation including:
    - Presence of arguments
    - File existence
    - File permissions
    - File extension validation
    - File size check
    - FASTQ format validation

    Parameters:
        files (list): List of file paths provided by the user

    Returns:
        bool: True if all validations pass

    Exits:
        Terminates program with exit code 1 if any validation fails
    """

    # Check if user provided at least one file as argument
    if not files:
        print("Usage: python3 fastq2fasta.py <file1.fastq> <file2.fastq> ...")
        sys.exit(1)

    # Validate each file individually before processing
    for file in files:
        # Verify file exists in the filesystem
        if not os.path.isfile(file):
            print(f"Error: {file} does not exist.")
            sys.exit(1)

        # Check if file has read permissions for current user
        if not os.access(file, os.R_OK):
            print(f"Error: {file} exists but cannot be read.")
            sys.exit(1)

        # Validate file extension (.fastq or .fq, case-insensitive)
        # Uses regex to match extension at end of filename
        if not re.search(r'\.(fastq|fq)$', file, re.I):
            print(
                f"Error: {file} does not have a valid '.fastq' or '.fq' extension.")
            sys.exit(1)

        # Check if file contains any data (size > 0 bytes)
        if os.path.getsize(file) == 0:
            print(f"Error: {file} is empty.")
            sys.exit(1)

        # Validate FASTQ format structure
        if not validate_fastq_format(file):
            sys.exit(1)

    # All validation checks passed successfully
    return True


def validate_fastq_format(file):
    """
    Validates basic FASTQ format structure by examining the first record.

    FASTQ files must follow a 4-line pattern per sequence record:
    - Line 1: Header starting with @
    - Line 2: Nucleotide sequence
    - Line 3: Separator starting with +
    - Line 4: Quality scores

    Parameters:
        file (str): Path to the FASTQ file to validate

    Returns:
        bool: True if file appears to be valid FASTQ format, False otherwise
    """

    try:
        # Open file and read first record (4 lines) to validate structure
        with open(file, 'r') as fq:
            line0 = fq.readline()  # Header line (must start with @)
            line1 = fq.readline()  # Sequence line (nucleotides)
            line2 = fq.readline()  # Separator line (must start with +)
            line3 = fq.readline()  # Quality scores line

            # Verify file contains at least 4 lines (minimum for one record)
            if not line0 or not line1 or not line2 or not line3:
                print(
                    f"Error: {file} has less than 4 lines (incomplete FASTQ).")
                return False

            # Check if first line starts with @ symbol (FASTQ header marker)
            if not line0.startswith('@'):
                print(
                    f"Error: {file} is not valid FASTQ (Header should start with @).")
                return False

            # Check if third line starts with + symbol (FASTQ separator marker)
            if not line2.startswith('+'):
                print(
                    f"Error: {file} is not valid FASTQ (Third line should start with +).")
                return False

            # File passed basic FASTQ format validation
            return True

    except Exception as e:
        # Catch any unexpected errors during file reading
        print(f"Error validating {file}: {e}")
        return False

# ===============================================================================
# CONVERSION FUNCTION
# ===============================================================================


def fastq_to_fasta(in_files):
    """
    Converts FASTQ files to FASTA format.

    The conversion process:
    1. Reads FASTQ file line by line
    2. Extracts header (line 1) and sequence (line 2) from each 4-line record
    3. Converts @ to > in header
    4. Discards quality information (lines 3 and 4)
    5. Writes header and sequence to FASTA file

    Parameters:
        in_files (list): List of FASTQ file paths to convert

    Exits:
        Terminates program with exit code 1 if conversion fails
    """

    # Process each input file sequentially
    for file in in_files:
        # Generate output filename by replacing .fastq extension with .fasta
        # Uses regex substitution to handle case sensitivity
        out_file = re.sub(r'\.fastq$', '.fasta', file)

        # Check if output file already exists to prevent accidental data loss
        if os.path.isfile(out_file):
            print(
                f"Warning: {out_file} already exists and will be overwritten.")
            answer = input("Do you want to continue? (y/n): ")
            # Accept variations of "yes" or just "y"
            if answer.lower() not in ['y', 'yes']:
                print("Operation cancelled by user.")
                sys.exit(0)

        # Verify write permissions for output directory
        # Use current directory '.' if no directory specified
        out_dir = os.path.dirname(out_file) or '.'
        if not os.access(out_dir, os.W_OK):
            print(f"Error: Cannot write to directory {out_dir}")
            sys.exit(1)

        try:
            # Open input (read mode) and output (write mode) files simultaneously
            # Using context managers ensures proper file closure even if errors occur
            with open(file, 'r') as fq, open(out_file, 'w') as fa:
                line_num = 0  # Track line position to identify record components

                # Process FASTQ file line by line
                for line in fq:

                    # Line 0, 4, 8, ... (every 4th line starting from 0): Header
                    if line_num % 4 == 0:
                        # Replace @ with > for FASTA format
                        # line[1:] strips the first character (@) and keeps the rest
                        fa.write(f">{line[1:]}")

                    # Line 1, 5, 9, ... (every 4th line starting from 1): Sequence
                    elif line_num % 4 == 1:
                        # Write sequence line unchanged to FASTA file
                        fa.write(line)

                    # Lines 2 and 3 (separator + and quality scores) are skipped
                    # These lines are not needed in FASTA format

                    line_num += 1

                # Validate that file contained complete 4-line records
                # Incomplete records suggest file corruption or truncation
                if line_num % 4 != 0:
                    print(
                        f"Warning: {file} had incomplete records ({line_num} lines).")

            # Confirm successful conversion to user
            print(f"  ✓ {file} → {out_file}")

        except IOError as e:
            # Handle file I/O errors (disk full, permission changes during execution, etc.)
            print(f"Error reading/writing {file}: {e}")
            sys.exit(1)
        except Exception as e:
            # Catch any other unexpected errors during conversion
            print(f"Unexpected error processing {file}: {e}")
            sys.exit(1)

# ===============================================================================
# MAIN PROGRAM EXECUTION
# ===============================================================================


if __name__ == "__main__":

    print("")
    print("─────────────────────────────────────────")
    print("        fastq2fasta converter")
    print("─────────────────────────────────────────")
    print("")

    # Validate all command-line arguments and input files
    argument_check(files)

    # Convert all validated FASTQ files to FASTA format
    fastq_to_fasta(files)

    print("")
    print("·········································")
    print(" All conversions completed successfully!")
    print("─────────────────────────────────────────")
