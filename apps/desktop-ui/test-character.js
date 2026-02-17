const fs = require('fs');
const path = require('path');

console.log('✓ Checking character demo files...');

// Check main-character.js exists
if (!fs.existsSync('main-character.js')) {
  console.error('✗ main-character.js not found');
  process.exit(1);
}
console.log('✓ main-character.js exists');

// Check renderer/character.html exists
if (!fs.existsSync('renderer/character.html')) {
  console.error('✗ renderer/character.html not found');
  process.exit(1);
}
console.log('✓ renderer/character.html exists');

// Check HTML contains stickman SVG
const html = fs.readFileSync('renderer/character.html', 'utf8');
if (!html.includes('stickman') || !html.includes('svg')) {
  console.error('✗ character.html missing stickman SVG');
  process.exit(1);
}
console.log('✓ character.html contains stickman SVG');

// Check HTML has speech bubble
if (!html.includes('speech-bubble')) {
  console.error('✗ character.html missing speech bubble');
  process.exit(1);
}
console.log('✓ character.html has speech bubble');

// Check HTML has dragging support
if (!html.includes('-webkit-app-region: drag')) {
  console.error('✗ character.html missing drag support');
  process.exit(1);
}
console.log('✓ character.html has drag support');

// Check main-character.js has required Electron setup
const mainJs = fs.readFileSync('main-character.js', 'utf8');
if (!mainJs.includes('transparent: true') || !mainJs.includes('alwaysOnTop: true')) {
  console.error('✗ main-character.js missing window configuration');
  process.exit(1);
}
console.log('✓ main-character.js has proper window setup');

// Check package.json has character script
const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
if (!pkg.scripts.character) {
  console.error('✗ package.json missing character script');
  process.exit(1);
}
console.log('✓ package.json has character command');

console.log('\n✅ All character demo files are properly configured!');
