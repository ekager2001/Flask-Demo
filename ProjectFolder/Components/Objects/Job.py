class Job:
    def __init__(self, values):
        self.title = values[0]
        self.company = values[1]
        self.description = values[2]
        self.html = None #merge html -> descirption, replace description with html 
        self.skillsRequired = None
        self.softSkillsRequired = None#Consider using only skills required 
        self.skillsNotMet = None
        self.match = None

    def getTitle(self):
        return self.title

    def getCompany(self):
        return self.company

    def getDescription(self):
        return self.description

    def getHTML(self):
        return self.html

    def getskillsRequire(self, soft=False):
        if(soft):
            return self.softSkillsRequired
        return self.skillsRequired

    def getMatch(self,match):
        return match 
        
    def setHTML(self, html):
        self.html = html

    def setSkillsReq(self, skillsRequired):
        self.skillsRequired = skillsRequired    

    def setSoftSkillsReq(self, softSkillsRequired):
        self.softSkillsRequired = softSkillsRequired          

    def setMatch(self, match):
        self.match = match

    def setSkillsNotMet(self, skillsNotMet):
        self.skillsNotMet = skillsNotMet      

    def getSkillsNotMet(self):
        return self.skillsNotMet