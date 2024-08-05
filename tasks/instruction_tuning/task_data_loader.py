from pathlib import Path
from datasets import load_dataset
import pandas as pd
from datasets import *

class TaskDataLoader:
    def __init__(self, dataset_name:str, approach_name:str, task_name: str,
                 train_type: str=None, val_type: str=None, test_type: str = None) -> None:
        '''
        params:dataset_name: str: name of the dataset
        params:approach_name: str: name of the approach, data splits are different for different approaches
        params:task_name: str: name of the task
        params:train_type: str: name of the csv file in the task data subfolder that will be used as training data
        params:val_type: str: name of the csv file in the task data subfolder that will be used as validation data
        params:test_type: str: name of the csv file in the task data subfolder that will be used as test data
        '''
        self.dataset_name = dataset_name
        self.approach_name = approach_name
        self.task_name = task_name
        self.train_type = train_type
        self.test_type = test_type
        self.val_type = val_type
        self.task_data_dir = Path(f'data/{dataset_name}/tasks') / approach_name / task_name
        data_files = {}
        for i in self.task_data_dir.iterdir():
            if i.is_file() and i.name.endswith('.csv'):
                data_files[i.stem] = str(i)
        self.data_files = data_files
        self.dataset = load_dataset("csv", data_files=data_files, keep_default_na=False)


    def load_train(self):
        if self.train_type is None:
            return None
        return self.dataset[self.train_type]

    def load_val(self):
        if self.val_type is None:
            return None
        return self.dataset[self.val_type]

    def load_test(self):
        if self.test_type is None:
            return None
        return self.dataset[self.test_type]

    def load_data(self):
        return self.load_train(), self.load_val(), self.load_test()
    
    def load_test_tiny(self,n=100):
        return self.dataset[self.test_type].select(range(n))

    def get_labels(self):
        # assume that the train data contain all the labels
        if 'label' in self.dataset["train"].column_names:
            label_names = sorted(set(label for label in self.dataset["train"]["label"]))
        elif 'gold' in self.dataset["train"].column_names:
            label_names = sorted(set(label for label in self.dataset["train"]["gold"]))
        else:
            raise ValueError('label or gold column not found in the dataset')

        label2id, id2label = dict(), dict()
        for i, label in enumerate(label_names):
            label2id[label] = i
            id2label[i] = label
        return label_names, label2id, id2label


def main():
    task_data_loader = TaskDataLoader(task_name='edit_intent_classification_M', train_type='train')


if __name__ == "__main__":
    main()

