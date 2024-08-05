B_INST, E_INST = "[INST] ", " [/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
B_OLD, E_OLD = "\n[OLD] ", " [/OLD]"
B_NEW, E_NEW = "\n[NEW] ", " [/NEW]"
EXAMPLE_START = "Examples: \n"
SYS_PROMPT = "You will read a review sentence. "\
            "Your task is to classify the sentence into one of the following classes: Yes, No. \n"\
            "Yes: the review sentence discusses weaknesses of the manuscript, or provides edit suggestions that can trigger revisions in the document.\n"\
            "No: the review sentence does not discuss weaknesses of the manuscript, and does not provide clear edit suggestions, which will possibly not trigger any revisions.\n\n"

DEF_L ="The text is: It merely multiplies the 50 examples without adding any new information. \n" \
      "LABEL: Yes \n\n" \
      "The text is: There are two typos in the first paragraph of the Discussion (detailed below) which should be revised. \n" \
      "LABEL: Yes \n\n" \
      "The text is: Nonetheless, in the absence of any positive sign of a stimulatory impact, this possibility cannot be ruled out and should probably be briefly discussed. \n" \
      "LABEL: Yes \n\n"\
      "The text is: The authors compare with CAD and show better in-domain and OOD performance. \n" \
      "LABEL: No \n\n"\
      

DEF_LR ="The text is: It merely multiplies the 50 examples without adding any new information. \n" \
      "LABEL: Yes \n" \
      "REASON: The sentence discusses the weakness in the processing of the examples, that might trigger changes in the document.  \n\n"\
      "The text is: There are two typos in the first paragraph of the Discussion (detailed below) which should be revised. \n" \
      "LABEL: Yes \n" \
      "REASON: The sentence provides a clear edit suggestion for grammar correction, which will most likely trigger some revisions. \n\n" \
      "The text is: Nonetheless, in the absence of any positive sign of a stimulatory impact, this possibility cannot be ruled out and should probably be briefly discussed. \n" \
      "LABEL: Yes \n"\
      "REASON: The sentence provides a clear edit suggestion that some discussion should be added, so the label is Yes. \n\n"\
      "The text is: The authors compare with CAD and show better in-domain and OOD performance. \n" \
      "LABEL: No \n"\
      "REASON: The sentence is a summary and general description of the manuscript. It neither discusses weaknesses nor provides clear edit suggestions. \n\n"

DEF_RL ="The text is: It merely multiplies the 50 examples without adding any new information. \n" \
      "REASON: The sentence discusses the weakness in the processing of the examples, that might trigger changes in the document.  \n"\
      "LABEL: Yes \n\n" \
      "The text is: There are two typos in the first paragraph of the Discussion (detailed below) which should be revised. \n" \
      "REASON: The sentence provides a clear edit suggestion for grammar correction, which will most likely trigger some revisions. \n" \
      "LABEL: Yes \n\n" \
      "The text is: Nonetheless, in the absence of any positive sign of a stimulatory impact, this possibility cannot be ruled out and should probably be briefly discussed. \n" \
      "REASON: The sentence provides a clear edit suggestion that some discussion should be added, so the label is Yes. \n"\
      "LABEL: Yes \n\n"\
      "The text is: The authors compare with CAD and show better in-domain and OOD performance. \n" \
      "REASON: The sentence is a summary and general description of the manuscript. It neither discusses weaknesses nor provides clear edit suggestions. \n"\
      "LABEL: No \n\n"

TASK_PROMPTS = {'LR': "Please read the following text. "\
                "Is the review sentence a comment that could trigger some revisions in the manuscript? Please answer with one of the labels: Yes, No. "\
                "Please always answer with the template and fill the template with your answer without additional texts:LABEL:<your answer> \n REASON:<your answer>.",
                'RL':"Please read the following text. "\
                "Is the review sentence a comment that could trigger some revisions in the manuscript? Please answer with one of the labels: Yes, No. "\
                "Please always answer with the template and fill the template with your answer without additional texts:REASON:<your answer> \n LABEL:<your answer>.",
                'L': "Please read the following text. "\
                "Is the review sentence a comment that could trigger some revisions in the manuscript? Please answer with one of the labels: Yes, No. "\
                "Please always answer with the template and fill the template with your answer without additional texts:LABEL:<your answer>.",
                }