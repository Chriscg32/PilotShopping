from typing import Dict, Any, List
from app.agents.base import BaseAgent

class DesignAgent(BaseAgent):
    """Design agent for UI/UX and visual design tasks."""
    
    def __init__(self):
        super().__init__(
            name="design",
            capabilities=[
                "ui_design",
                "ux_design",
                "logo_creation",
                "color_palette",
                "typography",
                "responsive_design",
                "design_templates",
                "brand_guidelines"
            ]
        )
        self.color_palettes = {
            "professional": ["#2C3E50", "#3498DB", "#ECF0F1", "#95A5A6"],
            "creative": ["#E74C3C", "#F39C12", "#9B59B6", "#1ABC9C"],
            "minimal": ["#000000", "#FFFFFF", "#F8F9FA", "#6C757D"],
            "warm": ["#D35400", "#E67E22", "#F39C12", "#FDF2E9"]
        }
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process design-related tasks."""
        task_type = task.get("type")
        
        if task_type == "create_design":
            return await self._create_design(task)
        elif task_type == "generate_palette":
            return await self._generate_color_palette(task)
        elif task_type == "design_logo":
            return await self._design_logo(task)
        elif task_type == "create_template":
            return await self._create_template(task)
        else:
            return {"error": f"Unknown design task: {task_type}"}
    
    async def get_capabilities(self) -> List[str]:
        """Get design agent capabilities."""
        return self.capabilities
    
    async def _create_design(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create a design based on specifications."""
        design_type = task.get("design_type", "landing_page")
        style = task.get("style", "professional")
        requirements = task.get("requirements", {})
        
        # Generate design specifications
        color_palette = self.color_palettes.get(style, self.color_palettes["professional"])
        
        design_specs = {
            "type": design_type,
            "style": style,
            "color_palette": color_palette,
            "typography": self._get_typography(style),
            "layout": self._get_layout(design_type),
            "components": self._get_components(design_type),
            "responsive_breakpoints": ["mobile", "tablet", "desktop"]
        }
        
        return {
            "design_id": f"design_{hash(str(task)) % 10000}",
            "specifications": design_specs,
            "assets_generated": self._generate_asset_list(design_type),
            "estimated_completion": "2-3 business days"
        }
    
    async def _generate_color_palette(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate color palette."""
        theme = task.get("theme", "professional")
        primary_color = task.get("primary_color")
        
        if primary_color:
            # Generate complementary colors based on primary
            palette = [primary_color, "#FFFFFF", "#F8F9FA", "#6C757D"]
        else:
            palette = self.color_palettes.get(theme, self.color_palettes["professional"])
        
        return {
            "theme": theme,
            "primary": palette[0],
            "secondary": palette[1],
            "accent": palette[2],
            "neutral": palette[3],
            "full_palette": palette,
            "usage_guidelines": {
                "primary": "Main brand color, buttons, headers",
                "secondary": "Background, cards, sections",
                "accent": "Highlights, call-to-actions",
                "neutral": "Text, borders, subtle elements"
            }
        }
    
    async def _design_logo(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Design logo specifications."""
        company_name = task.get("company_name", "Company")
        industry = task.get("industry", "technology")
        style = task.get("style", "modern")
        
        logo_concepts = {
            "modern": {
                "type": "wordmark",
                "font_style": "sans-serif",
                "characteristics": ["clean", "minimal", "geometric"]
            },
            "classic": {
                "type": "combination",
                "font_style": "serif",
                "characteristics": ["traditional", "elegant", "timeless"]
            },
            "creative": {
                "type": "symbol",
                "font_style": "custom",
                "characteristics": ["unique", "artistic", "memorable"]
            }
        }
        
        concept = logo_concepts.get(style, logo_concepts["modern"])
        
        return {
            "company_name": company_name,
            "industry": industry,
            "style": style,
            "concept": concept,
            "variations": ["horizontal", "vertical", "icon-only"],
            "file_formats": ["SVG", "PNG", "JPG", "PDF"],
            "color_versions": ["full-color", "monochrome", "white", "black"]
        }
    
    async def _create_template(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create design template."""
        template_type = task.get("template_type", "landing_page")
        industry = task.get("industry", "general")
        
        templates = {
            "landing_page": {
                "sections": ["hero", "features", "testimonials", "cta", "footer"],
                "components": ["navigation", "buttons", "forms", "cards"],
                "pages": 1
            },
            "dashboard": {
                "sections": ["sidebar", "header", "main_content", "widgets"],
                "components": ["charts", "tables", "cards", "navigation"],
                "pages": 5
            },
            "mobile_app": {
                "sections": ["splash", "onboarding", "main_screens", "profile"],
                "components": ["buttons", "forms", "lists", "navigation"],
                "pages": 8
            }
        }
        
        template = templates.get(template_type, templates["landing_page"])
        
        return {
            "template_type": template_type,
            "industry": industry,
            "structure": template,
            "responsive": True,
            "accessibility_compliant": True,
            "estimated_development_time": f"{template['pages'] * 2} days"
        }
    
    def _get_typography(self, style: str) -> Dict[str, str]:
        """Get typography recommendations."""
        typography_styles = {
            "professional": {
                "primary_font": "Inter",
                "secondary_font": "Source Sans Pro",
                "heading_weight": "600",
                "body_weight": "400"
            },
            "creative": {
                "primary_font": "Poppins",
                "secondary_font": "Open Sans",
                "heading_weight": "700",
                "body_weight": "400"
            },
            "minimal": {
                "primary_font": "Helvetica Neue",
                "secondary_font": "Arial",
                "heading_weight": "300",
                "body_weight": "300"
            }
        }
        return typography_styles.get(style, typography_styles["professional"])
    
    def _get_layout(self, design_type: str) -> Dict[str, Any]:
        """Get layout specifications."""
        layouts = {
            "landing_page": {
                "grid": "12-column",
                "max_width": "1200px",
                "spacing": "24px",
                "sections": ["hero", "features", "testimonials", "cta"]
            },
            "dashboard": {
                "grid": "flexible",
                "max_width": "100%",
                "spacing": "16px",
                "sections": ["sidebar", "header", "main", "footer"]
            }
        }
        return layouts.get(design_type, layouts["landing_page"])
    
    def _get_components(self, design_type: str) -> List[str]:
        """Get component list for design type."""
        components = {
            "landing_page": ["hero_section", "feature_cards", "testimonial_slider", "cta_button", "contact_form"],
            "dashboard": ["sidebar_nav", "top_bar", "data_cards", "charts", "tables"],
            "mobile_app": ["tab_bar", "cards", "buttons", "forms", "lists"]
        }
        return components.get(design_type, components["landing_page"])
    
    def _generate_asset_list(self, design_type: str) -> List[str]:
        """Generate list of assets to be created."""
        base_assets = ["mockups", "style_guide", "component_library"]
        
        if design_type == "landing_page":
            return base_assets + ["hero_images", "icons", "illustrations"]
        elif design_type == "dashboard":
            return base_assets + ["charts", "data_visualizations", "icons"]
        else:
            return base_assets + ["icons", "illustrations"]