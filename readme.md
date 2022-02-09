# Scraping Script for Scraping 13 Polish Job Advertisement Websites

In this project I write and manage 13 unique scraping script to scrape job ads from 13 websites. Below are the list of 13 websites which will be scrape:
* [holandia.jober.pl](https://holandia.jober.pl/?p=1)
* [en.silverhand.eu](https://en.silverhand.eu/candidate/jobs/?q=&location=)
* [praca-holandia24.pl](http://praca-holandia24.pl/)
* [covebo.pl](https://www.covebo.pl/oferty-pracy/)
* [timingjobs.pl](https://timingjobs.pl/)
* [jobs.pl](https://www.jobs.pl/praca-za-granica/praca-fizyczna/niemcy?locations[0]=8470&locations[1]=8266&locations[2]=8244&locations[3]=8236&locations[4]=8299&locations[5]=8324&locations[6]=8281&locations[7]=8419&locations[8]=8389)
* [eena.pl](https://eena.pl/aktualne-oferty-pracy-w-holandii.html)
* [robin.job](https://robin.jobs/job-offers-abroad)
* [pracuj.nl](https://pracuj.nl/oferty-pracy/-/-/-/10/0/title/-//)
* [pran.pl](https://www.pran.pl/oferty-pracy/)
* [startpeople.nl](https://startpeople.nl/en/candidate/vacancies)
* [sbaflex.com](https://www.sbaflex.com/pl_PL/vacatures)
* [werkze.pl](https://werkze.pl/jobs/48)

## Script Development

Most of the script only using requests, BeautifulSoup, and pandas module. For more details, requests script used to make a GET/POST requests into the websites and rendering the html on the backend, while BeautifulSoup module used to extract the desired data from html tags.