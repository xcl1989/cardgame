#!/usr/bin/env python3
"""
Workflow Manager Helper Script

This script helps manage workflow states and task tracking.
Can be used to:
- Create task templates
- Generate progress reports
- Export task status to markdown
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def create_task_template(task_name: str, steps: list[str]) -> dict:
    """Create a structured task template."""
    return {
        "name": task_name,
        "created": datetime.now().isoformat(),
        "status": "pending",
        "steps": [
            {"step": i + 1, "description": step, "status": "pending"}
            for i, step in enumerate(steps)
        ],
        "completed": None,
        "notes": [],
    }


def generate_progress_report(tasks: list[dict]) -> str:
    """Generate a markdown progress report."""
    report = ["# Workflow Progress Report\n"]
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    for task in tasks:
        report.append(f"## {task['name']}")
        report.append(f"Status: {task['status']}\n")

        completed = sum(1 for step in task["steps"] if step["status"] == "completed")
        total = len(task["steps"])
        report.append(f"Progress: {completed}/{total} steps\n")

        report.append("### Steps")
        for step in task["steps"]:
            checkbox = "✅" if step["status"] == "completed" else "⬜"
            report.append(f"- {checkbox} Step {step['step']}: {step['description']}")

        if task.get("notes"):
            report.append("\n### Notes")
            for note in task["notes"]:
                report.append(f"- {note}")

        report.append("")

    return "\n".join(report)


def main():
    if len(sys.argv) < 2:
        print("Usage: workflow_manager.py <command> [args]")
        print("Commands:")
        print("  create <task_name>  - Create a new task template")
        print("  report <tasks.json> - Generate progress report")
        sys.exit(1)

    command = sys.argv[1]

    if command == "create":
        task_name = sys.argv[2] if len(sys.argv) > 2 else "New Task"
        steps = sys.argv[3:] if len(sys.argv) > 3 else ["Step 1"]
        template = create_task_template(task_name, steps)
        print(json.dumps(template, indent=2))

    elif command == "report":
        if len(sys.argv) < 3:
            print("Error: Please provide tasks JSON file")
            sys.exit(1)
        tasks_file = Path(sys.argv[2])
        if not tasks_file.exists():
            print(f"Error: File not found: {tasks_file}")
            sys.exit(1)
        tasks = json.loads(tasks_file.read_text())
        print(generate_progress_report(tasks))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
