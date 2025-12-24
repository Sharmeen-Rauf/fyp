"""
CV/Resume Analyzer Service
Extracts text from CV files and analyzes them using AI
"""

from typing import Optional
import os
from openai import OpenAI
from app.core.config import settings

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False


class CVAnalyzer:
    """Service for analyzing CVs/resumes"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
    
    def extract_text(self, file_path: str, file_ext: str) -> str:
        """
        Extract text from CV file
        
        Args:
            file_path: Path to the CV file
            file_ext: File extension (.pdf, .docx, .txt)
        
        Returns:
            Extracted text
        """
        try:
            if file_ext == '.pdf':
                return self._extract_from_pdf(file_path)
            elif file_ext in ['.doc', '.docx']:
                return self._extract_from_docx(file_path)
            elif file_ext == '.txt':
                return self._extract_from_txt(file_path)
            else:
                return ""
        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF"""
        if not PDF_AVAILABLE:
            return "PDF extraction not available. Install PyPDF2: pip install PyPDF2"
        
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error reading PDF: {e}")
        return text
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX"""
        if not DOCX_AVAILABLE:
            return "DOCX extraction not available. Install python-docx: pip install python-docx"
        
        text = ""
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error reading DOCX: {e}")
        return text
    
    def _extract_from_txt(self, file_path: str) -> str:
        """Extract text from TXT"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading TXT: {e}")
            return ""
    
    def analyze_cv(self, cv_text: str, job_role: str) -> str:
        """
        Analyze CV using AI
        
        Args:
            cv_text: Extracted text from CV
            job_role: Job role applied for
        
        Returns:
            AI analysis of the CV
        """
        prompt = f"""
        Analyze this CV/resume for a {job_role} position.
        
        CV Content:
        {cv_text[:3000]}  # Limit to avoid token limits
        
        Provide analysis in the following format:
        1. Key Skills Match: List skills that match the job role
        2. Experience Relevance: Assess experience relevance
        3. Education: Review educational background
        4. Strengths: Highlight candidate strengths
        5. Recommendations: Provide hiring recommendations
        6. Overall Fit Score: Rate 1-10
        
        Be concise and objective.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert HR recruiter analyzing CVs. Be objective and thorough."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error analyzing CV: {e}")
            return "CV analysis unavailable. Please review manually."

