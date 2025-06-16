import asyncio
import httpx
from typing import Dict, Any, List, Optional
from app.core.config import get_settings
from app.core.logger import get_logger

class HuggingFaceService:
    """Enhanced Hugging Face service with model management."""
    
    def __init__(self):
        self.settings = get_settings()
        self.logger = get_logger(__name__)
        self.client = None
        self.model_cache = {}
        self.available_models = {
            "text_generation": [
                "gpt2",
                "microsoft/DialoGPT-medium",
                "facebook/blenderbot-400M-distill",
                "microsoft/DialoGPT-large"
            ],
            "sentiment_analysis": [
                "cardiffnlp/twitter-roberta-base-sentiment-latest",
                "nlptown/bert-base-multilingual-uncased-sentiment",
                "distilbert-base-uncased-finetuned-sst-2-english"
            ],
            "code_generation": [
                "microsoft/CodeBERT-base",
                "Salesforce/codet5-base",
                "microsoft/codebert-base-mlm"
            ],
            "question_answering": [
                "distilbert-base-cased-distilled-squad",
                "deepset/roberta-base-squad2"
            ],
            "summarization": [
                "facebook/bart-large-cnn",
                "t5-small",
                "sshleifer/distilbart-cnn-12-6"
            ]
        }
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    async def initialize(self):
        """Initialize the HTTP client."""
        if not self.client:
            timeout = httpx.Timeout(self.settings.HUGGINGFACE_TIMEOUT)
            self.client = httpx.AsyncClient(
                timeout=timeout,
                headers={
                    "Authorization": f"Bearer {self.settings.HUGGINGFACE_API_KEY}",
                    "Content-Type": "application/json"
                }
            )
            self.logger.info("Hugging Face service initialized")
    
    async def close(self):
        """Close the HTTP client."""
        if self.client:
            await self.client.aclose()
            self.client = None
            self.logger.info("Hugging Face service closed")
    
    async def get_available_models(self) -> Dict[str, List[str]]:
        """Get available models by category."""
        return self.available_models
    
    async def check_model_status(self, model_name: str) -> Dict[str, Any]:
        """Check if a model is available and loaded."""
        if not self.client:
            await self.initialize()
        
        try:
            url = f"{self.settings.HUGGINGFACE_API_URL}/{model_name}"
            response = await self.client.get(url)
            
            if response.status_code == 200:
                return {"available": True, "status": "loaded"}
            elif response.status_code == 503:
                return {"available": True, "status": "loading"}
            else:
                return {"available": False, "status": "error"}
        except Exception as e:
            self.logger.error(f"Error checking model status: {str(e)}")
            return {"available": False, "status": "error", "error": str(e)}
    
    async def generate_text(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_length: int = 150,
        temperature: float = 0.7,
        top_p: float = 0.9,
        do_sample: bool = True
    ) -> Dict[str, Any]:
        """Generate text using Hugging Face models."""
        if not self.client:
            await self.initialize()
        
        model = model or self.settings.DEFAULT_TEXT_MODEL
        
        try:
            url = f"{self.settings.HUGGINGFACE_API_URL}/{model}"
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": max_length,
                    "temperature": temperature,
                    "top_p": top_p,
                    "do_sample": do_sample,
                    "return_full_text": False
                }
            }
            
            response = await self.client.post(url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get("generated_text", "")
                    return {
                        "success": True,
                        "text": generated_text,
                        "model": model,
                        "prompt": prompt
                    }
                else:
                    return {"success": False, "error": "No text generated"}
            else:
                error_msg = f"API error: {response.status_code}"
                self.logger.error(error_msg)
                return {"success": False, "error": error_msg}
                
        except Exception as e:
            error_msg = f"Text generation error: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    async def analyze_customer_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of customer text."""
        if not self.client:
            await self.initialize()
        
        try:
            url = f"{self.settings.HUGGINGFACE_API_URL}/{self.settings.DEFAULT_SENTIMENT_MODEL}"
            
            payload = {"inputs": text}
            
            response = await self.client.post(url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "sentiment": result,
                    "model": self.settings.DEFAULT_SENTIMENT_MODEL,
                    "text": text
                }
            else:
                error_msg = f"Sentiment analysis error: {response.status_code}"
                self.logger.error(error_msg)
                return {"success": False, "error": error_msg}
                
        except Exception as e:
            error_msg = f"Sentiment analysis error: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    async def generate_marketing_copy(
        self,
        business_type: str,
        target_audience: str,
        tone: str,
        key_features: List[str]
    ) -> Dict[str, Any]:
        """Generate marketing copy using specialized prompts."""
        features_text = ", ".join(key_features) if key_features else "innovative solutions"
        
        prompt = f"""
        Create compelling marketing copy for a {business_type} targeting {target_audience}.
        
        Tone: {tone}
        Key features: {features_text}
        
        Generate:
        1. Headline:
        2. Subheadline:
        3. Call-to-action:
        4. Value proposition:
        """
        
        result = await self.generate_text(
            prompt=prompt,
            model=self.settings.DEFAULT_MARKETING_MODEL,
            max_length=200,
            temperature=0.8
        )
        
        if result["success"]:
            # Parse the generated text into components
            components = self._parse_marketing_copy(result["text"])
            return {
                "success": True,
                "components": components,
                "model": result["model"]
            }
        else:
            return result
    
    async def generate_social_content(
        self,
        platform: str,
        message: str,
        tone: str
    ) -> Dict[str, Any]:
        """Generate social media content."""
        char_limits = {
            "twitter": 280,
            "facebook": 500,
            "linkedin": 700,
            "instagram": 300
        }
        
        char_limit = char_limits.get(platform.lower(), 280)
        
        prompt = f"""
        Create a {tone} {platform} post about: {message}
        
        Requirements:
        - Keep under {char_limit} characters
        - Include relevant hashtags
        - Engaging and {tone} tone
        
        Post:
        """
        
        result = await self.generate_text(
            prompt=prompt,
            max_length=100,
            temperature=0.8
        )
        
        if result["success"]:
            return {
                "success": True,
                "content": result["text"],
                "platform": platform,
                "character_count": len(result["text"]),
                "character_limit": char_limit,
                "within_limit": len(result["text"]) <= char_limit
            }
        else:
            return result
    
    async def generate_code_documentation(
        self,
        code: str,
        language: str
    ) -> Dict[str, Any]:
        """Generate documentation for code."""
        prompt = f"""
        Generate comprehensive documentation for this {language} code:
        
        {language}
        {code}
        
        
        Documentation should include:
        - Purpose and functionality
        - Parameters and return values
        - Usage examples
        - Notes and considerations
        
        Documentation:
        """
        
        return await self.generate_text(
            prompt=prompt,
            model=self.settings.DEFAULT_CODE_MODEL,
            max_length=250,
            temperature=0.3
        )
    
    async def summarize_text(
        self,
        text: str,
        max_length: int = 100
    ) -> Dict[str, Any]:
        """Summarize long text."""
        if not self.client:
            await self.initialize()
        
        try:
            # Use a summarization model
            url = f"{self.settings.HUGGINGFACE_API_URL}/facebook/bart-large-cnn"
            
            payload = {
                "inputs": text,
                "parameters": {
                    "max_length": max_length,
                    "min_length": 30,
                    "do_sample": False
                }
            }
            
            response = await self.client.post(url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    summary = result[0].get("summary_text", "")
                    return {
                        "success": True,
                        "summary": summary,
                        "original_length": len(text),
                        "summary_length": len(summary),
                        "compression_ratio": len(summary) / len(text) if text else 0
                    }
            
            return {"success": False, "error": "Failed to generate summary"}
            
        except Exception as e:
            error_msg = f"Summarization error: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    async def answer_question(
        self,
        question: str,
        context: str
    ) -> Dict[str, Any]:
        """Answer questions based on context."""
        if not self.client:
            await self.initialize()
        
        try:
            url = f"{self.settings.HUGGINGFACE_API_URL}/distilbert-base-cased-distilled-squad"
            
            payload = {
                "inputs": {
                    "question": question,
                    "context": context
                }
            }
            
            response = await self.client.post(url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "answer": result.get("answer", ""),
                    "confidence": result.get("score", 0),
                    "question": question,
                    "context_length": len(context)
                }
            
            return {"success": False, "error": "Failed to answer question"}
            
        except Exception as e:
            error_msg = f"Question answering error: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def _parse_marketing_copy(self, text: str) -> Dict[str, str]:
        """Parse generated marketing copy into components."""
        components = {
            "headline": "",
            "subheadline": "",
            "call_to_action": "",
            "value_proposition": ""
        }
        
        lines = text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Identify sections
            if "headline:" in line.lower():
                current_section = "headline"
                components["headline"] = line.split(":", 1)[1].strip()
            elif "subheadline:" in line.lower():
                current_section = "subheadline"
                components["subheadline"] = line.split(":", 1)[1].strip()
            elif "call-to-action:" in line.lower() or "cta:" in line.lower():
                current_section = "call_to_action"
                components["call_to_action"] = line.split(":", 1)[1].strip()
            elif "value proposition:" in line.lower():
                current_section = "value_proposition"
                components["value_proposition"] = line.split(":", 1)[1].strip()
            elif current_section and line:
                # Continue previous section
                if components[current_section]:
                    components[current_section] += " " + line
                else:
                    components[current_section] = line
        
        return components
    
    def _extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from text."""
        import re
        hashtags = re.findall(r'#\w+', text)
        return hashtags
    
    async def get_available_models(self) -> List[str]:
        """Get list of available models."""
        # Common Hugging Face models for different tasks
        return [
            "gpt2",
            "gpt2-medium",
            "gpt2-large",
            "microsoft/DialoGPT-medium",
            "microsoft/CodeBERT-base",
            "cardiffnlp/twitter-roberta-base-sentiment-latest",
            "facebook/bart-large-cnn",
            "t5-base",
            "distilbert-base-uncased"
        ]

# Global service instance
_huggingface_service = None

def get_huggingface_service() -> HuggingFaceService:
    """Get Hugging Face service singleton."""
    global _huggingface_service
    if _huggingface_service is None:
        _huggingface_service = HuggingFaceService()
    return _huggingface_service