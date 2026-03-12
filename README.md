# Hebrew RTL Plugin

Automatically adds RTL (Right-to-Left) markers to Hebrew paragraphs in Claude Code for correct text display and formatting.

## What It Does

When you write or edit files in Hebrew, this plugin automatically:

1. **Detects paragraphs** that begin with Hebrew text
2. **Skips non-letter characters** (numbers, punctuation) to find the first actual letter
3. **Adds the U+202B (RLE) marker** to the start of Hebrew paragraphs
4. **Leaves English paragraphs untouched**

### Example

**Before:**
```
1. קטגוריה א
Some English text
```

**After (automatic):**
```
‫1. קטגוריה א
Some English text
```

The `‫` character ensures the Hebrew text displays in the correct direction.

## Installation

### Option 1: Install from this repository

```bash
# Clone the repository
git clone https://github.com/aviz85/hebrew-rtl-plugin.git

# Install as a user plugin
claude plugin install ./hebrew-rtl-plugin --scope user

# Or reload if already installed
/reload-plugins
```

### Option 2: Manual setup

1. Copy the plugin directory to `~/.claude/plugins/hebrew-rtl/`
2. In Claude Code, run: `/reload-plugins`
3. Verify it's active: `/plugin`

## How It Works

The plugin uses a **hook** that triggers on every `Write` or `Edit` action:

1. **Hook Event**: `PostToolUse` (after writing or editing a file)
2. **Matcher**: Targets `Write` and `Edit` operations
3. **Action**: Runs the Python fixer script on the file
4. **Result**: Adds RTL markers automatically

### Hook Configuration

The plugin includes `hooks.json` which defines:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/hebrew-rtl-fixer.py",
            "args": ["$FILE_PATH"]
          }
        ]
      }
    ]
  }
}
```

**Key elements:**
- `PostToolUse`: Hook fires after Write/Edit completes
- `matcher`: Applies to Write and Edit operations
- `$CLAUDE_PLUGIN_ROOT`: Plugin directory path (auto-resolved)
- `$FILE_PATH`: Path to the file that was edited

## File Structure

```
hebrew-rtl-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── hooks.json               # Hook definitions
├── scripts/
│   └── hebrew-rtl-fixer.py  # Python script that adds RTL markers
├── README.md                # This file
└── docs/
    ├── installation.html    # Web documentation
    └── architecture.md      # Technical details
```

## The RTL Fixer Script

**Location**: `scripts/hebrew-rtl-fixer.py`

**What it does:**
1. Reads a file
2. Splits into paragraphs
3. For each paragraph:
   - Finds the first letter (skipping numbers, spaces, punctuation)
   - Checks if it's Hebrew (Unicode range U+0590-U+05FF)
   - If Hebrew: adds U+202B at the beginning
   - If English: leaves it alone
4. Writes the file back

**Input/Output:**
```bash
# Modify file in place
python3 hebrew-rtl-fixer.py path/to/file.md

# Returns: ✓ Fixed Hebrew RTL markers in path/to/file.md
```

## Environment Variables

The hook uses these auto-provided variables:

| Variable | Meaning |
|----------|---------|
| `$CLAUDE_PLUGIN_ROOT` | Absolute path to the plugin directory |
| `$FILE_PATH` | Path to the file being written/edited |

## Troubleshooting

### Plugin not working?

1. **Check if enabled**: Run `/plugin` in Claude Code
2. **Reload**: Run `/reload-plugins`
3. **Verify path**: Check that the script is in `scripts/hebrew-rtl-fixer.py`
4. **Check logs**: Enable debug mode: `claude --debug`

### Script permission errors?

```bash
# Make the script executable
chmod +x ~/.claude/plugins/hebrew-rtl/scripts/hebrew-rtl-fixer.py
```

### RTL markers appearing in wrong places?

The plugin only adds markers to paragraphs that:
- Begin with Hebrew text (after skipping non-letters)
- Have actual content

English paragraphs are never modified.

## Development

### Testing locally

```bash
# Run Claude Code with the plugin directory
claude --plugin-dir ./hebrew-rtl-plugin

# In Claude Code
/reload-plugins
/plugin  # Should show hebrew-rtl as active
```

### Modifying the script

Edit `scripts/hebrew-rtl-fixer.py` and test:

```bash
# Test on a file
python3 scripts/hebrew-rtl-fixer.py test-file.md

# View the result
cat test-file.md
```

## Contributing

Found a bug or have an improvement? Open an issue on GitHub!

## License

MIT - Feel free to use and modify.

---

**Built by**: Aviz
**Repository**: https://github.com/aviz85/hebrew-rtl-plugin
**Documentation**: https://aviz85.github.io/hebrew-rtl-plugin/
