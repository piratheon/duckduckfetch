# DuckDuckFetch: A Python Library for DuckDuckGo Search

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)

DuckDuckFetch is a lightweight and easy-to-use Python library for scraping search results from DuckDuckGo's HTML and lite versions. It is designed to be simple, robust, and easy to integrate into your projects.

## Features

-   **Simple Interface**: A clean and straightforward API for fetching search results.
-   **Proxy Support**: Rotate through a list of proxies to avoid getting blocked.
-   **Multiple Output Formats**: Get results as a list of dictionaries, a JSON string, or formatted text.
-   **No JavaScript Required**: Scrapes the HTML-only versions of DuckDuckGo, so no need for a headless browser.

## Installation

You can install DuckDuckFetch directly from this GitHub repository:

```bash
git clone https://github.com/piratheon/duckduckfetch.git
cd duckduckfetch
python -m venv .venv
.venv/bin/pip install -r src/requirements.txt
```

## Usage

Here's a quick example of how to use DuckDuckFetch:

```python
from python.duckduckfetch import DuckDuckFetch

# Initialize the client (optionally with a proxy file)
ddf = DuckDuckFetch(proxy_file="python/proxies_example.txt")

try:
    # Perform a search and get a list of results
    results = ddf.search("Python web scraping", max_results=5)
    for result in results:
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Snippet: {result['snippet']}\n")

    # Get results as a JSON string
    json_results = ddf.search_json("machine learning tutorials", max_results=3)
    print(json_results)

except Exception as e:
    print(f"An error occurred: {e}")
```

## Proxy Support

To use proxies, create a file (e.g., `proxies.txt`) with a list of your proxies, one per line. The format is `scheme://ip:port` or `ip:port`.

```txt
# HTTP proxies
http://192.168.1.100:8080
https://proxy.example.com:3128

# SOCKS5 proxy
socks5://10.0.0.5:1080
```

Then, pass the path to your proxy file when initializing `DuckDuckFetch`:

```python
ddf = DuckDuckFetch(proxy_file="proxies.txt")
```

## API Reference

For a detailed API reference, please see [`docs/api_reference.md`](docs/api_reference.md).

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

>This library is intended for educational purposes only. Please respect DuckDuckGo's terms of service. I'm not responsible for any misuse of this library.
