import os
import re
import requests

def fetch_blocklist(url):
    """Fetch a blocklist from a URL and return a set of unique domains."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.text
        domains = set()
        for line in content.splitlines():
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue
            # Extract only valid domain from the line
            domain = re.sub(r'^(0\.0\.0\.0|127\.0\.0\.1)\s+', '', line)
            if domain:
                domains.add(domain)
        return domains
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return set()

def combine_blocklists(url_file):
    """Combines blocklists from URLs and removes duplicates."""
    combined_domains = set()
    
    # Read URLs from the URL file
    with open(url_file, 'r') as file:
        for url in file:
            url = url.strip()
            if url:
                print(f"Fetching blocklist from: {url}")
                combined_domains.update(fetch_blocklist(url))
    
    return combined_domains

def write_to_adguard_format(domains, output_file):
    """Writes the combined domains in AdGuard Home format."""
    with open(output_file, 'w') as file:
        for domain in sorted(domains):
            file.write(f"0.0.0.0 {domain}\n")
    print(f"Combined blocklist saved to {output_file}")

if __name__ == "__main__":
    # URL file containing list of blocklist URLs
    url_file = "blocklist_urls.txt"
    # Output file for AdGuard Home
    output_file = "combined_blocklist.txt"
    
    # Combine blocklists and remove duplicates
    combined_domains = combine_blocklists(url_file)
    # Write output in AdGuard Home format
    write_to_adguard_format(combined_domains, output_file)
