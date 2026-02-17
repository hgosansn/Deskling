import assert from 'node:assert/strict';
import {
    DEFAULT_SETTINGS,
    parseSettings,
    sanitizeSettings,
    serializeSettings
} from './settings_store.js';

assert.deepEqual(sanitizeSettings({}), DEFAULT_SETTINGS);
assert.deepEqual(
    sanitizeSettings({
        audio_device: 'usb mic',
        model_path: '/opt/models/llama',
        voice: 'piper:en_US-kathleen',
        skin_id: 'mint_wave'
    }),
    {
        audio_device: 'usb mic',
        model_path: '/opt/models/llama',
        voice: 'piper:en_US-kathleen',
        skin_id: 'mint_wave'
    }
);

assert.deepEqual(parseSettings('{"audio_device":"mic-a","model_path":"/m","voice":"v"}'), {
    audio_device: 'mic-a',
    model_path: '/m',
    voice: 'v',
    skin_id: DEFAULT_SETTINGS.skin_id
});

assert.deepEqual(parseSettings('not-json'), DEFAULT_SETTINGS);

const serialized = serializeSettings({ audio_device: 'line-in' });
assert.equal(JSON.parse(serialized).audio_device, 'line-in');
assert.equal(JSON.parse(serialized).voice, DEFAULT_SETTINGS.voice);

console.log('settings store tests passed');
