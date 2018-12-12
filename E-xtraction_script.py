
# coding: utf-8

# # Before The 17th

# In[1]: Imports


import requests as req
import os

from bs4 import BeautifulSoup as bs


# In[2]: Functions


# Directory Specifier
def mke(name):
    print("\n")
    os.chdir("../")
    os.mkdir("downloads")
    os.chdir("downloads")
    # Create target Directory if don't exist
    if not os.path.exists(name):
        os.mkdir(name)
        print("Directory ", name,  " Created\n")

    # cd into the dir
    curr_dir = os.getcwd()
    os.chdir("{}/{}".format(curr_dir, name))

# Downloader


def download_img(url):
    file_name = url.replace(
        "https://66.media.tumblr.com/", "").replace("/", "_")
    img = req.get(url, allow_redirects=True).content
    print("Downloading Image: ", file_name)
    output = open(file_name, 'wb')
    output.write(img)
    output.close()

# Scraper


def scrape(name, start, url_set):
    # url formatter to get just the images - requires resetting
    print("Fetching {}th most recent post".format(start+50))
    url = "https://{}.tumblr.com/api/read?type=photo&num=50&start={}".format(
        name, start)
    res = req.get(url)
    soup = bs(res.text, "lxml")
    page = soup.find_all('photo-url')

    counter = 0
    while counter <= 50:
        for i in page:
            # Make sure this is the highest Quality available
            if i['max-width'] == "1280":
                # Put it in a set to guarantee uniqueness of images
                url_set.add(i.text)
                counter += 1

# Main Driver


def main():
    print("Please Enter Your Tumblr Tag\nEx: if your blog address is https://jeansatsu.tumblr.com, please enter jeansatsu.")
    name = input()
    print("\n")

    # url formatter to get just the images - requires resetting
    url = "https://{}.tumblr.com/api/read?type=photo&num=50&start=0".format(
        name)
    res = req.get(url)
    soup = bs(res.text, "lxml")

    # Total number of posts with images
    total_posts = int(soup.find("posts")['total']) - 1

    # Calculate how many loops you would need to get the whole posts
    num_loop = total_posts // 50

    print("You have total of ", total_posts, ". This will take ", num_loop,
          " sessions to complete. Allow me to analyze the time required.\n")
    if total_posts < 500:
        print("Post Numbers Small: This will be done in no time. Stare at the screen.\n")
    elif total_posts < 1500:
        print("Post Number Medium: This will take a bit to complete. Go read through Memes and come back.\n")
    elif total_posts < 2500:
        print("Post Number Large: This will take a while to complete. Go through reddit for a bit and come back.\n")
    else:
        print("Post Number WTF: WTF have you done with your time for the last 4 years? Go get a cup of coffee with extra shot of regrets. And start a Youtube video\n")

    url_set = set()

    for i in range(0, num_loop):
        scrape(name, i*50, url_set)

    # mkdir && cd
    mke("tumblr-{}".format(name))

    # download
    for url in url_set:
        download_img(url)

    print("\n")
    print("All Your Images are retrieved! Have a Fapulous Day!")


# In[3]: Run Main


if __name__ == "__main__":
    main()
