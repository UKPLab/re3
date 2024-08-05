B_INST, E_INST = "[INST] ", " [/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
B_OLD, E_OLD = "\n[OLD] ", " [/OLD]"
B_NEW, E_NEW = "\n[NEW] ", " [/NEW]"
EXAMPLE_START = "Examples: \n"
SYS_PROMPT = "You are a helpful, respectful and honest revision analysis assistant. " \
            "You will read a text that is added to a document or entirely deleted from a document."\
      "Your task is to analyze the revision intent behind the addition or deletion of the text, based on the content of the text. "\
      "The intent can be one of the following labels: add/delete claim or statement (Claim), add/delete factual information (Fact/Evidence)."\
      "If none of the above labels are relevant, please answer with 'Other'. \n" 

DEF_L = "The old text is: \n"\
      "The new text is: There are several directions to improve ACTUNE.\n"\
      "LABEL: Claim \n\n"\
      "The old text is: For other SSAL methods, we mainly tune their key hyperparameters.\n"\
      "The new text is: \n"\
      "LABEL: Fact/Evidence \n\n"\
      "The old text is: \n"\
      "The new text is: Active Learning Setups. \n"\
      "LABEL: Other \n\n"
      
      
DEF_LR = "The old text is: \n"\
      "The new text is: There are several directions to improve ACTUNE.\n"\
      "LABEL: Claim \n"\
      "REASON: The old text is empty which means the new text is added into the document. The content of the new text is a subjective statement of the authors without any direct evidence, that is, a new claim is added, so the revision intent label is Claim.\n\n"\
      "The old text is: For other SSAL methods, we mainly tune their key hyperparameters.\n"\
      "The new text is: \n"\
      "LABEL: Fact/Evidence \n"\
      "REASON: The new text is empty which means the old text is deleted completly from the document. The content of the old text is a factual information that the authors tune the key hyperparameters of other SSAL methods, so the revision intent label is Fact/Evidence.\n\n"\
      "The old text is: \n"\
      "The new text is: Active Learning Setups. \n"\
      "LABEL: Other \n"\
      "REASON: The old text is empty which means the new text is added into the document. The content of the new text is a section title which is not related to claim or fact, the revision intent label is therfore Other. \n\n"\
                                
DEF_RL = "The old text is: \n"\
      "The new text is: There are several directions to improve ACTUNE.\n"\
      "REASON: The old text is empty which means the new text is added into the document. The content of the new text is a subjective statement of the authors without any direct evidence, that is, a new claim is added, so the revision intent label is Claim.\n"\
      "LABEL: Claim \n\n"\
      "The old text is: For other SSAL methods, we mainly tune their key hyperparameters.\n"\
      "The new text is: \n"\
      "REASON: The new text is empty which means the old text is deleted completly from the document. The content of the old text is a factual information that the authors tune the key hyperparameters of other SSAL methods, so the revision intent label is Fact/Evidence.\n"\
      "LABEL: Fact/Evidence \n\n"\
      "The old text is: \n"\
      "The new text is: Active Learning Setups. \n"\
      "REASON: The old text is empty which means the new text is added into the document. The content of the new text is a section title which is not related to claim or fact, the revision intent label is therfore Other. \n"\
      "LABEL: Other \n\n"\

TASK_PROMPTS = {'LR':  "Please read the following old and new texts. "\
                "What is the intent of the revision? Please answer with one of the labels: Claim, Fact/Evidence, Other. "\
                "Please always answer with the template and fill the template with your answer without additional texts:LABEL:<your answer> \n REASON:<your answer>.",
                'RL': "Please read the following old and new texts. "\
                "What is the intent of the revision? Please answer with one of the labels: Claim, Fact/Evidence, Other. "\
                "Please always answer with the template and fill the template with your answer without additional texts:REASON:<your answer> \n LABEL:<your answer>.",
                'L': "Please read the following old and new texts. "\
                "What is the intent of the revision? Please answer with one of the labels: Claim, Fact/Evidence, Other. "\
                "Please always answer with the template and fill the template with your answer without additional texts:LABEL:<your answer>.",
                }