"""
Scoring Engine
Calculates overall scores for interview responses
"""

from typing import Dict, Optional
from app.services.ai.sentiment_analyzer import SentimentAnalyzer
from app.services.ai.interview_agent import InterviewAgent


class ScoringEngine:
    """Engine for scoring interview responses"""
    
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        self.interview_agent = InterviewAgent()
    
    def score_response(
        self,
        question: str,
        answer: str,
        expected_keywords: Optional[list] = None
    ) -> Dict:
        """
        Score a candidate's response
        
        Args:
            question: Interview question
            answer: Candidate's answer
            expected_keywords: Keywords that should be in the answer
        
        Returns:
            Dictionary with all scores and analysis
        """
        # Sentiment and behavioral analysis
        sentiment_analysis = self.sentiment_analyzer.analyze(answer)
        
        # AI evaluation
        ai_evaluation = self.interview_agent.evaluate_response(
            question=question,
            answer=answer,
            expected_keywords=expected_keywords
        )
        
        # Extract scores
        sentiment_score = (sentiment_analysis["sentiment"]["compound"] + 1) / 2  # Normalize to 0-1
        confidence_score = sentiment_analysis["confidence_score"]
        clarity_score = sentiment_analysis["clarity_score"]
        relevance_score = ai_evaluation.get("relevance_score", 0.5)
        
        # Calculate overall score (weighted average)
        overall_score = (
            sentiment_score * 0.2 +
            confidence_score * 0.25 +
            clarity_score * 0.25 +
            relevance_score * 0.3
        )
        
        return {
            "sentiment_score": round(sentiment_score, 3),
            "confidence_score": round(confidence_score, 3),
            "clarity_score": round(clarity_score, 3),
            "relevance_score": round(relevance_score, 3),
            "overall_score": round(overall_score, 3),
            "sentiment_analysis": sentiment_analysis,
            "behavioral_cues": sentiment_analysis["behavioral_cues"],
            "ai_feedback": ai_evaluation.get("feedback", ""),
            "ai_evaluation": ai_evaluation
        }
    
    def calculate_interview_score(self, response_scores: list) -> float:
        """
        Calculate overall interview score from all responses
        
        Args:
            response_scores: List of overall scores from each response
        
        Returns:
            Average score
        """
        if not response_scores:
            return 0.0
        
        return sum(response_scores) / len(response_scores)

