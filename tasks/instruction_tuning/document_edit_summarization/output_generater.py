import pandas as pd
import tqdm
import openai

api_version=""
azure_endpoint=""
api_key=""# your api key

class OutputGenerater:
    def __init__(self):
        pass
    def generate(self, test_ds, model_name, exp_dir, save_prompt_examples:bool=True):
        self.outputs_file = exp_dir / 'outputs.csv'
        if save_prompt_examples:
            prompt_examples_file = exp_dir / 'prompt_examples.csv'
            test_df = test_ds.head(3)
            test_df.to_csv(prompt_examples_file, index=False)
        print('Start experiment...', exp_dir)
        print('model_name: ', model_name)

        doc_names = test_ds['doc_name'].unique().tolist()
        outputs = pd.DataFrame()
        for doc_name in tqdm.tqdm(doc_names):
            output = pd.DataFrame()
            row = test_ds[test_ds['doc_name'] == doc_name].iloc[0]
            output['doc_name'] = [doc_name]
            system_prompt = row['system_prompt']
            user_input = row['user_input']
            try:
                client = openai.AzureOpenAI(api_version=api_version,
                                            azure_endpoint=azure_endpoint,
                                            api_key=api_key)
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                )
                summ = response.choices[0].message.content
            except Exception as e:
                print(f"An error occurred: {e}")
                summ = 'none'
            output['edit_summary'] = [summ]
            output['generater'] = [model_name]
            outputs = pd.concat([outputs, output])
        outputs.to_csv(self.outputs_file, index=False)
