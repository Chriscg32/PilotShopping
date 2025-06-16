from typing import Dict, Any, List
from app.agents.base import BaseAgent
from app.services.huggingface_service import get_huggingface_service

class CustomerServiceAgent(BaseAgent):
    """Customer service agent with Hugging Face integration."""
    
    def __init__(self):
        super().__init__(
            name="customer_service",
            capabilities=[
                "ticket_management",
                "customer_support",
                "sentiment_analysis",
                "response_generation",
                "escalation_management",
                "knowledge_base_search",
                "chat_support",
                "feedback_analysis"
            ]
        )
        self.hf_service = get_huggingface_service()
        self.knowledge_base = self._initialize_knowledge_base()
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process customer service tasks."""
        task_type = task.get("type")
        
        if task_type == "handle_ticket":
            return await self._handle_ticket(task)
        elif task_type == "analyze_sentiment":
            return await self._analyze_sentiment(task)
        elif task_type == "generate_response":
            return await self._generate_response(task)
        elif task_type == "search_knowledge_base":
            return await self._search_knowledge_base(task)
        else:
            return {"error": f"Unknown customer service task: {task_type}"}
    
    async def _handle_ticket(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle customer support ticket."""
        ticket = task.get("ticket", {})
        message = ticket.get("message", "")
        priority = ticket.get("priority", "normal")
        category = ticket.get("category", "general")
        
        if not message:
            return {"error": "Ticket message is required"}
        
        # Analyze sentiment
        sentiment_result = await self.hf_service.analyze_customer_sentiment(message)
        
        # Generate response
        response_prompt = f"""
        Customer inquiry: {message}
        Category: {category}
        Priority: {priority}
        
        Generate a helpful, professional customer service response:
        """
        
        response_result = await self.hf_service.generate_text(
            prompt=response_prompt,
            model="microsoft/DialoGPT-medium",
            max_length=150,
            temperature=0.6
        )
        
        # Determine if escalation is needed
        needs_escalation = self._check_escalation_needed(message, sentiment_result)
        
        return {
            "result": {
                "ticket_id": self._generate_ticket_id(),
                "category": category,
                "priority": priority,
                "sentiment_analysis": sentiment_result.get("sentiment", {}),
                "suggested_response": response_result.get("text", ""),
                "needs_escalation": needs_escalation,
                "estimated_resolution_time": self._estimate_resolution_time(category, priority),
                "knowledge_base_articles": self._find_relevant_articles(message)
            }
        }
    
    async def _analyze_sentiment(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze customer sentiment."""
        text = task.get("text", "")
        
        if not text:
            return {"error": "Text is required for sentiment analysis"}
        
        result = await self.hf_service.analyze_customer_sentiment(text)
        
        if result["success"]:
            sentiment_data = result["sentiment"]
            
            # Extract sentiment information
            if isinstance(sentiment_data, list) and len(sentiment_data) > 0:
                top_sentiment = max(sentiment_data, key=lambda x: x.get("score", 0))
                
                return {
                    "result": {
                        "text": text,
                        "sentiment": top_sentiment.get("label", "NEUTRAL"),
                        "confidence": top_sentiment.get("score", 0.0),
                        "all_sentiments": sentiment_data,
                        "recommendation": self._get_sentiment_recommendation(top_sentiment)
                    }
                }
        
        return {"error": "Failed to analyze sentiment"}
    
    async def _generate_response(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate customer service response."""
        customer_message = task.get("customer_message", "")
        context = task.get("context", "")
        tone = task.get("tone", "professional")
        
        if not customer_message:
            return {"error": "Customer message is required"}
        
        prompt = f"""
        Customer message: {customer_message}
        Context: {context}
        Tone: {tone}
        
        Generate a helpful customer service response:
        """
        
        result = await self.hf_service.generate_text(
            prompt=prompt,
            model="microsoft/DialoGPT-medium",
            max_length=120,
            temperature=0.7
        )
        
        if result["success"]:
            return {
                "result": {
                    "customer_message": customer_message,
                    "generated_response": result["text"],
                    "tone": tone,
                    "response_length": len(result["text"]),
                    "generated_with": result["model"]
                }
            }
        else:
            return {"error": f"Failed to generate response: {result.get('error', 'Unknown error')}"}
    
    async def _search_knowledge_base(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Search knowledge base for relevant articles."""
        query = task.get("query", "")
        
        if not query:
            return {"error": "Search query is required"}
        
        # Simple keyword matching (in production, use vector search)
        relevant_articles = self._find_relevant_articles(query)
        
        return {
            "result": {
                "query": query,
                "articles_found": len(relevant_articles),
                "articles": relevant_articles,
                "search_suggestions": self._get_search_suggestions(query)
            }
        }
    
    def _initialize_knowledge_base(self) -> List[Dict[str, Any]]:
        """Initialize knowledge base with common articles."""
        return [
            {
                "id": "kb001",
                "title": "How to reset your password",
                "category": "account",
                "keywords": ["password", "reset", "login", "account"],
                "content": "To reset your password, click on 'Forgot Password' on the login page..."
            },
            {
                "id": "kb002",
                "title": "Billing and payment issues",
                "category": "billing",
                "keywords": ["billing", "payment", "charge", "invoice", "refund"],
                "content": "For billing inquiries, please check your account dashboard..."
            },
            {
                "id": "kb003",
                "title": "Technical support",
                "category": "technical",
                "keywords": ["bug", "error", "technical", "not working", "broken"],
                "content": "If you're experiencing technical issues, please try these steps..."
            },
            {
                "id": "kb004",
                "title": "Account cancellation",
                "category": "account",
                "keywords": ["cancel", "close", "delete", "account", "subscription"],
                "content": "To cancel your account, please contact our support team..."
            }
        ]
    
    def _find_relevant_articles(self, query: str) -> List[Dict[str, Any]]:
        """Find relevant knowledge base articles."""
        query_lower = query.lower()
        relevant_articles = []
        
        for article in self.knowledge_base:
            # Check if any keywords match the query
            for keyword in article["keywords"]:
                if keyword in query_lower:
                    relevant_articles.append({
                        "id": article["id"],
                        "title": article["title"],
                        "category": article["category"],
                        "relevance_score": self._calculate_relevance(query_lower, article["keywords"])
                    })
                    break
        
        # Sort by relevance score
        relevant_articles.sort(key=lambda x: x["relevance_score"], reverse=True)
        return relevant_articles[:5]  # Return top 5 articles
    
    def _calculate_relevance(self, query: str, keywords: List[str]) -> float:
        """Calculate relevance score between query and keywords."""
        matches = sum(1 for keyword in keywords if keyword in query)
        return matches / len(keywords) if keywords else 0
    
    def _check_escalation_needed(self, message: str, sentiment_result: Dict[str, Any]) -> bool:
        """Check if ticket needs escalation."""
        escalation_keywords = ["urgent", "emergency", "complaint", "angry", "frustrated", "legal"]
        message_lower = message.lower()
        
        # Check for escalation keywords
        has_escalation_keywords = any(keyword in message_lower for keyword in escalation_keywords)
        
        # Check sentiment
        negative_sentiment = False
        if sentiment_result.get("success") and sentiment_result.get("sentiment"):
            sentiment_data = sentiment_result["sentiment"]
            if isinstance(sentiment_data, list):
                for sentiment in sentiment_data:
                    if sentiment.get("label") == "NEGATIVE" and sentiment.get("score", 0) > 0.7:
                        negative_sentiment = True
                        break
        
        return has_escalation_keywords or negative_sentiment
    
    def _estimate_resolution_time(self, category: str, priority: str) -> str:
        """Estimate resolution time based on category and priority."""
        time_matrix = {
            ("account", "high"): "2-4 hours",
            ("account", "normal"): "24 hours",
            ("account", "low"): "2-3 days",
            ("billing", "high"): "1-2 hours",
            ("billing", "normal"): "4-8 hours",
            ("billing", "low"): "1-2 days",
            ("technical", "high"): "4-8 hours",
            ("technical", "normal"): "1-2 days",
            ("technical", "low"): "3-5 days",
            ("general", "high"): "4-6 hours",
            ("general", "normal"): "1-2 days",
            ("general", "low"): "2-4 days"
        }
        
        return time_matrix.get((category, priority), "1-2 days")
    
    def _get_sentiment_recommendation(self, sentiment: Dict[str, Any]) -> str:
        """Get recommendation based on sentiment."""
        label = sentiment.get("label", "NEUTRAL")
        score = sentiment.get("score", 0)
        
        if label == "NEGATIVE" and score > 0.8:
            return "High priority - customer is very upset. Consider immediate escalation."
        elif label == "NEGATIVE" and score > 0.6:
            return "Medium priority - customer is dissatisfied. Respond with empathy."
        elif label == "POSITIVE":
            return "Customer seems satisfied. Maintain positive tone."
        else:
            return "Neutral sentiment. Provide helpful, professional response."
    
    def _get_search_suggestions(self, query: str) -> List[str]:
        """Get search suggestions based on query."""
        suggestions = []
        query_lower = query.lower()
        
        if "password" in query_lower or "login" in query_lower:
            suggestions.extend(["password reset", "account access", "login issues"])
        if "billing" in query_lower or "payment" in query_lower:
            suggestions.extend(["billing support", "payment methods", "refund policy"])
        if "technical" in query_lower or "bug" in query_lower:
            suggestions.extend(["technical support", "troubleshooting", "system status"])
        
        return suggestions[:3]
    
    def _generate_ticket_id(self) -> str:
        """Generate unique ticket ID."""
        import uuid
        return f"TKT-{str(uuid.uuid4())[:8].upper()}"