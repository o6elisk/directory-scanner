# Directory Scanner

A Python tool that automatically generates and maintains a live directory structure visualization in markdown format. The tool watches for file system changes and updates the directory structure documentation in real-time.

## Prerequisites

### All Systems
- Python 3.x (3.7 or higher recommended)

## Features

- 🔄 Real-time directory structure monitoring and updates
- 📝 Markdown-formatted output with ASCII tree structure
- 🎨 Optional emoji icons for different file types
- ⚙️ Comprehensive ignore patterns configuration
- 🎯 Automatic project root detection
- 🚀 Automatic virtual environment handling
- 🛡️ Cross-platform compatibility

## Installation

1. Clone the repository to your project's root directory (the directory you want scanned).
```bash
git clone https://github.com/obelisk/directory-scanner.git
```

2. Navigate into the directory and run the installation script:
```bash
cd directory-scanner
python install.py
```

This will:
- Create a virtual environment
- Install required dependencies
- Generate a default configuration file
- Prompt for emoji preference

## Usage

Simply run:
```bash
python scanner.py
```

The scanner will:
1. Automatically create/activate virtual environment if needed
2. Detect the project root directory
3. Generate an initial directory structure in `directory-structure.md` in your project root.
4. Start monitoring for changes
5. Automatically update the structure when changes occur
6. Deactivate virtual environment on exit

To stop the scanner, press `Ctrl+C`

## Configuration

The tool uses `config.yaml` for configuration. You can modify these settings:

```yaml
# Scanner Configuration
use_emojis: true  # Set to false for plain ASCII tree

# Files and directories to ignore
ignore_patterns:
    exact_names:
        - ".git"
        - "venv"
        - "cache"
        - ".next"
        # ... more exact names
        
    extensions:
        - ".pyc"
        - ".pyo"
        # ... more extensions
        
    patterns:
        - "*.egg-info/*"
        - "*cache/*"
        # ... more patterns
        
    containing:
        - ".git"
        - "cache"
        # ... more patterns

# Output file name
output_file: "directory-structure.md"
```

### Ignore Pattern Types
- `exact_names`: Exact file or directory names to ignore
- `extensions`: File extensions to ignore
- `patterns`: Glob patterns for more complex matching
- `containing`: Ignore paths containing these strings

## Output Format

### With Emojis (use_emojis: true)
```
# Project Directory Structure

├── 📁 app
│   ├── 📁 components
│   │   ├── ⚛️ header.tsx
│   │   └── ⚛️ footer.tsx
│   ├── 📁 pages
│   │   ├── ⚛️ index.tsx
│   │   └── ⚛️ about.tsx
│   └── 🎨 globals.css
├── 📁 public
│   ├── 🖼️ favicon.ico
│   └── 🖼️ logo.png
├── 📋 package.json
├── 📋 next.config.js
└── 📝 README.md
```

### Without Emojis (use_emojis: false)
```
# Project Directory Structure

├── app
│   ├── components
│   │   ├── header.tsx
│   │   └── footer.tsx
│   ├── pages
│   │   ├── index.tsx
│   │   └── about.tsx
│   └── globals.css
├── public
│   ├── favicon.ico
│   └── logo.png
├── package.json
├── next.config.js
└── README.md
```

## File Type Emojis

The scanner recognizes various file types and assigns appropriate emojis:

- 📁 Directories
- 🐍 Python files (.py)
- 📜 JavaScript files (.js)
- ⚛️ React files (.jsx, .tsx)
- 🌐 HTML files (.html)
- 🎨 Style files (.css, .scss)
- 📝 Markdown files (.md)
- 📋 Data files (.json, .yaml)
- 📊 Spreadsheets (.csv, .xlsx)
- 🖼️ Images (.jpg, .png, etc.)
- 📄 Default files

## Project Structure

```
your-project/               # Your actual project
└── directory-scanner/      # Our tool directory
    ├── install.py         # Installation and setup script
    ├── scanner.py        # Main scanner implementation
    ├── requirements.txt  # Python dependencies
    ├── config.yaml      # Configuration file
    └── .gitignore      # Git ignore patterns
```

## Troubleshooting

### Common Issues

1. **Module Not Found Errors**
   - The scanner will automatically handle virtual environment setup
   - If issues persist, try deleting the `venv` folder and running again

2. **Files Not Being Ignored**
   - Check your `config.yaml` file
   - Make sure the ignore pattern is in the correct section
   - Try adding the path to multiple ignore pattern types

3. **Permission Issues**
   - Ensure you have write permissions in the directory
   - Try running with elevated privileges if needed

4. **Virtual Environment Issues**
   - Delete the `venv` folder
   - Delete `config.yaml`
   - Run `python install.py` again for fresh setup

5. **Clean and Reinstall**
   ```bash
    rm -rf venv/ config.yaml directory-structure.md __pycache__/ *.pyc
    python install.py
   ```

## License

MIT License

## Author

[@obeliskk](https://x.com/o6eliskk)
