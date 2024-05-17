#!/bin/bash

# Function to display usage information
usage() {
    echo "Usage: $0 [-d <target_domain>] [-t <num_threads>] [-w <wordlist>] [-l <wordlist_path>] [-h]"
    echo " -d <target_domain>   Target domain to perform recon on (required)"
    echo " -t <num_threads>     Number of threads for parallelization (default: 10)"
    echo " -w <wordlist>        Wordlist for directory bruteforcing (default: dicc.txt)"
    echo " -l <wordlist_path>   Path to the directory containing the wordlist (default: ~/dirsearch/db/)"
    echo " -h                   Display this help message"
    exit 1
}

# Parse command-line arguments
while getopts "d:t:w:l:h" opt; do
    case $opt in
        d) target_domain="$OPTARG" ;;
        t) num_threads="$OPTARG" ;;
        w) wordlist="$OPTARG" ;;
        l) wordlist_path="$OPTARG" ;;
        h) usage ;;
        *) usage ;;
    esac
done

# Check if target domain is provided
if [ -z "$target_domain" ]; then
    echo "Error: Target domain is required"
    usage
fi

# Set default values for optional arguments
num_threads=${num_threads:-10}
wordlist=${wordlist:-"dicc.txt"}
wordlist_path=${wordlist_path:-"${HOME}/dirsearch/db/"}

# Create a directory for storing the results
output_dir="recon-${target_domain}"
mkdir -p "$output_dir" || { echo "Error: Unable to create output directory"; exit 1; }
cd "$output_dir" || { echo "Error: Unable to change to output directory"; exit 1; }

# Check if required tools are installed
required_tools="/usr/bin/nmap /usr/bin/httprobe /usr/bin/python3"
for tool in $required_tools; do
    if [ ! -x "$tool" ]; then
        echo "Error: $tool is not installed or not executable. Please install it before running this script."
        exit 1
    fi
done

# Perform port scanning using nmap
echo "Starting port scan..."
nmap -sS -T4 "$target_domain" -oN nmap.txt

# Perform subdomain enumeration using custom script
echo "Starting subdomain enumeration..."
python3 /Recon-Tool/Sub-DomainEnum.py -d "$target_domain" -t "$num_threads" -o domains.txt

# Perform HTTP(S) probing using httprobe
echo "Starting HTTP(S) probing..."
cat domains.txt | httprobe -c "$num_threads" > urls.txt

# Perform directory bruteforcing using dirsearch
echo "Starting directory bruteforcing..."
python3 ~/dirsearch/dirsearch.py -L urls.txt -e php,asp,aspx,jsp,html,txt,cgi -t "$num_threads" -w "${wordlist_path}/${wordlist}" -o dirsearch.txt

echo "Recon complete! Results are stored in $output_dir"
