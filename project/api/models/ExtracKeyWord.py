import spacy

class KeywordExtractor:
    def __init__(self, threshold=0.5):
        self.threshold = threshold
        self.nlp = spacy.load("en_core_web_sm")

   

    def extract_keywords(self, text):
        doc = self.nlp(text)
        keyword_scores = [(token.text, token.rank) for token in doc if token.is_alpha and not token.is_stop]
        keyword_scores.sort(key=lambda x: x[1], reverse=True)
        return [keyword for keyword, _ in keyword_scores[:5]]  # You can adjust the number of keywords to return

    def extract_keywords_withstops(self, text):
        doc = self.nlp(text)
        target_skills = ["python", "java", "javascript", "scanning", "machine learning", "PowerPoint"]
        # keyword_scores = [token.text for token in doc if not token.is_stop]
        mentioned_skills = [skill for skill in target_skills if skill.lower() in [token.text.lower() for token in doc]]
        print(mentioned_skills)
        return mentioned_skills
    
    def extract_keywords_withstops_fromlist(self, text, target_skills):
        doc = self.nlp(text)
        # target_skills = ["python", "java", "javascript", "scanning", "machine learning", "PowerPoint"]
        # keyword_scores = [token.text for token in doc if not token.is_stop]
        mentioned_skills = [skill for skill in target_skills if skill.lower() in [token.text.lower() for token in doc]]
        # print(mentioned_skills)
        return mentioned_skills