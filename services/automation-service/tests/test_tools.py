import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'services' / 'automation-service'))

from tools import LowRiskToolExecutor, ToolError  # noqa: E402


class LowRiskToolExecutorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.allowed = Path(self.tmp.name)
        self.executor = LowRiskToolExecutor(allowed_paths=[self.tmp.name])

    def tearDown(self):
        self.tmp.cleanup()

    def test_clipboard_roundtrip(self):
        write = self.executor.execute('clipboard.write', {'text': 'hello'})
        read = self.executor.execute('clipboard.read')
        self.assertTrue(write['ok'])
        self.assertEqual(read['text'], 'hello')

    def test_notify_send(self):
        result = self.executor.execute('notify.send', {'title': 'Deskling', 'body': 'ready'})
        self.assertTrue(result['ok'])
        self.assertIn('queued', result['summary'])

    def test_apps_open(self):
        result = self.executor.execute('apps.open', {'app': 'firefox'})
        self.assertTrue(result['ok'])
        self.assertIn('firefox', result['summary'])

    def test_browser_open_url_dry_run(self):
        result = self.executor.execute('browser.open_url', {'url': 'https://example.com', 'dry_run': True})
        self.assertTrue(result['ok'])
        self.assertEqual(result['engine'], 'playwright')
        self.assertTrue(result['dry_run'])

    def test_unknown_tool_rejected(self):
        with self.assertRaises(ToolError) as err:
            self.executor.execute('files.delete_path', {'path': '/tmp/x'})
        self.assertEqual(err.exception.code, 'ERR_UNKNOWN_TOOL')

    def test_browser_open_url_rejects_invalid_url(self):
        with self.assertRaises(ToolError) as err:
            self.executor.execute('browser.open_url', {'url': 'file:///tmp/a'})
        self.assertEqual(err.exception.code, 'ERR_INVALID_ARGS')

    def test_files_write_read_and_list(self):
        target = self.allowed / 'notes' / 'todo.txt'
        self.executor.execute('files.write_text', {'path': str(target), 'text': 'deskling'})

        read = self.executor.execute('files.read_text', {'path': str(target)})
        listing = self.executor.execute('files.list_dir', {'path': str(target.parent)})

        self.assertEqual(read['text'], 'deskling')
        self.assertIn('todo.txt', listing['entries'])

    def test_files_write_blocks_overwrite_without_flag(self):
        target = self.allowed / 'todo.txt'
        self.executor.execute('files.write_text', {'path': str(target), 'text': 'v1'})
        with self.assertRaises(ToolError) as err:
            self.executor.execute('files.write_text', {'path': str(target), 'text': 'v2'})
        self.assertEqual(err.exception.code, 'ERR_OVERWRITE_BLOCKED')

    def test_files_reject_outside_allowlist(self):
        outside = Path('/tmp') / 'outside-allowlist.txt'
        with self.assertRaises(ToolError) as err:
            self.executor.execute('files.write_text', {'path': str(outside), 'text': 'nope'})
        self.assertEqual(err.exception.code, 'ERR_PATH_NOT_ALLOWED')

    def _token(self, trace_id='trace-1', tools=None, expires_at=9999999999.0, token_id='tok-1'):
        return {
            'token_id': token_id,
            'trace_id': trace_id,
            'tools': tools or ['files.write_text'],
            'expires_at': expires_at
        }

    def test_medium_risk_requires_confirm_token(self):
        target = self.allowed / 'secure.txt'
        with self.assertRaises(ToolError) as err:
            self.executor.execute_with_policy('files.write_text', {'path': str(target), 'text': 'x'}, trace_id='trace-1')
        self.assertEqual(err.exception.code, 'ERR_CONFIRM_REQUIRED')

    def test_confirm_token_enforces_trace_scope_and_expiry(self):
        target = self.allowed / 'secure.txt'

        with self.assertRaises(ToolError) as err_trace:
            self.executor.execute_with_policy(
                'files.write_text',
                {'path': str(target), 'text': 'x'},
                trace_id='trace-abc',
                confirm_token=self._token(trace_id='trace-def', token_id='tok-trace')
            )
        self.assertEqual(err_trace.exception.code, 'ERR_CONFIRM_TRACE_MISMATCH')

        with self.assertRaises(ToolError) as err_scope:
            self.executor.execute_with_policy(
                'files.write_text',
                {'path': str(target), 'text': 'x'},
                trace_id='trace-1',
                confirm_token=self._token(tools=['notify.send'], token_id='tok-scope')
            )
        self.assertEqual(err_scope.exception.code, 'ERR_CONFIRM_SCOPE')

        with self.assertRaises(ToolError) as err_expired:
            self.executor.execute_with_policy(
                'files.write_text',
                {'path': str(target), 'text': 'x'},
                trace_id='trace-1',
                confirm_token=self._token(expires_at=10.0, token_id='tok-expired'),
                now=20.0
            )
        self.assertEqual(err_expired.exception.code, 'ERR_CONFIRM_EXPIRED')

    def test_confirm_token_single_use(self):
        target = self.allowed / 'secure.txt'
        token = self._token(token_id='tok-reuse')

        first = self.executor.execute_with_policy(
            'files.write_text',
            {'path': str(target), 'text': 'x'},
            trace_id='trace-1',
            confirm_token=token
        )
        self.assertTrue(first['ok'])

        with self.assertRaises(ToolError) as err:
            self.executor.execute_with_policy(
                'files.write_text',
                {'path': str(target), 'text': 'y', 'overwrite': True},
                trace_id='trace-1',
                confirm_token=token
            )
        self.assertEqual(err.exception.code, 'ERR_CONFIRM_REUSED')

    def test_run_call_includes_audit_on_success(self):
        call = self.executor.run_call('notify.send', {'title': 'Deskling', 'body': 'ok'}, trace_id='trace-9', now=10.0)
        self.assertTrue(call['ok'])
        self.assertEqual(call['audit']['trace_id'], 'trace-9')
        self.assertEqual(call['audit']['policy_decision'], 'allowed')
        self.assertEqual(call['audit']['outcome'], 'ok')

    def test_run_call_includes_audit_on_error(self):
        call = self.executor.run_call('notify.send', {'title': '', 'body': 'x'}, trace_id='trace-10', now=10.0)
        self.assertFalse(call['ok'])
        self.assertEqual(call['audit']['trace_id'], 'trace-10')
        self.assertEqual(call['audit']['policy_decision'], 'blocked')
        self.assertEqual(call['audit']['outcome'], 'error')
        self.assertEqual(call['error']['code'], 'ERR_INVALID_ARGS')


if __name__ == '__main__':
    unittest.main()
