import assert from 'node:assert/strict';
import { buildConfirmGrant, requiresConfirmation } from './confirm_policy.js';

assert.equal(requiresConfirmation({ proposed_tools: [{ name: 'notify.send', risk: 'low' }] }), false);
assert.equal(requiresConfirmation({ proposed_tools: [{ name: 'files.write_text', risk: 'medium' }] }), true);
assert.equal(requiresConfirmation({ proposed_tools: [{ name: 'shell.run', risk: 'high' }] }), true);

const grant = buildConfirmGrant(
    {
        proposed_tools: [
            { name: 'files.write_text', risk: 'medium' },
            { name: 'browser.open_url', risk: 'low' }
        ]
    },
    'trace123'
);

assert.equal(grant.confirm_token, 'confirm_trace123');
assert.deepEqual(grant.tools, ['files.write_text', 'browser.open_url']);
assert.equal(grant.ttl_seconds, 60);
assert.equal(grant.decision, 'approved');

console.log('confirm policy tests passed');
