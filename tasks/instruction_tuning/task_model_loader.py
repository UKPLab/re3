
from transformers import AutoModelForCausalLM, AutoTokenizer, logging

class TaskModelLoader:
    def __init__(self, model_root_path: str, model_name: str, model_version: str):
        self.model_root_path = model_root_path
        self.model_name = model_name
        self.model_version = model_version
        print('Loading the model: ', model_name, ',', model_version)

    def load_model(self):
        if 'llama-2' in self.model_name:
            model, tokenizer = self.llama2()
        else:
            raise Exception('Invalid model name.')
        return model, tokenizer

    def llama2(self):

        logging.set_verbosity_info()

        tokenizer = AutoTokenizer.from_pretrained(
            self.model_root_path + "/models--" + self.model_name + "/" + self.model_version)

        model = AutoModelForCausalLM.from_pretrained(
            self.model_root_path + "/models--" + self.model_name + "/" + self.model_version,
            device_map="auto",
            load_in_8bit=True
            )
        tokenizer.pad_token_id = tokenizer.eos_token_id
        return model, tokenizer



