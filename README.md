# Re3: A Holistic Framework and Dataset for Modeling Collaborative Document Revision
This is the official code repository for the paper "Re3: A Holistic Framework and Dataset for Modeling Collaborative Document Revision", presented at ACL 2024 main conference.

Please find the paper [here](https://arxiv.org/abs/2406.00197), and star the repository to stay updated with the latest information.

In case of questions please contact [Qian Ruan](mailto:ruan@ukp.tu-darmstadt.de).

## Abstract
Collaborative review and revision of textual documents is the core of knowledge work and a promising target for empirical analysis and NLP assistance. Yet, a holistic framework that would allow modeling complex relationships between document revisions, reviews and author responses is lacking. To address this gap, we introduce Re3, a framework for joint analysis of collaborative document revision. We instantiate this framework in the scholarly domain, and present Re3-Sci, a large corpus of aligned scientific paper revisions manually labeled according to their action and intent, and supplemented with the respective peer reviews and human-written edit summaries. We use the new data to provide first empirical insights into collaborative document revision in the academic domain, and to assess the capabilities of state-of-the-art LLMs at automating edit analysis and facilitating text-based collaboration. We make our annotation environment and protocols, the resulting data and experimental code publicly available. 

![](/resource/re3.png)

*Figure 1. Re3 offers a holistic framework for studying the relationships between reviews (a), revisions (b-c) and responses (d) in text-based collaboration. It is instantiated in the Re3-Sci dataset that covers all edits in 314 full-length scientific publications manually labeled with edit action and intent (e) on different granularity levels, along with reviews that trigger edits and manually curated responses that summarize all edits made including self-initiated ones (f).*

## Quickstart
1. Install the package from github.
```bash
pip install git+https://github.com/UKPLab/re3
```

2. Download the newest version of the Re3-Sci dataset here: https://tudatalib.ulb.tu-darmstadt.de/handle/tudatalib/4300

3. Extract the dataset into the 'data' directory.

4. Load e.g. the data for edit intent classification (modification pairs only)
```python
  # load the data by task name
  # basic settings
  # <settings>
  dataset_name = 'Re3-Sci_v1'
  approach_name = 'instruction_tuning'
  task_name = 'edit_intent_classification_M' 
  # task_name in ['edit_intent_classification','edit_intent_classification_M','edit_intent_classification_AD', 'revision_alignment','review_request_extraction']
  train_type = 'train'  # name of the training data, see subfolders in 'tasks' of the dataset
  test_type = 'test'  # name of the test data, see subfolders in 'tasks' of the dataset
  # </settings>
  from tasks.instruction_tuning.task_data_loader import TaskDataLoader
  task_data_loader = TaskDataLoader(dataset_name=dataset_name,
                                      approach_name=approach_name,
                                      task_name=task_name,
                                      train_type=train_type,
                                      test_type=test_type)
  train_ds, val_ds, test_ds = task_data_loader.load_data()
  #test_ds = task_data_loader.load_test_tiny(n=100)  # you can run the code with a smaller test set of n samples for debugging
  labels, label2id, id2label = task_data_loader.get_labels()
  print('========== 1. Task data loaded: ==========')
  print(f'train_ds: {train_ds}')
  print(f'test_ds: {test_ds}')
  print(f'labels: {labels}')
  print(f'label2id: {label2id}')
  print(f'id2label: {id2label}')
```

## Re3-Sci Data Structure
```    
> Re3-Sci_v1
   > data_human: collection of human annotations
     > response: human-written document edit summaries and the corresponding human annotations, see README in the subfolder for more details
     > review: human annotations of alignments between review requests and related edits, see README in the subfolder for more details
     > revision: human annotations of edits and edit action and intent labels, at sentence(s), paragraph(p), section(sec) and subsentence(ss) levels, 
                 see README in the subfolder for more details
   > docs: document revisions, reviews and document edit summaries in ITG format. 
           The corresponding human annotations can be found in the CSV files within the 'data_human' directory, identified by the 'doc_name' attribute.
     > subfolder structure:
       > v1.json: the original document in ITG format
       > v2.json: the revised document in ITG format
       > review: the review document(s) in ITG format
       > response: the document edit summary in ITG format
   > tasks: 
     > instruction_tuning: data splits for the four NLP tasks using instruction tuning approaches, read the README in the subfolder for more details.
       > edit_intent_classification
       > edit_intent_classification_AD
       > edit_intent_classification_M
       > revision_alignment
       > review_request_extraction
       > document_edit_summarization
```    

### NLP Tasks
Check the following scripts for the complete pipeline code: *inference_EIC_M.py*, *inference_EIC_AD.py*, *inference_RA*.py, *inference_RRE.py*, and *inference_DES*.py. These scripts handle tasks including edit intent classification (EIC, differentiating between modification pairs and additions + deletions), revision alignment (RA), review request extraction (RRE), and document edit summarization (DES). The arguments within <settings> and </settings> can be customized. Also refer to the paper for more details

For example, proceed with data loading for the task 'edit_intent_classification_M':

2. Generate Prompts

```python
    # generate prompts
    # settings for prompt generater
    # <settings>
    prompt_type = '+diff3+def-LR'
    #static default examples only: ['+def-LR','+def-RL','+def-L',...]
    #static examples followed by dynamic examples: ['+def-LR+diff3','+def-RL+loc3','+def-L+cat3',...]
    #dynamic examples only: ['+diff3','+loc3','+cat3',...]
    #dynamic examples followed by static examples: ['+diff3+def-LR','+loc3+def-LR','+cat3+def-LR',...]
    # the following variables should be set according to the prompt_type
    icl_static = 'def'  
    # select from ['','def'], '' means no static examples, use the default examples in tasks/instruction_tuning/<task_name>/prompt_utils.py
    cot_type = 'LR'  
    # select from ['LR','RL','L'], the Chain-of-Though format, LR: label followed by rational, RL: rational followed by label, L:label only
    icl_dynamic = 'diff'  
    # select from ['','cat','diff','loc'], dynamic example selection method, '' means no dynamic examples
    icl_dynamic_n = 3  
    # select from [1,3,5,8], count of dynamic examples
    icl_dynamic_file = Path(f'resource/EIC_M_test_icl_roberta_cosine.pt') 
    # pre-computed dynamic example selection files are saved in the resource folder
    # </settings>
    from tasks.instruction_tuning.task_prompt_generater import TaskPromptGenerater
    task_prompt_generater = TaskPromptGenerater(task_name=task_name).prompt_generater
    test_ds = task_prompt_generater.generate_prompt(train_ds, test_ds, prompt_type, icl_static, cot_type,
                                                    icl_dynamic, icl_dynamic_n, icl_dynamic_file)
    print('========== 2. Prompt generated for test data: ==========')
    print(f'prompt_type: {prompt_type}')
    print(f'test_ds: {test_ds}')
```
3. Load Model

```python
    # load model from path
    # <settings>
    model_root_path = '' # path to the model root folder
    model_name = "llama-2-hf"
    model_version = "70B-Chat"
    # </settings>
    from tasks.instruction_tuning.task_model_loader import TaskModelLoader
    model_loader = TaskModelLoader(model_root_path=model_root_path, model_name=model_name, model_version=model_version)
    model, tokenizer = model_loader.load_model()
    print('========== 3. Model loaded: ==========')
    print(f'model: {model}')
```

4. Create Experiment Directory

```python
    # create experiment directory in the 'results' folder, with the settings above
    from tasks.instruction_tuning.task_exp_dir_creater import TaskExpDirCreater
    args = {'approach_name': approach_name, 'task_name': task_name,
            'model_name': model_name, 'model_version': model_version,
            'prompt_type': prompt_type, 'test_type': test_type}
    exp_dir = TaskExpDirCreater().create_exp_dir(args)
    print('========== 4. Experiment directory created: ==========')
    print(f'exp_dir: {exp_dir}')
```
5. Generate Outputs

```python
    # generate outputs, saved in exp_dir/outputs.csv
    # <settings>
    batch_size = 8
    max_length = 4096
    max_new_tokens = 200
    exp_mode = 'new_exp'  # select from ['continue_exp','new_exp']
    # </settings>
    from tasks.instruction_tuning.task_output_generater import TaskOutputGenerater
    output_generater = TaskOutputGenerater(task_name=task_name).output_generater
    output_generater.process_batch(test_ds, model, tokenizer, labels, exp_mode, exp_dir, batch_size, max_length, max_new_tokens)
    print('========== 5. Outputs generated: ==========')
    print(f'exp_dir: {exp_dir}')
```
6. Evaluate

```python
    # evaluate outputs, evaluation results saved in exp_dir/eval.json
    from tasks.instruction_tuning.task_evaluator import TaskEvaluator
    task_evaluator = TaskEvaluator(exp_dir)
    task_evaluator.evaluate(label2id)
    print('========== 6. Evaluation done: ==========')
    print(f'exp_dir: {exp_dir}')
    print('========== Done ==========')
```

## Citation

Please use the following citation:

```
@article{ruan2024re3,
      title={Re3: A Holistic Framework and Dataset for Modeling Collaborative Document Revision},
      author={Qian Ruan and Ilia Kuznetsov and Iryna Gurevych},
      year={2024},
      journal={arXiv preprint arXiv:2406.00197},
      url={https://arxiv.org/abs/2406.00197},
}
```

Contact Persons: Qian Ruan, Ilia Kuznetsov

<https://intertext.ukp-lab.de/>

<https://www.ukp.tu-darmstadt.de>

<https://www.tu-darmstadt.de>


This repository contains experimental software and is published for the sole purpose of giving additional background details on the respective publication.