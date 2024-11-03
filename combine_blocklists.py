import requests

# List of blocklist URLs (replace with your actual URLs)
blocklist_urls = [
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts",
    "https://big.oisd.nl/",
    # Add more URLs as needed
]

output_file = "combined_blocklist.txt"

def fetch_blocklist(url):
    """Fetches a blocklist and returns its lines."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.splitlines()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

def is_valid_host(line):
    """Checks if a line contains a valid host entry."""
    return (
        not line.startswith("#") and  # Exclude lines that start with #
        not line.startswith("||#") and  # Exclude lines that start with ||#
        (line.startswith("0.0.0.0") or
         line.startswith("127.0.0.1") or
         line.startswith("255.255.255.255") or
         line.startswith("::1") or
         line.startswith("||") or
         line.startswith("*.") or
         ("." in line and not line.startswith("!")))  # General hostname check
    )

def extract_host(line):
    """Extracts and formats the host from a line."""
    # Handle different formats
    if line.startswith("0.0.0.0") or line.startswith("127.0.0.1") or line.startswith("255.255.255.255") or line.startswith("::1"):
        return line.split()[1]  # Get the hostname after the IP
    elif line.startswith("||"):
        return line[2:-1]  # Remove || and trailing ^
    elif line.startswith("*."):
        return line.strip()  # Keep wildcard entries as is
    else:
        return line.strip()  # Strip any extra spaces for standard hosts

def combine_blocklists():
    """Combines multiple blocklists, counts unique hosts, and formats the output."""
    seen_hosts = set()
    combined_lines = []

    for url in blocklist_urls:
        lines = fetch_blocklist(url)
        print(f"Fetched {len(lines)} lines from {url}")  # Log the number of lines fetched

        for line in lines:
            if is_valid_host(line):
                host_entry = extract_host(line)
                if host_entry not in seen_hosts:
                    seen_hosts.add(host_entry)
                    # Format for AdGuard Home
                    if not line.startswith("||"):
                        formatted_entry = f"||{host_entry}^"  # Add AdGuard format
                    else:
                        formatted_entry = line  # Keep existing AdGuard format
                    combined_lines.append(formatted_entry)

    unique_host_count = len(seen_hosts)
    print(f"Total unique hosts counted: {unique_host_count}")  # Log unique host count
    combined_lines.insert(0, f"! Combined blocklist - {unique_host_count} unique hosts")
    
    # Write combined list to file
    with open(output_file, "w") as f:
        f.write("\n".join(combined_lines))
    print(f"Combined blocklist saved to {output_file} with {unique_host_count} unique hosts.")

if __name__ == "__main__":
    combine_blocklists()
