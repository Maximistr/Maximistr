import subprocess
import sys
def ensure_module_installed(module_name, package_name=None):
    """Check if a module is installed, and install it if not."""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
    except ImportError:
        print(f"Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
# Ensure click tracking library is installed
ensure_module_installed("mouse")
ensure_module_installed("pyautogui")
import mouse
import pyautogui

stop_program = False

def on_click():
    """Callback function that prints mouse position when clicked."""
    pos = pyautogui.position()
    print(f"Click detected at position: {pos}")

def on_middle_click():
    """Stop the program on middle click."""
    global stop_program
    stop_program = True
    print("\nStopped by middle click.")

print("Click listener active. Press Ctrl+C to stop.\n")
print("Left click = print position | Middle click = exit\n")
mouse.on_click(on_click)
mouse.on_middle_click(on_middle_click)

# Keep the program running
try:
    while not stop_program:
        pass
except KeyboardInterrupt: 
    print("\nStopped.")

