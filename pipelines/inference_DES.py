import pandas as pd
from pathlib import Path

def main():
    ############################################################################
    # basic settings
    # <settings>
    dataset_name = 'Re3-Sci_v1'
    approach_name = 'instruction_tuning'
    task_name = 'document_edit_summarization'  # task_name in ['edit_intent_classification_M','edit_intent_classification_AD', 'revision_alignment','review_request_extraction']
    train_type = ''  # name of the training data
    test_type = 'test'  # name of the test data
    # </settings>
    print('========== Basic settings: ==========')
    print(f'dataset_name: {dataset_name}')
    print(f'approach_name: {approach_name}')
    print(f'task_name: {task_name}')
    print(f'train_type: {train_type}')
    print(f'test_type: {test_type}')

    ############################################################################
    # load task data
    from re3.tasks.instruction_tuning.task_data_loader import TaskDataLoader
    task_data_loader = TaskDataLoader(dataset_name=dataset_name,
                                      approach_name=approach_name,
                                      task_name=task_name,
                                      train_type=train_type,
                                      test_type=test_type)
    test_ds = task_data_loader.load_test()
    # test_ds = task_data_loader.load_test_tiny(n=100)  # you can run the code with a smaller test set for debugging
    print('========== 1. Task data loaded: ==========')
    print(f'test_ds: {test_ds}')
    ############################################################################
    # generate prompts
    from tasks.instruction_tuning.task_prompt_generater import TaskPromptGenerater
    task_prompt_generater = TaskPromptGenerater(task_name=task_name).prompt_generater
    test_ds = task_prompt_generater.generate_prompt(test_ds)
    print('========== 2. Prompt generated for test data: ==========')
    print(f'test_ds: {test_ds}')
    ############################################################################
    # <settings>
    model_name = "gpt-4-1106-preview"  # "gpt-4-turbo"
    model_version = ""
    # </settings>
    ############################################################################
    # create experiment directory in the 'results' folder
    from tasks.instruction_tuning.task_exp_dir_creater import TaskExpDirCreater
    args = {'approach_name': approach_name, 'task_name': task_name,
            'model_name': model_name, 'model_version': model_version,
            'test_type': test_type}
    exp_dir = TaskExpDirCreater().create_exp_dir(args)
    print('========== 4. Experiment directory created: ==========')
    print(f'exp_dir: {exp_dir}')

    ############################################################################
    # generate outputs
    from tasks.instruction_tuning.task_output_generater import TaskOutputGenerater
    output_generater = TaskOutputGenerater(task_name=task_name).output_generater
    output_generater.generate(test_ds, model_name, exp_dir)
    print('========== 5. Outputs generated: ==========')
    print(f'exp_dir: {exp_dir}')
    print('========== Done ==========')


if __name__ == "__main__":
    main()
