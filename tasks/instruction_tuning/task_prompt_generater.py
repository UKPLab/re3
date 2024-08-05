from pathlib import Path
import importlib


class TaskPromptGenerater:
    def __init__(self, task_name: str) -> None:
        pck = importlib.import_module(f"tasks.instruction_tuning.{task_name}")
        prompt_generater = getattr(pck, 'PromptGenerater')
        self.task_name = task_name
        self.prompt_generater = prompt_generater()


def main():
    task_name = 'edit_intent_classification_M'
    task_prompt_generater = TaskPromptGenerater(task_name).prompt_generater

if __name__ == "__main__":
    main()