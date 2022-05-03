class Candidate:
    def __init__(self, values):
        self.name = values[0]
        self.text = values[1]
        self.html = None #merge html -> descirption, replace description with html 
        self.skillSet = None
        self.softSkillSet = None#Consider using only skills required 
        self.skillsNotMet = None
        self.skillsMet = None
        self.match = None

    def getName(self):
        return self.name

    def getText(self):
        return self.text

    def getHTML(self):
        return self.html

    def getSkillSet(self, soft=False):
        if(soft):
            return self.softSkillSet
        return self.skillSet

    def getMatch(self,match):
        return match 

    def getSkillsNotMet(self):
        return self.skillsNotMet

    def getSkillsMet(self):
        return self.skillsMet

    def setHTML(self, html):
        self.html = html

    def setSkillSet(self, skillSet):
        self.skillSet = skillSet    

    def setSoftSkillSet(self, softSkillSet):
        self.softSkillSet = softSkillSet          

    def setMatch(self, match):
        self.match = match

    def setSkillsNotMet(self, skillsNotMet):
        self.skillsNotMet = skillsNotMet  
           
    def setSkillsMet(self, skillsMet):
        self.skillsMet = skillsMet      
