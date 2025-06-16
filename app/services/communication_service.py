import asyncio
import json
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime
from app.core.logger import get_logger

class CommunicationService:
    """Service for handling inter-agent communication."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.message_queue = asyncio.Queue()
        self.subscribers = {}
        self.message_history = []
        self.is_running = False
    
    async def start(self):
        """Start the communication service."""
        if self.is_running:
            return
        
        self.is_running = True
        self.logger.info("Communication service started")
        
        # Start message processing loop
        asyncio.create_task(self._process_messages())
    
    async def stop(self):
        """Stop the communication service."""
        self.is_running = False
        self.logger.info("Communication service stopped")
    
    async def send_message(self, sender: str, recipient: str, message_type: str, data: Dict[str, Any]) -> bool:
        """Send message between agents."""
        try:
            message = {
                "id": self._generate_message_id(),
                "sender": sender,
                "recipient": recipient,
                "type": message_type,
                "data": data,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "pending"
            }
            
            await self.message_queue.put(message)
            self.message_history.append(message)
            
            self.logger.info(f"Message queued: {sender} -> {recipient} ({message_type})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send message: {str(e)}")
            return False
    
    async def broadcast_message(self, sender: str, message_type: str, data: Dict[str, Any]) -> bool:
        """Broadcast message to all subscribers."""
        try:
            message = {
                "id": self._generate_message_id(),
                "sender": sender,
                "recipient": "broadcast",
                "type": message_type,
                "data": data,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "broadcasting"
            }
            
            # Send to all subscribers
            for subscriber_id, callback in self.subscribers.items():
                try:
                    await callback(message)
                except Exception as e:
                    self.logger.error(f"Failed to deliver broadcast to {subscriber_id}: {str(e)}")
            
            self.message_history.append(message)
            self.logger.info(f"Broadcast sent: {sender} -> all ({message_type})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to broadcast message: {str(e)}")
            return False
    
    def subscribe(self, subscriber_id: str, callback: Callable) -> bool:
        """Subscribe to receive messages."""
        try:
            self.subscribers[subscriber_id] = callback
            self.logger.info(f"Subscriber added: {subscriber_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add subscriber {subscriber_id}: {str(e)}")
            return False
    
    def unsubscribe(self, subscriber_id: str) -> bool:
        """Unsubscribe from receiving messages."""
        try:
            if subscriber_id in self.subscribers:
                del self.subscribers[subscriber_id]
                self.logger.info(f"Subscriber removed: {subscriber_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to remove subscriber {subscriber_id}: {str(e)}")
            return False
    
    async def _process_messages(self):
        """Process messages from the queue."""
        while self.is_running:
            try:
                # Wait for message with timeout
                message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                
                # Process the message
                await self._deliver_message(message)
                
            except asyncio.TimeoutError:
                # No message received, continue loop
                continue
            except Exception as e:
                self.logger.error(f"Error processing message: {str(e)}")
    
    async def _deliver_message(self, message: Dict[str, Any]):
        """Deliver message to recipient."""
        try:
            recipient = message["recipient"]
            
            if recipient == "broadcast":
                # Already handled in broadcast_message
                return
            
            # Find recipient subscriber
            if recipient in self.subscribers:
                callback = self.subscribers[recipient]
                await callback(message)
                message["status"] = "delivered"
                self.logger.info(f"Message delivered: {message['id']}")
            else:
                message["status"] = "failed"
                self.logger.warning(f"Recipient not found: {recipient}")
                
        except Exception as e:
            message["status"] = "failed"
            self.logger.error(f"Failed to deliver message {message['id']}: {str(e)}")
    
    def get_message_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent message history."""
        return self.message_history[-limit:]
    
    def get_communication_stats(self) -> Dict[str, Any]:
        """Get communication statistics."""
        total_messages = len(self.message_history)
        delivered_messages = len([m for m in self.message_history if m["status"] == "delivered"])
        failed_messages = len([m for m in self.message_history if m["status"] == "failed"])
        
        return {
            "total_messages": total_messages,
            "delivered_messages": delivered_messages,
            "failed_messages": failed_messages,
            "success_rate": (delivered_messages / total_messages * 100) if total_messages > 0 else 0,
            "active_subscribers": len(self.subscribers),
            "queue_size": self.message_queue.qsize(),
            "service_running": self.is_running
        }
    
    def _generate_message_id(self) -> str:
        """Generate unique message ID."""
        import uuid
        return str(uuid.uuid4())[:8]