#!/usr/bin/env python3
import os
import subprocess
import platform
import sys
from pathlib import Path
import time

class Colors:
    # Only use colors if the system supports it
    if sys.stdout.isatty() and platform.system() != 'Windows':
        HEADER = '\033[95m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
    else:
        HEADER = ''
        BLUE = ''
        GREEN = ''
        YELLOW = ''
        RED = ''
        ENDC = ''
        BOLD = ''

def clear_screen():
    if sys.stdout.isatty():  # Only clear if running in a terminal
        os.system('cls' if platform.system() == 'Windows' else 'clear')

def print_header():
    print("\n" + "="*40)
    print("    Directory Scanner Setup")
    print("="*40 + "\n")

def print_step(step, message):
    print(f"[{step}] {message}")

def print_success(message):
    print(f"SUCCESS: {message}")

def print_error(message):
    print(f"ERROR: {message}")

def print_warning(message):
    print(f"WARNING: {message}")

def get_user_input(prompt, default=None):
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    
    try:
        value = input(prompt).strip()
        return value if value else default
    except EOFError:
        return default

def create_venv():
    """Create virtual environment if it doesn't exist."""
    try:
        if not Path('venv').exists():
            print_step("1/4", "Creating virtual environment...")
            subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
            print_success("Virtual environment created successfully")
        else:
            print_warning("Virtual environment already exists, skipping creation")
        
        # Determine the correct pip and python commands
        pip_cmd = 'venv/Scripts/pip.exe' if platform.system() == 'Windows' else 'venv/bin/pip'
        
        print_step("2/4", "Installing required packages...")
        result = subprocess.run([pip_cmd, 'install', '-r', 'requirements.txt'], 
                              capture_output=True, 
                              text=True)
        
        if result.returncode == 0:
            print_success("Packages installed successfully")
            return True
        else:
            print_error(f"Failed to install packages: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to set up virtual environment: {str(e)}")
        return False
    except Exception as e:
        print_error(f"An unexpected error occurred: {str(e)}")
        return False

def setup_config(use_emojis=True):
    """Create default config if it doesn't exist."""
    try:
        print_step("3/4", "Creating configuration file...")
        
        config_path = Path('config.yaml')
        if config_path.exists():
            overwrite = get_user_input("Configuration file already exists. Overwrite? (y/n)", "n")
            if overwrite.lower() != 'y':
                print_warning("Keeping existing configuration file")
                return True

        default_config = f"""# Scanner Configuration
use_emojis: {str(use_emojis).lower()}

# Files and directories to ignore
ignore_patterns:
    exact_names:
        - ".git"
        - ".venv"
        - "venv"
        - "__pycache__"
        - "node_modules"
        - ".idea"
        - ".vscode"
        - "build"
        - "dist"
        - ".DS_Store"
        - "Thumbs.db"
        - ".pytest_cache"
        - ".coverage"
        - "htmlcov"
        - ".env"
        - ".env.local"
        - ".env.*.local"
        - "cache"
        - ".cache"
        - ".next"
        
    extensions:
        - ".pyc"
        - ".pyo"
        - ".pyd"
        - ".so"
        - ".dll"
        - ".dylib"
        - ".egg"
        - ".egg-info"
        - ".coverage"
        - ".pytest_cache"
        - ".DS_Store"
        - ".env"
        - ".log"
        - ".pot"
        - ".pyc"
        - ".pyo"
        - ".pyd"
        - ".swp"
        - ".swo"
        - "~"
        
    patterns:
        - "*.egg-info/*"
        - "*.egg/*"
        - "*.pytest_cache/*"
        - "*__pycache__*"
        - "*.git/*"
        - "*venv/*"
        - "*.idea/*"
        - "*.vscode/*"
        - "*node_modules/*"
        - "*build/*"
        - "*dist/*"
        - "*.env"
        - "*.env.*"
        - "*coverage/*"
        - "*.coverage"
        - "*htmlcov/*"
        - "*cache/*"
        - "*.cache/*"
        - "*.next/*"
        
    containing:
        - ".git"
        - "venv"
        - "__pycache__"
        - "node_modules"
        - ".idea"
        - ".vscode"
        - "build"
        - "dist"
        - ".env"
        - "coverage"
        - "htmlcov"
        - ".pytest_cache"
        - "cache"
        - ".cache"
        - ".next"

# Output file name
output_file: "directory-structure.md"
"""
        # Write the config file
        config_path.write_text(default_config)
        print_success("Configuration file created successfully")
        return True
        
    except Exception as e:
        print_error(f"Failed to create configuration file: {str(e)}")
        return False

def print_final_instructions():
    """Print final instructions for using the scanner."""
    print("\n" + "="*60)
    print("🎉 Setup Complete! Getting Started:")
    print("="*60)
    
    print("\n📌 Running the Scanner:")
    print("   Simply run:")
    print("   python scanner.py")
    
    print("\n🔄 The scanner will automatically:")
    print("   1. Create/activate virtual environment if needed")
    print("   2. Install required dependencies")
    print("   3. Generate directory structure")
    print("   4. Monitor for changes")
    print("   5. Deactivate virtual environment on exit")
    
    print("\n⌨️  Controls:")
    print("   • Press Ctrl+C to stop the scanner")
    print("   • The virtual environment will be handled automatically")
    
    print("\n⚙️  Configuration:")
    print("   • Edit config.yaml to customize ignore patterns")
    print("   • The scanner will create directory-structure.md in your project root")
    
    print("\n🔍 Status Indicators:")
    print("   • The scanner will show when virtual environment is active")
    print("   • You'll see real-time monitoring status")
    print("   • Clear messages will show when starting and stopping")
    
    print("\n❓ Need help?")
    print("   • Check README.md for detailed instructions")
    print("   • Report issues on the project repository")
    
    print("\n💡 Quick Start:")
    print("   python scanner.py")
    
    print("\n" + "="*60)
    print("Ready to scan! Run the command above to start monitoring.")
    print("="*60 + "\n")

def main():
    try:
        clear_screen()
        print_header()
        
        print("Welcome to Directory Scanner Setup!")
        print("This will set up the directory scanner tool in your project.\n")
        
        # Get user preferences
        use_emojis = get_user_input("Use emojis in directory tree (y/n)", "y").lower() == 'y'
        
        # Perform installation steps with better error handling
        venv_success = create_venv()
        if not venv_success:
            print_error("Virtual environment setup failed")
            sys.exit(1)
            
        config_success = setup_config(use_emojis)
        if not config_success:
            print_error("Configuration setup failed")
            sys.exit(1)
            
        print_final_instructions()
        
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
