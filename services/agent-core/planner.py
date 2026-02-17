"""Agent planner - generates plans and tool proposals from user requests."""

from typing import Dict, List, Optional
import re


class AgentPlanner:
    """Plan generation and tool proposal logic."""

    def __init__(self):
        # Simple keyword-based planning for now (will be replaced with LLM)
        self.tool_patterns = {
            "clipboard": ["clipboard", "copy", "paste", "clip"],
            "notify": ["notify", "notification", "alert", "remind"],
            "apps": ["open app", "launch", "start program"],
            "files": ["file", "folder", "directory", "read", "write", "search"],
            "browser": ["browser", "website", "url", "web", "navigate"]
        }

    def analyze_request(self, user_text: str) -> Dict:
        """
        Analyze user request and generate a plan with tool proposals.
        
        Returns dict with:
        - plan_text: natural language description
        - steps: list of step dicts
        - requires_confirmation: bool
        - tool_calls: list of proposed tool calls
        """
        user_text_lower = user_text.lower()
        
        # Detect tool category
        detected_tools = []
        for category, keywords in self.tool_patterns.items():
            if any(kw in user_text_lower for kw in keywords):
                detected_tools.append(category)
        
        # Generate plan based on detected tools
        if not detected_tools:
            # No tools needed, just a conversation
            return {
                "plan_text": "I'll respond to your message.",
                "steps": [
                    {"description": "Understand your request", "risk": "low"},
                    {"description": "Provide a helpful response", "risk": "low"}
                ],
                "requires_confirmation": False,
                "tool_calls": [],
                "response_text": self._generate_simple_response(user_text)
            }
        
        # Tool-based plan
        steps = []
        tool_calls = []
        max_risk = "low"
        
        for tool_cat in detected_tools:
            if tool_cat == "clipboard":
                if "copy" in user_text_lower:
                    steps.append({
                        "description": "Copy text to clipboard",
                        "risk": "low",
                        "tool_call": {
                            "tool": "clipboard.write",
                            "args": {"text": "Example text"}
                        }
                    })
                    tool_calls.append({
                        "tool": "clipboard.write",
                        "args": {"text": "Example text"}
                    })
                elif "read" in user_text_lower or "paste" in user_text_lower:
                    steps.append({
                        "description": "Read clipboard contents",
                        "risk": "low",
                        "tool_call": {
                            "tool": "clipboard.read",
                            "args": {}
                        }
                    })
                    tool_calls.append({
                        "tool": "clipboard.read",
                        "args": {}
                    })
            
            elif tool_cat == "notify":
                steps.append({
                    "description": "Send desktop notification",
                    "risk": "low",
                    "tool_call": {
                        "tool": "notify.send",
                        "args": {
                            "title": "Deskling",
                            "message": "Test notification"
                        }
                    }
                })
                tool_calls.append({
                    "tool": "notify.send",
                    "args": {
                        "title": "Deskling",
                        "message": "Test notification"
                    }
                })
            
            elif tool_cat == "files":
                if "write" in user_text_lower or "create" in user_text_lower:
                    steps.append({
                        "description": "Write to file",
                        "risk": "medium",
                        "tool_call": {
                            "tool": "files.write_text",
                            "args": {
                                "path": "~/Documents/test.txt",
                                "content": "Example content"
                            }
                        }
                    })
                    tool_calls.append({
                        "tool": "files.write_text",
                        "args": {
                            "path": "~/Documents/test.txt",
                            "content": "Example content"
                        }
                    })
                    max_risk = "medium"
                else:
                    steps.append({
                        "description": "Search or read file",
                        "risk": "low",
                        "tool_call": {
                            "tool": "files.search",
                            "args": {"pattern": "*.txt", "path": "~/Documents"}
                        }
                    })
                    tool_calls.append({
                        "tool": "files.search",
                        "args": {"pattern": "*.txt", "path": "~/Documents"}
                    })
            
            elif tool_cat == "browser":
                # Extract URL if present
                url_match = re.search(r'https?://[^\s]+', user_text)
                url = url_match.group(0) if url_match else "https://example.com"
                
                steps.append({
                    "description": f"Open {url} in browser",
                    "risk": "low",
                    "tool_call": {
                        "tool": "browser.open_url",
                        "args": {"url": url}
                    }
                })
                tool_calls.append({
                    "tool": "browser.open_url",
                    "args": {"url": url}
                })
        
        # Determine if confirmation needed
        requires_confirmation = max_risk in ["medium", "high"]
        
        plan_text = f"I'll help you with that. I plan to: {', '.join(s['description'].lower() for s in steps)}."
        
        return {
            "plan_text": plan_text,
            "steps": steps,
            "requires_confirmation": requires_confirmation,
            "tool_calls": tool_calls
        }

    def _generate_simple_response(self, user_text: str) -> str:
        """Generate a simple conversational response."""
        greetings = ["hello", "hi", "hey", "greetings"]
        if any(g in user_text.lower() for g in greetings):
            return "Hello! How can I assist you today?"
        
        if "help" in user_text.lower():
            return ("I can help you with clipboard operations, desktop notifications, "
                   "file management, opening applications, and browser automation. "
                   "What would you like to do?")
        
        if "thank" in user_text.lower():
            return "You're welcome! Let me know if you need anything else."
        
        return ("I understand you said: " + user_text + ". "
               "I'm still learning, so my responses are basic for now. "
               "Try asking me to notify you, copy text, or open a website!")
