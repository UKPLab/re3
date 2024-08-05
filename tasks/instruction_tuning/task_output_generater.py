from pathlib import Path
import importlib


class TaskOutputGenerater:
    def __init__(self, task_name: str) -> None:
        pck = importlib.import_module(f"tasks.instruction_tuning.{task_name}")
        output_generater = getattr(pck, 'OutputGenerater')
        self.task_name = task_name
        self.output_generater = output_generater()


def main():
    task_name = 'edit_intent_classification_M'
    task_output_generater = TaskPromptGenerater(task_name).output_generater

if __name__ == "__main__":
    main()