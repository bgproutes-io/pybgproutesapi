import subprocess
import os
import pytest

EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), "examples")

# List of all example script filenames
example_scripts = [
    "readme_example.py",
    "rib_prefix_visibility.py",
    "rib_shortest_path.py",
    "ripe_90.py",
    "updates_regexp.py"
]

@pytest.mark.parametrize("script", example_scripts)
def test_example_script(script):
    script_path = os.path.join(EXAMPLES_DIR, script)
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    
    print(f"\n=== STDOUT for {script} ===\n{result.stdout}")
    print(f"\n=== STDERR for {script} ===\n{result.stderr}")

    assert result.returncode == 0, f"{script} exited with error code {result.returncode}"