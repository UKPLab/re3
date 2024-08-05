from pathlib import Path
import torch
from datasets import Dataset
from .prompt_utils import *

def add_unique_id(data):
        data = data.fillna('')
        data['id'] = ''
        for i, row in data.iterrows():
            ix = str(int(row['edit_index'])) if row['edit_index'] != '' else 'no-ix'
            id = (ix + '=' + str(row['node_ix_src']).strip() + '=' + str(row['node_ix_tgt']).strip()).strip()
            data.loc[i, 'id'] = id
        return data

class PromptGenerater:
    def __init__(self):
        pass

    def check_prompt_type(self):
        if not self.cot_type in self.prompt_type:
            raise ValueError(f'cot_type {self.cot_type} is not in prompt_type {self.prompt_type}')
        if self.icl_dynamic != '':
            if not self.icl_dynamic + str(self.icl_dynamic_n) in self.prompt_type:
                raise ValueError(f'{self.icl_dynamic + str(self.icl_dynamic_n)} is not in prompt_type {self.prompt_type}')
        if self.icl_static != '':
            if not self.icl_static in self.prompt_type:
                raise ValueError(f'{self.icl_static} is not in prompt_type {self.prompt_type}')

    def generate_prompt(self, train_ds, test_ds, prompt_type:str, icl_static:str, cot_type:str,
                        icl_dynamic:str, icl_dynamic_n:int, icl_dynamic_file:Path):

        self.train_ds = train_ds
        self.test_ds = test_ds
        self.prompt_type = prompt_type
        self.icl_static = icl_static
        self.cot_type = cot_type
        self.icl_dynamic = icl_dynamic
        self.icl_dynamic_n = icl_dynamic_n
        if icl_dynamic_file is not None:
            self.icl_dynamic_file = torch.load(icl_dynamic_file)
        else:
            self.icl_dynamic_file = None
        self.check_prompt_type()

        test_df = test_ds.to_pandas()
        print('Generating prompt for test data ...')
        test_df['prompt'] = test_df.apply(lambda x: self.generate_prompt_instance(x), axis=1)
        #test_df['prompt_len'] = [len(x.split()) for x in test_df['prompt']]
        test_ds = Dataset.from_pandas(test_df)
        return test_ds

    def generate_prompt_instance(self, instance):
        prompt_components = self.prompt_type.split('+')
        prompt_components = [x for x in prompt_components if x.strip() != '']
        input_text = '\nThe old text is: ' + instance['text_tgt'] + '\nThe new text is: ' + instance['text_src']
        if self.cot_type in ['LR', 'RL']:
            input_text += '\n\nLet\'s think step by step. \n'

        if 'def-LR' in prompt_components:
            static_example_text = DEF_LR
        elif 'def-RL' in prompt_components:
            static_example_text = DEF_RL
        elif 'def-L' in prompt_components:
            static_example_text = DEF_L
        else:
            static_example_text = ''

        if self.icl_dynamic == '':
            dynamic_example_text = ''
        else:
            dynamic_examples = self.get_dynamic_examples(instance, f'icl_{self.icl_dynamic}')
            dynamic_example_text = self.generate_dynamic_example_text(dynamic_examples)

        if len(prompt_components) > 1:
            if 'def' in prompt_components[0]:
                prompts = [B_INST, B_SYS, SYS_PROMPT, E_SYS, EXAMPLE_START,
                           static_example_text, dynamic_example_text, TASK_PROMPTS[self.cot_type], input_text, E_INST]
            elif 'def' in prompt_components[1]:
                prompts = [B_INST, B_SYS, SYS_PROMPT, E_SYS, EXAMPLE_START,
                           dynamic_example_text, static_example_text, TASK_PROMPTS[self.cot_type], input_text, E_INST]
        else:
            if 'def' in prompt_components[0]:
                prompts = [B_INST, B_SYS, SYS_PROMPT, E_SYS, EXAMPLE_START,
                           static_example_text, TASK_PROMPTS[self.cot_type], input_text, E_INST]
            else:
                prompts = [B_INST, B_SYS, SYS_PROMPT, E_SYS, EXAMPLE_START,
                           dynamic_example_text, TASK_PROMPTS[self.cot_type], input_text, E_INST]
        prompts = [x for x in prompts if x != '']
        prompt = ''.join(prompts)
        return prompt

    def generate_dynamic_example_text(self, dynamic_examples):
        dynamic_examples_text = []
        for _, row in dynamic_examples.iterrows():
            label = row['label']
            text = '\nThe old text is: ' + row['text_tgt'] +'\nThe new text is: ' + row['text_src'] + '\nLABEL: ' + label
            dynamic_examples_text.append(text)
        assert len(dynamic_examples_text) == self.icl_dynamic_n
        text = '\n\n'.join(dynamic_examples_text)
        return text+'\n\n'

    def get_dynamic_examples(self, instance, icl_type):
        example_ixs = self.icl_dynamic_file[str(instance['edit_index'])][icl_type][:self.icl_dynamic_n]
        example_ixs = [int(ix) for ix in example_ixs]
        train_df = self.train_ds.to_pandas()
        dynamic_examples = train_df[train_df['edit_index'].isin(example_ixs)]
        # order icl_examples by examples_ixs (most similar first)
        dynamic_examples = dynamic_examples.set_index('edit_index').loc[example_ixs].reset_index()
        # reverse the order of icl_examples (most similar last)
        dynamic_examples =  dynamic_examples.iloc[::-1]
        return dynamic_examples
        
    
    

