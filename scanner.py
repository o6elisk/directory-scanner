#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import fnmatch
from pathlib import Path
import atexit
import signal

def print_status(message, status="info"):
    """Print formatted status messages."""
    colors = {
        "success": "\033[92m",  # Green
        "info": "\033[94m",     # Blue
        "warning": "\033[93m",  # Yellow
        "error": "\033[91m",    # Red
        "end": "\033[0m"        # Reset
    }
    
    # Only use colors if terminal supports it
    if sys.stdout.isatty():
        print(f"{colors.get(status, '')}{message}{colors['end']}")
    else:
        print(message)

def ensure_venv():
    """Ensure virtual environment is active and dependencies are installed."""
    venv_path = Path('venv')
    requirements_path = Path('requirements.txt')
    
    # Check if we're already in a venv
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if not in_venv:
        print_status("🔄 Virtual environment not active, setting up...", "info")
        
        # Create venv if it doesn't exist
        if not venv_path.exists():
            print_status("📦 Creating virtual environment...", "info")
            subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
        
        # Determine the correct python and pip commands
        if os.name == 'nt':  # Windows
            python_path = venv_path / 'Scripts' / 'python.exe'
            pip_path = venv_path / 'Scripts' / 'pip.exe'
        else:  # Unix-like
            python_path = venv_path / 'bin' / 'python'
            pip_path = venv_path / 'bin' / 'pip'
        
        # Install requirements if needed
        if requirements_path.exists():
            print_status("📥 Installing requirements...", "info")
            subprocess.run([str(pip_path), 'install', '-r', 'requirements.txt'], check=True)
        
        print_status("🔄 Restarting with virtual environment...", "info")
        os.execv(str(python_path), [str(python_path), __file__])
    else:
        print_status("✅ Virtual environment is active", "success")
        print_status(f"📍 Using Python from: {sys.executable}", "info")

def deactivate_venv():
    """Deactivate the virtual environment."""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("\nDeactivating virtual environment...")
        if os.name == 'nt':  # Windows
            subprocess.run(['deactivate'], shell=True)
        else:  # Unix-like
            subprocess.run(['deactivate'], shell=True)

# Register the deactivate function to run on normal exit and signals
atexit.register(deactivate_venv)
signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))
signal.signal(signal.SIGTERM, lambda x, y: sys.exit(0))

# Ensure venv is active before importing other dependencies
ensure_venv()

# Now import the dependencies that require venv
import yaml
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# File type to emoji mapping
FILE_ICONS = {
    # Programming Languages
    '.py': '🐍',
    '.js': '📜',
    '.ts': '📘',
    '.jsx': '⚛️',
    '.tsx': '⚛️',
    '.html': '🌐',
    '.css': '🎨',
    '.scss': '🎨',
    '.sass': '🎨',
    '.less': '🎨',
    '.php': '🐘',
    '.java': '☕',
    '.cpp': '⚙️',
    '.c': '⚙️',
    '.go': '🐹',
    '.rb': '💎',
    '.rs': '🦀',
    '.swift': '🍎',
    '.kt': '📱',
    
    # Data Files
    '.json': '📋',
    '.yaml': '📋',
    '.yml': '📋',
    '.xml': '📋',
    '.csv': '📊',
    '.xls': '📊',
    '.xlsx': '📊',
    
    # Documentation
    '.md': '📝',
    '.txt': '📄',
    '.pdf': '📕',
    '.doc': '📘',
    '.docx': '📘',
    
    # Images
    '.jpg': '🖼️',
    '.jpeg': '🖼️',
    '.png': '🖼️',
    '.gif': '🖼️',
    '.svg': '🖼️',
    
    # Default
    '': '📄'
}

