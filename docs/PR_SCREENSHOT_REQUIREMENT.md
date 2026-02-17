# PR Demo Screenshot Requirement

## Overview

All pull requests that modify UI components, services, or user-facing functionality **must include demo screenshots** showing the changes in action.

## Automated Screenshot Capture

Screenshots are automatically captured by the **PR Demo Screenshots** GitHub Actions workflow when you open or update a pull request.

### What Gets Captured

The workflow automatically captures 6 screenshots showing:

1. **Idle State** - Application ready for input
2. **User Input** - Typing a message in the chat interface
3. **Message Sent** - User message displayed in the chat
4. **Assistant Response** - AI assistant's reply
5. **Low-Risk Action** - Tool execution requiring simple approval (e.g., notification)
6. **Medium-Risk Action** - File operations requiring explicit confirmation

### How It Works

When you create or update a PR, the workflow:
1. Sets up the Python environment with all dependencies
2. Starts the IPC Hub and Agent Core services
3. Uses Playwright to render the Desktop UI in a headless browser
4. Captures screenshots of different interaction states
5. Uploads screenshots as workflow artifacts
6. Comments on the PR with links to the screenshots

## Manual Screenshot Capture

You can also capture screenshots locally for testing:

```bash
# Run the screenshot capture script
./scripts/capture_screenshots.sh

# Screenshots will be saved to demo-screenshots/
ls demo-screenshots/
```

## Viewing Screenshots

### In Pull Requests

Screenshots are posted as a comment on your PR by the GitHub Actions bot. The comment includes:
- Description of each screenshot
- Links to download the images from workflow artifacts

### Downloading from Artifacts

1. Go to the PR's "Checks" tab
2. Find the "PR Demo Screenshots" workflow run
3. Click on the workflow run
4. Scroll to "Artifacts" section
5. Download "demo-screenshots.zip"

## Requirements for PR Approval

✅ **Required**:
- PR must trigger the screenshot workflow (if UI/service changes are included)
- Workflow must complete successfully
- Screenshots must be available in artifacts

❌ **Not Required**:
- You don't need to manually add screenshots to the PR description
- Screenshots are not committed to the repository (they're in artifacts)

## Troubleshooting

### Workflow Fails

If the screenshot workflow fails:

1. Check the workflow logs for errors
2. Ensure all Python dependencies are properly listed in requirements.txt
3. Verify the UI HTML is valid and can be loaded
4. Test locally using `./scripts/capture_screenshots.sh`

### Screenshots Don't Show Expected Changes

If your UI changes aren't visible in screenshots:

1. The workflow captures the base UI states - you may need to customize `scripts/capture_demo.py` for specific scenarios
2. Add custom screenshot scenarios in `capture_demo.py` for your feature
3. Ensure your changes are in files watched by the workflow trigger

### Adding Custom Screenshot Scenarios

Edit `scripts/capture_demo.py` to add custom scenarios:

```python
# Example: Add a new screenshot scenario
print("  📸 Capturing my custom scenario...")
await page.evaluate("""
    // Your JavaScript to set up the scenario
    // Example: simulate a specific interaction
""")
await page.wait_for_timeout(500)
await page.screenshot(path=os.path.join(output_dir, "07-my-custom-scenario.png"))
```

## Benefits

- **Visual validation**: Reviewers can see the actual UI changes
- **Regression detection**: Compare screenshots across PRs to spot unintended changes
- **Documentation**: Screenshots serve as visual documentation of features
- **Consistency**: Automated capture ensures every PR has screenshots

## Workflow Configuration

The workflow is triggered on:
- Pull request opened
- Pull request synchronized (new commits)
- Pull request reopened

For files in:
- `apps/desktop-ui/**`
- `apps/ipc-hub/**`
- `services/agent-core/**`
- `services/automation-service/**`
- `shared/**`
- Screenshot scripts themselves

## Future Enhancements

Potential improvements:
- Visual regression testing (compare screenshots to baseline)
- Capture video recordings of interactions
- Test real Electron app (not just browser-based UI)
- Performance metrics alongside screenshots
- Mobile/responsive view screenshots

---

For questions or issues with the screenshot system, please open an issue with the `ci/cd` label.
