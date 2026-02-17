import './styles.css';
import { buildConfirmGrant, requiresConfirmation } from './confirm_policy.js';
import {
    DEFAULT_SETTINGS,
    SETTINGS_KEY,
    parseSettings,
    sanitizeSettings,
    serializeSettings
} from './settings_store.js';
import { applySkin } from './skins.js';
import { reduceUiState, UI_STATES } from './state_machine.js';

const state = {
    socket: null,
    authOk: false,
    heartbeatTimer: null,
    panelOpen: true,
    uiState: UI_STATES.ERROR,
    pendingPlan: null,
    settings: { ...DEFAULT_SETTINGS },
    drag: {
        active: false,
        moved: false,
        startX: 0,
        startY: 0,
        baseX: 24,
        baseY: 24
    }
};

const root = document.querySelector('.shell');
root.innerHTML = `
    <div id="widget" class="widget" style="left: 24px; top: 24px;">
        <button id="avatar" class="avatar" type="button" aria-label="Toggle chat panel">Deskling</button>
        <section id="panel" class="panel panel--open">
            <header class="panel__header">
                <h1>Deskling</h1>
                <div class="panel__status">
                    <span id="mode" class="mode mode--error">error</span>
                    <span id="status" class="status status--down">disconnected</span>
                    <button id="settings-toggle" class="settings-toggle" type="button">Settings</button>
                </div>
            </header>
            <p class="panel__subtitle">Typed chat slice: desktop-ui -> ipc-hub -> agent-core</p>
            <section id="chat" class="chat" aria-live="polite"></section>
            <form id="composer" class="composer">
                <input id="prompt" type="text" placeholder="Type a message" autocomplete="off" />
                <button type="submit">Send</button>
            </form>
            <section id="settings-panel" class="settings settings--hidden">
                <label>
                    Audio Device
                    <select id="settings-audio">
                        <option value="default">Default</option>
                        <option value="usb-mic">USB Mic</option>
                        <option value="line-in">Line In</option>
                    </select>
                </label>
                <label>
                    Model Path
                    <input id="settings-model-path" type="text" placeholder="/models/llm/default" />
                </label>
                <label>
                    Voice
                    <select id="settings-voice">
                        <option value="piper:en_US-amy-medium">Amy (EN)</option>
                        <option value="piper:en_US-kathleen-low">Kathleen (EN)</option>
                        <option value="piper:fr_FR-tom-medium">Tom (FR)</option>
                    </select>
                </label>
                <label>
                    Skin
                    <select id="settings-skin">
                        <option value="default_skin">Default</option>
                        <option value="mint_wave">Mint Wave</option>
                        <option value="ember_dawn">Ember Dawn</option>
                    </select>
                </label>
                <button id="settings-save" type="button">Save Settings</button>
            </section>
            <aside id="confirm-dialog" class="confirm confirm--hidden">
                <h2>Confirm Action</h2>
                <p id="confirm-summary">A risky tool action requires confirmation.</p>
                <ul id="confirm-tools"></ul>
                <div class="confirm__actions">
                    <button id="confirm-approve" type="button">Approve</button>
                    <button id="confirm-reject" type="button">Reject</button>
                </div>
            </aside>
        </section>
    </div>
`;

const widgetEl = document.getElementById('widget');
const avatarEl = document.getElementById('avatar');
const panelEl = document.getElementById('panel');
const modeEl = document.getElementById('mode');
const statusEl = document.getElementById('status');
const chatEl = document.getElementById('chat');
const composerEl = document.getElementById('composer');
const promptEl = document.getElementById('prompt');
const confirmDialogEl = document.getElementById('confirm-dialog');
const confirmSummaryEl = document.getElementById('confirm-summary');
const confirmToolsEl = document.getElementById('confirm-tools');
const confirmApproveEl = document.getElementById('confirm-approve');
const confirmRejectEl = document.getElementById('confirm-reject');
const settingsToggleEl = document.getElementById('settings-toggle');
const settingsPanelEl = document.getElementById('settings-panel');
const settingsAudioEl = document.getElementById('settings-audio');
const settingsModelPathEl = document.getElementById('settings-model-path');
const settingsVoiceEl = document.getElementById('settings-voice');
const settingsSkinEl = document.getElementById('settings-skin');
const settingsSaveEl = document.getElementById('settings-save');

