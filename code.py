import subprocess
import os

# --- Configuration ---
# You can change these variables
REPO_DIR = '.'  # Current directory (assuming the script is inside the repo)
COMMIT_MESSAGE = "Automated commit via Python script"
FILE_TO_COMMIT = "new_file.txt"

# --- 1. Create a dummy file to commit (for demonstration) ---
try:
    with open(FILE_TO_COMMIT, 'w') as f:
        f.write("This file was created and committed using a Python script!\n")
    print(f"Created file: {FILE_TO_COMMIT}")
except IOError as e:
    print(f"Error creating file: {e}")
    exit(1)

# --- 2. Function to execute Git commands ---
def execute_git_command(command):
    """Executes a Git command and handles errors."""
    try:
        # The 'shell=True' is used here for simplicity in some environments,
        # but 'shell=False' (default) and passing the command as a list is generally safer.
        # We will use the list approach for better security.
        process = subprocess.run(
            command,
            cwd=REPO_DIR,
            check=True,  # Raises an exception for non-zero exit codes
            capture_output=True,
            text=True
        )
        print(f"✅ Success: {' '.join(command[1:])}") # Print successful command
        print(process.stdout.strip())
        return process.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing command: {' '.join(command[1:])}")
        print(f"Standard Error:\n{e.stderr.strip()}")
        # Check for specific authentication/remote errors
        if "Authentication failed" in e.stderr or "Please make sure you have the correct access rights" in e.stderr:
             print("\n🚨 **Authentication Error:** Ensure your GitHub credentials (PAT/SSH) are correctly set up.")
        return None
    except FileNotFoundError:
        print("❌ Error: Git command not found. Is Git installed and in your PATH?")
        return None

# --- 3. Execute Git Commands ---

# 3a. git add <file>
# Add the newly created file (or '.' to add all changes)
execute_git_command(["git", "add", FILE_TO_COMMIT])
# 

# 3b. git commit -m "<message>"
# Commit the staged changes
execute_git_command(["git", "commit", "-m", COMMIT_MESSAGE])

# 3c. git push
# Push the commit to the remote repository (assumes 'origin' and 'master' or 'main' branch)
print("\n--- Starting Push Operation ---")
execute_git_command(["git", "push"])
print("--- Push Operation Finished ---\n")

print("✨ **Script execution complete.** Check your GitHub repository!")
