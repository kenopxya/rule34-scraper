import os
import math
import requests
import bs4


HEADERS = {     
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
}

COLORS = {
    'red': '\033[31m',
    'green': '\033[32m',
    'reset': '\033[0m' 
}

BASE_PAG_URL = "https://rule34.xxx"

folder="defaultFolder"
principal_url = "https://rule34.xxx/index.php?page=post&s=list&tags=jahy"
download_mode = "all"
dl_count = 1
interval = [1, 1]

def download_file(post_url, file_name="defaultName"):      
    response = requests.get(post_url, headers=HEADERS)

    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        anchors = soup.find_all("a")

        for anchor in anchors:              
            href = anchor.get("href")

            if href and "//images" in href:         

                response_2 = requests.get(href, headers=HEADERS)
                
                if response_2.status_code == 200:
                    if "jpeg" in href or "png" in href or "jpg" in href:
                        with open(f"output/{folder}/{file_name}.png", "wb") as img:
                            img.write(response_2.content)
                            print(f"[{COLORS['green']}{file_name}{COLORS['reset']}] The PNG file at the url: {post_url} has been downloaded")
                    elif "gif" in href:
                        with open(f"output/{folder}/{file_name}.gif", "wb") as gif:
                            gif.write(response_2.content)
                            print(f"[{COLORS['green']}{file_name}{COLORS['reset']}] The GIF at the url: {post_url} has been downloaded")
                    elif "mp4" in href:
                        with open(f"output/{folder}/{file_name}.mp4", "wb") as mp4:
                            mp4.write(response_2.content)
                            print(f"[{COLORS['green']}{file_name}{COLORS['reset']}] The mp4 at the url: {post_url} has been downloaded")
                    else:
                        print(f"[{COLORS['red']}{file_name} the file type of the url was not recognized: {post_url} therefore it will not download")
                else:
                    print(f"{COLORS['red']}[ERROR]{COLORS['reset']} Received status code {response_2.status_code} in download_file, response_2")
    else:
        print(f"{COLORS['red']}[ERROR]{COLORS['reset']} Received status code {response.status_code} in download_file, response_1")


def get_posts_urls(pag_url):
    obtained_urls = []
    response = requests.get(pag_url, headers=HEADERS)

    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        anchors = soup.find_all("a")

        for anchor in anchors:
            preview = anchor.find("img", class_="preview")

            if preview:
                post_url = anchor.get("href")
                post_url = BASE_PAG_URL + post_url
                obtained_urls.append(post_url)

        return obtained_urls
    else:
        print(f"{COLORS['red']}[ERROR]{COLORS['reset']} Received status code {response.status_code} in get_pag_urls, response")

def check_page(pag_url):
    response = requests.get(pag_url, headers=HEADERS)

    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        anchors = soup.find_all("a")

        for anchor in anchors:
            preview = anchor.find("img", class_="preview")

            if preview:
                return True
            
        return False    

    else:
        print(f"{COLORS['red']}[ERROR]{COLORS['reset']} Received status code {response.status_code} in check_page, response")
        return False

def get_pags_urls():

    obtained_urls = []

    if download_mode == "all":
        i = 1
        while True:
            pid = f"&pid={42*i - 42}"
            pag_url = principal_url + pid
            
            if check_page(pag_url):
                obtained_urls.append(pag_url)
                i += 1
            else:
                break
            
    elif download_mode == "amount":
        pages_to_check = math.ceil(dl_count / 42)

        for i in range(1, pages_to_check + 1):
            pid = f"&pid={42*i - 42}"
            pag_url = principal_url + pid

            if check_page(pag_url):
                obtained_urls.append(pag_url)
            else:
                break

    elif download_mode == "interval":
        pages_to_check = range(interval[0], interval[1] + 1)

        for i in pages_to_check:
            pid = f"&pid={42*i - 42}"
            pag_url = principal_url + pid

            if check_page(pag_url):
                obtained_urls.append(pag_url)
            else:
                break
    
    return obtained_urls

def execute_scraper():
    print("initiating processes...")
    print("(This process may take a while if a large number of images need to be processed.)")
    pags_urls = get_pags_urls()
    posts_urls = []

    for pag_url in pags_urls:
        temp = get_posts_urls(pag_url)
        posts_urls = posts_urls + temp

    if download_mode == "amount":
        if dl_count < len(posts_urls):
            del_amount = len(posts_urls) - dl_count
            del posts_urls[-del_amount:]

    while True:
        choice = input(f"a total of {len(posts_urls)} files will be downloaded, do you want to continue? [Y/N]: ")
        print("")
        choice = choice.lower()
        choice = choice.replace(" ", "")

        if choice == "y" or choice == "n":
            break
        else:
            print(f"{COLORS['red']}[ERROR]{COLORS['reset']} choose a valid option.")

    if choice == "y":
        try: 
            for post_url in posts_urls:
                download_file(post_url, f"{posts_urls.index(post_url) + 1}")
            print("Download process finished. come back soon! ;)")
        except KeyboardInterrupt:
            print("detected, the files download process was stopped.")
    else:
        print("No files will be downloaded.")

