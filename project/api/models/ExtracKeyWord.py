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
