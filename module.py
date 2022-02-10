import requests
from datetime import datetime
from bs4 import BeautifulSoup
from math import nan, ceil
import json, re, os

headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"}

# html renderer functions
def render_html(url):
    req = requests.get(url,headers=headers)
    page = BeautifulSoup(req.text,"html.parser")
    return page

# tags: used in sbaflex
def get_urls(url,including=None):
    
    # optional functions
    def get_max(page):
        pagination = []
        for d in page.find("ul",class_="pagination").find_all("li"):
            try:
                d = int(d.get_text())
                pagination.append(d)
            except: pass
        return pagination[-1]

    urls = []
    page = render_html(url)
    ref = "https://www.sbaflex.com"
    for section in page.find_all("section",class_="vacancy-card"):
        link = ref+section.find("a")['href']
        urls.append(link)
    urls = list(dict.fromkeys(urls))
    if including == "max_page":
        max_page = get_max(page)
        return urls, max_page
    else:
        return urls

# tags: used in startpeople
def get_jobs_startpeople(url,including=None):
    
    # optional functions
    def get_max(page):
        total = page.find("span",{"class":"vacancies-counter","data-cy":"resultCounter"}).get_text()
        total = re.search("\d+",total).group()
        total = ceil(int(total)/10)
        return total
    
    page = render_html(url)
    results = page.find("div",id="vacancyResults").find("ul")
    ref = "https://startpeople.nl"
    jobs = []
    for li in results.find_all("li",class_="vacancy-card"):
        link = ref+li.find("a")['href']
        title = li.find("h2",class_="vacancy-title").get_text()
        city = li.find("span",class_="uc-map-marker").find_previous().get_text()
        hours = li.find("span",class_="uc-clock").find_previous().get_text()
        wage = li.find("span",class_="uc-euro").find_previous().get_text()
        desc = li.find("div",class_="vacancy-description").get_text().strip()
        job = {
            "Link": link,
            "Title": title,
            "City": city,
            "Hours": hours,
            "Wage": "€"+wage,
            "Description": desc
        }
        jobs.append(job)
    if including == "max_page":
        max_page = get_max(page)
        return jobs, max_page
    else:
        return jobs

# tags: used in pran
def get_jobs_pran(url,include=None):
    def get_max(page):
        pagination = page.find("div",id="pagination")
        numbers = []
        for tag in pagination.find_all("a",class_="page-numbers"):
            try:
                number = int(tag.get_text())
                numbers.append(number)
            except: pass
        max_page = max(numbers)
        return max_page
    jobs = []
    page = render_html(url)
    for a in page.find_all("a",class_=["job-block","d-block"]):
        try:
            try: link = a['data-url']
            except: link = nan
            try: title = a['data-title']
            except: title = nan
            try: city = a['data-location']
            except: city = nan
            try: wage = a.find("p").find_next("p").get_text()
            except: wage = nan
            try: hours = a['data-hours']
            except: hours = nan
            try: type_ = a['data-industry']
            except: type_ = nan
            job = {
                "Link": link,
                "Title": title,
                "City": city,
                "Wage": wage,
                "Hours": hours,
                "Type": type_
            }
            jobs.append(job)
        except: pass
    if include == "max_page":
        max_page = get_max(page)
        return jobs, max_page
    else:
        return jobs

# tags: used in robinjobs
def get_jobs_robinjobs(page):
    jobs = []
    for a in page.find_all("a",class_="vacancy-item"):
        try:
            link = a['href']
            title = a.find("h2").get_text().strip()
            company = a.find("div",class_="vacancy-item__name").get_text().strip()
            city = a.find("div",class_="vacancy-item__location").get_text().strip()
            pos_open = a.find("div",class_="vacancy-item__info").find("strong").get_text().strip()
            desc = a.find("div",class_="vacancy-item__description").get_text().strip()
            job = {
                "Link": link,
                "Title": title,
                "Company": company,
                "City": city,
                "Position Open": pos_open,
                "Description": desc
            }
            jobs.append(job)
        except: pass
    return jobs

# tags: used in covebo
def get_jobs_covebo(url,include=None):

    # optional functions
    def get_max(page):
        pagination = page.find("div",id="pagination")
        numbers = []
        for tag in pagination.find_all("a",class_="page-numbers"):
            try:
                number = int(tag.get_text())
                numbers.append(number)
            except: pass
        max_page = max(numbers)
        return max_page

    jobs = []
    page = render_html(url)
    for a in page.find_all("a",class_=["job-block","d-block"]):
        try:
            link = a['data-url']
            title = a['data-title']
            city = a['data-location']
            wage = a.find("span").find_next("span").get_text().strip()
            hours = a['data-hours']
            type_ = a['data-industry']
            job = {
                "Link": link,
                "Title": title,
                "City": city,
                "Wage": wage,
                "Hours": hours,
                "Type": type_
            }
            jobs.append(job)
        except: pass    
    if include == "max_page":
        max_page = get_max(page)
        return jobs, max_page
    else:
        return jobs

