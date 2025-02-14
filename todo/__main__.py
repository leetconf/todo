import argparse, json
from pathlib import Path

from .database import Database
from .util import setup_logging
from . import __version__

current_dir = Path(__file__).resolve().parent
data_folder = current_dir / "data"

db = Database(data_folder / "tasks.json")

def edit_task(id: int, new_desc: str) -> None:
    task = db.find_task(id)
    if task:
        task.description = new_desc
        db.update_task(task)

def toggle_completed_status(ids: list) -> None:
    for id in ids:
        task = db.find_task(id)
        if task:
            task.completed = not task.completed
            db.update_task(task)

def list_tasks() -> None:
    tasks = db.load_tasks()
    for task in tasks:
        info = f"\033[1m{task.id}\033[0m "
        if task.completed:
            info += f"\033[9m{task.description}\033[0m"
        else:
            info += task.description
        print(info)

def main() -> None:
    setup_logging()
    
    parser = argparse.ArgumentParser(description="Manage your tasks through the terminal with ease")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    with open(data_folder / "help.json", "r", encoding="utf-8") as file:
        manual = json.load(file)

    add_task_parser = subparsers.add_parser("add", help=manual["add"]["help"])
    add_task_parser.add_argument("description", help=manual["add"]["args"]["description"], type=str)

    toggle_task_parser = subparsers.add_parser("tg", help=manual["tg"]["help"])
    toggle_task_parser.add_argument("ids", help=manual["tg"]["args"]["ids"], type=int, nargs="+")

    edit_task_parser = subparsers.add_parser("edit", help=manual["edit"]["help"])
    edit_task_parser.add_argument("id", help=manual["edit"]["args"]["id"], type=int)
    edit_task_parser.add_argument("new_description", help=manual["edit"]["args"]["new_description"], type=str)

    remove_task_parser = subparsers.add_parser("rm", help=manual["rm"]["help"])
    remove_task_parser.add_argument("ids", help=manual["rm"]["args"]["ids"], type=int, nargs="+")

    subparsers.add_parser("ls", help=manual["ls"]["help"])

    args = parser.parse_args()

    commands = {
        "add": lambda: db.add_task(args.description),
        "tg": lambda: toggle_completed_status(args.ids),
        "edit": lambda: edit_task(args.id, args.new_description),
        "rm": lambda: [db.remove_task(id) for id in args.ids],
        "ls": list_tasks
    }

    commands[args.command]()

if __name__ == "__main__":
    main()
