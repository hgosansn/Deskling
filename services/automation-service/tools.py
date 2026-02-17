"""Low-risk automation tools for P4-T1 baseline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import time
from typing import Any
from uuid import uuid4


@dataclass
class ToolError(Exception):
    code: str
    message: str


class LowRiskToolExecutor:
    def __init__(self, allowed_paths: list[str] | None = None) -> None:
        self._clipboard_text = ''
        self._allowed_paths = [Path(path).resolve() for path in (allowed_paths or ['/tmp'])]
        self._used_confirm_tokens: set[str] = set()

    TOOL_RISK = {
        'clipboard.write': 'low',
        'clipboard.read': 'low',
        'notify.send': 'low',
        'apps.open': 'low',
        'browser.open_url': 'low',
        'files.list_dir': 'low',
        'files.read_text': 'low',
        'files.write_text': 'medium'
    }

    def execute(self, tool_name: str, args: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = args or {}

        if tool_name == 'clipboard.write':
            return self._clipboard_write(payload)
        if tool_name == 'clipboard.read':
            return self._clipboard_read()
        if tool_name == 'notify.send':
            return self._notify_send(payload)
        if tool_name == 'apps.open':
            return self._apps_open(payload)
        if tool_name == 'browser.open_url':
            return self._browser_open_url(payload)
        if tool_name == 'files.list_dir':
            return self._files_list_dir(payload)
        if tool_name == 'files.read_text':
            return self._files_read_text(payload)
        if tool_name == 'files.write_text':
            return self._files_write_text(payload)

        raise ToolError('ERR_UNKNOWN_TOOL', f'unsupported tool: {tool_name}')

    def execute_with_policy(
        self,
        tool_name: str,
        args: dict[str, Any] | None,
        trace_id: str,
        confirm_token: dict[str, Any] | None = None,
        now: float | None = None
    ) -> dict[str, Any]:
        risk = self.TOOL_RISK.get(tool_name)
        if risk is None:
            raise ToolError('ERR_UNKNOWN_TOOL', f'unsupported tool: {tool_name}')

        if risk in ('medium', 'high'):
            self._validate_confirm_token(confirm_token, tool_name, trace_id, now=now)

        return self.execute(tool_name, args)

    def _validate_confirm_token(
        self,
        token: dict[str, Any] | None,
        tool_name: str,
        trace_id: str,
        now: float | None = None
    ) -> None:
        if not isinstance(token, dict):
            raise ToolError('ERR_CONFIRM_REQUIRED', 'confirm token required for this tool risk level')

        token_id = token.get('token_id')
        token_trace_id = token.get('trace_id')
        tools = token.get('tools')
        expires_at = token.get('expires_at')

        if not isinstance(token_id, str) or not token_id.strip():
            raise ToolError('ERR_CONFIRM_INVALID', 'confirm token missing token_id')
        if token_id in self._used_confirm_tokens:
            raise ToolError('ERR_CONFIRM_REUSED', 'confirm token already used')
        if token_trace_id != trace_id:
            raise ToolError('ERR_CONFIRM_TRACE_MISMATCH', 'confirm token trace mismatch')
        if not isinstance(tools, list) or tool_name not in tools:
            raise ToolError('ERR_CONFIRM_SCOPE', 'confirm token does not allow this tool')
        if not isinstance(expires_at, (int, float)):
            raise ToolError('ERR_CONFIRM_INVALID', 'confirm token missing expiry')

        now_ts = time.time() if now is None else now
        if now_ts > float(expires_at):
            raise ToolError('ERR_CONFIRM_EXPIRED', 'confirm token expired')

        self._used_confirm_tokens.add(token_id)

    def run_call(
        self,
        tool_name: str,
        args: dict[str, Any] | None,
        trace_id: str,
        confirm_token: dict[str, Any] | None = None,
        now: float | None = None
    ) -> dict[str, Any]:
        started_at = time.time() if now is None else now
        call_id = f'call_{uuid4().hex[:12]}'
        risk = self.TOOL_RISK.get(tool_name, 'unknown')

        try:
            result = self.execute_with_policy(tool_name, args, trace_id, confirm_token=confirm_token, now=now)
            ended_at = time.time() if now is None else now
            return {
                'ok': True,
                'result': result,
                'audit': {
                    'trace_id': trace_id,
                    'call_id': call_id,
                    'tool': tool_name,
                    'risk': risk,
                    'policy_decision': 'allowed',
                    'outcome': 'ok',
                    'started_at': started_at,
                    'ended_at': ended_at
                }
            }
        except ToolError as err:
            ended_at = time.time() if now is None else now
            return {
                'ok': False,
                'error': {'code': err.code, 'message': err.message},
                'audit': {
                    'trace_id': trace_id,
                    'call_id': call_id,
                    'tool': tool_name,
                    'risk': risk,
                    'policy_decision': 'blocked',
                    'outcome': 'error',
                    'error_code': err.code,
                    'started_at': started_at,
                    'ended_at': ended_at
                }
            }

    def _clipboard_write(self, args: dict[str, Any]) -> dict[str, Any]:
        text = args.get('text')
        if not isinstance(text, str):
            raise ToolError('ERR_INVALID_ARGS', 'clipboard.write requires string arg text')

        self._clipboard_text = text
        return {'ok': True, 'tool': 'clipboard.write', 'chars': len(text)}

    def _clipboard_read(self) -> dict[str, Any]:
        return {'ok': True, 'tool': 'clipboard.read', 'text': self._clipboard_text}

    def _notify_send(self, args: dict[str, Any]) -> dict[str, Any]:
        title = args.get('title')
        body = args.get('body')

        if not isinstance(title, str) or not title.strip():
            raise ToolError('ERR_INVALID_ARGS', 'notify.send requires non-empty title')
        if not isinstance(body, str):
            raise ToolError('ERR_INVALID_ARGS', 'notify.send requires string body')

        # Baseline implementation is structured return only; OS integration comes later.
        return {'ok': True, 'tool': 'notify.send', 'summary': f'notification queued: {title}'}

    def _apps_open(self, args: dict[str, Any]) -> dict[str, Any]:
        app = args.get('app')
        if not isinstance(app, str) or not app.strip():
            raise ToolError('ERR_INVALID_ARGS', 'apps.open requires non-empty app name')

        # Baseline is policy-validated proposal execution without process spawn.
        return {'ok': True, 'tool': 'apps.open', 'summary': f'app open accepted: {app.strip()}'}

    def _browser_open_url(self, args: dict[str, Any]) -> dict[str, Any]:
        url = args.get('url')
        dry_run = bool(args.get('dry_run', True))

        if not isinstance(url, str) or not url.strip():
            raise ToolError('ERR_INVALID_ARGS', 'browser.open_url requires non-empty url')
        if not (url.startswith('http://') or url.startswith('https://')):
            raise ToolError('ERR_INVALID_ARGS', 'browser.open_url only supports http(s) urls')

        if dry_run:
            return {
                'ok': True,
                'tool': 'browser.open_url',
                'engine': 'playwright',
                'url': url,
                'dry_run': True
            }

        try:
            from playwright.sync_api import sync_playwright
        except ImportError as err:
            raise ToolError('ERR_PLAYWRIGHT_MISSING', f'playwright dependency missing: {err}') from err

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until='domcontentloaded')
            title = page.title()
            browser.close()

        return {
            'ok': True,
            'tool': 'browser.open_url',
            'engine': 'playwright',
            'url': url,
            'dry_run': False,
            'title': title
        }

    def _resolve_allowed_path(self, raw_path: Any) -> Path:
        if not isinstance(raw_path, str) or not raw_path.strip():
            raise ToolError('ERR_INVALID_ARGS', 'file tool requires non-empty string path')

        candidate = Path(raw_path).expanduser().resolve()
        if not any(candidate == base or base in candidate.parents for base in self._allowed_paths):
            raise ToolError('ERR_PATH_NOT_ALLOWED', f'path outside allowlist: {candidate}')
        return candidate

    def _files_list_dir(self, args: dict[str, Any]) -> dict[str, Any]:
        path = self._resolve_allowed_path(args.get('path'))
        if not path.exists() or not path.is_dir():
            raise ToolError('ERR_PATH_INVALID', f'not a directory: {path}')

        entries = sorted([entry.name for entry in path.iterdir()])
        return {'ok': True, 'tool': 'files.list_dir', 'path': str(path), 'entries': entries}

    def _files_read_text(self, args: dict[str, Any]) -> dict[str, Any]:
        path = self._resolve_allowed_path(args.get('path'))
        if not path.exists() or not path.is_file():
            raise ToolError('ERR_PATH_INVALID', f'not a file: {path}')
        return {'ok': True, 'tool': 'files.read_text', 'path': str(path), 'text': path.read_text(encoding='utf-8')}

    def _files_write_text(self, args: dict[str, Any]) -> dict[str, Any]:
        path = self._resolve_allowed_path(args.get('path'))
        text = args.get('text')
        overwrite = bool(args.get('overwrite', False))

        if not isinstance(text, str):
            raise ToolError('ERR_INVALID_ARGS', 'files.write_text requires string text')

        if path.exists() and not overwrite:
            raise ToolError('ERR_OVERWRITE_BLOCKED', f'file exists and overwrite is false: {path}')

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        return {'ok': True, 'tool': 'files.write_text', 'path': str(path), 'bytes': len(text.encode('utf-8'))}
