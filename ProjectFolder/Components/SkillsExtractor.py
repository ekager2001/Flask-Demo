#spacy
import spacy

#Visualization
from spacy import displacy
import en_core_web_sm

#nltk
import spacy

#warning
import warnings
warnings.filterwarnings('ignore')

from .Objects.Skill import Skill
#Adapted from Abid Ali Awan
#https://deepnote.com/@abid/spaCy-Resume-Analysis-81ba1e4b-7fa8-45fe-ac7a-0b7bf3da7826
class SkillsExtractor:
    def __init__(self, skill_pattern_path):
        self.skill_pattern_path = skill_pattern_path
        self.nlp = ""
        self.colors = {
        "SKILL": "linear-gradient(90deg, #9BE15D, #00E3AE)",
        "SOFT-SKILL": "linear-gradient(20deg, #FFAFBD, #FFC3A0)"  #ORIGINAL ADDITION 
        }
        self.options = {
            "ents": [
                "SKILL",
                "SOFT-SKILL"  #ORIGINAL ADDITION 
            ],
            "colors": self.colors
        }

    def setNLP(self, nlp):  #ORIGINAL ADDITION 
        self.nlp = nlp   #ORIGINAL ADDITION 

    def getNLP(self):  #ORIGINAL ADDITION 
        return self.nlp   #ORIGINAL ADDITION 
        
    def start(self, inputNLP=None):
        if inputNLP == None:  #ORIGINAL ADDITION 
            nlp = spacy.load("en_core_web_sm")
        else:  #ORIGINAL ADDITION 
            nlp = spacy.load(inputNLP)
            self.setNLP(nlp)
        ruler = nlp.add_pipe("entity_ruler") 
        ruler.from_disk(self.skill_pattern_path) 
        self.setNLP(nlp)  #ORIGINAL ADDITION 
        
    def get_skills(self, text):
        nlp = self.getNLP()  #ORIGINAL ADDITION 
        doc = nlp(text)
        myset = []
        subset = []
        for ent in doc.ents:
            if ent.label_ == "SKILL":
                subset.append( Skill((ent.text, "SKILL")) )
        myset.append(subset)
        return subset

    def get_soft_skills(self, text):
        nlp = self.getNLP()  #ORIGINAL ADDITION 
        doc = nlp(text)
        myset = []
        subset = []
        for ent in doc.ents:
            if ent.label_ == "SOFT-SKILL":  #ORIGINAL ADDITION 
                subset.append( Skill((ent.text, "SOFT-SKILL")) )  #ORIGINAL ADDITION 
        myset.append(subset)
        return subset

    def unique_skills(self, x):
        return list(set(x))

    def display(self, text): 
        nlp = self.getNLP() #ORIGINAL ADDITION 
        docx = nlp(text.lower())
        html = displacy.render(docx, style='ent', options=self.options)
        return html

    #NOT MY ORIGINAL WORK BELOW
    def skillsCheck(self, req_skills, extract=None):
        skillSet = [] #ORIGINAL ADDITION 
        extract_skills = extract  #ORIGINAL ADDITION 
        score = 0
        for x in extract_skills:
            if x in req_skills:  #ORIGINAL ADDITION 
                skillSet.append(x) #ORIGINAL ADDITION 
                score += 1
                #print("{} matches from resume to job description".format(x))
            else:
                continue
                #print("{} This skill was not shown in the resume".format(x))
        req_skills_len = len(req_skills)
        skillsNotMet = list(set(req_skills) - set(skillSet)) #ORIGINAL ADDITION 
        skillsMet = list(set(req_skills) - set(skillsNotMet)) #ORIGINAL ADDITION 
        #print(skillsMet)
        #Zero division error 
        if req_skills_len != 0:
            match = round(score / req_skills_len * 100, 1)
            print(match)  #ORIGINAL ADDITION 
            return (match, skillsNotMet, skillsMet)  #ORIGINAL ADDITION 
        return (0.0, skillsNotMet, skillsMet)  #ORIGINAL ADDITION 