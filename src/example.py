from duckduckfetch import DuckDuckFetch

# Initialize with an optional proxy file
# The proxy file should contain one proxy per line
# Format: [protocol://]host:port
ddg = DuckDuckGoHTML(proxy_file="proxies_example.txt")

try:
    # 1. Get JSON output for a query
    print("--- Searching for 'python web scraping' (JSON) ---")
    json_results = ddg.search_json("python web scraping", region="us-en", max_results=5)
    print(json_results)
    print("-" * 20)

    # 2. Get formatted text output for another query
    print("\n--- Searching for 'machine learning tutorials' (Text) ---")
    text_results = ddg.search_text("machine learning tutorials", time_filter="m", max_results=3)
    print(text_results)
    print("-" * 20)

    # 3. Get a list of result objects (dictionaries)
    print("\n--- Searching for 'open source projects' (Python objects) ---")
    results = ddg.search("open source projects", max_results=4)
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   Snippet: {result['snippet']}\n")

except Exception as e:
    print(f"An error occurred: {e}")