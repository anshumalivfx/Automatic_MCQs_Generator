import pandas as pd
from pandas import DataFrame
import re
import random
import string
from parrot.parrot import Parrot


parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)



def modify_question(ques: str) -> str:
    # Regular expressions to match variable, class, and function names
    variable_pattern:str = r'\b(int|double|float|char|bool)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*;'
    class_pattern:str = r'\bclass\s+([a-zA-Z_][a-zA-Z0-9_]*)\b'
    function_pattern:str = r'\b(int|double|float|char|bool)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*)\)\s*{'
    inherit_pattern:str = r'\bclass\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*public\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*{'
    # new object created pattern eg :- B b;
    new_object_pattern:str = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*;'
    # Objects calling functions pattern eg :- b.func();
    object_function_pattern:str = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*)\)\s*;'
    
    function_declaration_pattern:str = r'\b(int|double|float|char|bool|void)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*)\)\s*;'
    pattern = r"(?i)(?:what|how|when|why|which|who|whom|where|can|do|is)\s.*[?].*"
    
    
    # Function to generate random word
    def generate_random_word() -> str:
        prefix:str = random.choice(['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta'])
        suffix = ''.join(random.choices(string.ascii_uppercase, k=random.randint(1, 3)))
        return f'{prefix}{suffix}'
    
    def random_letter() -> str:
        return random.choice(string.ascii_lowercase)
    

    # Replace variable, class, and function names with random words
    # Does code have classes
    replaced_code = ques
    
    
    if re.search(pattern, ques):
        # Replace class names with random words
        questions = re.findall(pattern, ques)
        print(questions[0])
        new_questions = parrot.augment(input_phrase=questions[0], use_gpu=False)
        # choose any random from the new_questions that is a list of tuples 
        if new_questions:
            new_question = random.choice(new_questions)
            new_question = new_question[0]
            replaced_code = re.sub(pattern, new_question, ques)
    
    
    if re.search(class_pattern, ques):
        # Replace class names with random words
        new_class_name = generate_random_word()
        replaced_code = re.sub(class_pattern, 'class ' + new_class_name, ques)
        
        # Does code have inheritance
        if re.search(inherit_pattern, replaced_code):
            # Replace inheritance names with random words
            replaced_code = re.sub(inherit_pattern, 'class ' + generate_random_word() + ' : public ' + new_class_name, replaced_code)
    # Doe
    # Does code have functions
    if re.search(function_pattern, replaced_code):
        # Replace function names with random words
        replaced_code = re.sub(function_pattern, 'int ' + generate_random_word() + '()', replaced_code)
        
    # Does code have function declarations
    if re.search(function_declaration_pattern, replaced_code):
        # Replace function names with random words
        replaced_code = re.sub(function_declaration_pattern, 'int ' + generate_random_word() + '();', replaced_code)
        
    # Does code have variables
    if re.search(variable_pattern, replaced_code):
        # Replace variable names with random words
        replaced_code = re.sub(variable_pattern, 'int ' + random_letter() + ';', replaced_code)
        
    # Does code have new objects
    if re.search(new_object_pattern, replaced_code):
        # Replace new object names with random words with new class names
        object_name = random_letter()
        replaced_code = re.sub(new_object_pattern, new_class_name + ' ' + object_name + ';', replaced_code)
    
    # Does code have objects calling functions
    if re.search(object_function_pattern, replaced_code):
        # Replace object names with random words
        replaced_code = re.sub(object_function_pattern, object_name + '.' + generate_random_word() + '();', replaced_code)
    return replaced_code



def generate_question(input_ques: DataFrame) -> str:
    print("Hello")
    ques:str = ""
    for i in range(len(input_ques)):
        ques += f"Q.{i+1} " + modify_question(input_ques.iloc[i]['question']) + "<br/><br/>" + "A." + str(input_ques.iloc[i]['a']) + "<br/>" + "B." + str(input_ques.iloc[i]['b']) + "<br />" + "C." + str(input_ques.iloc[i]['c']) + "<br/>" + "D." + str(input_ques.iloc[i]['d']) + "<br /><br/>"

    return ques