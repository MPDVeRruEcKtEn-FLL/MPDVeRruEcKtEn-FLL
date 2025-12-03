"""
Upload library files to LEGO Spike Prime Hub using mpremote.

This script uploads DriveBase.py and Logger.py to the /flash/lib/ directory
on the LEGO hub, making them available for import in programs.
Uses a virtual environment for isolated mpremote installation.
"""

import subprocess
import sys
import os
import time


# Virtual environment path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(SCRIPT_DIR, '.venv')
VENV_PYTHON = os.path.join(VENV_DIR, 'Scripts' if os.name == 'nt' else 'bin', 'python')
VENV_MPREMOTE = os.path.join(VENV_DIR, 'Scripts' if os.name == 'nt' else 'bin', 'mpremote')


def ensure_venv() -> bool:
    """
    Ensure virtual environment exists and has mpremote installed.
    
    Returns:
        bool: True if venv is ready, False otherwise
    """
    # Create venv if it doesn't exist
    if not os.path.exists(VENV_DIR):
        print("Creating virtual environment...")
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'venv', VENV_DIR],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"✗ Failed to create virtual environment: {result.stderr}")
                return False
            print("✓ Virtual environment created")
        except Exception as e:
            print(f"✗ Error creating virtual environment: {e}")
            return False
    else:
        print("✓ Virtual environment exists")
    
    # Check if mpremote is installed in venv
    if os.path.exists(VENV_MPREMOTE):
        print("✓ mpremote is installed in virtual environment")
        return True
    
    print("Installing mpremote in virtual environment...")
    try:
        install_result = subprocess.run(
            [VENV_PYTHON, '-m', 'pip', 'install', 'mpremote'],
            capture_output=True,
            text=True
        )
        
        if install_result.returncode == 0:
            print("✓ mpremote installed successfully in virtual environment!")
            return True
        else:
            print(f"✗ Installation failed: {install_result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error during installation: {e}")
        return False


def test_connection() -> bool:
    """
    Test connection to the LEGO hub.
    
    Returns:
        bool: True if connected, False otherwise
    """
    result = subprocess.run(
        [VENV_MPREMOTE, 'exec', "print('Connected')"],
        capture_output=True,
        text=True
    )
    return result.returncode == 0


def soft_reset() -> None:
    """
    Perform a reset on the hub to exit REPL mode and return to normal operation.
    This prevents the hub from staying in an interactive state after mpremote commands.
    """
    try:
        subprocess.run(
            [VENV_MPREMOTE, 'reset'],
            capture_output=True,
            text=True,
            timeout=3
        )
        # Give the hub a moment to reset
        time.sleep(1.5)
    except subprocess.TimeoutExpired:
        # Timeout is expected as the connection drops during reset
        pass
    except Exception:
        # Ignore errors during reset
        pass


def upload_libraries() -> bool:
    """
    Upload DriveBase.py and Logger.py to /flash/lib/ on the LEGO hub.
    
    Returns:
        bool: True if successful, False otherwise
    """
    drivebase_path = os.path.join(SCRIPT_DIR, 'DriveBase.py')
    logger_path = os.path.join(SCRIPT_DIR, 'Logger.py')
    
    # Verify files exist
    if not os.path.exists(drivebase_path):
        print(f"✗ Error: DriveBase.py not found at {drivebase_path}")
        return False
    
    if not os.path.exists(logger_path):
        print(f"✗ Error: Logger.py not found at {logger_path}")
        return False
    
    print("Uploading libraries to LEGO hub...")
    
    # Create /flash/lib directory and upload files
    commands = [
        VENV_MPREMOTE,
        'exec', "import os\ntry:\n    os.mkdir('/flash/lib')\nexcept OSError:\n    pass",
        '+',
        'cp', drivebase_path, ':/flash/lib/DriveBase.py',
        '+',
        'cp', logger_path, ':/flash/lib/Logger.py'
    ]
    
    result = subprocess.run(commands, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ DriveBase.py uploaded successfully")
        print("✓ Logger.py uploaded successfully")
        
        # Soft reset to exit REPL mode
        print("\nResetting hub to normal operation mode...")
        soft_reset()
        print("✓ Hub reset complete")
        
        print("\nLibraries can now be imported with:")
        print("  from DriveBase import DriveBase")
        print("  from Logger import Logger")
        return True
    else:
        print(f"✗ Upload failed: {result.stderr}")
        return False


def main():
    """Main execution function."""
    print("=" * 50)
    print("LEGO Spike Prime - Library Upload Tool")
    print("=" * 50)
    print()
    
    # Ensure virtual environment is set up with mpremote
    if not ensure_venv():
        sys.exit(1)
    
    print()
    print("-" * 50)
    print()
    
    # Test connection
    print("Testing connection to LEGO hub...")
    if not test_connection():
        print("✗ Connection failed. Please ensure:")
        print("  1. The LEGO hub is connected via USB")
        print("  2. No other program is using the hub")
        sys.exit(1)
    
    print("✓ Connected to LEGO hub")
    print()
    print("-" * 50)
    print()
    
    # Upload libraries
    if upload_libraries():
        print()
        print("=" * 50)
        print("Upload completed successfully!")
        print("=" * 50)
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
