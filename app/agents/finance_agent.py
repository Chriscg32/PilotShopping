from typing import Dict, Any, List
from app.agents.base import BaseAgent

class FinanceAgent(BaseAgent):
    """Finance agent for payment processing and financial operations."""
    
    def __init__(self):
        super().__init__(
            name="finance",
            capabilities=[
                "payment_processing",
                "invoice_generation",
                "financial_analysis",
                "tax_calculations",
                "payment_tracking",
                "financial_reporting"
            ]
        )
        self.tax_rates = {
            "US": 0.08,
            "UK": 0.20,
            "CA": 0.13,
            "default": 0.10
        }
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process finance-related tasks."""
        task_type = task.get("type")
        
        if task_type == "process_payment":
            return await self._process_payment(task)
        elif task_type == "generate_invoice":
            return await self._generate_invoice(task)
        elif task_type == "calculate_taxes":
            return await self._calculate_taxes(task)
        elif task_type == "financial_report":
            return await self._generate_financial_report(task)
        else:
            return {"error": f"Unknown finance task: {task_type}"}
    
    async def get_capabilities(self) -> List[str]:
        """Get finance agent capabilities."""
        return self.capabilities
    
    async def _process_payment(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process payment transaction."""
        payment_data = task.get("payment", {})
        amount = payment_data.get("amount", 0)
        currency = payment_data.get("currency", "USD")
        method = payment_data.get("method", "card")
        customer_id = payment_data.get("customer_id")
        
        # Simulate payment processing
        import uuid
        transaction_id = str(uuid.uuid4())
        
        # Basic validation
        if amount <= 0:
            return {
                "success": False,
                "error": "Invalid amount",
                "transaction_id": None
            }
        
        # Simulate processing fee
        processing_fee = amount * 0.029  # 2.9% processing fee
        net_amount = amount - processing_fee
        
        return {
            "success": True,
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": currency,
            "method": method,
            "processing_fee": processing_fee,
            "net_amount": net_amount,
            "status": "completed",
            "processed_at": "2024-01-XX 10:00:00"
        }
    
    async def _generate_invoice(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate invoice."""
        invoice_data = task.get("invoice", {})
        customer = invoice_data.get("customer", {})
        items = invoice_data.get("items", [])
        country = invoice_data.get("country", "US")
        
        # Calculate totals
        subtotal = sum(item.get("price", 0) * item.get("quantity", 1) for item in items)
        tax_rate = self.tax_rates.get(country, self.tax_rates["default"])
        tax_amount = subtotal * tax_rate
        total = subtotal + tax_amount
        
        # Generate invoice number
        import uuid
        invoice_number = f"INV-{str(uuid.uuid4())[:8].upper()}"
        
        return {
            "invoice_number": invoice_number,
            "customer": customer,
            "items": items,
            "subtotal": subtotal,
            "tax_rate": tax_rate,
            "tax_amount": tax_amount,
            "total": total,
            "currency": "USD",
            "due_date": "2024-02-XX",
            "status": "pending"
        }
    
    async def _calculate_taxes(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate taxes for transaction."""
        amount = task.get("amount", 0)
        country = task.get("country", "US")
        tax_type = task.get("tax_type", "sales")
        
        tax_rate = self.tax_rates.get(country, self.tax_rates["default"])
        tax_amount = amount * tax_rate
        
        return {
            "amount": amount,
            "country": country,
            "tax_type": tax_type,
            "tax_rate": tax_rate,
            "tax_amount": tax_amount,
            "total_with_tax": amount + tax_amount
        }
    
    async def _generate_financial_report(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate financial report."""
        period = task.get("period", "monthly")
        transactions = task.get("transactions", [])
        
        # Calculate metrics
        total_revenue = sum(t.get("amount", 0) for t in transactions if t.get("type") == "income")
        total_expenses = sum(t.get("amount", 0) for t in transactions if t.get("type") == "expense")
        net_profit = total_revenue - total_expenses
        
        return {
            "period": period,
            "total_transactions": len(transactions),
            "total_revenue": total_revenue,
            "total_expenses": total_expenses,
            "net_profit": net_profit,
            "profit_margin": (net_profit / total_revenue * 100) if total_revenue > 0 else 0,
            "generated_at": "2024-01-XX 10:00:00"
        }