#!/usr/bin/env python3
"""
CV Personal Data Extraction System
Extracts personal information from CVs using DeepSeek API
"""

import os
import sys
import csv
import json
import logging
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime

from openai import OpenAI
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cv_extraction.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class CVExtractor:
    """Extract personal data from CV files using DeepSeek API"""
    
    SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.txt', '.doc'}
    
    EXTRACTION_PROMPT = """You are an expert CV/Resume parser. Analyze the provided CV content and extract the following personal information:

Name
Email
Phone/Mobile Number
Location/Address (City, Country)
LinkedIn Profile URL
GitHub Profile URL (if available)
Professional Summary/Objective (first line or brief summary)
Current/Most Recent Job Title
Current/Most Recent Company
Years of Experience (total)
Education (Highest Degree)
University/Institution Name

Return the information as a JSON object with these exact keys:
{
    "name": "",
    "email": "",
    "phone": "",
    "location": "",
    "linkedin": "",
    "github": "",
    "professional_summary": "",
    "current_job_title": "",
    "current_company": "",
    "years_experience": "",
    "education": "",
    "institution": ""
}

If any field is not found or not clearly mentioned, use null for that field.
Return ONLY the JSON object, no other text."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the CV Extractor with DeepSeek API client"""
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable not set")
        
        # DeepSeek uses OpenAI-compatible API
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )
        self.extraction_results = []
        
    def extract_text_from_file(self, file_path: Path) -> Optional[str]:
        """Extract text from various file formats"""
        try:
            if file_path.suffix.lower() == '.pdf':
                return self._extract_from_pdf(file_path)
            elif file_path.suffix.lower() in {'.docx', '.doc'}:
                return self._extract_from_docx(file_path)
            elif file_path.suffix.lower() == '.txt':
                return self._extract_from_txt(file_path)
            else:
                logger.warning(f"Unsupported file format: {file_path.suffix}")
                return None
        except Exception as e:
            logger.error(f"Error extracting text from {file_path.name}: {str(e)}")
            return None
    
    def _extract_from_pdf(self, file_path: Path) -> Optional[str]:
        """Extract text from PDF"""
        try:
            import PyPDF2
            text = ""
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()
            return text if text.strip() else None
        except Exception as e:
            logger.error(f"PDF extraction error: {str(e)}")
            return None
    
    def _extract_from_docx(self, file_path: Path) -> Optional[str]:
        """Extract text from DOCX"""
        try:
            from docx import Document
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text if text.strip() else None
        except Exception as e:
            logger.error(f"DOCX extraction error: {str(e)}")
            return None
    
    def _extract_from_txt(self, file_path: Path) -> Optional[str]:
        """Extract text from TXT"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                text = file.read()
            return text if text.strip() else None
        except Exception as e:
            logger.error(f"TXT extraction error: {str(e)}")
            return None
    
    def extract_personal_data(self, cv_text: str, filename: str) -> Optional[Dict]:
        """Use DeepSeek API to extract personal data from CV text"""
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                max_tokens=1024,
                temperature=0.3,
                messages=[
                    {
                        "role": "system",
                        "content": self.EXTRACTION_PROMPT
                    },
                    {
                        "role": "user",
                        "content": f"CV Filename: {filename}\n\nCV Content:\n{cv_text[:4000]}"
                    }
                ]
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                # Remove ```json or ``` from start
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            if not response_text:
                logger.error(f"Empty response from API for {filename}")
                return None
            
            # Extract JSON from response (sometimes LLM adds extra text)
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                logger.error(f"No JSON found in response for {filename}")
                return None
            
            json_str = response_text[json_start:json_end]
            extracted_data = json.loads(json_str)
            extracted_data['filename'] = filename
            
            return extracted_data
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error for {filename}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Extraction error for {filename}: {str(e)}")
            return Noner(f"JSON parsing error for {filename}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Extraction error for {filename}: {str(e)}")
            return None
    
    def process_cv_folder(self, folder_path: str) -> List[Dict]:
        """Process all CVs in a folder"""
        folder = Path(folder_path)
        
        if not folder.exists():
            logger.error(f"Folder not found: {folder_path}")
            return []
        
        cv_files = []
        for ext in self.SUPPORTED_EXTENSIONS:
            cv_files.extend(folder.glob(f"*{ext}"))
            cv_files.extend(folder.glob(f"*{ext.upper()}"))
        
        if not cv_files:
            logger.warning(f"No CV files found in {folder_path}")
            return []
        
        logger.info(f"Found {len(cv_files)} CV files to process")
        
        for idx, cv_file in enumerate(cv_files, 1):
            logger.info(f"Processing [{idx}/{len(cv_files)}] {cv_file.name}")
            
            # Extract text from file
            cv_text = self.extract_text_from_file(cv_file)
            if not cv_text:
                logger.warning(f"Could not extract text from {cv_file.name}")
                continue
            
            # Extract personal data using Claude
            personal_data = self.extract_personal_data(cv_text, cv_file.name)
            if personal_data:
                self.extraction_results.append(personal_data)
                logger.info(f"✓ Extracted data from {cv_file.name}")
            else:
                logger.warning(f"✗ Failed to extract data from {cv_file.name}")
        
        return self.extraction_results
    
    def save_to_csv(self, output_path: str) -> bool:
        """Save extracted data to CSV file"""
        try:
            if not self.extraction_results:
                logger.warning("No data to save")
                return False
            
            # Define CSV columns
            fieldnames = [
                'filename',
                'name',
                'email',
                'phone',
                'location',
                'linkedin',
                'github',
                'professional_summary',
                'current_job_title',
                'current_company',
                'years_experience',
                'education',
                'institution'
            ]
            
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for result in self.extraction_results:
                    # Ensure all fields are present
                    row = {field: result.get(field, '') for field in fieldnames}
                    writer.writerow(row)
            
            logger.info(f"Data saved to {output_path}")
            logger.info(f"Total records: {len(self.extraction_results)}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving to CSV: {str(e)}")
            return False


def main():
    """Main entry point"""
    # Get configuration from environment or user input
    cv_folder = os.getenv('CV_FOLDER_PATH')
    output_csv = os.getenv('OUTPUT_CSV_PATH', './extracted_data.csv')
    
    if not cv_folder:
        print("\n" + "="*60)
        print("CV Personal Data Extraction System")
        print("="*60)
        cv_folder = input("\nEnter the path to the CV folder: ").strip()
    
    if not cv_folder:
        logger.error("CV folder path is required")
        sys.exit(1)
    
    try:
        # Initialize extractor
        logger.info("Initializing CV Extractor...")
        extractor = CVExtractor()
        
        # Process CVs
        logger.info(f"Starting to process CVs from: {cv_folder}")
        results = extractor.process_cv_folder(cv_folder)
        
        if results:
            # Save to CSV
            extractor.save_to_csv(output_csv)
            print(f"\n✓ Successfully extracted data from {len(results)} CVs")
            print(f"✓ Results saved to: {output_csv}")
        else:
            print("\n✗ No data was extracted")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
