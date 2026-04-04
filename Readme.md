# subdomain-enum

Subdomain enumeration tool using wordlists and DNS resolution. Built for recon phases during pentesting engagements.

## How it works

Reads a wordlist, prepends each word to the target domain, and checks if the subdomain resolves to a valid IP. Supports threading for faster scans.

## Usage

```bash
python3 subenum.py -d target.com -w wordlists/common.txt
python3 subenum.py -d target.com -w wordlists/common.txt -t 50 -o results.txt
```

## Options

| Flag | Description |
|------|-------------|
| `-d` | Target domain |
| `-w` | Wordlist file |
| `-t` | Number of threads (default: 20) |
| `-o` | Output file |
| `-v` | Verbose mode |
| `--timeout` | DNS timeout in seconds (default: 3) |

## Wordlists

Included in `wordlists/`:
- `common.txt` - Top 1000 most common subdomains
- `dev.txt` - Development/staging related names

## TODO

- [ ] Add wildcard detection
- [ ] Support for custom DNS resolvers
- [ ] Add brute-force mode with permutations
- [ ] Certificate transparency log parsing

## Disclaimer

For authorized testing only.
