<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/3514f5e3-f354-4191-9acc-9538c6320c9a" />

# fastq2fasta

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Bash](https://img.shields.io/badge/Bash-4.0%2B-green.svg)](https://www.gnu.org/software/bash/)
[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)

FASTQ to FASTA, Solved Twice. A pair of robust Bash and Python tools that convert fastq files into fasta, for minimizing file size and ensuring compatibility with FASTA-only bioinformatics programs.

---

## 🎴 Overview

FASTQ files contain both sequence data and quality scores (4 lines per record), while FASTA files contain only sequences (2 lines per record). These converters extract the sequence information and discard quality scores, providing comprehensive validation and error handling throughout the process.

### Features

- **Comprehensive validation** - File existence, permissions, format, and integrity checks
- **Robust error handling** - Detailed error messages and graceful failure modes
- **Batch processing** - Convert multiple files in a single command
- **Safety checks** - Warns before overwriting existing files
- **Format verification** - Validates FASTQ structure before conversion
- **Cross-platform** - Bash version for Unix/Linux/macOS, Python version for any OS

---

## Quick Overview

### Bash Version

```bash
# Make the script executable
chmod +x fastq2fasta.sh

# Convert a single file
./fastq2fasta.sh sample.fastq

# Convert multiple files
./fastq2fasta.sh sample1.fastq sample2.fastq sample3.fq
```

### Python Version

```bash
# Convert a single file
python3 fastq2fasta.py sample.fastq

# Convert multiple files
python3 fastq2fasta.py sample1.fastq sample2.fastq sample3.fq
```
---

## Installation

### Clone the Repository

```bash
git clone https://github.com/BioInUmer/fastq2fasta.git
cd fastq2fasta
```

### ☑︎ Requirements

**Bash version:**
- Bash 4.0 or higher
- Standard Unix tools: `awk`, `wc`, `head`, `tail`, `dirname`

**Python version:**
- Python 3.x
- Standard library only (no external dependencies)

---

## ▶︎ Usage

### Command Syntax

```bash
# Bash
./fastq2fasta.sh file1.fastq [file2.fastq ...]

# Python
python3 fastq2fasta.py file1.fastq [file2.fastq ...]
```

### Input Requirements

- Files must have `.fastq` or `.fq` extension (case-insensitive for Python version)
- Files must follow standard FASTQ format (4 lines per sequence record)
- Files must be readable and non-empty

### Output

- Creates `.fasta` files in the same directory as input files
- Original FASTQ files remain unchanged
- Example: `sample.fastq` → `sample.fasta`

### Example Output

```
──────────────────────────────────────────
        fastq2fasta converter
──────────────────────────────────────────

  ✓ sample1.fastq → sample1.fasta
  ✓ sample2.fastq → sample2.fasta

·········································
 All conversions completed successfully!
──────────────────────────────────────────
```

---

## File Format Details

### FASTQ Format (Input)
```
@SEQ_ID
GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCACAGTTT
+
!''*((((***+))%%%++)(%%%%).1***-+*''))**55CCF>>>>>>CCCCCCC65
```

4 lines per record:
1. Header line starting with `@`
2. Nucleotide sequence
3. Separator line starting with `+`
4. Quality scores (same length as sequence)

### FASTA Format (Output)
```
>SEQ_ID
GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCACAGTTT
```

2 lines per record:
1. Header line starting with `>`
2. Nucleotide sequence

---

## Validation Features

Both implementations perform the following validations:

- ✓ Command-line arguments provided
- ✓ File existence verification
- ✓ Read permission checks
- ✓ File extension validation (`.fastq` or `.fq`)
- ✓ Non-zero file size check
- ✓ FASTQ format structure validation
- ✓ Complete record verification (line count divisible by 4)
- ✓ Write permission checks for output directory
- ✓ Overwrite confirmation for existing output files

---

## ⚠️ Error Handling

The converters handle various error conditions:

- Missing or invalid input files
- Permission denied errors
- Invalid FASTQ format
- Incomplete records (corrupted files)
- Disk space or write permission issues
- User cancellation of overwrites

All errors produce descriptive messages and exit with code 1.

---

## ⊚ Choosing Between Versions

### Use the Bash version when:
- Working primarily on Unix/Linux/macOS systems
- You prefer minimal dependencies
- You need maximum performance for very large files
- Integration with existing shell scripts

### Use the Python version when:
- Cross-platform compatibility is required
- Working on Windows systems
- You prefer Python's readability and maintainability
- Integration with Python pipelines

Both versions produce identical output and have equivalent functionality.

---

## Examples

### Basic Conversion
```bash
./fastq2fasta.sh reads.fastq
# Creates: reads.fasta
```

### Batch Processing
```bash
./fastq2fasta.sh data/*.fastq
# Converts all FASTQ files in the data directory
```

### With Wildcards
```bash
python3 fastq2fasta.py sample*.fq
# Converts all files matching the pattern
```

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Bug Reports

If you encounter any issues, please report them at:
https://github.com/BioInUmer/fastq2fasta/issues

## Acknowledgments

- Designed for bioinformatics workflows and sequence analysis pipelines
- Follows FASTQ and FASTA format specifications
- Built with reliability and user experience in mind

---

**Note:** These tools are designed for standard FASTQ files. Multi-line FASTA output is not currently supported (each sequence is written as a single line).
