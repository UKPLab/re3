B_INST, E_INST = "[INST] ", " [/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
B_OLD, E_OLD = "\n[OLD] ", " [/OLD]"
B_NEW, E_NEW = "\n[NEW] ", " [/NEW]"
EXAMPLE_START = "Examples: \n"
SYS_PROMPT = "You are a helpful, respectful and honest revision analysis assistant.  " \
            "You will read two versions of texts. "\
            "Your task is to analyze the revision intent behind the diffreneces of the two texts."\
            "The intent can be one of the following labels: fix grammar (Grammar), improve clarity (Clarity), " \
             "change claim or statement(Claim), change factual information (Fact/Evidence). " \
             "Grammar and Clarity are more about surface language improvements, " \
             "while Fact/Evidence and Claim are more about meaning changes. "\
            "If none of the above labels are relevant, please answer with 'Other'. "
DEF_L = "The old text is: Recent work have shown that deep learning models in NLP are highly sensitive to lowlevel correlations between simple features and specific output labels, leading to overfitting and lack of generalization. \n" \
            "The new text is: Recent work has shown that deep learning models in NLP are highly sensitive to low-level correlations between simple features and specific output labels, leading to overfitting and lack of generalization. \n"\
            "LABEL: Grammar \n\n" \
            "The old text is: A naive way to eliminate spurious correlations is to stop using large-scale datasets altogether. \n" \
            "The new text is: A naive way to mitigate spurious correlations is to stop using large-scale datasets altogether. \n" \
            "LABEL: Clarity \n\n"\
            "The old text is: The 2-STAGE system is generally on par with the 3-STAGE system (or better), which indicates that implicit aggregation using the PC-AGG model may be sufficient. \n" \
            "The new text is: The 2-STAGE system is generally on par with the 3-STAGE system or better, which indicates that explicit aggregation using the AGG model may not be necessary. \n" \
            "LABEL: Claim \n\n"\
            "The old text is: Empirical studies on the datasets across 7 different languages confirm the effectiveness of the proposed model. \n" \
            "The new text is: Empirical studies on the three datasets across 7 different languages confirm the effectiveness of the proposed model. \n" \
            "LABEL: Fact/Evidence \n\n"\
            "The old text is: Entity Recognizer \n" \
            "The new text is: Entity Recognizer Teacher \n" \
            "LABEL: Other \n\n"
DEF_LR= "The old text is: Recent work have shown that deep learning models in NLP are highly sensitive to lowlevel correlations between simple features and specific output labels, leading to overfitting and lack of generalization. \n" \
            "The new text is: Recent work has shown that deep learning models in NLP are highly sensitive to low-level correlations between simple features and specific output labels, leading to overfitting and lack of generalization. \n"\
            "LABEL: Grammar \n" \
            "REASON: The old text has two grammar errors: 'have' should be 'has' and 'lowlevel' should be 'low-level', which have been corrected. The revision intent is therefore Grammar. \n\n"\
            "The old text is: A naive way to eliminate spurious correlations is to stop using large-scale datasets altogether. \n" \
            "The new text is: A naive way to mitigate spurious correlations is to stop using large-scale datasets altogether. \n" \
            "LABEL: Clarity \n"\
            "REASON: The dominant intent is to improve clarity of the text by changing the word 'eliminate' to 'mitigate', while the meaning of the text is not changed. \n\n"\
            "The old text is: The 2-STAGE system is generally on par with the 3-STAGE system (or better), which indicates that implicit aggregation using the PC-AGG model may be sufficient. \n" \
            "The new text is: The 2-STAGE system is generally on par with the 3-STAGE system or better, which indicates that explicit aggregation using the AGG model may not be necessary. \n" \
            "LABEL: Claim \n"\
            "REASON: The main change is in the later clause, which is a statement based on the fact in the first clause. The statement is changed so the revision intent laebl is Claim. \n\n"\
            "The old text is: Empirical studies on the datasets across 7 different languages confirm the effectiveness of the proposed model. \n" \
            "The new text is: Empirical studies on the three datasets across 7 different languages confirm the effectiveness of the proposed model. \n" \
            "LABEL: Fact/Evidence \n"\
            "REASON: The factual information that the empirmal studies are conducted on 'three' datasets is added to the text, which is a Fact/Evidence revision. \n\n"\
            "The old text is: Entity Recognizer \n" \
            "The new text is: Entity Recognizer Teacher \n" \
            "LABEL: Other \n"\
            "REASON: The section title is changed by adding the word 'Teacher'. However, the old text doesn't have grammar errors, and it is not hard to understand so it is not a clarity change. And it refers to the same model so the meaning is not changed. The label is therfore Other. \n\n"
