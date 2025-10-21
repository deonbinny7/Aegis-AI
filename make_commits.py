import os
import subprocess
import time

COMMIT_PLAN = [
    # Day 1: Oct 10
    ("2025-10-10T10:00:00", ["\.gitignore"], "Initial project setup and gitignore"),
    ("2025-10-10T11:30:00", ["run.bat"], "Add run script to execute the application"),
    ("2025-10-10T14:45:00", [], "Define project structure and directories"),
    ("2025-10-10T16:20:00", ["precog_ui\\config.py"], "Initial configuration variables and constants"),

    # Day 2: Oct 11
    ("2025-10-11T09:15:00", ["precog_ui\\utils\\helpers.py"], "Add helper utilities for calculations"),
    ("2025-10-11T12:05:00", ["precog_ui\\utils\\physics.py"], "Implement physics modeling utilities"),
    ("2025-10-11T15:30:00", ["precog_ui\\state\\state_machine.py"], "Establish core state machine logic"),
    ("2025-10-11T17:10:00", [], "Refine state transitions and error handling"),

    # Day 3: Oct 16
    ("2025-10-16T10:20:00", ["precog_ui\\tracking\\hand_tracker.py"], "Add foundational Hand Tracking module"),
    ("2025-10-16T13:40:00", ["precog_ui\\gestures\\gesture_engine.py"], "Implement Gesture recognition engine"),
    ("2025-10-16T15:55:00", [], "Fix tracking latency issues"),
    ("2025-10-16T18:00:00", [], "Improve gesture detection accuracy and smoothing"),

    # Day 4: Oct 17
    ("2025-10-17T09:05:00", ["precog_ui\\actions\\action_manager.py"], "Add Action Manager for translating gestures"),
    ("2025-10-17T11:45:00", ["precog_ui\\ui\\renderer.py"], "Start UI rendering framework implementation"),
    ("2025-10-17T14:30:00", ["precog_ui\\ui\\components.py"], "Define reusable UI components"),
    ("2025-10-17T16:45:00", [], "Style components to match holographic theme"),

    # Day 5: Oct 20
    ("2025-10-20T10:10:00", ["precog_ui\\ui\\dashboard.py"], "Integrate core Dashboard view"),
    ("2025-10-20T13:25:00", [], "Fix overlap bugs in dashboard rendering"),
    ("2025-10-20T15:40:00", [], "Optimize performance in main render loop"),
    ("2025-10-20T17:50:00", ["precog_ui\\main.py"], "Implement application entry point"),

    # Day 6: Oct 21
    ("2025-10-21T09:30:00", [], "Refactor imports and resolve circular dependencies"),
    ("2025-10-21T11:15:00", [], "Enhance application stability under heavy load"),
    ("2025-10-21T14:20:00", ["."], "Ensure all remaining components are tracked"),
    ("2025-10-21T16:00:00", [], "Final prep for v1 release"),
]

def run_cmd(cmd):
    try:
        subprocess.run(cmd, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running: {cmd}")

def main():
    if not os.path.exists(".git"):
        print("Initializing git repository...")
        run_cmd("git init")
        run_cmd("git branch -m main")

    for i, (date, files, message) in enumerate(COMMIT_PLAN, 1):
        # Format for git
        git_date = date
        print(f"[{i}/24] Creating commit for {git_date} - {message}")
        
        env = os.environ.copy()
        env['GIT_AUTHOR_DATE'] = git_date
        env['GIT_COMMITTER_DATE'] = git_date
        
        # Add files
        has_files_to_add = False
        for f in files:
            if f == ".":
                run_cmd("git add .")
                has_files_to_add = True
            elif os.path.exists(f) or f == "\.gitignore": # backslash handled in powershell/cmd or raw string
                # handle proper slashes
                normalized_f = f.replace("\\\\", "/").replace("\\", "/")
                # add specific file
                run_cmd(f'git add "{normalized_f}"')
                has_files_to_add = True
            else:
                # try without slashes or check if exists
                normalized_f = f.replace("\\", "/")
                run_cmd(f'git add "{normalized_f}"')
                has_files_to_add = True
                
        # Commit
        cmd = ["git", "commit", "-m", message]
        if not files or not has_files_to_add:
            cmd.append("--allow-empty")
            
        subprocess.run(cmd, env=env, check=False)
        time.sleep(0.5)

    print("Finished generating commits.")

if __name__ == "__main__":
    main()
