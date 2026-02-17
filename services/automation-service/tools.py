"""Tool execution implementations."""

import subprocess
import os
from pathlib import Path
from typing import Dict, Any, Optional
import json
from datetime import datetime


class ToolExecutor:
    """Execute tools with safety checks and audit logging."""

    def __init__(self, allowed_paths: list = None):
        self.allowed_paths = allowed_paths or [
            str(Path.home() / "Documents"),
            str(Path.home() / "Downloads"),
        ]
        self.audit_log = []

    def execute_tool(self, tool_name: str, args: Dict[str, Any], trace_id: str) -> Dict:
        """
        Execute a tool and return the result.
        
        Returns dict with:
        - success: bool
        - result: any (tool-specific)
        - error: str (if failed)
        - audit_info: dict (for logging)
        """
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "trace_id": trace_id,
            "tool": tool_name,
            "args": args,
            "result": None,
            "error": None
        }
        
        try:
            if tool_name == "clipboard.read":
                result = self._clipboard_read()
            elif tool_name == "clipboard.write":
                result = self._clipboard_write(args.get("text", ""))
            elif tool_name == "notify.send":
                result = self._notify_send(args.get("title", ""), args.get("message", ""))
            elif tool_name == "files.read_text":
                result = self._files_read_text(args.get("path"))
            elif tool_name == "files.write_text":
                result = self._files_write_text(args.get("path"), args.get("content", ""))
            elif tool_name == "files.search":
                result = self._files_search(args.get("pattern", "*"), args.get("path"))
            elif tool_name == "browser.open_url":
                result = self._browser_open_url(args.get("url"))
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
            
            audit_entry["result"] = result
            self.audit_log.append(audit_entry)
            
            return {
                "success": True,
                "result": result,
                "error": None,
                "audit_info": audit_entry
            }
            
        except Exception as e:
            audit_entry["error"] = str(e)
            self.audit_log.append(audit_entry)
            
            return {
                "success": False,
                "result": None,
                "error": str(e),
                "audit_info": audit_entry
            }

    def _clipboard_read(self) -> str:
        """Read from clipboard."""
        try:
            import pyperclip
            return pyperclip.paste()
        except ImportError:
            # Fallback for environments without pyperclip
            return "[Clipboard not available - pyperclip not installed]"

    def _clipboard_write(self, text: str) -> str:
        """Write to clipboard."""
        try:
            import pyperclip
            pyperclip.copy(text)
            return f"Copied {len(text)} characters to clipboard"
        except ImportError:
            return "[Clipboard not available - pyperclip not installed]"

    def _notify_send(self, title: str, message: str) -> str:
        """Send desktop notification."""
        # Try platform-specific notification methods
        if os.name == 'posix':
            # Linux/Mac
            try:
                subprocess.run(
                    ['notify-send', title, message],
                    check=True,
                    capture_output=True
                )
                return f"Notification sent: {title}"
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Fallback: just log it
                return f"[Would send notification] {title}: {message}"
        else:
            # Windows or unsupported
            return f"[Would send notification] {title}: {message}"

    def _is_path_allowed(self, path: str) -> bool:
        """Check if path is in allowed directories."""
        abs_path = os.path.abspath(os.path.expanduser(path))
        for allowed in self.allowed_paths:
            allowed_abs = os.path.abspath(os.path.expanduser(allowed))
            if abs_path.startswith(allowed_abs):
                return True
        return False

    def _files_read_text(self, path: str) -> str:
        """Read text from file."""
        if not self._is_path_allowed(path):
            raise PermissionError(f"Path not allowed: {path}")
        
        expanded_path = os.path.expanduser(path)
        with open(expanded_path, 'r') as f:
            content = f.read()
        
        return f"Read {len(content)} characters from {path}"

    def _files_write_text(self, path: str, content: str) -> str:
        """Write text to file."""
        if not self._is_path_allowed(path):
            raise PermissionError(f"Path not allowed: {path}")
        
        expanded_path = os.path.expanduser(path)
        
        # Create parent directories if needed
        os.makedirs(os.path.dirname(expanded_path), exist_ok=True)
        
        with open(expanded_path, 'w') as f:
            f.write(content)
        
        return f"Wrote {len(content)} characters to {path}"

    def _files_search(self, pattern: str, path: str) -> str:
        """Search for files matching pattern."""
        if not self._is_path_allowed(path):
            raise PermissionError(f"Path not allowed: {path}")
        
        expanded_path = os.path.expanduser(path)
        if not os.path.exists(expanded_path):
            return f"Path does not exist: {path}"
        
        # Simple glob search
        from glob import glob
        matches = glob(os.path.join(expanded_path, pattern))
        
        return f"Found {len(matches)} files matching '{pattern}' in {path}"

    def _browser_open_url(self, url: str) -> str:
        """Open URL in default browser."""
        import webbrowser
        webbrowser.open(url)
        return f"Opened {url} in browser"

    def get_audit_log(self) -> list:
        """Return the audit log."""
        return self.audit_log
