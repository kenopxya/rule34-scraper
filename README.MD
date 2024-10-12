# rule34-scraper
rule34-scraper is a Python script created to facilitate the `automatic download` of multiple files in formats such as `png`, `gif` and `mp4` from `rule34.xxx`. Through a terminal interface, you can enter a specific URL or tags that identify the files you want to download. From this information, the script offers several options: you can choose to download all files matching the tags, select a specific number of files or choose a range of pages to download the files.
## Installation
To install rule34-scraper, follow these steps:

1. Clone the repository: Open a terminal and run the following command to clone the repository:
    ```bash
    git clone https://github.com/kenopxya/rule34-scraper.git
    ```
2. Navigate to the project directory: Access the directory of the cloned project.:
    ```bash
    cd rule34-scraper
    ```
3. Install dependencies: Make sure you have pip installed. This project uses the       following libraries:

    - requests: to perform HTTP requests.
    - bs4 (Beautiful Soup 4): for parsing HTML content.
    ```bash
    pip install requests beautifulsoup4
    ```
4. Run the script: You can now run the script using Python:
    ```bash
    python rule34-scraper.py
    ```