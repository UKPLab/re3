from pathlib import Path
import pandas as pd
import json
from sklearn.metrics import classification_report


class TaskEvaluator:
    def __init__(self, exp_dir:Path) -> None:
        '''
        params:exp_dir: Path: path to the experiment directory
        '''
        self.exp_dir = exp_dir

    def evaluate(self, labels2id):	
        outputs_file = self.exp_dir/'outputs.csv'
        if not outputs_file.exists():
            print('outputs.csv not exist:', outputs_file)
            return
        
        data = pd.read_csv(outputs_file)
        data = data.fillna('')
        data = data.drop_duplicates()

        eval_file = self.exp_dir / 'eval.json'
        self.report_classification(data, eval_file, target_labels=labels2id)

    def clean_pred(self, pred, target_labels):
        pred = pred.strip()
        if pred in target_labels.keys():
            return pred
        for label in target_labels.keys():
            if label in pred:
                return label


    def report_classification(self, data, eval_file, target_labels, report_pred_error=True):
        data['gold_'] = data['label']
        # add a new column for cleaned pred
        for i, row in data.iterrows():
            if row['pred'] not in target_labels.keys():
                pred = self.clean_pred(row['pred'], target_labels)
            else:
                pred = row['pred']
            data.at[i, 'pred_'] = pred
        
        if report_pred_error:
            pred_error = data[~data['pred_'].isin(target_labels.keys())]
            if len(pred_error) > 0:
                print('pred_error:', pred_error[['pred', 'pred_']])
                f = eval_file.parent / f'{eval_file.name}_pred_error.csv'
                pred_error.to_csv(f, index=False)
        
        data = data[data['pred_'].isin(target_labels.keys())]
        y_true = data['gold_'].apply(lambda x: target_labels[x])
        y_pred = data['pred_'].apply(lambda x: target_labels[x])

        eval_dict = classification_report(y_true, y_pred, labels=list(target_labels.values()),
                                        target_names=target_labels.keys(), output_dict=True, zero_division=0)
        eval_dict['pred'] = {}
        eval_dict['gold'] = {}
        for k, v in data['pred_'].value_counts().items():
            eval_dict['pred'][k] = v
        for k, v in data['gold_'].value_counts().items():
            eval_dict['gold'][k] = v
        with open(eval_file, 'w') as f:
            json.dump(eval_dict, f, indent=4)

        return data



def main():
    exp_dir = Path('exp')
    task_evaluator = TaskEvaluator(exp_dir)
    


if __name__ == "__main__":
    main()

