import assert from 'node:assert/strict';
import { reduceUiState, UI_STATES } from './state_machine.js';

assert.equal(reduceUiState(UI_STATES.IDLE, 'USER_MESSAGE_SENT'), UI_STATES.THINK);
assert.equal(reduceUiState(UI_STATES.THINK, 'ASSISTANT_MESSAGE'), UI_STATES.IDLE);
assert.equal(reduceUiState(UI_STATES.IDLE, 'VOICE_CAPTURE_START'), UI_STATES.LISTEN);
assert.equal(reduceUiState(UI_STATES.LISTEN, 'VOICE_TTS_START'), UI_STATES.SPEAK);
assert.equal(reduceUiState(UI_STATES.IDLE, 'TOOL_EXECUTE_START'), UI_STATES.RUN);
assert.equal(reduceUiState(UI_STATES.IDLE, 'SOCKET_ERROR'), UI_STATES.ERROR);
assert.equal(reduceUiState(UI_STATES.THINK, 'UNKNOWN_EVENT'), UI_STATES.THINK);

console.log('state machine tests passed');
