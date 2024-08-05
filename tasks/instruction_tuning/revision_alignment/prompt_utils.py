B_INST, E_INST = "[INST] ", " [/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
B_OLD, E_OLD = "\n[OLD] ", " [/OLD]"
B_NEW, E_NEW = "\n[NEW] ", " [/NEW]"
EXAMPLE_START = "Examples: \n"
SYS_PROMPT = "You are a helpful, respectful and honest revision analysis assistant. " \
                            "You will read two texts taken from the new version and the old version of a document respectively. "\
                            "Your task is to analyze whether the two texts are aligned. If the two texts are two versions of the same text, and they have common content, then they are aligned (yes)."\
                            "If the two texts are not related to each other, and the content are very different, then there is no alignment (no). "\
                            "The answer can be one of the following labels: 'yes' means the two texts are aligned, 'no' means there is no alignment. \n\n"

DEF_L ="The old text is: We conclude by questioning the basic procedure of large-scale fine-tuning, and suggest focusing on zero-and few-shot learning.\n"\
      "The new text is: Finally, we question the basic procedure of large-scale fine-tuning, and suggest focusing on zero-and few-shot learning instead .\n"\
      "LABEL: yes \n\n"\
      "The old text is: For each (question, image) pair in the VQA dataset (left), VQA2.0 adds another image, for which the answer is different (right).\n"\
      "The new text is: However, we argue that following the human strategy of relying on a fallback option in cases of uncertainty will promote models' communication abilities.\n"\
      "LABEL: no \n\n"
      

DEF_LR ="The old text is: We conclude by questioning the basic procedure of large-scale fine-tuning, and suggest focusing on zero-and few-shot learning.\n"\
      "The new text is: Finally, we question the basic procedure of large-scale fine-tuning, and suggest focusing on zero-and few-shot learning instead .\n"\
      "LABEL: yes \n"\
      "REASON: The major part of the two texts are almost the same, so they are related to each other. The label is therefore yes. \n\n"\
      "The old text is: For each (question, image) pair in the VQA dataset (left), VQA2.0 adds another image, for which the answer is different (right).\n"\
      "The new text is: However, we argue that following the human strategy of relying on a fallback option in cases of uncertainty will promote models' communication abilities.\n"\
      "LABEL: no \n"\
      "REASON: The two texts do not share common content, and the topics are totally different. Therefore the label is no.\n\n"

DEF_RL ="The old text is: We conclude by questioning the basic procedure of large-scale fine-tuning, and suggest focusing on zero-and few-shot learning.\n"\
      "The new text is: Finally, we question the basic procedure of large-scale fine-tuning, and suggest focusing on zero-and few-shot learning instead .\n"\
      "REASON: The major part of the two texts are almost the same, so they are related to each other. The label is therefore yes. \n"\
      "LABEL: yes \n\n"\
      "The old text is: For each (question, image) pair in the VQA dataset (left), VQA2.0 adds another image, for which the answer is different (right).\n"\
      "The new text is: However, we argue that following the human strategy of relying on a fallback option in cases of uncertainty will promote models' communication abilities.\n"\
      "REASON: The two texts do not share common content, and the topics are totally different. Therefore the label is no.\n"\
      "LABEL: no \n\n"


TASK_PROMPTS = {'LR': "Please read the following old and new texts. "\
                "Are the two texts aligned? Please answer with one of the labels: yes, no. "\
                "Please always answer with the template and fill the template with your answer without additional texts:LABEL:<your answer> \n REASON:<your answer>.",
                'RL':"Please read the following old and new texts. "\
                "Are the two texts aligned? Please answer with one of the labels: yes, no. "\
                "Please always answer with the template and fill the template with your answer without additional texts:REASON:<your answer> \n LABEL:<your answer>.",
                'L': "Please read the following old and new texts. "\
                "Are the two texts aligned? Please answer with one of the labels: yes, no. "\
                "Please always answer with the template and fill the template with your answer without additional texts:LABEL:<your answer>.",
                }