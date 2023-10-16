import spacy

# from textblob import TextBlob

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
    
    # Define a function for document parsing
    # def parse_document(self, text):
    #     # Process the input text using spaCy
    #     doc = self.nlp(text)

    #     # Initialize lists to store extracted information
    #     named_entities = []
    #     verbs = []
    #     noun_phrases = []

    #     # Extract named entities (persons, organizations, locations, etc.)
    #     for entity in doc.ents:
    #         named_entities.append((entity.text, entity.label_))

    #     # Extract verbs
    #     for token in doc:
    #         if token.pos_ == "VERB":
    #             verbs.append(token.text)

    #     # Extract noun phrases
    #     for chunk in doc.noun_chunks:
    #         noun_phrases.append(chunk.text)

    #     # Return the extracted information
    #     return {
    #         "named_entities": named_entities,
    #         "verbs": verbs,
    #         "noun_phrases": noun_phrases
    #     }
    
    # # Define a function for document parsing
    # def parse_documents(self, text, topics):
    #     # Process the input text using spaCy
    #     doc = self.nlp(text)

    #     # Initialize lists to store extracted information
    #     named_entities = []
    #     verbs = []
    #     noun_phrases = []

    #     # Extract named entities (persons, organizations, locations, etc.)
    #     for entity in doc.ents:
    #         named_entities.append((entity.text, entity.label_))

    #     # Extract verbs
    #     for token in doc:
    #         if token.pos_ == "VERB":
    #             verbs.append(token.text)

    #     # Extract noun phrases
    #     for chunk in doc.noun_chunks:
    #         noun_phrases.append(chunk.text)

    #     # Perform sentiment analysis using TextBlob
    #     sentiment = TextBlob(text)
    #     sentiment_score = sentiment.sentiment.polarity

    #     # Perform topic extraction (dummy implementation)
    #     # topics = ["Technology", "Business"]  # Replace with your topic extraction logic

    #     # Summarize the document (dummy implementation)
    #     summary = "This is a dummy summary. Replace it with a proper summarization algorithm."

    #     # Return the extracted information
    #     return {
    #         "named_entities": named_entities,
    #         "verbs": verbs,
    #         "noun_phrases": noun_phrases,
    #         "sentiment_score": sentiment_score,
    #         "topics": topics,
    #         "summary": summary
    #     }