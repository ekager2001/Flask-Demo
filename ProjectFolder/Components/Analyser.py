import time
from .Objects.Candidate import Candidate
from .SkillsExtractor import SkillsExtractor
from .WebScraper import WebScraper
from .Objects.Skills import Skills
from .Objects.Job import Job 
from .Objects.Candidate import Candidate
import sys

#This class combines the Skills extractor and Web scraper to make them easy to access:`
#This is all my original owrk
class Analyser:
    def __init__(self):
        self.SkillsExtractor = ""
        self.WebScraper = ""

    #Getters and setters
    def setSkillsExtractor(self, SkillsExtractor):
        self.SkillsExtractor = SkillsExtractor

    def getSE(self):
        return self.SkillsExtractor

    def setWebScraper(self, WebScraper):
        self.WebScraper = WebScraper
        
    def getWS(self):
        return self.WebScraper

    #Create Skills extractor and implement pre-made model
    def createSkillsExtractor(self, skill_pattern_path):
        SE = SkillsExtractor(skill_pattern_path)
        self.setSkillsExtractor(SE)
        print(sys.path[1])
        self.getSE().start("ProjectFolder/Components/ModelData/model-last")
        
    #Delete previous webscraper, create a new one
    def createWebScraper(self):
        WS= WebScraper()
        self.setWebScraper(WS)

    #extract skills
    def skillsExtract(self, rawtext):
        entitySkills = []
        skills =  self.getSE().unique_skills(self.getSE().get_skills(rawtext.lower()))
        #print(skills)
        softSkills = self.getSE().unique_skills(self.getSE().get_soft_skills(rawtext.lower())) 
        #print(softSkills)
        entitySkills.append(Skills((skills,softSkills)))
        html = self.getSE().display(rawtext.lower())
        return (html, entitySkills)

    def webScrape(self, searchQ, resumeSkills):
       #searchQ=(position, location)
        self.getWS().set_Mode('url')
        JobPosts= self.getWS().webScrape(searchQuery=searchQ)
        self.getWS().set_Mode('job')
        JobPostings =  self.getWS().webScrape(jbPost=JobPosts)
        jobs =[Job(list(j)) for j in JobPostings]
        for j in jobs:
            j.setHTML(self.getSE().display(str(j.getDescription())))
            j.setSkillsReq(self.getSE().unique_skills(self.getSE().get_skills(str(j.getDescription()).lower())))
            j.setSoftSkillsReq(self.getSE().unique_skills(self.getSE().get_soft_skills(str(j.getDescription()).lower())))
            resume_Skills = resumeSkills[0].getSkills().copy()
            resume_SoftSkills = resumeSkills[0].getSoftSkills().copy()           
            resume_Skills.extend(resume_SoftSkills)
            req_Skills = j.getskillsRequire().copy()
            req_SoftSkills = j.getskillsRequire(soft=True).copy()
            req_Skills.extend(req_SoftSkills)
            tuple = self.getSE().skillsCheck(req_Skills, extract=resume_Skills)
            match = tuple[0]
            skillsNotMet = tuple[1]
            skillsMet = tuple[2]
            j.setSkillsNotMet(skillsNotMet)
            j.setMatch(match)
        jobs.sort(key=lambda x: x.match, reverse = True)
        return jobs

    def rankCandidates(self, listCandidates, jobDescSkills):
        candidates = [Candidate(list(c)) for c in listCandidates]
        for c in candidates:
            c.setHTML(self.getSE().display(str(c.getText())))
            c.setSkillSet(self.getSE().unique_skills(self.getSE().get_skills(str(c.getText()).lower())))
            c.setSoftSkillSet(self.getSE().unique_skills(self.getSE().get_soft_skills(str(c.getText()).lower())))
            reqSkillset = jobDescSkills[0].getSkills().copy()
            reqSoftSkills = jobDescSkills[0].getSoftSkills().copy()           
            reqSkillset.extend(reqSoftSkills)
            print(reqSoftSkills[1].skill)
            skillSet = c.getSkillSet().copy()
            softSkillSet = c.getSkillSet(soft=True).copy()
            skillSet.extend(softSkillSet)
            tuple = self.getSE().skillsCheck(reqSkillset, extract=skillSet)
            match = tuple[0]
            skillsNotMet = tuple[1]
            skillsMet = tuple[2]
            c.setSkillsNotMet(skillsNotMet)
            c.setSkillsMet(skillsMet)
            c.setMatch(match)
        candidates.sort(key=lambda x: x.match, reverse = True)
        return candidates

    def compare(self, jobInfo, resumeSkills):
       #searchQ=(position, location)
        j = Job(jobInfo)
        j.setHTML(self.getSE().display(str(j.getDescription())))
        j.setSkillsReq(self.getSE().unique_skills(self.getSE().get_skills(str(j.getDescription()).lower())))
        j.setSoftSkillsReq(self.getSE().unique_skills(self.getSE().get_soft_skills(str(j.getDescription()).lower())))
        resume_Skills = resumeSkills[0].getSkills().copy()
        resume_SoftSkills = resumeSkills[0].getSoftSkills().copy()           
        resume_Skills.extend(resume_SoftSkills)
        req_Skills = j.getskillsRequire().copy()
        req_SoftSkills = j.getskillsRequire(soft=True).copy()
        req_Skills.extend(req_SoftSkills)
        tuple = self.getSE().skillsCheck(req_Skills, extract=resume_Skills)
        match = tuple[0]
        skillsNotMet = tuple[1]
        skillsMet = tuple[2]
        j.setSkillsNotMet(skillsNotMet)
        j.setMatch(match)
        return [j]