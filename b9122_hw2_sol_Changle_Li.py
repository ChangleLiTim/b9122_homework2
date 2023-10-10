#!/usr/bin/env python
# coding: utf-8

# In[1]:


import urllib.request
import urllib.parse
from bs4 import BeautifulSoup


# ## Question 1 (1)

# In[2]:


# Set up the seed url
Seed_Url = "https://press.un.org/en"
Press_Releases = []    # Create a list to store web addresses
urls = [Seed_Url]    # Queue of urls to crawl
seen = [Seed_Url]    # Stack of urls seen so far
Number_of_Press_Release = 0

# Custom User-Agent Header
Headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

while len(Press_Releases) < 10:
    curr_url = urls.pop(0)
    try:
        # First Step: Start by visiting the seed
        info = urllib.request.Request(curr_url,headers=Headers)
        html = urllib.request.urlopen(info)
        
        # We do not want content type other than html
        if 'html' not in html.headers.get('Content-Type').lower():
            print(f"This {curr_url} is not an HTML, so we are skipping")
            continue
            
        # Turn the html into a bytes object
        webpage = html.read()
        soup = BeautifulSoup(webpage,'html.parser')
        
        # Check whether this HTML is a press release
        if soup.find('a', {'href': '/en/press-release', 'hreflang': 'en'}):
            if "crisis" in soup.get_text().lower() and curr_url not in Press_Releases:
                Press_Releases.append(curr_url)
                Number_of_Press_Release += 1
                with open(f"1_{Number_of_Press_Release}.txt", "w", encoding="utf-8") as file:
                    file.write(str(soup))
        
        # Second Step: Identify hyperlinks
        for link in soup.find_all('a', href=True):
            Child_Url = urllib.parse.urljoin(Seed_Url, link['href'])
            # Ignore other websites' contents
            if Child_Url not in seen and Child_Url.startswith(Seed_Url):
                urls.append(Child_Url)
                seen.append(Child_Url)
            
    except Exception as ex:
        # we could examine our code error if necessary by printing the error
        continue

# Final Step: Print the examined web addresses
if len(Press_Releases) != 0:
    print("Found United Nations Press Releases Containing the Word 'crisis':")
    for Web_Addresses in Press_Releases:
        print(Web_Addresses)
else:
    print("Nothing Found")


# ## Question 1 (2)

# In[3]:


# Set up the seed URL
Seed_Url = "https://www.europarl.europa.eu/news/en/press-room"
Press_Rooms = []    # Create a list to store web addresses
urls = [Seed_Url]      # Queue of URLs to crawl
seen = [Seed_Url]      # Stack of URLs seen so far
Number_of_Press_Release = 0

# Custom User-Agent Header
Headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

while len(Press_Rooms) < 10:
    curr_url = urls.pop(0)
    try:
        # First Step: Start by visiting the seed
        info = urllib.request.Request(curr_url, headers=Headers)
        html = urllib.request.urlopen(info)
        
        # We do not want content type other than html
        if 'html' not in html.headers.get('Content-Type').lower():  # ensure that we are dealing with an HTML file
            print(f"This {curr_url} is not an HTML, so we are skipping")
            continue
        
        # Turn the html into a bytes object
        webpage = html.read()
        soup = BeautifulSoup(webpage, 'html.parser')

        # Check whether this HTML is a plenary session
        if soup.find('span', {'class': 'ep_name'}, string="Plenary session"):
            # Aviods the websites that are not an actual article
            if "crisis" in soup.get_text().lower() and curr_url not in Press_Rooms and not ("contentType" in curr_url or "keywordValue" in curr_url):
                Press_Rooms.append(curr_url)
                Number_of_Press_Release += 1
                with open(f"2_{Number_of_Press_Release}.txt", "w", encoding="utf-8") as file:
                    file.write(str(soup))

        # Second Step: Identify hyperlinks
        for link in soup.find_all('a', href=True):
            Child_Url = urllib.parse.urljoin(Seed_Url, link['href'])
            # Ignore other websites' contents
            if Child_Url not in seen and Child_Url.startswith(Seed_Url):
                urls.append(Child_Url)
                seen.append(Child_Url)

    except Exception as ex:
        # we could examine our code error if necessary by printing the error
        continue

# Final Step: Print the examined web addresses
if len(Press_Rooms) != 0:
    print("Found European Parliament Press Releases Covering Plenary Sessions and Containing the Word 'crisis':")
    for url in Press_Rooms:
        print(url)
else:
    print("Nothing Found")

# Both codes are similar but they have different find attribute
