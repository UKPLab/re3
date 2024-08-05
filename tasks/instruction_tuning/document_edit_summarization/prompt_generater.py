from .prompt_utils import *
import pandas as pd

def add_unique_id(data):
        data = data.fillna('')
        data['id'] = data['doc_name'] # the unique id for each doc
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

    def generate_prompt(self, test_ds):
        test_edits_df = test_ds.to_pandas()
        test_docs = test_edits_df['doc_name'].unique()
        test_df = pd.DataFrame()
        for doc in test_docs:
            doc_df = test_edits_df[test_edits_df['doc_name'] == doc]
            doc_prompt = self.generate_doc_prompt(doc_df, doc)
            test_df = pd.concat([test_df, doc_prompt])
        return test_df

    def generate_doc_prompt(self, doc_df, doc_name):
        doc_prompt = pd.DataFrame()
        user_input = self.generate_user_input(doc_df)
        doc_prompt['doc_name'] = [doc_name]
        doc_prompt['system_prompt'] = [SYS_PROMPT]
        doc_prompt['user_input'] = [user_input]
        return doc_prompt

    def generate_user_input(self, doc_df):
        user_prompt = ''
        for index, row in doc_df.iterrows():
            user_prompt += f"The original text in the section with the title {row['sec_title_tgt']}: {row['text_tgt']}. The revised text in the section with the title {row['sec_title_src']}: {row['text_src']}. The revision label and intention is {row['gold']}.\n"
        return user_prompt


        
    
    

