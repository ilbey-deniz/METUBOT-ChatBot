import json
import pandas as pd


admin_json_path = "./questions_from_admin.json"
qapairs_path = "../../Elasticsearch/qa_pairs.json"
qapairs_ascii_path = "../../nlp/fasttext/qa_pairs_ascii.json"
excel_path = "./metubot.xlsx"
q_path = "./questions.txt"
a_path = "./answers.txt"
c_path = "./categories.txt"

#THREE HELPERS
def reset_and_initialize_json(path):
    dict = {"qa-pairs":[]}
    write_json(dict,path)    
def file_to_list(file):
    with open(file) as f:
        return [line.rstrip('\n') for line in f]
def write_json(dict,jsonfilepath):
	f = open(jsonfilepath, "w")
	json.dump(dict, f, indent=4, ensure_ascii=False)
	f.close()
	return

#FILL JSON VIA DIFFERENT METHODS
def add_questions_from_files(path=qapairs_path, overwrite=True, q_path=q_path, a_path=a_path, c_path=c_path):
    if overwrite:
        reset_and_initialize_json(path)

    questions = file_to_list(q_path)
    answers = file_to_list(a_path)
    categories = file_to_list(c_path)

    dict = json.load(open(path))

    for i in range(len(questions)):
        dict["qa-pairs"].append({"question":questions[i].split("#"),"answer":answers[i].split("#"),"category":categories[i]})
    write_json(dict,path)

def add_questions_from_excel(path=qapairs_path, qpath=excel_path, overwrite=False):
    if overwrite:
        reset_and_initialize_json(path)

    d = pd.read_excel(qpath)
    q = d['questions'].values.tolist()
    a = d['answers'].values.tolist()
    c = d['categories'].values.tolist()

    dict = json.load(open(path))
    for i in range(len(q)):
        dict["qa-pairs"].append({"question":q[i],"answer":a[i],"category":c[i]})
    write_json(dict,path)

    
def add_questions_manually(questions, answers, category, path=admin_json_path):
    #add new question with 1 question 1 answer and category.
    #for adding more questions and answers to the same pair, use add_alternative_question function
    with open(path) as fp:
        dict_obj = json.load(fp)

    qa_pair = {
        "question": questions,
        "answer": answers,
        "category": category
    }
    dict_obj["qa-pairs"].append(qa_pair)
    write_json(dict_obj,path)

#A COMPREHENSIVE FUNCTION TO ALLOW ADMIN TO MANIPUATE QUESTION
def edit_questions(mode, structure_type, old=None, new=None, path=qapairs_path):
    with open(path) as f:
        dict = json.load(f)

    def remove_single_question(question): 
        for pair in dict["qa_pairs"]:
            if question in pair["question"]:
                pair["question"].remove(question)
                print("SUCCESS")
                return #only removes the first occurence
        print("There's no such question to remove question")
    def remove_single_answer(answer):  #removes first occurence of the answer
        for pair in dict["qa_pairs"]:
            if answer in pair["answer"]:
                pair["answer"].remove(answer)
                print("SUCCESS")
                return #only removes the first occurence
        print("There's no such answer to remove answer")
    def remove_pair(questionorpair): #removes the qa-pair
        for pair in dict["qa_pairs"]:
            if questionorpair == pair or questionorpair in pair["question"]:
                dict["qa_pairs"].remove(pair)
                print("SUCCESS")
                return
        print("There's no such pair/question to remove pair")
    def change_single_question(oldquestion, newquestion): 
        for pair in dict["qa_pairs"]:
            if oldquestion in pair["question"]:
                pair["question"].remove(oldquestion)
                pair["question"].remove(newquestion)
                print("SUCCESS")
                return #only removes the first occurence
        print("There's no such old question to change")
    def change_single_answer(oldanswer, newanswer):
        for pair in dict["qa_pairs"]:
            if oldanswer in pair["answer"]:
                pair["answer"].remove(oldanswer)
                pair["answer"].append(newanswer)
                print("SUCCESS")
                return #only removes the first occurence
        print("There's no such old answer to change")
    def change_category(questionorpair, newcategory):
        for pair in dict["qa_pairs"]:
            if questionorpair == pair or questionorpair in pair["question"]:
                pair["category"] = newcategory
                print("SUCCESS")
                return #only changes the first occurence
        print("There's no such pair/question to change its category")
    def add_alternative_question(answer, newquestion): #to an existing qa-pair
        for pair in dict["qa_pairs"]:
            if answer in pair["answer"]:
                pair["question"].append(newquestion)
                print("SUCCESS")
                return #only adds into first occurence
        print("There's no such old answer to add its question")
    def add_alternative_answer(question, newanswer): #to an existing qa-pair
        for pair in dict["qa_pairs"]:
            if question in pair["question"]:
                pair["answer"].append(newanswer)
                print("SUCCESS")
                return #only adds into first occurence
        print("There's no such old question to add its answer")

    if mode == "change" or mode == "swap" or mode == "replace":
        if structure_type == "question":
            change_single_question(old, new)
        elif structure_type == "answer":
            change_single_answer(old, new)
        elif structure_type == "category":
            change_category(old, new) #note that old should be a question (str) or a pair (dict)
        else:
            print("UNKNOWN STRUCTURE TYPE, NOTHING WAS REPLACED")
    elif mode == "add" or mode == "insert" or mode == "append":
        if structure_type == "question":
            add_alternative_question(old,new) #note that old should be an answer (str)
        elif structure_type == "answer":
            add_alternative_answer(old,new)#note that old should be a question (str)
        else:
            print("UNKNOWN STRUCTURE TYPE, NOTHING WAS ADDED")
    elif mode == "remove" or mode == "delete":
        if structure_type == "question":
            remove_single_question(old)
        elif structure_type == "answer":
            remove_single_answer(old)
        elif structure_type == "pair":
            remove_pair(old) #note that old should be a question (str) or a pair (dict)
        else:
            print("UNKNOWN STRUCTURE TYPE, NOTHING WAS REMOVED")
    else:
        print("UNKNOWN MODE, NOTHING WAS EDITED")




if __name__ == "__main__":
    add_questions_from_files()

add_questions_from_excel()
