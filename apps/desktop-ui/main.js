/**
 * Deskling Desktop UI - Electron Main Process
 */

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const WebSocket = require('ws');

let mainWindow;
let ipcHubWs;
let authenticated = false;

// State machine states
const States = {
    IDLE: 'idle',
    LISTEN: 'listen',
    THINK: 'think',
    SPEAK: 'speak',
    RUN: 'run',
    ERROR: 'error'
};

let currentState = States.IDLE;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 400,
        height: 600,
        transparent: true,
        frame: false,
        alwaysOnTop: true,
        skipTaskbar: false,
        resizable: true,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    mainWindow.loadFile('renderer/index.html');

    // Open DevTools in development
    if (process.argv.includes('--dev')) {
        mainWindow.webContents.openDevTools({ mode: 'detach' });
    }

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

async function connectToIPCHub() {
    return new Promise((resolve, reject) => {
        console.log('🔌 Connecting to IPC Hub...');
        
        ipcHubWs = new WebSocket('ws://127.0.0.1:17171');

        ipcHubWs.on('open', () => {
            console.log('✅ Connected to IPC Hub');
            
            // Send auth.hello
            const authMsg = {
                v: 1,
                id: generateULID(),
                ts: new Date().toISOString(),
                from: 'desktop-ui',
                to: 'ipc-hub',
                topic: 'auth.hello',
                reply_to: null,
                trace_id: generateULID(),
                payload: {
                    service_name: 'desktop-ui',
                    capabilities: ['chat.user_message', 'confirm.grant'],
                    version: '0.1.0'
                }
            };
            
            ipcHubWs.send(JSON.stringify(authMsg));
        });

        ipcHubWs.on('message', (data) => {
            try {
                const msg = JSON.parse(data.toString());
                console.log('📨 Received:', msg.topic);
                
                if (msg.topic === 'auth.ok') {
                    authenticated = true;
                    console.log('✅ Authenticated to IPC Hub');
                    resolve();
                    
                    // Start heartbeat
                    setInterval(() => {
                        if (authenticated) {
                            sendHeartbeat();
                        }
                    }, 30000);
                    
                } else if (msg.topic === 'auth.error') {
                    console.error('❌ Auth error:', msg.payload.message);
                    reject(new Error(msg.payload.message));
                    
                } else if (msg.topic === 'chat.assistant_message') {
                    // Forward to renderer
                    if (mainWindow) {
                        mainWindow.webContents.send('assistant-message', msg.payload);
                    }
                    setState(States.IDLE);
                    
                } else if (msg.topic === 'chat.assistant_plan') {
                    // Show confirmation if needed
                    if (mainWindow) {
                        mainWindow.webContents.send('assistant-plan', msg.payload);
                    }
                    if (msg.payload.requires_confirmation) {
                        setState(States.IDLE);  // Wait for user confirmation
                    }
                }
                
            } catch (e) {
                console.error('Error handling message:', e);
            }
        });

        ipcHubWs.on('error', (error) => {
            console.error('WebSocket error:', error);
            reject(error);
        });

        ipcHubWs.on('close', () => {
            console.log('Disconnected from IPC Hub');
            authenticated = false;
        });
    });
}

function sendHeartbeat() {
    if (!ipcHubWs || ipcHubWs.readyState !== WebSocket.OPEN) return;
    
    const msg = {
        v: 1,
        id: generateULID(),
        ts: new Date().toISOString(),
        from: 'desktop-ui',
        to: 'ipc-hub',
        topic: 'hb.ping',
        reply_to: null,
        trace_id: generateULID(),
        payload: {}
    };
    
    ipcHubWs.send(JSON.stringify(msg));
}

function setState(newState) {
    currentState = newState;
    if (mainWindow) {
        mainWindow.webContents.send('state-change', newState);
    }
    console.log(`State: ${newState}`);
}

// IPC handlers from renderer
ipcMain.on('send-user-message', (event, text) => {
    if (!authenticated) {
        console.error('Not authenticated to IPC Hub');
        return;
    }
    
    setState(States.THINK);
    
    const msg = {
        v: 1,
        id: generateULID(),
        ts: new Date().toISOString(),
        from: 'desktop-ui',
        to: 'agent-core',
        topic: 'chat.user_message',
        reply_to: null,
        trace_id: generateULID(),
        payload: {
            text: text,
            context: {}
        }
    };
    
    ipcHubWs.send(JSON.stringify(msg));
});

ipcMain.on('grant-confirmation', (event, confirmToken) => {
    if (!authenticated) return;
    
    setState(States.RUN);
    
    const msg = {
        v: 1,
        id: generateULID(),
        ts: new Date().toISOString(),
        from: 'desktop-ui',
        to: 'agent-core',
        topic: 'confirm.grant',
        reply_to: null,
        trace_id: generateULID(),
        payload: {
            confirm_token: confirmToken
        }
    };
    
    ipcHubWs.send(JSON.stringify(msg));
});

// Simple ULID-like ID generator (simplified for demo)
function generateULID() {
    return Date.now().toString(36) + Math.random().toString(36).substring(2);
}

// App lifecycle
app.whenReady().then(async () => {
    createWindow();
    
    try {
        await connectToIPCHub();
        setState(States.IDLE);
    } catch (e) {
        console.error('Failed to connect to IPC Hub:', e);
        setState(States.ERROR);
    }

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('before-quit', () => {
    if (ipcHubWs) {
        ipcHubWs.close();
    }
});
