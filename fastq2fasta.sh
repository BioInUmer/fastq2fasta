#!/bin/bash
#===============================================================================
# FASTQ to FASTA Converter
#
# Description:
#   Converts one or more FASTQ files to FASTA format with comprehensive
#   validation and error handling. FASTQ files contain both sequence data
#   and quality scores, while FASTA files contain only sequences.
#
# Usage:
#   ./script.sh file1.fastq [file2.fastq ...]
#
# Arguments:
#   One or more FASTQ files (.fastq or .fq extension)
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
#   - bash
#   - awk
#   - Standard Unix tools (wc, head, tail, dirname)
#===============================================================================

#===============================================================================
# INPUT VALIDATION
#===============================================================================
echo ""
echo "─────────────────────────────────────────"
echo "        fastq2fasta converter"
echo "─────────────────────────────────────────"
echo ""

# Check if at least one argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 file1.fastq [file2.fastq ...]" >&2
    exit 1
fi

# Store all command-line arguments (FASTQ files) in an array
FASTQ_FILES=("$@")

#===============================================================================
# VALIDATION FUNCTION
#===============================================================================

# Validates FASTQ file format and accessibility
# Parameters:
#   $1 - Path to FASTQ file to validate
# Returns:
#   0 if valid, 1 if invalid
validate_fastq() {
    local file="$1"
    
    # Check if file exists in the filesystem
    if [ ! -f "$file" ]; then
        echo "Error: $file does not exist." >&2
        return 1
    fi
    
    # Check if file has read permissions
    if [ ! -r "$file" ]; then
        echo "Error: $file exists but cannot be read." >&2
        return 1
    fi
    
    # Verify file has valid FASTQ extension (.fastq or .fq)
    if [[ ! "$file" =~ \.(fastq|fq)$ ]]; then
        echo "Error: $file does not have a valid '.fastq' or '.fq' extension." >&2
        return 1
    fi
    
    # Check if file contains any data (size > 0 bytes)
    if [ ! -s "$file" ]; then
        echo "Error: $file is empty." >&2
        return 1
    fi
    
    # Validate basic FASTQ structure by examining first record
    # Extract first and third lines to check format markers
    local line1=$(head -n 1 "$file")
    local line3=$(head -n 3 "$file" | tail -n 1)
    
    # First line must start with @ (sequence identifier marker)
    if [[ ! "$line1" =~ ^@ ]]; then
        echo "Error: $file is not valid FASTQ (line 1 should start with @)." >&2
        return 1
    fi
    
    # Third line must start with + (separator marker)
    if [[ ! "$line3" =~ ^\+ ]]; then
        echo "Error: $file is not valid FASTQ (line 3 should start with +)." >&2
        return 1
    fi
    
    # All validation checks passed
    return 0
}

#===============================================================================
# MAIN PROCESSING LOOP
#===============================================================================

# Process each FASTQ file provided as command-line argument
for file in "${FASTQ_FILES[@]}"; do
    
    # Run validation checks on current file
    if ! validate_fastq "$file"; then
        exit 1
    fi
    
    # Generate output filename by replacing FASTQ extension with .fasta
    # First, remove .fastq extension if present
    base="${file%.fastq}"
    # Then, remove .fq extension if present
    base="${base%.fq}"
    # Append .fasta extension
    out_file="${base}.fasta"
    
    # Check if output file already exists to prevent accidental overwrites
    if [ -f "$out_file" ]; then
        echo "Warning: $out_file already exists and will be overwritten."
        read -p "Do you want to continue? (y/n): " answer
        # Accept 'y', 'Y', 'yes', or 'Yes' as confirmation
        if [[ ! "$answer" =~ ^[Yy](es)?$ ]]; then
            echo "Operation cancelled by user."
            exit 0
        fi
    fi
    
    # Verify write permissions for output directory
    out_dir=$(dirname "$out_file")
    if [ ! -w "$out_dir" ]; then
        echo "Error: Cannot write to directory $out_dir" >&2
        exit 1
    fi
    
    # Verify FASTQ file integrity by checking line count
    # FASTQ format requires exactly 4 lines per record
    line_count=$(wc -l < "$file")
    if [ $((line_count % 4)) -ne 0 ]; then
        echo "Error: $file has incomplete records ($line_count lines, not divisible by 4)." >&2
        echo "The file is corrupted or improperly formatted." >&2
        exit 1
    fi
    
    #===========================================================================
    # CONVERSION PROCESS
    #===========================================================================
    
    # Convert FASTQ to FASTA using awk
    # NR%4==1: Process every 4th line starting from line 1 (sequence headers)
    #          Replace @ with > and print the identifier
    #          substr($0, 2) removes the @ symbol from position 1
    # NR%4==2: Process every 4th line starting from line 2 (sequences)
    #          Print the sequence as-is
    # Lines 3 and 4 (+ separator and quality scores) are ignored
    if awk 'NR%4==1 {print ">" substr($0, 2)} NR%4==2 {print}' "$file" > "$out_file"; then
        
        # Verify successful file creation and non-zero size
        if [ -s "$out_file" ]; then
            echo -e "  ✓ $file → $out_file"
        else
            # Handle case where conversion completed but output is empty
            echo "Error: Output file $out_file is empty." >&2
            rm -f "$out_file"  # Clean up empty file
            exit 1
        fi
    else
        # Handle awk or file write errors
        echo "Error: Failed to convert $file" >&2
        # Remove incomplete or corrupted output file
        rm -f "$out_file"
        exit 1
    fi
    
done

#===============================================================================
# COMPLETION
#===============================================================================

# Indicate successful completion of all conversions
echo ""
echo "·········································"
echo " All conversions completed successfully!"
echo "─────────────────────────────────────────"
exit 0