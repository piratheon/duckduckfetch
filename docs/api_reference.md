# API Reference

This document provides a detailed reference for the `DuckDuckFetch` Python library.

## `DuckDuckFetch` Class

The main class for interacting with DuckDuckGo search.

**`__init__(self, proxy_file: Optional[str] = None)`**

Initializes the `DuckDuckFetch` client.

-   **`proxy_file`** (Optional[str]): The path to a file containing a list of proxies.

**`search(self, query: str, region: Optional[str] = None, time_filter: Optional[str] = None, max_results: int = 10, retries: int = 3) -> List[Dict[str, str]]`**

Performs a search and returns a list of result dictionaries.

-   **`query`** (str): The search query.
-   **`region`** (Optional[str]): The region code (e.g., "us-en").
-   **`time_filter`** (Optional[str]): The time filter ("d", "w", "m", "y").
-   **`max_results`** (int): The maximum number of results to return.
-   **`retries`** (int): The number of times to retry with different proxies.

**Returns:** A list of dictionaries, where each dictionary represents a search result and has the following keys: `title`, `url`, and `snippet`.

**`search_json(self, query: str, region: Optional[str] = None, time_filter: Optional[str] = None, max_results: int = 10) -> str`**

Performs a search and returns the results as a JSON string.

-   **`query`** (str): The search query.
-   **`region`** (Optional[str]): The region code (e.g., "us-en").
-   **`time_filter`** (Optional[str]): The time filter ("d", "w", "m", "y").
-   **`max_results`** (int): The maximum number of results to return.

**Returns:** A JSON string representing the list of search results.

**`search_text(self, query: str, region: Optional[str] = None, time_filter: Optional[str] = None, max_results: int = 10) -> str`**

Performs a search and returns the results as a formatted text string.

-   **`query`** (str): The search query.
-   **`region`** (Optional[str]): The region code (e.g., "us-en").
-   **`time_filter`** (Optional[str]): The time filter ("d", "w", "m", "y").
-   **`max_results`** (int): The maximum number of results to return.

**Returns:** A formatted text string of the search results.
