import json
from anyascii import anyascii 

admin_json_path = "./questions_from_admin.json"
qapairs_path = "../../Elasticsearch/qa_pairs.json"
qapairs_ascii_path = "../../nlp/fasttext/qa_pairs_ascii.json"
q_path = "./questions.txt"
a_path = "./answers.txt"
c_path = "./categories.txt"

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

def add_questions_from_files(path=qapairs_path, path2=qapairs_ascii_path, overwrite=True, q_path=q_path, a_path=a_path, c_path=c_path):
    if overwrite:
        reset_and_initialize_json(path)
        reset_and_initialize_json(path2)

    questions = file_to_list(q_path)
    answers = file_to_list(a_path)
    categories = file_to_list(c_path)

    dict = json.load(open(path))
    dict2 = json.load(open(path2))

    for i in range(len(questions)):
        dict["qa-pairs"].append({"question":questions[i].split("#"),"answer":answers[i].split("#"),"category":categories[i]})
        dict2["qa-pairs"].append({"question":anyascii(questions[i]).split("#"),"answer":anyascii(answers[i]).split("#"),"category":anyascii(categories[i])})
    write_json(dict,path)
    write_json(dict2,path2)


def add_questions_from_csv(path=qapairs_path, overwrite=True, q_path=q_path, a_path=a_path, c_path=c_path):
    #TODO:
    ...

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

def remove_single_question(question, path=qapairs_path): 
    with open(path) as f:
        dict = json.load(f)
    for pair in dict["qa_pairs"]:
        if question in pair["question"]:
            pair["question"].remove(question)
            return #only removes the first occurence

def remove_single_answer(answer, path=qapairs_path):  #removes first occurence of the answer
    with open(path) as f:
        dict = json.load(f)
    for pair in dict["qa_pairs"]:
        if answer in pair["answer"]:
            pair["answer"].remove(answer)
            return #only removes the first occurence

def remove_pair(): #removes the qa-pair
    #TODO:
    ...

def change_single_question(oldquestion, newquestion): 
    #TODO:
    ...

def change_single_answer(oldanswer, newanswer):
    #TODO:
    ...

def change_category(questionorpair, oldcategory, newcategory):
    #TODO:
    ...



def add_alternative_question(new_question, answer, path=qapairs_path): #to an existing qa-pair
    with open(path) as f:
        dict = json.load(f)
    for pair in dict["qa_pairs"]:
        if answer in pair["answer"]:
            pair["question"].append(new_question)
            return #only adds into first occurence

def add_alternative_answer(question, new_answer, path=qapairs_path): #to an existing qa-pair
    with open(path) as f:
        dict = json.load(f)
    for pair in dict["qa_pairs"]:
        if question in pair["question"]:
            pair["answer"].append(new_answer)
            return #only adds into first occurence




if __name__ == "__main__":
    add_questions_from_files()

