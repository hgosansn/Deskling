#!/usr/bin/env python3
"""
Capture demo screenshots of the Deskling Desktop UI.
Uses Playwright to render the Electron app UI in a browser for screenshot capture.
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ Playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)


async def capture_ui_screenshots(output_dir: str):
    """Capture screenshots of the Desktop UI."""
    
    # Since we can't easily launch Electron in headless mode in CI,
    # we'll create a browser-based version of the UI for screenshot purposes
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 400, 'height': 600},
            device_scale_factor=2  # Retina display
        )
        
        page = await context.new_page()
        
        # Load the renderer HTML (we'll need to serve it or create a test page)
        ui_html_path = Path(__file__).parent.parent / "apps" / "desktop-ui" / "renderer" / "index.html"
        
        if not ui_html_path.exists():
            print(f"❌ UI HTML not found at {ui_html_path}")
            await browser.close()
            return
        
        # Create a standalone version for screenshot
        standalone_html = create_standalone_ui_html(ui_html_path)
        test_html_path = Path(output_dir) / "test_ui.html"
        test_html_path.write_text(standalone_html)
        
        # Load the page
        await page.goto(f"file://{test_html_path.absolute()}")
        
        # Wait for page to load
        await page.wait_for_timeout(1000)
        
        # Screenshot 1: Initial idle state
        print("  📸 Capturing idle state...")
        await page.screenshot(path=os.path.join(output_dir, "01-idle-state.png"))
        
        # Screenshot 2: Simulate typing a message
        print("  📸 Capturing with user message...")
        await page.fill('#input-box', 'Hello, can you help me?')
        await page.wait_for_timeout(500)
        await page.screenshot(path=os.path.join(output_dir, "02-user-typing.png"))
        
        # Screenshot 3: Simulate clicking send
        print("  📸 Capturing after send...")
        await page.evaluate("""
            // Add user message
            const chatArea = document.getElementById('chat-area');
            const msg = document.createElement('div');
            msg.className = 'message user';
            msg.textContent = 'Hello, can you help me?';
            chatArea.appendChild(msg);
            document.getElementById('input-box').value = '';
        """)
        await page.wait_for_timeout(500)
        await page.screenshot(path=os.path.join(output_dir, "03-user-message-sent.png"))
        
        # Screenshot 4: Simulate assistant response
        print("  📸 Capturing assistant response...")
        await page.evaluate("""
            const chatArea = document.getElementById('chat-area');
            const msg = document.createElement('div');
            msg.className = 'message assistant';
            msg.textContent = "I'm here to help! I can assist with clipboard operations, notifications, file management, and browser automation. What would you like to do?";
            chatArea.appendChild(msg);
            chatArea.scrollTop = chatArea.scrollHeight;
        """)
        await page.wait_for_timeout(500)
        await page.screenshot(path=os.path.join(output_dir, "04-assistant-response.png"))
        
        # Screenshot 5: Simulate a plan with confirmation
        print("  📸 Capturing plan with confirmation...")
        await page.evaluate("""
            const chatArea = document.getElementById('chat-area');
            
            // Add user message
            const userMsg = document.createElement('div');
            userMsg.className = 'message user';
            userMsg.textContent = 'Send me a notification';
            chatArea.appendChild(userMsg);
            
            // Add plan box
            const planDiv = document.createElement('div');
            planDiv.className = 'plan-box';
            planDiv.innerHTML = `
                <h4>Plan:</h4>
                <p>I'll help you with that. I plan to: send desktop notification.</p>
                <div style="margin-top: 8px;">
                    <div class="plan-step">1. Send desktop notification <span style="color: #4CAF50">[low]</span></div>
                </div>
                <div class="confirm-buttons">
                    <button class="approve">Approve</button>
                    <button class="deny">Deny</button>
                </div>
            `;
            chatArea.appendChild(planDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        """)
        await page.wait_for_timeout(500)
        await page.screenshot(path=os.path.join(output_dir, "05-plan-with-confirmation.png"))
        
        # Screenshot 6: Different risk level example
        print("  📸 Capturing medium-risk action...")
        await page.evaluate("""
            // Clear and show medium risk example
            const chatArea = document.getElementById('chat-area');
            
            const userMsg = document.createElement('div');
            userMsg.className = 'message user';
            userMsg.textContent = 'Write a test file';
            chatArea.appendChild(userMsg);
            
            const planDiv = document.createElement('div');
            planDiv.className = 'plan-box';
            planDiv.innerHTML = `
                <h4>Plan:</h4>
                <p>I'll help you with that. I plan to: write to file.</p>
                <div style="margin-top: 8px;">
                    <div class="plan-step">1. Write to file <span style="color: #FFC107">[medium]</span></div>
                </div>
                <div class="confirm-buttons">
                    <button class="approve">Approve</button>
                    <button class="deny">Deny</button>
                </div>
            `;
            chatArea.appendChild(planDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        """)
        await page.wait_for_timeout(500)
        await page.screenshot(path=os.path.join(output_dir, "06-medium-risk-action.png"))
        
        # Clean up
        await browser.close()
        test_html_path.unlink()  # Remove temporary HTML file
        
        print(f"\n✅ Captured 6 screenshots in {output_dir}")


def create_standalone_ui_html(original_html_path: Path) -> str:
    """Create a standalone HTML file that doesn't require Electron."""
    
    html_content = original_html_path.read_text()
    
    # Replace Electron require with a mock
    standalone_html = html_content.replace(
        "const { ipcRenderer } = require('electron');",
        """
        // Mock ipcRenderer for standalone mode
        const ipcRenderer = {
            send: (channel, data) => console.log('Mock send:', channel, data),
            on: (channel, callback) => console.log('Mock on:', channel)
        };
        """
    )
    
    return standalone_html


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 capture_demo.py <output_directory>")
        sys.exit(1)
    
    output_dir = sys.argv[1]
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"📸 Capturing Deskling UI screenshots...")
    print(f"Output directory: {output_dir}\n")
    
    # Run async screenshot capture
    asyncio.run(capture_ui_screenshots(output_dir))


if __name__ == "__main__":
    main()
