export const SETTINGS_KEY = 'deskling_ui_settings_v1';

export const DEFAULT_SETTINGS = Object.freeze({
    audio_device: 'default',
    model_path: '/models/llm/default',
    voice: 'piper:en_US-amy-medium',
    skin_id: 'default_skin'
});

function normalizeString(value, fallback) {
    if (typeof value !== 'string') {
        return fallback;
    }
    const trimmed = value.trim();
    return trimmed.length > 0 ? trimmed : fallback;
}

export function sanitizeSettings(input) {
    const source = input && typeof input === 'object' ? input : {};
    return {
        audio_device: normalizeString(source.audio_device, DEFAULT_SETTINGS.audio_device),
        model_path: normalizeString(source.model_path, DEFAULT_SETTINGS.model_path),
        voice: normalizeString(source.voice, DEFAULT_SETTINGS.voice),
        skin_id: normalizeString(source.skin_id, DEFAULT_SETTINGS.skin_id)
    };
}

export function parseSettings(raw) {
    try {
        return sanitizeSettings(JSON.parse(raw));
    } catch {
        return { ...DEFAULT_SETTINGS };
    }
}

export function serializeSettings(settings) {
    return JSON.stringify(sanitizeSettings(settings));
}
