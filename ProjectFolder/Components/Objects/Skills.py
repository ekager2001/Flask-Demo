class Skills:
    def __init__(self, values):
        self.skills = values[0]
        self.softSkills = values[1]

    def getSkills(self):
        return self.skills

    def getSoftSkills(self):
        return self.softSkills