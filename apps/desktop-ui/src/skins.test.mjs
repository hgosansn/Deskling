import assert from 'node:assert/strict';
import { SKINS, applySkin } from './skins.js';

const fakeStyle = {
    props: {},
    setProperty(key, value) {
        this.props[key] = value;
    }
};

const applied = applySkin('mint_wave', fakeStyle);
assert.equal(applied, 'mint_wave');
assert.equal(fakeStyle.props['--accent'], SKINS.mint_wave['--accent']);

const fallback = applySkin('unknown-skin', fakeStyle);
assert.equal(fallback, 'default_skin');
assert.equal(fakeStyle.props['--accent'], SKINS.default_skin['--accent']);

console.log('skin tests passed');
