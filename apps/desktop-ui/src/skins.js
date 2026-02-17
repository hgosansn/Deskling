export const SKINS = Object.freeze({
    default_skin: {
        '--panel-bg': 'rgba(7, 14, 28, 0.82)',
        '--panel-border': 'rgba(238, 244, 255, 0.22)',
        '--accent': '#ff7a18'
    },
    mint_wave: {
        '--panel-bg': 'rgba(7, 28, 24, 0.82)',
        '--panel-border': 'rgba(187, 247, 208, 0.24)',
        '--accent': '#10b981'
    },
    ember_dawn: {
        '--panel-bg': 'rgba(38, 14, 8, 0.82)',
        '--panel-border': 'rgba(254, 215, 170, 0.26)',
        '--accent': '#fb923c'
    }
});

export function applySkin(skinId, style) {
    const target = style || document.documentElement.style;
    const skin = SKINS[skinId] || SKINS.default_skin;

    for (const [key, value] of Object.entries(skin)) {
        target.setProperty(key, value);
    }

    return Object.keys(SKINS).includes(skinId) ? skinId : 'default_skin';
}