function newId() {
    return crypto.randomUUID().replaceAll('-', '');
}

function nowIso() {
    return new Date().toISOString();
}

function setStatus(online, text) {
    statusEl.textContent = text;
    statusEl.className = `status ${online ? 'status--up' : 'status--down'}`;
}

function setUiState(eventName) {
    state.uiState = reduceUiState(state.uiState, eventName);
    modeEl.textContent = state.uiState;
    modeEl.className = `mode mode--${state.uiState}`;
}

function appendMessage(role, text) {
    const item = document.createElement('article');
    item.className = `msg msg--${role}`;
    item.textContent = text;
    chatEl.appendChild(item);
    chatEl.scrollTop = chatEl.scrollHeight;
}

function openConfirmDialog(plan) {
    state.pendingPlan = plan;
    confirmSummaryEl.textContent = plan?.summary || 'Risky tool actions are proposed.';
    confirmToolsEl.innerHTML = '';

    const tools = Array.isArray(plan?.proposed_tools) ? plan.proposed_tools : [];
    for (const tool of tools) {
        const row = document.createElement('li');
        row.textContent = `${tool?.name || 'unknown.tool'} (${tool?.risk || 'unknown'})`;
        confirmToolsEl.appendChild(row);
    }

    confirmDialogEl.classList.remove('confirm--hidden');
}

function closeConfirmDialog() {
    state.pendingPlan = null;
    confirmDialogEl.classList.add('confirm--hidden');
}

function readSettingsFromUi() {
    return sanitizeSettings({
        audio_device: settingsAudioEl.value,
        model_path: settingsModelPathEl.value,
        voice: settingsVoiceEl.value,
        skin_id: settingsSkinEl.value
    });
}

function writeSettingsToUi(settings) {
    settingsAudioEl.value = settings.audio_device;
    settingsModelPathEl.value = settings.model_path;
    settingsVoiceEl.value = settings.voice;
    settingsSkinEl.value = settings.skin_id;
    applySkin(settings.skin_id);
}

function loadSettings() {
    const raw = window.localStorage.getItem(SETTINGS_KEY);
    const parsed = raw ? parseSettings(raw) : { ...DEFAULT_SETTINGS };
    state.settings = parsed;
    writeSettingsToUi(parsed);
}

function saveSettings() {
    state.settings = readSettingsFromUi();
    const appliedSkin = applySkin(state.settings.skin_id);
    state.settings.skin_id = appliedSkin;
    window.localStorage.setItem(SETTINGS_KEY, serializeSettings(state.settings));
    appendMessage('system', 'settings saved');
}

function buildEnvelope(topic, target, payload, traceId, replyTo = null) {
    return {
        v: 1,
        id: newId(),
        ts: nowIso(),
        from: 'desktop-ui',
        to: target,
        topic,
        reply_to: replyTo,
        trace_id: traceId,
        payload
    };
}

function connect() {
    const socket = new WebSocket('ws://127.0.0.1:17171/ws');
    state.socket = socket;

    socket.addEventListener('open', () => {
        setUiState('SOCKET_OPEN');
        setStatus(true, 'connected');
        const traceId = newId();
        socket.send(
            JSON.stringify(
                buildEnvelope('auth.hello', 'ipc-hub', { service: 'desktop-ui', token: 'dev-token' }, traceId)
            )
        );

        state.heartbeatTimer = window.setInterval(() => {
            if (state.socket && state.socket.readyState === WebSocket.OPEN) {
                state.socket.send(JSON.stringify(buildEnvelope('hb.ping', 'ipc-hub', { source: 'desktop-ui' }, newId())));
            }
        }, 5000);
    });

    socket.addEventListener('message', (event) => {
        const envelope = JSON.parse(event.data);

        if (envelope.topic === 'auth.ok') {
            setUiState('AUTH_OK');
            state.authOk = true;
            appendMessage('system', 'ipc-hub auth successful');
            return;
        }

        if (envelope.topic === 'chat.assistant_message') {
            setUiState('ASSISTANT_MESSAGE');
            appendMessage('assistant', envelope.payload?.text ?? '[empty reply]');
            return;
        }

        if (envelope.topic === 'chat.assistant_plan') {
            const plan = envelope.payload || {};
            appendMessage('system', plan.summary || 'assistant proposed a tool plan');
            if (requiresConfirmation(plan)) {
                openConfirmDialog(plan);
            }
            return;
        }

        if (envelope.topic === 'ipc.error') {
            appendMessage('system', `ipc error: ${envelope.payload?.code ?? 'unknown'}`);
        }
    });

    socket.addEventListener('close', () => {
        setUiState('SOCKET_CLOSE');
        setStatus(false, 'disconnected');
        state.authOk = false;
        if (state.heartbeatTimer) {
            window.clearInterval(state.heartbeatTimer);
            state.heartbeatTimer = null;
        }
        appendMessage('system', 'connection closed, retrying in 1.5s');
        window.setTimeout(connect, 1500);
    });

    socket.addEventListener('error', () => {
        setUiState('SOCKET_ERROR');
        setStatus(false, 'error');
    });
}

