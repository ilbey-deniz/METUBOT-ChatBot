import json 

admin_json_path = "./questions_from_admin.json"

def reset_and_initialize_json(path):
    dict = {"qa-pairs":[]}
    write_json(dict,path)

    
def file_to_list(file):
    with open(file) as f:
        return [line.rstrip('\n') for line in f]

def add_questions_from_files(path, q_path, a_path, c_path, overwrite):
    if overwrite:
        reset_and_initialize_json(path)
    questions = file_to_list(q_path)
    answers = file_to_list(a_path)
    categories = file_to_list(c_path)
    dict = json.load(open(path))
    for i in range(len(questions)):
        dict["qa-pairs"].append({"question":questions[i].split("#"),"answer":answers[i].split("#"),"category":categories[i]})
    write_json(dict,path)

def add_questions_manually(questions, answers, category, path=admin_json_path):

    with open(path) as fp:
        dict_obj = json.load(fp)

    qa_pair = {
        "question": questions,
        "answer": answers,
        "category": category
    }
    dict_obj["qa-pairs"].append(qa_pair)

    write_json(dict_obj,path)

def add_alternative_question(question, answer):
    #TODO:
    ...


def write_json(dict,jsonfilepath):
	f = open(jsonfilepath, "w")
	json.dump(dict, f, indent=4, ensure_ascii=False)
	f.close()
	return

path = "../../Elasticsearch/qa_pairs.json"
q_path = "./questions.txt"
a_path = "./answers.txt"
c_path = "./categories.txt"

if __name__ == "__main__":
    add_questions_from_files(path,q_path,a_path,c_path, True)

