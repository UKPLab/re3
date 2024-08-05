from pathlib import Path
import shutil

class TaskExpDirCreater:
    def __init__(self):
        pass

    def create_exp_dir(self, args, remove=False):
        results_dir = Path('results')
        results_dir.mkdir(parents=True, exist_ok=True)
        approach_dir = results_dir / args['approach_name']
        approach_dir.mkdir(parents=True, exist_ok=True)
        task_dir = approach_dir / args['task_name']
        task_dir.mkdir(parents=True, exist_ok=True)
        exp_dir_name = args['model_name'] + '_' + args['model_version']
        if 'prompt_type' in args:
            exp_dir_name = exp_dir_name + '_' + args['prompt_type']
        if 'test_type' in args:
            exp_dir_name = exp_dir_name + '_' + args['test_type']
        exp_dir = task_dir / exp_dir_name
        if remove and exp_dir.exists():
            shutil.rmtree(exp_dir)
        exp_dir.mkdir(parents=True, exist_ok=True)
        return exp_dir



