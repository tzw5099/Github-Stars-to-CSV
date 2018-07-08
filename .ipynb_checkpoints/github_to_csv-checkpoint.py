import pandas as pd
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 
from tqdm import tqdm

def GitHubStarsToCSV(GitHubUsername):
    df_list = []
    url1 = urlopen("https://github.com/{}?page=1&tab=stars".format(GitHubUsername)).read().decode('utf-8')
    soup = BeautifulSoup(url1, features='lxml')
    last_page = soup.find_all("div","pagination")
    last_page = [l.get_text().split(" ") for l in last_page]
    last_page = int(last_page[0][-2])
    for k in tqdm(range(1,last_page+1)):
        try:
            url = urlopen("https://github.com/{}?page={}&tab=stars".format(GitHubUsername,k)).read().decode('utf-8')
            soup = BeautifulSoup(url, features='lxml')
            all_href = soup.find_all("div","d-inline-block mb-1")
            all_href = [l.a["href"].split("/") for l in all_href]
            all_users = []
            all_repos = []
            url_list = []
            for a,x in enumerate(soup.find_all("div","d-inline-block mb-1")):
                for anchor in x.findAll('a', href=True):
                    url_list.append("{}{}".format("https://github.com/",anchor['href']))

            for x in all_href:
                all_users.append(x[1])
                all_repos.append(x[2])
            all_desc = []
            all_desc_loop = soup.find_all("div","py-1")
            for n,x in enumerate(all_descr_loop):
                if "d-inline-block col-9 text-gray pr-4" in str(x): 
                    for e in (x.find_all("p",itemprop="description")):
                        all_desc.append(e.get_text(strip=True))
                if "d-inline-block col-9 text-gray pr-4" not in str(x): 
                    all_desc.append("")
            all_lang_list = []
            all_lang = soup.find_all("div","f6 text-gray mt-2")
            for n,x in enumerate(all_lang):
                if "programmingLanguage" in str(x): 
                    for e in (x.find_all("span",itemprop="programmingLanguage")):
                        all_lang_list.append(e.get_text(strip=True))
                if "programmingLanguage" not in str(x): 
                    all_lang_list.append("")

            len(all_lang_list)
            all_count_stars = []
            all_count_forks = []
            for a,x in enumerate(soup.find_all("div","f6 text-gray mt-2")):
                if "octicon-repo-forked" in str(x): 
                        for asf,asd in enumerate(x):
                            if "octicon-star" in str(asd): 
                                all_count_stars.append(asd.get_text(strip=True))
                            if "octicon-repo-forked" in str(asd): 
                                all_count_forks.append(asd.get_text(strip=True))
                if "octicon-repo-forked" not in str(x):
                    for asf,asd in enumerate(x):
                        if "octicon-star" in str(asd): 
                                    all_count_stars.append(asd.get_text(strip=True))
                    all_count_forks.append(0)
            all_time = soup.find_all("relative-time")
            all_easy_time = [l.get_text(strip=True) for l in all_time]
            all_time = [l["datetime"] for l in all_time]
            df = pd.DataFrame.from_dict({'repo_url':url_list,'username':all_users,'repos':all_repos,'description':all_desc,'language':all_lang_list,'forks':all_count_forks,'count_stars':all_count_stars, 'easy_time':all_easy_time,'time':all_time})
            df_list.append(df)
        except Exception as e:
            print (str(e))
    return df_list

df_list = GitHubStarsToCSV("tzw5099") #<-- Change to your username