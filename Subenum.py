#!/usr/bin/env python3
"""
subdomain-enum - Fast subdomain enumeration via DNS resolution
"""

import socket
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

BANNER = """
     _     _                        
 ___| |_  | |__   ___ _ __  _   _ _ __ ___  
/ __| '_ \\| '_ \\ / _ \\ '_ \\| | | | '_ ` _ \\ 
\\__ \\ |_) | |_) |  __/ | | | |_| | | | | | |
|___/_.__/|_.__/ \\___|_| |_|\\__,_|_| |_| |_|
                              v1.3.2
"""


def resolve_subdomain(subdomain, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        ip = socket.gethostbyname(subdomain)
        return subdomain, ip
    except (socket.gaierror, socket.timeout):
        return subdomain, None


def load_wordlist(filepath):
    try:
        with open(filepath, 'r') as f:
            words = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return words
    except FileNotFoundError:
        print(f"[!] Wordlist not found: {filepath}")
        sys.exit(1)


def check_wildcard(domain):
    """Check if domain has wildcard DNS"""
    random_sub = f"thissubdomainshouldnotexist1337.{domain}"
    try:
        socket.gethostbyname(random_sub)
        return True
    except socket.gaierror:
        return False


def run_enum(domain, wordlist_path, threads=20, timeout=3, verbose=False):
    words = load_wordlist(wordlist_path)
    found = []
    
    print(f"[*] Target: {domain}")
    print(f"[*] Wordlist: {wordlist_path} ({len(words)} entries)")
    print(f"[*] Threads: {threads}")
    print(f"[*] Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    # wildcard check
    if check_wildcard(domain):
        print("[!] WARNING: Wildcard DNS detected. Results may contain false positives.")
        print("-" * 50)
    
    subdomains = [f"{word}.{domain}" for word in words]
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(resolve_subdomain, sub, timeout): sub 
            for sub in subdomains
        }
        
        completed = 0
        for future in as_completed(futures):
            completed += 1
            subdomain, ip = future.result()
            
            if ip:
                found.append((subdomain, ip))
                print(f"  [+] {subdomain} -> {ip}")
            elif verbose:
                print(f"  [-] {subdomain}")
            
            if completed % 100 == 0 and not verbose:
                sys.stdout.write(f"\r[*] Progress: {completed}/{len(subdomains)}")
                sys.stdout.flush()
    
    print(f"\n\n[+] Enumeration complete. Found {len(found)} subdomains.")
    return found


def save_results(results, output_file):
    with open(output_file, 'w') as f:
        for subdomain, ip in sorted(results):
            f.write(f"{subdomain},{ip}\n")
    print(f"[+] Results saved to {output_file}")


def main():
    print(BANNER)
    
    parser = argparse.ArgumentParser(description="subdomain-enum - Fast subdomain enumeration")
    parser.add_argument('-d', '--domain', required=True, help='Target domain')
    parser.add_argument('-w', '--wordlist', required=True, help='Wordlist file')
    parser.add_argument('-t', '--threads', type=int, default=20, help='Thread count')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show failed lookups')
    parser.add_argument('--timeout', type=int, default=3, help='DNS timeout')
    
    args = parser.parse_args()
    
    results = run_enum(
        args.domain,
        args.wordlist,
        threads=args.threads,
        timeout=args.timeout,
        verbose=args.verbose
    )
    
    if args.output and results:
        save_results(results, args.output)


if __name__ == "__main__":
    main()