# tags: used in praca24
def get_max_page(page):
    max_page = page.find("div",class_="pages").find("span").get_text()
    max_page = [int(d) for d in re.findall("\d+",max_page)][-1]
    return max_page

# tags: used in praca24
def get_jobs_praca24(page):

    def get_description(job_url):
        page = render_html(job_url)
        published = page.find("li",id="cp_listed").get_text().split(": ")[-1]
        h3 = page.find("div",class_="single-main").find("h3",class_="description-area")
        description = h3.find_next("p").get_text().strip()
        return published, description

    jobs = []
    stop_signal = False
    curr_year = datetime.now().year
    for item in page.find_all("div",class_="post-block"):
        a = item.find("a")
        link = a['href']
        title = a['title']
        date, desc = get_description(link)
        date = [d for d in date.split(" ") if ":" not in d]
        year = int(date[-1])
        wage = item.find("p",class_="post-price").get_text().strip()
        if year == curr_year:
            job = {
                "Link": link,
                "Title": title,
                "Jop Description": desc,
                "Wage": wage,
                "Date": " ".join(date)
            }
            jobs.append(job)
        else:
            stop_signal = True
            break
    return jobs, stop_signal

# tags: used in holandiajoberall
def get_details(page):
    detail_dict = {}
    ul = page.find("ul",class_="job-details")
    for li in ul:
        text = li.get_text().strip()
        if ":" in text:
            key = text.split(":")[0].strip()
            value = text.split(":")[1].strip()
            detail_dict.update({key:value})
    for li in ul.find_next("ul"):
        text = li.get_text().strip()
        if ":" in text:
            key = text.split(":")[0].strip()
            value = text.split(":")[1].strip()
            detail_dict.update({key:value})
    return detail_dict

