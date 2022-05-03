import asyncio
from urllib.request import Request, urlopen
import re
from bs4 import BeautifulSoup

#Original Work
class WebScraper: #Indeed specific code
    def __init__(self, mode="url"):
        self.url = ""
        self.mode = ""
        self.soup = ""
    def getMode(self):
        return self.mode 

    def set_Mode(self, mode):
        self.mode = mode

    def getURL(self):
        return self.url 

    def set_URL(self, url):
        #structure for values tuple (0:template for url, 1:tuple of values)
        if self.getMode() == "url":
            self.url = url
            self.url = self.url.replace(" ", "%20")
        if self.getMode() =="job":
            self.url = url
            print(self.url)

    def createSoup(self):
        req = Request(self.getURL(), headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        self.soup = BeautifulSoup(webpage, 'html.parser')
    

    def webScrape(self, jbPost=[], searchQuery=["",""]):
        #URL mode will return a list of  tuples of (jobTitle, jobCompany, JobID)
        cleaner =  re.compile('<.*?>')
        jobPosts=[]
        if self.getMode() =="url":
            position = searchQuery[0]
            location = searchQuery[1] 
            position = position.replace(" ", "-").lower()
            location = location.replace(" ", "-").lower()
            searchString = "{}-jobs-in-{}".format(position,location)
            url = 'https://www.reed.co.uk/jobs/{}'.format(searchString)
            self.set_URL(url)
            self.createSoup()
            cards = self.soup.find_all('article', class_='job-result')
            jobIDs = self.getIds(cards)
            index = 0
            while index < 3:
                c = cards[index]
                title = c.find('h3').text
                companyName = c.find('div', 'posted-by').find('a').text
                jobPosts.append((title,companyName,jobIDs[index]))
                index += 1
            return jobPosts
        #job mode will return a list of  tuples of (jobTitle, jobCompany, JobDesc)
        if self.getMode() == "job":
            jobsList = []
            for j in jbPost:
                position = j[0].replace(" ", "-").lower().strip('\n')
                url = 'https://www.reed.co.uk/jobs/{}/{}'.format(position,j[2])
                self.set_URL(url)
                self.createSoup()
                jobDesc= self.jobDescription(self.soup)
                clean = self.cleanhtml(jobDesc, cleaner)
                jobsList.append((j[0],j[1],clean))
            return jobsList

    def jobDescription(self, jobSoup):
        desc = jobSoup.find('div','description')
        if desc == None:
            desc = jobSoup.find('div','branded-job--description')
        return desc.span.text

    def cleanhtml(self,raw_html,cleaned):
            cleantext = re.sub(cleaned, ' ' , str(raw_html))
            return cleantext 

    def getIds(self, cards):
        x=0
        ids = []
        spans = []
        for c in cards:
            spans.append(c.find_all('span', class_='job-result-anchor'))
            x += 1
        for s in spans:
            ids.append(s[0].get('id')[3:])
        return ids