#----------------------------------------------------------------------------------#

if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")

print("            _      _____ _  _                     ")
print(" _ __ _   _| | ___|___ /| || |  __  ____  ____  __.")
print("| '__| | | | |/ _ \ |_ \| || |_ \ \/ /\ \/ /\ \/ /")
print("| |  | |_| | |  __/___) |__   _| >  <  >  <  >  < ")
print("|_|_  \__,_|_|\___|____/   |_|(_)_/\_\/_/\_\/_/\_\.")
print("/ __|/ __| '__/ _` | '_ \ / _ \ '__|              ")
print("\__ \ (__| | | (_| | |_) |  __/ |                 ")
print("|___/\___|_|  \__,_| .__/ \___|_|                 ")
print("                   |_|                            ")
print("                                       by kenopxya")

while True:
    print("")
    print("select an option to set the URL:")
    print("1. Paste url")
    print("2. Use tags")

    choose = input("Choose an option (1/2): ")

    if choose == "1" or choose == "2":
        break
    else:
        print(f"\n{COLORS['red']}[ERROR]{COLORS['reset']} Choose a valid option.")

while True:
    if choose == "1":
        print("")
        print("Please paste the URL of the first page, ensuring that it does not contain '&pid=0.'")
        temp = input("Paste the url: ")
        if temp[:51] == "https://rule34.xxx/index.php?page=post&s=list&tags=":
            if not "&pid=" in temp:
                principal_url = temp
                break
            else:
                print(f"\n{COLORS['red']}[ERROR]{COLORS['reset']} Paste a valid url (paste the url without the '&pid=..').")
                print("example: https://rule34.xxx/index.php?page=post&s=list&tags=all")
        else:
            print(f"\n{COLORS['red']}[ERROR]{COLORS['reset']} Paste a valid url.")
            print("example: https://rule34.xxx/index.php?page=post&s=list&tags=all")
    else:
        print("")
        print("write the tags separated by spaces")
        print("example: tag_1 tag_2 tag_3 ...")
        tags = input("Enter tags: ")
        tags = tags.split(" ")

        temp = "https://rule34.xxx/index.php?page=post&s=list&tags="

        for tag in tags:
            temp = f"{temp}{tag}+"

        print("")
        print(f"generated URL: {temp}")
        principal_url = temp
        break

while True:
    print("")
    print("Choose the download mode:")
    print("1. Download all files")
    print("2. Download a specific amount of files") 
    print("3. Download files from a range of pages")

    choose = input("Enter your choice (1/2/3): ")

    if choose == "1" or choose == "2" or choose == "3":
        break
    else:
        print(f"\n{COLORS['red']}[ERROR]{COLORS['reset']} Choose a valid option.")

while True:
    if choose == "1":
        download_mode = "all"
        break
    elif choose == "2":
        print("")
        temp = input("Type the number of files to download: ")

        try:
            temp = int(temp)
            if temp > 0:
                dl_count = temp
                download_mode = "amount"
                break
            else:
                print(f"\n{COLORS['red']}[ERROR]{COLORS['reset']} Enter a number greater than 0.")
        except ValueError:
            print(f"\n{COLORS['red']}[ERROR]{COLORS['reset']} Enter a valid number.")
    else:
        print("")
        print("Please enter a closed interval separated by a comma.")
        print("For example, '1, 5'")
        temp_interval = input("Type the interval: ")
        temp_interval = temp_interval.replace(" ", "")
        temp_interval = temp_interval.split(",")
        
        try:
            if len(temp_interval) == 0 or len(temp_interval) > 2:
                print(f"\n{COLORS['red']}[ERROR]{COLORS['reset']} Enter a valid interval.")
            elif len(temp_interval) == 1:
                temp_interval = [int(temp_interval[0]), int(temp_interval[0])]
                interval = temp_interval
                download_mode = "interval"
                break
            else:
                temp_interval = [int(temp_interval[0]), int(temp_interval[1])]
                interval = temp_interval
                download_mode = "interval"          
                break
        except ValueError:
            print(f"\n{COLORS['red']}[ERROR]{COLORS['reset']} Enter a valid int nashe.")


print("")
print("Enter the name for the folder that will contain the downloaded files.")
print("The path for this folder will be: /output/{folder_name}")

folder = input("Type the name of the folder: ")

output_path = os.path.join("output")
path = os.path.join("output", folder)

if not os.path.exists(output_path):
    os.makedirs(output_path)

if not os.path.exists(path):
    os.makedirs(path)

print("")
print("Summary:")
print("URL:", principal_url)
print("Download mode:", download_mode)

if download_mode == "amount":
    print("amount of files to download:", dl_count)
elif download_mode == "interval":
    print("interval:", interval)
print("output folder:", folder)
print("")

execute_scraper()