This folder contains workspace-level VS Code settings that minimize or disable editor autocomplete/autofill for this project so you can learn without suggestions.

What was changed
- `.vscode/settings.json` — disables quick suggestions, inline suggestions, parameter hints, and reduces language-server indexing/auto-search for Python in this workspace.

How to revert
1. Remove the workspace settings file (this will restore your global/editor defaults):

   rm .vscode/settings.json

2. Or, open VS Code Command Palette (⇧⌘P) → "Preferences: Open Workspace Settings (JSON)" and edit or remove any settings you don't want.

3. If you still see suggestions, some extensions (Pylance, Copilot, TabNine, etc.) may need to be disabled for this workspace. Open the Extensions view, right-click the extension, and choose "Disable (Workspace)".

Notes
- These settings are only for this workspace folder. Your global/user settings are not changed.
- If you'd like I can also try to add explicit workspace toggles for specific extensions you have installed — tell me which extensions to target and I can add recommended workspace entries or instructions.
