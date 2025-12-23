"""
Sentiment Analysis Service
Analyzes candidate responses for tone, confidence, and emotional cues
"""

from typing import Dict, List
import nltk
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import spacy

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')


class SentimentAnalyzer:
    """Sentiment and behavioral analysis for interview responses"""
    
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Warning: spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
    
    def analyze(self, text: str) -> Dict:
        """
        Comprehensive sentiment and behavioral analysis
        
        Args:
            text: Text to analyze
        
        Returns:
            Dictionary with sentiment scores and behavioral cues
        """
        # VADER Sentiment
        vader_scores = self.vader.polarity_scores(text)
        
        # TextBlob Sentiment
        blob = TextBlob(text)
        textblob_polarity = blob.sentiment.polarity
        textblob_subjectivity = blob.sentiment.subjectivity
        
        # Behavioral cues
        behavioral_cues = self._extract_behavioral_cues(text)
        
        # Confidence indicators
        confidence_score = self._calculate_confidence(text)
        
        # Clarity score
        clarity_score = self._calculate_clarity(text)
        
        return {
            "sentiment": {
                "compound": vader_scores["compound"],
                "positive": vader_scores["pos"],
                "neutral": vader_scores["neu"],
                "negative": vader_scores["neg"],
                "polarity": textblob_polarity,
                "subjectivity": textblob_subjectivity,
                "overall": self._get_overall_sentiment(vader_scores["compound"])
            },
            "confidence_score": confidence_score,
            "clarity_score": clarity_score,
            "behavioral_cues": behavioral_cues,
            "word_count": len(text.split()),
            "sentence_count": len(text.split('.'))
        }
    
    def _extract_behavioral_cues(self, text: str) -> Dict[str, List[str]]:
        """Extract behavioral indicators from text"""
        cues = {
            "confidence_indicators": [],
            "uncertainty_indicators": [],
            "enthusiasm_indicators": [],
            "professional_indicators": []
        }
        
        text_lower = text.lower()
        
        # Confidence indicators
        confidence_words = ["confident", "certain", "definitely", "sure", "proven", "successful"]
        cues["confidence_indicators"] = [w for w in confidence_words if w in text_lower]
        
        # Uncertainty indicators
        uncertainty_words = ["maybe", "perhaps", "might", "uncertain", "not sure", "think"]
        cues["uncertainty_indicators"] = [w for w in uncertainty_words if w in text_lower]
        
        # Enthusiasm indicators
        enthusiasm_words = ["excited", "passionate", "love", "enjoy", "enthusiastic", "eager"]
        cues["enthusiasm_indicators"] = [w for w in enthusiasm_words if w in text_lower]
        
        # Professional indicators
        professional_words = ["collaborate", "team", "professional", "experience", "skills"]
        cues["professional_indicators"] = [w for w in professional_words if w in text_lower]
        
        return cues
    
    def _calculate_confidence(self, text: str) -> float:
        """Calculate confidence score (0-1)"""
        behavioral_cues = self._extract_behavioral_cues(text)
        
        confidence_indicators = len(behavioral_cues["confidence_indicators"])
        uncertainty_indicators = len(behavioral_cues["uncertainty_indicators"])
        
        # Base score
        base_score = 0.5
        
        # Adjust based on indicators
        confidence_score = base_score + (confidence_indicators * 0.1) - (uncertainty_indicators * 0.1)
        
        # Clamp between 0 and 1
        return max(0.0, min(1.0, confidence_score))
    
    def _calculate_clarity(self, text: str) -> float:
        """Calculate clarity score based on structure and coherence"""
        if not text or len(text.strip()) == 0:
            return 0.0
        
        # Factors for clarity:
        # 1. Sentence length (optimal: 15-20 words)
        sentences = text.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        
        # 2. Word count (more words can indicate better explanation)
        word_count = len(text.split())
        
        # 3. Structure indicators
        structure_indicators = ["first", "second", "then", "finally", "because", "therefore"]
        structure_count = sum(1 for indicator in structure_indicators if indicator in text.lower())
        
        # Calculate clarity score
        length_score = 1.0 - abs(avg_sentence_length - 17.5) / 17.5  # Optimal around 17.5 words
        length_score = max(0.0, min(1.0, length_score))
        
        word_score = min(1.0, word_count / 50.0)  # More words = better (up to a point)
        structure_score = min(1.0, structure_count / 3.0)
        
        clarity = (length_score * 0.4 + word_score * 0.3 + structure_score * 0.3)
        return max(0.0, min(1.0, clarity))
    
    def _get_overall_sentiment(self, compound_score: float) -> str:
        """Get overall sentiment label"""
        if compound_score >= 0.05:
            return "positive"
        elif compound_score <= -0.05:
            return "negative"
        else:
            return "neutral"

