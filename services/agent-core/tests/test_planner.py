import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'services' / 'agent-core'))

from planner import propose_plan  # noqa: E402


class PlannerTests(unittest.TestCase):
    def test_returns_none_for_non_tool_request(self):
        self.assertIsNone(propose_plan('tell me a joke'))

    def test_low_risk_plan(self):
        plan = propose_plan('please notify me at 5pm')
        self.assertIsNotNone(plan)
        self.assertEqual(plan['proposed_tools'][0]['risk'], 'low')
        self.assertFalse(plan['needs_confirmation'])
        self.assertEqual(plan['proposed_calls'][0]['tool_name'], 'notify.send')
        self.assertFalse(plan['proposed_calls'][0]['confirmation_required'])

    def test_medium_risk_requires_confirmation(self):
        plan = propose_plan('write hello in a file')
        self.assertTrue(plan['needs_confirmation'])
        self.assertIn('files.write_text', [tool['name'] for tool in plan['proposed_tools']])

    def test_high_risk_requires_confirmation(self):
        plan = propose_plan('delete the temp folder')
        self.assertTrue(plan['needs_confirmation'])
        self.assertIn('high', [tool['risk'] for tool in plan['proposed_tools']])
        self.assertTrue(plan['proposed_calls'][0]['confirmation_required'])


if __name__ == '__main__':
    unittest.main()
