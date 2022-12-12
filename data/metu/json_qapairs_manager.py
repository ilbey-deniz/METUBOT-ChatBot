import json 

def reset_and_initialize_json(path):
    dict = {"qa-pairs":[]}
    write_json(dict,path)

    
def file_to_list(file):
    with open(file) as f:
        return [line.rstrip('\n') for line in f]

def add_questions_from_files(path, q_path, a_path):
    questions = file_to_list(q_path)
    answers = file_to_list(a_path)
    dict = json.load(open(path))
    for i in range(len(questions)):
        dict["qa-pairs"].append({"question":questions[i],"answer":answers[i]})
    write_json(dict,path)

def add_questions_manually(path, question, answer):
    ...

def write_json(dict,jsonfilepath):
    json_string = json.dumps(dict)
    f = open(jsonfilepath, "w")
    f.write(json_string)
    f.close()
    return

path = "../../Elasticsearch/qa_pairs.json"
q_path = "./questions.txt"
a_path = "./answers.txt"
add_questions_from_files(path,q_path,a_path)