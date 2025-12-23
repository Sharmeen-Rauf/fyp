"""
AI Interview Agent - Agentic AI Implementation
Manages the interview flow and question generation
"""

from typing import List, Dict, Optional
from openai import OpenAI
from app.core.config import settings


class InterviewAgent:
    """AI Agent for conducting interviews"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
    
    def generate_questions(
        self,
        role: str,
        category: str = "mixed",
        num_questions: int = 5,
        difficulty: str = "medium"
    ) -> List[Dict[str, str]]:
        """
        Generate interview questions based on role and category
        
        Args:
            role: Job role (e.g., "developer", "designer")
            category: Question category (technical, behavioral, situational)
            num_questions: Number of questions to generate
            difficulty: Difficulty level (easy, medium, hard)
        
        Returns:
            List of question dictionaries
        """
        prompt = f"""
        Generate {num_questions} interview questions for a {role} position.
        Category: {category}
        Difficulty: {difficulty}
        
        For each question, provide:
        1. The question text
        2. Expected keywords or topics that should be covered in a good answer
        3. Question type (technical, behavioral, or situational)
        
        Format as JSON array with keys: question, expected_keywords, type
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert HR interviewer. Generate relevant interview questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            import json
            questions_text = response.choices[0].message.content
            # Extract JSON from response
            questions = json.loads(questions_text)
            return questions if isinstance(questions, list) else [questions]
            
        except Exception as e:
            print(f"Error generating questions: {e}")
            return self._get_fallback_questions(role, num_questions)
    
    def evaluate_response(
        self,
        question: str,
        answer: str,
        expected_keywords: Optional[List[str]] = None
    ) -> Dict:
        """
        Evaluate a candidate's response using AI
        
        Args:
            question: The interview question
            answer: Candidate's answer
            expected_keywords: Keywords that should be in the answer
        
        Returns:
            Dictionary with scores and feedback
        """
        prompt = f"""
        Evaluate this interview response:
        
        Question: {question}
        Answer: {answer}
        {"Expected keywords: " + ", ".join(expected_keywords) if expected_keywords else ""}
        
        Provide evaluation in JSON format with:
        1. relevance_score (0-1): How relevant is the answer to the question
        2. clarity_score (0-1): How clear and well-structured is the answer
        3. sentiment: Overall sentiment (positive, neutral, negative)
        4. confidence_indicators: List of confidence indicators found
        5. feedback: Constructive feedback for the candidate
        6. strengths: List of strengths in the answer
        7. improvements: List of areas for improvement
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert interviewer evaluating candidate responses. Be objective and constructive."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            import json
            evaluation_text = response.choices[0].message.content
            evaluation = json.loads(evaluation_text)
            return evaluation
            
        except Exception as e:
            print(f"Error evaluating response: {e}")
            return self._get_default_evaluation()
    
    def generate_followup_question(
        self,
        previous_question: str,
        previous_answer: str,
        context: str = ""
    ) -> str:
        """Generate a follow-up question based on previous answer"""
        prompt = f"""
        Based on this interview exchange, generate a relevant follow-up question:
        
        Previous Question: {previous_question}
        Candidate's Answer: {previous_answer}
        Context: {context}
        
        Generate one concise follow-up question that deepens understanding.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert interviewer asking insightful follow-up questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating follow-up: {e}")
            return "Can you elaborate on that?"
    
    def _get_fallback_questions(self, role: str, num: int) -> List[Dict]:
        """Fallback questions if AI generation fails"""
        fallback = {
            "developer": [
                {"question": "Tell me about your experience with version control systems.", "expected_keywords": ["git", "version control", "collaboration"], "type": "technical"},
                {"question": "How do you approach debugging a complex issue?", "expected_keywords": ["debugging", "problem-solving", "systematic"], "type": "technical"},
            ],
            "designer": [
                {"question": "Walk me through your design process.", "expected_keywords": ["research", "iteration", "user-centered"], "type": "behavioral"},
                {"question": "How do you handle feedback on your designs?", "expected_keywords": ["feedback", "iteration", "collaboration"], "type": "behavioral"},
            ]
        }
        return fallback.get(role.lower(), [])[:num]
    
    def _get_default_evaluation(self) -> Dict:
        """Default evaluation if AI evaluation fails"""
        return {
            "relevance_score": 0.5,
            "clarity_score": 0.5,
            "sentiment": "neutral",
            "confidence_indicators": [],
            "feedback": "Response received. Further evaluation needed.",
            "strengths": [],
            "improvements": []
        }