def scrape(name):

    if name == "holandiajoberall":
        i = 1
        urls = []
        max_target = 1000
        while len(urls) < max_target:
            url = f"https://holandia.jober.pl/?p={i}"
            page = render_html(url)
            a_tags = page.find("table",class_="job-results").find_all("a")
            urls.extend(a_tags)
            i += 1            
        jobs = []
        for i in range(len(urls)):
            url = urls[i]['href']
            title = urls[i]['title']
            e = {"url": url, "title": title}
            jobs.append(e)

        i = 1
        data = []
        for e in jobs:
            try:
                page = render_html(e['url'])
                detail_dict = get_details(page)
            except: detail_dict = None            
            if detail_dict != None:            
                agency = detail_dict['Firma']
                wage = detail_dict['Pensja']
                city = detail_dict['Miejscowość']
                country = detail_dict['Państwo']
                job = {
                    "Link": e['url'],
                    "Job Title": e['title'],
                    "Agency (Firma)": agency,
                    "Wage (Pansja)": wage,
                    "City (Miejscowosc)": city,
                    "Country (Panstwo)": country
                }
                data.append(job)
            i += 1
        return data

    elif name == "silverhand":

        # render the html
        url = "https://en.silverhand.eu/candidate/jobs/"
        page = render_html(url)

        # extract data
        jobs = []
        for li in page.find_all("li"):
            a = li.find("a",class_="job-link")
            if a != None:
                link = a['href']
                location = a.find("div",class_="job-location").get_text().strip()
                location = location.split(":")[-1].strip()
                wage = a.find("div",class_="value").get_text().strip()
                wage = wage.replace(" / ","/").replace(" /","/").replace("/ ","/")
                title = a.find("h3",class_="title").get_text().strip()
                job = {
                    "Link": link,
                    "Workplace": location,
                    "Title": title,
                    "Wage": wage,
                }
                jobs.append(job)
        return jobs
    
    elif name == "praca24":
        
        # scrape the first page
        url = "http://praca-holandia24.pl/ogloszenia"
        page = render_html(url)
        max_page = get_max_page(page)
        jobs, stop_signal = get_jobs_praca24(page)
            
        # iterate and scrape the next page
        for i in range(2,max_page+1):
            url = f"http://praca-holandia24.pl/ogloszenia/page/{i}/"
            page = render_html(url)
            new_jobs, stop_signal = get_jobs_praca24(page)
            jobs.extend(new_jobs)
            if stop_signal:
                break
        return jobs
    
    elif name == "covebo":
        url = "https://www.covebo.pl/oferty-pracy/?_page=1"
        jobs, max_page = get_jobs_covebo(url,include="max_page")
        for i in range(2,max_page+1):
            url = f"https://www.covebo.pl/oferty-pracy/?_page={i}"
            new_jobs = get_jobs_covebo(url)
            jobs.extend(new_jobs)
        return jobs
    
    elif name == "timingjobs":
        
        # scrape the li tags
        containers = []
        for i in range(1,7):
            url = "https://timingjobs.pl/jm-ajax/get_listings/"
            payload = {
                "lang": "",
                "search_categories": "",
                "search_keywords": "",
                "search_location": "",
                "filter_post_status": "publish",
                "per_page": 6,
                "orderby": "featured",
                "order": "desc",
                "page": i,
                "show_pagination": False,
            }
            data = requests.post(url,headers=headers,data=json.dumps(payload)).json()
            li_s = data['html']    
            containers.append(li_s)

        jobs = []
        for container in containers:
            tag = BeautifulSoup(container.strip(),"html.parser")
            for li in tag.find_all("li",class_="job_listing"):
                link = li.find("a")['href']
                title = li['data-title']
                company = li.find("img")['alt']
                location = li.find("div",{"class":"location"}).get_text().strip()
                wage = li.find("li",{"class":"job-type"}).get_text().strip()
                date = li.find("time")['datetime']
                job = {
                    "Link": link,
                    "Title": title,
                    "Company": company,
                    "Location": location,
                    "Wage": wage,
                    "Date": date,
                }
                jobs.append(job)
        return jobs
    
    elif name == "robinjobs":
        
        # scrape first page
        url = "https://robin.jobs/job-offers-abroad"
        page = render_html(url)
        jobs = get_jobs_robinjobs(page)

        # iterate and scrape the next page
        i = 2
        while True:
            url = f"https://robin.jobs/wp-admin/admin-ajax.php?action=getVacancyArchive&page={i}&firstArchivePostId=false"
            req = requests.get(url,headers=headers)
            data = req.json()
            result = data['firstArchivePostId']
            page = BeautifulSoup(data['postsHTML'],"html.parser")
            new_jobs = get_jobs_robinjobs(page)
            jobs.extend(new_jobs)
            if result == False: i += 1
            else: break
        return jobs
    
    elif name == "pran":

        # extract the data
        url = "https://www.pran.pl/oferty-pracy/?_page=1"
        jobs, max_page = get_jobs_pran(url,include="max_page")
        for i in range(2,max_page+1):
            url = f"https://www.pran.pl/oferty-pracy/?_page={i}"
            new_jobs = get_jobs_pran(url)
            jobs.extend(new_jobs)
        return jobs
    
    elif name == "startpeople":

        # extract the data
        url = "https://startpeople.nl/en/candidate/vacancies"
        jobs, max_page = get_jobs_startpeople(url,including="max_page")
        for i in range(2,max_page+1):
            try:
                url = f"https://startpeople.nl/en/candidate/vacancies?refinementList[language][0]=en&page={i}   "
                new_jobs = get_jobs_startpeople(url)
                jobs.extend(new_jobs)
            except: break
        return jobs
    
    elif name == "sbaflex":
        
        # scrape the initial
        url = "https://www.sbaflex.com/pl_PL/vacatures"
        urls, max_page = get_urls(url,including="max_page")
        curr_year = datetime.now().year

        # scrape jobs
        j = 0
        for i in range(max_page):
            url = f"https://www.sbaflex.com/pl_PL/vacatures/offset/{j}"
            new_urls = get_urls(url)
            urls.extend(new_urls)
            j += 10

        # extract the data
        jobs = []
        for url in urls:
            page = render_html(url)
            try:
                h1 = page.find("section",class_="vacancies-detail").find("h1")
                title = h1.get_text().strip()
            except: title = nan
            items = {}
            for key in ["date","city","salary","hours"]:
                try: value = page.find("span",class_=key).get_text().strip()
                except: value = nan
                items.update({key:value})
            
            job = {
                'Link': url,
                'Active Form': items['date'],
                'Region': items['city'],
                'Wage': items['salary'],
                'Hours': items['hours'],
                'Title': title
            }
            jobs.append(job)
        return jobs
    
    elif name == "werkze":

        # get all the items
        max_item = 500
        i = 16
        container = []
        while len(container) < max_item:
            url = "https://werkze.pl/jobs/" + str(i)
            page = render_html(url)
            ul = page.find("ul",class_="pages pagination")
            pagination = [li.get_text() for li in ul.find_all("li")]
            container.extend(page.find_all("div",class_="item"))
            if pagination[-1] == ">>" or pagination[-1] == ">":
                i += 16
            else:
                break

        # extract the data
        jobs = []
        for item in container[:500]:
            h5 = item.find("h5")
            link = h5.find("a")['href']
            title = item.find("h4").get_text().strip()
            p = item.find("p")
            wage = re.sub("\s+"," ",p.get_text())
            city = p.find_next("p").get_text().strip()
            job = {
                "Link": link,
                "Title": title,
                "Wage": wage,
                "City": city,
            }
            jobs.append(job)
        return jobs