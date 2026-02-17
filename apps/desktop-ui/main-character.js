/**
 * Deskling Character Demo - Standalone Electron Main Process
 * MVP: Simple draggable character with speech bubbles
 */

const { app, BrowserWindow } = require('electron');

let characterWindow;

function createCharacterWindow() {
    characterWindow = new BrowserWindow({
        width: 300,
        height: 400,
        transparent: true,
        frame: false,
        alwaysOnTop: true,
        skipTaskbar: false,
        resizable: false,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    // Load the character renderer
    characterWindow.loadFile('renderer/character.html');

    // Open DevTools in development
    if (process.argv.includes('--dev')) {
        characterWindow.webContents.openDevTools({ mode: 'detach' });
    }

    characterWindow.on('closed', () => {
        characterWindow = null;
    });
}

// App lifecycle
app.whenReady().then(() => {
    createCharacterWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createCharacterWindow();
        }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
