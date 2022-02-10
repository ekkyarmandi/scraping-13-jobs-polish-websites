# import libraries
from module import scrape
from tqdm import tqdm
import pandas as pd
import os

# clear the terminal
try: os.system("cls")
except: os.system("clear")

# preparing the websites name
websites = [
    "silverhand",
    "praca24",
    "covebo",
    "timingjobs",
    "robinjobs",
    "pran",
    "startpeople",
    "sbaflex",
    "werkze",
    "holandiajoberall"
]

writer = pd.ExcelWriter("results.xlsx")
msg = f"Scraping {len(websites)} Job Ads"
for name in tqdm(websites,msg):
    jobs = scrape(name)
    df = pd.DataFrame(jobs)
    df.to_excel(
        writer,
        sheet_name = name,
        index = False,
        encoding = "utf-8"
    )
writer.save()