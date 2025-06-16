from typing import Dict, Any, List
from app.agents.base import BaseAgent
from app.services.huggingface_service import get_huggingface_service

class MarketingAgent(BaseAgent):
    """Enhanced marketing agent with comprehensive campaign management."""
    
    def __init__(self):
        super().__init__(
            name="marketing",
            capabilities=[
                "campaign_creation",
                "content_generation",
                "social_media_management",
                "email_marketing",
                "seo_optimization",
                "analytics_reporting",
                "ab_testing",
                "audience_analysis",
                "competitor_analysis",
                "brand_development"
            ]
        )
        self.hf_service = get_huggingface_service()
        self.campaign_templates = self._initialize_campaign_templates()
        self.social_platforms = ["twitter", "facebook", "instagram", "linkedin", "tiktok"]
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process marketing tasks."""
        task_type = task.get("type")
        
        if task_type == "create_campaign":
            return await self._create_campaign(task)
        elif task_type == "generate_content":
            return await self._generate_content(task)
        elif task_type == "social_media_post":
            return await self._create_social_media_post(task)
        elif task_type == "email_campaign":
            return await self._create_email_campaign(task)
        elif task_type == "seo_content":
            return await self._create_seo_content(task)
        elif task_type == "analyze_audience":
            return await self._analyze_audience(task)
        elif task_type == "competitor_analysis":
            return await self._analyze_competitors(task)
        elif task_type == "brand_strategy":
            return await self._develop_brand_strategy(task)
        else:
            return {"error": f"Unknown marketing task: {task_type}"}
    
    async def _create_campaign(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive marketing campaign."""
        campaign_data = task.get("campaign", {})
        business_type = campaign_data.get("business_type", "")
        target_audience = campaign_data.get("target_audience", "")
        budget = campaign_data.get("budget", 0)
        duration = campaign_data.get("duration", "30 days")
        objectives = campaign_data.get("objectives", [])
        
        if not business_type or not target_audience:
            return {"error": "Business type and target audience are required"}
        
        # Generate campaign strategy
        strategy_result = await self._generate_campaign_strategy(
            business_type, target_audience, objectives, budget, duration
        )
        
        # Generate content for different channels
        content_calendar = await self._generate_content_calendar(
            business_type, target_audience, duration
        )
        
        # Generate ad copy variations
        ad_variations = await self._generate_ad_variations(
            business_type, target_audience
        )
        
        campaign_id = self._generate_campaign_id()
        
        return {
            "result": {
                "campaign_id": campaign_id,
                "business_type": business_type,
                "target_audience": target_audience,
                "budget": budget,
                "duration": duration,
                "objectives": objectives,
                "strategy": strategy_result,
                "content_calendar": content_calendar,
                "ad_variations": ad_variations,
                "recommended_channels": self._recommend_channels(target_audience),
                "kpi_metrics": self._define_kpi_metrics(objectives),
                "timeline": self._create_campaign_timeline(duration)
            }
        }
    
    async def _generate_campaign_strategy(
        self,
        business_type: str,
        target_audience: str,
        objectives: List[str],
        budget: float,
        duration: str
    ) -> Dict[str, Any]:
        """Generate comprehensive campaign strategy."""
        objectives_text = ", ".join(objectives) if objectives else "increase brand awareness"
        
        prompt = f"""
        Create a comprehensive marketing strategy for:
        Business: {business_type}
        Target Audience: {target_audience}
        Objectives: {objectives_text}
        Budget: ${budget}
        Duration: {duration}
        
        Strategy should include:
        1. Key messaging
        2. Channel recommendations
        3. Budget allocation
        4. Success metrics
        5. Risk mitigation
        
        Marketing Strategy:
        """
        
        result = await self.hf_service.generate_text(
            prompt=prompt,
            max_length=300,
            temperature=0.7
        )
        
        if result["success"]:
            return {
                "strategy_text": result["text"],
                "key_channels": self._extract_channels(result["text"]),
                "budget_breakdown": self._suggest_budget_allocation(budget),
                "timeline_phases": self._create_strategy_phases(duration)
            }
        else:
            return {"error": "Failed to generate strategy"}
    
    async def _generate_content_calendar(
        self,
        business_type: str,
        target_audience: str,
        duration: str
    ) -> Dict[str, Any]:
        """Generate content calendar for the campaign."""
        content_types = [
            "educational", "promotional", "entertaining", 
            "behind-the-scenes", "user-generated", "testimonial"
        ]
        
        calendar = {}
        
        for week in range(1, 5):  # 4 weeks
            week_content = []
            
            for content_type in content_types[:3]:  # 3 content types per week
                prompt = f"""
                Create a {content_type} content idea for {business_type} targeting {target_audience}.
                
                Content idea:
                Title:
                Description:
                Platform:
                Best posting time:
                """
                
                result = await self.hf_service.generate_text(
                    prompt=prompt,
                    max_length=100,
                    temperature=0.8
                )
                
                if result["success"]:
                    week_content.append({
                        "type": content_type,
                        "content": result["text"],
                        "suggested_platforms": self._suggest_platforms_for_content(content_type)
                    })
            
            calendar[f"week_{week}"] = week_content
        
        return {
            "calendar": calendar,
            "total_content_pieces": sum(len(week) for week in calendar.values()),
            "content_mix": self._analyze_content_mix(calendar)
        }
    
    async def _generate_ad_variations(
        self,
        business_type: str,
        target_audience: str
    ) -> List[Dict[str, Any]]:
        """Generate multiple ad copy variations for A/B testing."""
        variations = []
        tones = ["professional", "casual", "urgent", "friendly"]
        
        for i, tone in enumerate(tones):
            result = await self.hf_service.generate_marketing_copy(
                business_type=business_type,
                target_audience=target_audience,
                tone=tone,
                key_features=["quality", "reliability", "innovation"]
            )
            
            if result["success"]:
                variations.append({
                    "variation_id": f"var_{i+1}",
                    "tone": tone,
                    "components": result["components"],
                    "recommended_for": self._recommend_variation_usage(tone)
                })
        
        return variations
    
    async def _create_social_media_post(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create social media post for specific platform."""
        platform = task.get("platform", "twitter")
        message = task.get("message", "")
        tone = task.get("tone", "professional")
        include_hashtags = task.get("include_hashtags", True)
        include_cta = task.get("include_cta", True)
        
        if not message:
            return {"error": "Message content is required"}
        
        # Generate platform-specific content
        result = await self.hf_service.generate_social_content(
            platform=platform,
            message=message,
            tone=tone
        )
        
        if result["success"]:
            # Enhance with hashtags and CTA if requested
            enhanced_content = result["content"]
            
            if include_hashtags:
                hashtags = self._generate_hashtags(message, platform)
                enhanced_content += f"\n\n{' '.join(hashtags)}"
            
            if include_cta:
                cta = self._generate_cta(platform, tone)
                enhanced_content += f"\n\n{cta}"
            
            return {
                "result": {
                    "platform": platform,
                    "original_content": result["content"],
                    "enhanced_content": enhanced_content,
                    "character_count": len(enhanced_content),
                    "within_limit": result["within_limit"],
                    "optimal_posting_time": self._get_optimal_posting_time(platform),
                    "engagement_predictions": self._predict_engagement(enhanced_content, platform),
                    "suggested_improvements": self._suggest_content_improvements(enhanced_content, platform)
                }
            }
        else:
            return result
    
    async def _create_email_campaign(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create email marketing campaign."""
        campaign_type = task.get("campaign_type", "newsletter")
        subject_line = task.get("subject_line", "")
        target_audience = task.get("target_audience", "")
        business_type = task.get("business_type", "")
        call_to_action = task.get("call_to_action", "")
        
        if not target_audience or not business_type:
            return {"error": "Target audience and business type are required"}
        
        # Generate subject line if not provided
        if not subject_line:
            subject_result = await self._generate_email_subject(campaign_type, business_type)
            subject_line = subject_result.get("subject", "Important Update")
        
        # Generate email content
        prompt = f"""
        Create an email {campaign_type} for {business_type} targeting {target_audience}.
        
        Subject: {subject_line}
        
        Email should include:
        - Engaging opening
        - Main content relevant to {campaign_type}
        - Clear call-to-action: {call_to_action}
        - Professional closing
        
        Email content:
        """
        
        result = await self.hf_service.generate_text(
            prompt=prompt,
            max_length=400,
            temperature=0.7
        )
        
        if result["success"]:
            # Generate multiple subject line variations
            subject_variations = await self._generate_subject_variations(subject_line, campaign_type)
            
            return {
                "result": {
                    "campaign_type": campaign_type,
                    "subject_line": subject_line,
                    "subject_variations": subject_variations,
                    "email_content": result["text"],
                    "target_audience": target_audience,
                    "estimated_open_rate": self._estimate_open_rate(subject_line),
                    "personalization_suggestions": self._get_personalization_suggestions(),
                    "a_b_test_recommendations": self._get_ab_test_recommendations(),
                    "send_time_optimization": self._optimize_send_time(target_audience)
                }
            }
        else:
            return result
    
    async def _create_seo_content(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create SEO-optimized content."""
        topic = task.get("topic", "")
        keywords = task.get("keywords", [])
        content_type = task.get("content_type", "blog_post")
        target_length = task.get("target_length", 800)
        
        if not topic:
            return {"error": "Topic is required for SEO content"}
        
        keywords_text = ", ".join(keywords) if keywords else "relevant keywords"
        
        prompt = f"""
        Create SEO-optimized {content_type} about: {topic}
        
        Target keywords: {keywords_text}
        Target length: {target_length} words
        
        Content should include:
        - Compelling title with primary keyword
        - Meta description
        - Headers (H1, H2, H3)
        - Keyword-rich content
        - Internal linking opportunities
        
        SEO Content:
        """
        
        result = await self.hf_service.generate_text(
            prompt=prompt,
            max_length=min(target_length // 2, 500),
            temperature=0.6
        )
        
        if result["success"]:
            content = result["text"]
            
            return {
                "result": {
                    "topic": topic,
                    "content_type": content_type,
                    "content": content,
                    "target_keywords": keywords,
                    "seo_analysis": self._analyze_seo_content(content, keywords),
                    "readability_score": self._calculate_readability(content),
                    "optimization_suggestions": self._get_seo_suggestions(content, keywords),
                    "meta_description": self._generate_meta_description(topic, keywords),
                    "suggested_internal_links": self._suggest_internal_links(topic),
                    "content_structure": self._analyze_content_structure(content)
                }
            }
        else:
            return result
    
    async def _analyze_audience(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze target audience characteristics."""
        audience_data = task.get("audience_data", {})
        demographics = audience_data.get("demographics", {})
        interests = audience_data.get("interests", [])
        behaviors = audience_data.get("behaviors", [])
        
        # Generate audience insights
        prompt = f"""
        Analyze this target audience:
        Demographics: {demographics}
        Interests: {', '.join(interests)}
        Behaviors: {', '.join(behaviors)}
        
        Provide insights on:
        1. Marketing preferences
        2. Content consumption habits
        3. Preferred communication channels
        4. Pain points and motivations
        5. Buying behavior patterns
        
        Audience Analysis:
        """
        
        result = await self.hf_service.generate_text(
            prompt=prompt,
            max_length=300,
            temperature=0.6
        )
        
        if result["success"]:
            return {
                "result": {
                    "audience_profile": {
                        "demographics": demographics,
                        "interests": interests,
                        "behaviors": behaviors
                    },
                    "insights": result["text"],
                    "recommended_channels": self._recommend_channels_for_audience(demographics, interests),
                    "content_preferences": self._analyze_content_preferences(interests, behaviors),
                    "messaging_strategy": self._develop_messaging_strategy(demographics, interests),
                    "persona_templates": self._create_persona_templates(demographics, interests)
                }
            }
        else:
            return result
    
    async def _analyze_competitors(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze competitor marketing strategies."""
        competitors = task.get("competitors", [])
        industry = task.get("industry", "")
        analysis_focus = task.get("focus", ["content", "social_media", "advertising"])
        
        if not competitors:
            return {"error": "Competitor list is required"}
        
        competitor_analysis = {}
        
        for competitor in competitors:
            prompt = f"""
            Analyze marketing strategy for {competitor} in the {industry} industry.
            
            Focus areas: {', '.join(analysis_focus)}
            
            Provide analysis on:
            1. Brand positioning
            2. Content strategy
            3. Social media presence
            4. Advertising approach
            5. Strengths and weaknesses
            
            Competitor Analysis:
            """
            
            result = await self.hf_service.generate_text(
                prompt=prompt,
                max_length=250,
                temperature=0.6
            )
            
            if result["success"]:
                competitor_analysis[competitor] = {
                    "analysis": result["text"],
                    "estimated_strengths": self._extract_strengths(result["text"]),
                    "estimated_weaknesses": self._extract_weaknesses(result["text"]),
                    "opportunities": self._identify_opportunities(result["text"])
                }
        
        return {
            "result": {
                "industry": industry,
                "competitors_analyzed": len(competitors),
                "analysis": competitor_analysis,
                "market_gaps": self._identify_market_gaps(competitor_analysis),
                "differentiation_opportunities": self._find_differentiation_opportunities(competitor_analysis),
                "competitive_advantages": self._suggest_competitive_advantages(competitor_analysis)
            }
        }
    
    async def _develop_brand_strategy(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Develop comprehensive brand strategy."""
        brand_data = task.get("brand", {})
        company_name = brand_data.get("name", "")
        industry = brand_data.get("industry", "")
        values = brand_data.get("values", [])
        target_market = brand_data.get("target_market", "")
        
        if not company_name or not industry:
            return {"error": "Company name and industry are required"}
        
        prompt = f"""
        Develop a comprehensive brand strategy for {company_name} in the {industry} industry.
        
        Company values: {', '.join(values)}
        Target market: {target_market}
        
        Brand strategy should include:
        1. Brand positioning statement
        2. Unique value proposition
        3. Brand personality
        4. Visual identity guidelines
        5. Voice and tone guidelines
        6. Brand messaging framework
        
        Brand Strategy:
        """
        
        result = await self.hf_service.generate_text(
            prompt=prompt,
            max_length=350,
            temperature=0.7
        )
        
        if result["success"]:
            return {
                "result": {
                    "company_name": company_name,
                    "industry": industry,
                    "brand_strategy": result["text"],
                    "brand_elements": {
                        "values": values,
                        "target_market": target_market,
                        "suggested_colors": self._suggest_brand_colors(industry, values),
                        "suggested_fonts": self._suggest_brand_fonts(industry),
                        "logo_concepts": self._suggest_logo_concepts(company_name, industry)
                    },
                    "messaging_pillars": self._create_messaging_pillars(values, target_market),
                    "brand_guidelines": self._create_brand_guidelines(company_name, industry),
                    "implementation_roadmap": self._create_brand_implementation_roadmap()
                }
            }
        else:
            return result
    
    # Helper methods
    def _initialize_campaign_templates(self) -> Dict[str, Dict]:
        """Initialize campaign templates."""
        return {
            "product_launch": {
                "phases": ["awareness", "consideration", "conversion"],
                "duration": "60 days",
                "channels": ["social_media", "email", "content_marketing", "paid_ads"]
            },
            "brand_awareness": {
                "phases": ["reach", "engagement", "recall"],
                "duration": "90 days",
                "channels": ["social_media", "content_marketing", "influencer", "pr"]
            },
            "lead_generation": {
                "phases": ["attract", "capture", "nurture"],
                "duration": "45 days",
                "channels": ["content_marketing", "email", "paid_ads", "webinars"]
            }
        }
    
    def _generate_campaign_id(self) -> str:
        """Generate unique campaign ID."""
        import uuid
        return f"camp_{uuid.uuid4().hex[:8]}"
    
    def _recommend_channels(self, target_audience: str) -> List[str]:
        """Recommend marketing channels based on target audience."""
        audience_lower = target_audience.lower()
        
        if "young" in audience_lower or "millennial" in audience_lower or "gen z" in audience_lower:
            return ["instagram", "tiktok", "twitter", "youtube", "snapchat"]
        elif "professional" in audience_lower or "business" in audience_lower:
            return ["linkedin", "email", "content_marketing", "webinars"]
        elif "senior" in audience_lower or "older" in audience_lower:
            return ["facebook", "email", "traditional_media", "direct_mail"]
        else:
            return ["facebook", "instagram", "email", "content_marketing", "google_ads"]
    
    def _define_kpi_metrics(self, objectives: List[str]) -> Dict[str, List[str]]:
        """Define KPI metrics based on objectives."""
        kpis = {}
        
        for objective in objectives:
            obj_lower = objective.lower()
            if "awareness" in obj_lower:
                kpis[objective] = ["reach", "impressions", "brand_mentions", "share_of_voice"]
            elif "engagement" in obj_lower:
                kpis[objective] = ["likes", "shares", "comments", "engagement_rate", "time_on_page"]
            elif "conversion" in obj_lower or "sales" in obj_lower:
                kpis[objective] = ["conversion_rate", "cost_per_acquisition", "revenue", "roi"]
            elif "traffic" in obj_lower:
                kpis[objective] = ["website_visits", "page_views", "bounce_rate", "session_duration"]
            else:
                kpis[objective] = ["impressions", "clicks", "engagement_rate", "conversion_rate"]
        
        return kpis
    
    def _create_campaign_timeline(self, duration: str) -> Dict[str, List[str]]:
        """Create campaign timeline with milestones."""
        # Parse duration (assuming format like "30 days", "8 weeks", etc.)
        timeline = {}
        
        if "day" in duration:
            days = int(duration.split()[0])
            weeks = days // 7
        elif "week" in duration:
            weeks = int(duration.split()[0])
        else:
            weeks = 4  # Default
        
        for week in range(1, weeks + 1):
            week_activities = []
            
            if week == 1:
                week_activities = ["Campaign setup", "Content creation", "Asset preparation"]
            elif week == weeks:
                week_activities = ["Campaign optimization", "Final push", "Results analysis"]
            else:
                week_activities = ["Content publishing", "Performance monitoring", "Optimization"]
            
            timeline[f"Week {week}"] = week_activities
        
        return timeline
    
    def _extract_channels(self, strategy_text: str) -> List[str]:
        """Extract recommended channels from strategy text."""
        channels = []
        text_lower = strategy_text.lower()
        
        channel_keywords = {
            "social media": ["social", "facebook", "instagram", "twitter", "linkedin"],