function togglePanel() {
    state.panelOpen = !state.panelOpen;
    panelEl.classList.toggle('panel--open', state.panelOpen);
    panelEl.classList.toggle('panel--closed', !state.panelOpen);
}

function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
}

function onDragStart(event) {
    state.drag.active = true;
    state.drag.moved = false;
    state.drag.startX = event.clientX;
    state.drag.startY = event.clientY;
    widgetEl.setPointerCapture(event.pointerId);
}

function onDragMove(event) {
    if (!state.drag.active) {
        return;
    }

    const dx = event.clientX - state.drag.startX;
    const dy = event.clientY - state.drag.startY;

    if (Math.abs(dx) > 3 || Math.abs(dy) > 3) {
        state.drag.moved = true;
    }

    const maxX = window.innerWidth - widgetEl.offsetWidth - 8;
    const maxY = window.innerHeight - avatarEl.offsetHeight - 8;

    const nextX = clamp(state.drag.baseX + dx, 8, Math.max(8, maxX));
    const nextY = clamp(state.drag.baseY + dy, 8, Math.max(8, maxY));

    widgetEl.style.left = `${nextX}px`;
    widgetEl.style.top = `${nextY}px`;
}

function onDragEnd(event) {
    if (!state.drag.active) {
        return;
    }

    const rect = widgetEl.getBoundingClientRect();
    state.drag.baseX = rect.left;
    state.drag.baseY = rect.top;
    state.drag.active = false;
    widgetEl.releasePointerCapture(event.pointerId);
}

avatarEl.addEventListener('pointerdown', onDragStart);
avatarEl.addEventListener('pointermove', onDragMove);
avatarEl.addEventListener('pointerup', (event) => {
    const moved = state.drag.moved;
    onDragEnd(event);
    if (!moved) {
        togglePanel();
    }
});
avatarEl.addEventListener('pointercancel', onDragEnd);

composerEl.addEventListener('submit', (event) => {
    event.preventDefault();

    const text = promptEl.value.trim();
    if (!text) {
        return;
    }

    if (!state.socket || state.socket.readyState !== WebSocket.OPEN || !state.authOk) {
        appendMessage('system', 'not connected to ipc-hub yet');
        return;
    }

    const traceId = newId();
    setUiState('USER_MESSAGE_SENT');
    state.socket.send(JSON.stringify(buildEnvelope('chat.user_message', 'agent-core', { text }, traceId)));
    appendMessage('user', text);
    promptEl.value = '';
});

appendMessage('system', 'connecting to ipc-hub...');
loadSettings();
connect();

confirmApproveEl.addEventListener('click', () => {
    if (!state.pendingPlan || !state.socket || state.socket.readyState !== WebSocket.OPEN) {
        closeConfirmDialog();
        return;
    }

    setUiState('TOOL_EXECUTE_START');
    const traceId = newId();
    const payload = buildConfirmGrant(state.pendingPlan, traceId);
    state.socket.send(JSON.stringify(buildEnvelope('confirm.grant', 'agent-core', payload, traceId)));
    appendMessage('system', 'confirmation granted');
    closeConfirmDialog();
});

confirmRejectEl.addEventListener('click', () => {
    appendMessage('system', 'confirmation rejected');
    closeConfirmDialog();
});

settingsToggleEl.addEventListener('click', () => {
    settingsPanelEl.classList.toggle('settings--hidden');
});

settingsSaveEl.addEventListener('click', () => {
    saveSettings();
});
