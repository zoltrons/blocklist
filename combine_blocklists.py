import requests
import os

# List of blocklist URLs
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

def combine_blocklists():
    """Combines multiple blocklists, counts unique hosts, and formats the output."""
    seen_hosts = set()
    combined_lines = []

    for url in blocklist_urls:
        lines = fetch_blocklist(url)
        for line in lines:
            # Preserve metadata comments
            if line.startswith("!") or line.startswith("#"):
                continue  # Skip existing descriptions
            elif line.startswith("0.0.0.0") or line.startswith("127.0.0.1"):
                # Standardize and check if host is already added
                host_entry = line.split()[1]
                if host_entry not in seen_hosts:
                    seen_hosts.add(host_entry)
                    combined_lines.append(line)

    # Create a new description with the count of unique hosts
    unique_host_count = len(seen_hosts)
    combined_lines.insert(0, f"! Combined blocklist - {unique_host_count} unique hosts")
    
    # Write combined list to file
    with open(output_file, "w") as f:
        f.write("\n".join(combined_lines))
    print(f"Combined blocklist saved to {output_file} with {unique_host_count} unique hosts.")

if __name__ == "__main__":
    combine_blocklists()
