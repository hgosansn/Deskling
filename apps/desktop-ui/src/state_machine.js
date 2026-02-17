export const UI_STATES = Object.freeze({
    IDLE: 'idle',
    LISTEN: 'listen',
    THINK: 'think',
    SPEAK: 'speak',
    RUN: 'run',
    ERROR: 'error'
});

export function reduceUiState(currentState, eventName) {
    switch (eventName) {
        case 'SOCKET_OPEN':
        case 'AUTH_OK':
        case 'ASSISTANT_MESSAGE':
            return UI_STATES.IDLE;
        case 'USER_MESSAGE_SENT':
            return UI_STATES.THINK;
        case 'VOICE_CAPTURE_START':
            return UI_STATES.LISTEN;
        case 'VOICE_TTS_START':
            return UI_STATES.SPEAK;
        case 'TOOL_EXECUTE_START':
            return UI_STATES.RUN;
        case 'SOCKET_ERROR':
        case 'SOCKET_CLOSE':
            return UI_STATES.ERROR;
        default:
            return currentState;
    }
}
