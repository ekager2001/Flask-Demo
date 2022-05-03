class Skill:
    def __init__(self, values): #"skills, type "softSkill, Skill"
        self.skill = values[0]
        self.type = values[1]

    def getSkill(self):
        return self.skill

    def getType(self):
        return self.type

    def __hash__(self):
        return hash((self.skill))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.skill == other.skill 