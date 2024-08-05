from pathlib import Path
from typing import List
import pandas as pd
import torch
import tqdm
from .prompt_utils import E_INST
from .prompt_generater import add_unique_id

class OutputGenerater:
    def __init__(self):
        pass
    
    def load_instances(self):
        instances = self.test_ds.to_pandas()
        instances = instances.fillna('')
        if self.exp_mode == 'continue_exp':
            print('############## continue experiment...')
            if self.outputs_file.exists():
                data = pd.read_csv(self.outputs_file)
                data = data.fillna('')
                data = data.drop_duplicates()
                if len(data) > 0:
                    instances = add_unique_id(instances)
                    data = add_unique_id(data)
                    data = data.drop_duplicates(subset=['id'])
                    instances = instances[~instances['id'].isin(data['id'])]
                    print(f'{len(data)} samples already processed, continue experiment...')
                    del data
                    print(instances)

        elif self.exp_mode == 'new_exp':
            print('############## new experiment...')
            if self.outputs_file.exists():
                print(f'{self.outputs_file} exists, remove it...')
                self.outputs_file.unlink()
            instances = add_unique_id(instances)

        return instances


    def clean_outputs(self, outputs: List[str]):
        #check if the outputs are in the correct format
        for t in outputs:
            if not len(t.split(E_INST)) == 2:
                print('len(t.split(E_INST))!=2', len(t.split(E_INST)))
                for x in t.split(E_INST):
                    print('====')
                    print(x)
                    return [t.split('[/INST')[1].strip() for t in outputs] #one possible error
        return [t.split(E_INST)[1].strip() for t in outputs]

    def get_label_from_outputs(self, outputs: List[str]):
        labels = []
        for t in outputs:
            flag = True
            for t2 in t.split('\n'):
                if 'LABEL' in t2:
                    label = t2.replace('LABEL:', '').strip()
                    if label not in self.target_labels:
                        label += '_error'
                    labels.append(label)
                    flag = False
                    break
            if flag:
                labels.append(t)
        return labels

    def get_reason_from_outputs(self, outputs: List[str]):
        reasons = []
        for t in outputs:
            flag = True
            for t2 in t.split('\n'):
                if 'REASON' in t2:
                    r = t2.replace('REASON:', '').strip()
                    reasons.append(r)
                    flag = False
                    break
            if flag:
                reasons.append(t.split('\n'))
        return reasons

    def process_batch(self,test_ds,
                 model, 
                 tokenizer, 
                 target_labels: List[str],
                 exp_mode: str,
                 exp_dir: Path,
                 batch_size: int,
                 max_length: int,
                 max_new_tokens: int,
                 save_prompt_examples:bool=True):
        self.test_ds = test_ds
        self.target_labels = target_labels
        self.exp_mode = exp_mode
        self.exp_dir = exp_dir
        self.model = model
        self.tokenizer = tokenizer
        self.batch_size = batch_size
        self.max_length = max_length
        self.max_new_tokens = max_new_tokens
        self.outputs_file = exp_dir / 'outputs.csv'
        if save_prompt_examples:
            prompt_examples_file = exp_dir / 'prompt_examples.csv'
            test_df = test_ds.to_pandas().head(10)
            test_df.to_csv(prompt_examples_file, index=False)
    

        print('Start experiment...', self.exp_dir)
        print('batch_size: ', self.batch_size)
        print('max_new_tokens', self.max_new_tokens)
        print('exp_mode: ', self.exp_mode)

        instances = self.load_instances()
        if len(instances) == 0:
            print('No instances to process...')
            return

        for i in tqdm.tqdm(range(0, len(instances), self.batch_size)):
            with torch.no_grad():
                inputs = self.tokenizer([p for p in instances["prompt"].iloc[i:i + self.batch_size]],
                                            return_tensors="pt",
                                            max_length=self.max_length,
                                            truncation=True,
                                            padding=True)
                

                output_sequences = self.model.generate(input_ids=inputs["input_ids"].to("cuda"),
                                                       attention_mask=inputs["attention_mask"].to("cuda"),
                                                       max_new_tokens=self.max_new_tokens,
                                                       do_sample=False,
                                                       num_beams=1,
                                                       early_stopping=False,
                                                       top_k=0,
                                                       temperature=1,
                                                       penalty_alpha=0)

                
                outputs = self.tokenizer.batch_decode(output_sequences, skip_special_tokens=True)
                outputs = self.clean_outputs(outputs)
                preds = self.get_label_from_outputs(outputs)
                reasons = self.get_reason_from_outputs(outputs)
                data = pd.DataFrame({"edit_index": instances["edit_index"].iloc[i:i + self.batch_size],
                                     "doc_name": instances["doc_name"].iloc[i:i + self.batch_size],
                                     "node_ix_src": instances["node_ix_src"].iloc[i:i + self.batch_size],
                                     "node_ix_tgt": instances["node_ix_tgt"].iloc[i:i + self.batch_size],
                                     "label": instances["label"].iloc[i:i + self.batch_size],
                                     "pred": preds,
                                     'reason': reasons
                                     })

                data.to_csv(self.exp_dir / "outputs.csv",
                            mode="a",
                            index=False,
                            header=not (self.exp_dir / "outputs.csv").exists())
                