class DirectoryScanner:
    def __init__(self):
        self.config = self.load_config()
        self.root_dir = self.find_root_directory()
        self.ignore_patterns = self.config['ignore_patterns']
        self.output_file = self.config['output_file']
        self.use_emojis = str(self.config.get('use_emojis', 'true')).lower() == 'true'
        self.last_tree = ""

    def load_config(self):
        """Load configuration from config.yaml."""
        with open('config.yaml', 'r') as f:
            return yaml.safe_load(f)

    def find_root_directory(self):
        """Find the root directory by looking for common project markers."""
        current = Path.cwd()
        while current != current.parent:
            if any((current / marker).exists() for marker in ['.git', 'package.json', 'setup.py']):
                return current
            current = current.parent
        return Path.cwd()

    def should_ignore(self, path):
        """Enhanced ignore pattern checking."""
        try:
            path_str = str(path.relative_to(self.root_dir))
            
            # Get ignore patterns from config
            ignore_patterns = self.config.get('ignore_patterns', {})
            
            # Check exact names
            if path.name in ignore_patterns.get('exact_names', []):
                return True
                
            # Check file extensions
            if path.is_file():
                if any(path.name.endswith(ext) for ext in ignore_patterns.get('extensions', [])):
                    return True
                    
            # Check glob patterns
            for pattern in ignore_patterns.get('patterns', []):
                if fnmatch.fnmatch(path_str, pattern):
                    return True
                    
            # Check containing strings
            for contains in ignore_patterns.get('containing', []):
                if contains in path_str:
                    return True
                    
            return False
        except Exception as e:
            print(f"Error checking ignore patterns for {path}: {e}")
            return False

    def get_file_icon(self, path):
        """Get the appropriate emoji for a file."""
        if not self.use_emojis:
            return ''
            
        if path.is_dir():
            return '📁'
            
        # Check exact filename first
        if path.name in FILE_ICONS:
            return FILE_ICONS[path.name]
            
        # Check extension
        return FILE_ICONS.get(path.suffix.lower(), FILE_ICONS[''])

    def generate_tree(self):
        """Generate the directory tree structure with ASCII art and optional emojis."""
        tree = ["# Project Directory Structure\n"]
        
        def add_to_tree(directory, prefix="", is_last=True):
            entries = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
            entries = [e for e in entries if not self.should_ignore(e)]
            
            for i, entry in enumerate(entries):
                is_last_entry = i == len(entries) - 1
                
                # Create the branch graphics
                if is_last_entry:
                    branch = "└── "
                    new_prefix = prefix + "    "
                else:
                    branch = "├── "
                    new_prefix = prefix + "│   "
                
                # Get emoji if enabled
                emoji = self.get_file_icon(entry) + " " if self.use_emojis else ""
                
                # Add the entry to the tree
                tree.append(f"{prefix}{branch}{emoji}{entry.name}")
                
                # Recursively add subdirectories
                if entry.is_dir():
                    add_to_tree(entry, new_prefix, is_last_entry)
        
        add_to_tree(self.root_dir)
        return "\n".join(tree)

    def update_tree_file(self):
        """Update the directory structure file."""
        tree = self.generate_tree()
        if tree != self.last_tree:
            output_path = self.root_dir / self.output_file
            output_path.write_text(tree)
            print(f"Updated {self.output_file}")
            self.last_tree = tree

class DirectoryChangeHandler(FileSystemEventHandler):
    def __init__(self, scanner):
        self.scanner = scanner
        self.last_update = 0
        self.update_delay = 1  # seconds

    def on_any_event(self, event):
        current_time = time.time()
        if current_time - self.last_update >= self.update_delay:
            self.scanner.update_tree_file()
            self.last_update = current_time

def main():
    try:
        # Print a clear header
        print("\n" + "="*50)
        print_status("📁 Directory Scanner", "info")
        print("="*50 + "\n")
        
        # Show venv status
        print_status("🔍 Checking virtual environment...", "info")
        ensure_venv()
        
        scanner = DirectoryScanner()
        event_handler = DirectoryChangeHandler(scanner)
        observer = Observer()
        observer.schedule(event_handler, str(scanner.root_dir), recursive=True)
        observer.start()

        print("\n" + "-"*50)
        print_status(f"👀 Monitoring directory: {scanner.root_dir}", "success")
        print_status("⌨️  Press Ctrl+C to stop", "info")
        print("-"*50 + "\n")
        
        scanner.update_tree_file()  # Generate initial tree
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n" + "-"*50)
        print_status("🛑 Stopping directory scanner...", "warning")
        observer.stop()
        observer.join()
        print_status("✅ Virtual environment deactivated", "success")
        print("-"*50 + "\n")
    except Exception as e:
        print_status(f"❌ An error occurred: {e}", "error")
        observer.stop()
        observer.join()
    finally:
        # The deactivate function will be called automatically through atexit
        pass

if __name__ == "__main__":
    main()