DEF_RL= "The old text is: Recent work have shown that deep learning models in NLP are highly sensitive to lowlevel correlations between simple features and specific output labels, leading to overfitting and lack of generalization. \n" \
            "The new text is: Recent work has shown that deep learning models in NLP are highly sensitive to low-level correlations between simple features and specific output labels, leading to overfitting and lack of generalization. \n"\
            "REASON: The old text has two grammar errors: 'have' should be 'has' and 'lowlevel' should be 'low-level', which have been corrected. The revision intent is therefore Grammar. \n"\
            "LABEL: Grammar \n\n" \
            "The old text is: A naive way to eliminate spurious correlations is to stop using large-scale datasets altogether. \n" \
            "The new text is: A naive way to mitigate spurious correlations is to stop using large-scale datasets altogether. \n" \
            "REASON: The dominant intent is to improve clarity of the text by changing the word 'eliminate' to 'mitigate', while the meaning of the text is not changed. \n"\
            "LABEL: Clarity \n\n"\
            "The old text is: The 2-STAGE system is generally on par with the 3-STAGE system (or better), which indicates that implicit aggregation using the PC-AGG model may be sufficient. \n" \
            "The new text is: The 2-STAGE system is generally on par with the 3-STAGE system or better, which indicates that explicit aggregation using the AGG model may not be necessary. \n" \
            "REASON: The main change is in the later clause, which is a statement based on the fact in the first clause. The statement is changed so the revision intent laebl is Claim. \n"\
            "LABEL: Claim \n\n"\
            "The old text is: Empirical studies on the datasets across 7 different languages confirm the effectiveness of the proposed model. \n" \
            "The new text is: Empirical studies on the three datasets across 7 different languages confirm the effectiveness of the proposed model. \n" \
            "REASON: The factual information that the empirmal studies are conducted on 'three' datasets is added to the text, which is a Fact/Evidence revision. \n"\
            "LABEL: Fact/Evidence \n\n"\
            "The old text is: Entity Recognizer \n" \
            "The new text is: Entity Recognizer Teacher \n" \
            "REASON: The section title is changed by adding the word 'Teacher'. However, the old text doesn't have grammar errors, and it is not hard to understand so it is not a clarity change. And it refers to the same model so the meaning is not changed. The label is therfore Other. \n" \
            "LABEL: Other \n\n"
TASK_PROMPTS = {'LR': "Please read the following old and new texts. "\
                "What is the intent of the revision? Please answer with one of the labels: Grammar, Clarity, Claim, Fact/Evidence and Other. "\
                "Please always answer with the template and fill the template with your answer without additional texts:LABEL:<your answer> \n REASON:<your answer>.",
                'RL':"Please read the following old and new texts. "\
                "What is the intent of the revision? Please answer with one of the labels: Grammar, Clarity, Claim, Fact/Evidence and Other. "\
                "Please always answer with the template and fill the template with your answer without additional texts:REASON:<your answer> \n LABEL:<your answer>.",
                'L': "Please read the following old and new texts. " \
                      "What is the intent of the revision? Please answer with one of the labels: Grammar, Clarity, Claim, Fact/Evidence and Other. " \
                      "Please always answer with the template and fill the template with your answer without additional texts:LABEL:<your answer>",
                }