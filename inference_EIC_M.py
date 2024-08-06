import pandas as pd
from pathlib import Path

def main():
    ############################################################################
    # basic settings
    # <settings>
    dataset_name = 'Re3-Sci_v1'
    approach_name = 'instruction_tuning'
    task_name = 'edit_intent_classification_M' # task_name in ['edit_intent_classification_M','edit_intent_classification_AD', 'revision_alignment','review_request_extraction']
    train_type = 'train'  # name of the training data
    test_type = 'test_small'  # name of the test data
    # </settings>
    print('========== Basic settings: ==========')
    print(f'dataset_name: {dataset_name}')
    print(f'approach_name: {approach_name}')
    print(f'task_name: {task_name}')
    print(f'train_type: {train_type}')
    print(f'test_type: {test_type}')
   
    ############################################################################
    # load task data
    from tasks.instruction_tuning.task_data_loader import TaskDataLoader
    task_data_loader = TaskDataLoader(dataset_name=dataset_name,
                                      approach_name=approach_name,
                                      task_name=task_name,
                                      train_type=train_type,
                                      test_type=test_type)
    train_ds, val_ds, test_ds = task_data_loader.load_data()
    #test_ds = task_data_loader.load_test_tiny(n=100) # you can run the code with a smaller test set for debugging
    labels, label2id, id2label = task_data_loader.get_labels()
    print('========== 1. Task data loaded: ==========')
    print(f'train_ds: {train_ds}')
    print(f'val_ds: {val_ds}')
    print(f'test_ds: {test_ds}')
    print(f'labels: {labels}')
    print(f'label2id: {label2id}')
    print(f'id2label: {id2label}')
   
    ############################################################################
    # generate prompts
    # settings for prompt generater
    # <settings>
    prompt_type = '+diff3+def-LR'
    #static default examples only: ['+def-LR','+def-RL','+def-L',...]
    #static examples followed by dynamic examples: ['+def-LR+diff3','+def-RL+loc3','+def-L+cat3',...]
    #dynamic examples only: ['+diff3','+loc3','+cat3',...]
    #dynamic examples followed by static examples: ['+diff3+def-LR','+loc3+def-LR','+cat3+def-LR',...]
    # the following variables should be set according to the prompt_type
    icl_static = 'def'  # select from ['','def'], '' means no static examples
    cot_type = 'LR'  # select from ['LR','RL','L']
    icl_dynamic = 'diff'  # select from ['','cat','diff','loc'], '' means no dynamic examples
    icl_dynamic_n = 3  # select from [1,3,5,8]
    icl_dynamic_file = Path(f'resource/EIC_M_test_icl_roberta_cosine.pt') # pre-computed icl selection files are saved in the resource folder
    # </settings>
    from tasks.instruction_tuning.task_prompt_generater import TaskPromptGenerater
    task_prompt_generater = TaskPromptGenerater(task_name=task_name).prompt_generater
    test_ds = task_prompt_generater.generate_prompt(train_ds, test_ds, prompt_type, icl_static, cot_type,
                                                    icl_dynamic, icl_dynamic_n, icl_dynamic_file)
    print('========== 2. Prompt generated for test data: ==========')
    print(f'prompt_type: {prompt_type}')
    print(f'test_ds: {test_ds}')
    
    ############################################################################
    # load model from path
    # <settings>
    model_root_path = ''  # path to the model root directory
    model_name = "llama-2-hf"
    model_version = "70B-Chat"
    # </settings>
    from tasks.instruction_tuning.task_model_loader import TaskModelLoader
    model_loader = TaskModelLoader(model_root_path=model_root_path, model_name=model_name, model_version=model_version)
    model, tokenizer = model_loader.load_model()
    print('========== 3. Model loaded: ==========')
    print(f'model: {model}')
    
    ############################################################################
    # create experiment directory in the 'results' folder
    from tasks.instruction_tuning.task_exp_dir_creater import TaskExpDirCreater
    args = {'approach_name': approach_name, 'task_name': task_name,
            'model_name': model_name, 'model_version': model_version,
            'prompt_type': prompt_type, 'test_type': test_type}
    exp_dir = TaskExpDirCreater().create_exp_dir(args)
    print('========== 4. Experiment directory created: ==========')
    print(f'exp_dir: {exp_dir}')
    
    ############################################################################
    # generate outputs
    # <settings>
    batch_size = 8
    max_length = 4096
    max_new_tokens = 200
    exp_mode = 'continue_exp'  # select from ['continue_exp','new_exp']
    # </settings>
    from tasks.instruction_tuning.task_output_generater import TaskOutputGenerater
    output_generater = TaskOutputGenerater(task_name=task_name).output_generater
    output_generater.process_batch(test_ds, model, tokenizer, labels, exp_mode, exp_dir, batch_size, max_length, max_new_tokens)
    print('========== 5. Outputs generated: ==========')
    print(f'exp_dir: {exp_dir}')
    ############################################################################
    # evaluate outputs
    from tasks.instruction_tuning.task_evaluator import TaskEvaluator
    task_evaluator = TaskEvaluator(exp_dir)
    task_evaluator.evaluate(label2id)
    print('========== 6. Evaluation done: ==========')
    print(f'exp_dir: {exp_dir}')
    print('========== Done ==========')



if __name__ == "__main__":
    main()
