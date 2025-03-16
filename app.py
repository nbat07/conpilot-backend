import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from openai import OpenAI
import javalang
import random

app = Flask(__name__)
CORS(app)
client = OpenAI()

openai.api_key = os.getenv("OPENAI_API_KEY")

def calculate_accuracy(output, errors):
    if errors:
        return 0
    # Example: If all tests pass, return 100% accuracy
    return 100 if 'OK' in output else 0

def log_to_file(log_message):
    with open('terminalLog.txt', 'a') as log_file:
        log_file.write(log_message + '\n')

def choose_random_line(code_completion):
    lines = code_completion.split('\n')
    non_empty_lines = [line for line in lines if line.strip() and line.strip() not in ['{', '}']]
    if non_empty_lines:
        return random.choice(non_empty_lines)
    return None

def parse_and_replace_line_old(code_completion, chosen_line):
    try:
        tokens = javalang.tokenizer.tokenize(chosen_line)
        parser = javalang.parser.Parser(tokens)
        try:
            # Try to parse as an expression
            expression = parser.parse_expression()
            chosen_line_with_error = inject_error_into_line(expression)
            print(f"Chosen line with error: {expression}")
            parsed_code = ast_to_code_expression(chosen_line_with_error)
        except:
            # If parsing as an expression fails, try to parse as a statement
            statement = parser.parse_statement()
            chosen_line_with_error = inject_error_into_line(statement)
            print(f"Chosen line with error: {statement}")
            parsed_code = ast_to_code_statement(chosen_line_with_error, 0)
        return code_completion.replace(chosen_line, parsed_code)
    except Exception as e:
        print(f"Error parsing expression: {e}")
        return "Error" 

def parse_and_replace_line(code_completion, chosen_line):
    try:
        # Inject an error into the chosen line using string manipulation
        chosen_line_with_error = inject_error_into_line(chosen_line)
        print(f"Chosen line with error: {chosen_line_with_error}")
        # Replace the original line with the modified line in codeCompletion
        return code_completion.replace(chosen_line, chosen_line_with_error)
    except Exception as e:
        print(f"Error injecting error into line: {e}")
        return "Error"      
    
def inject_error_into_line(line):
    # Example error injection: Change binary operations, change 'for' to 'while', change 'return true' to 'return false'
    error_count = 0
    max_errors = 2
    injected_categories = set()

    def replace_and_count(line, old, new, category):
        nonlocal error_count
        if error_count < max_errors and old in line and category not in injected_categories:
            line = line.replace(old, new)
            error_count += 1
            injected_categories.add(category)
        return line
    
    def replace_method_arguments(line):
        nonlocal error_count
        if error_count < max_errors:
            import re
            pattern = r'(\.\w+)\(([^)]*)\)'
            matches = re.findall(pattern, line)
            for match in matches:
                method_call, args = match
                if args:
                    new_args = ', '.join(['0' for _ in args.split(',')])
                    line = line.replace(f"{method_call}({args})", f"{method_call}({new_args})")
                    error_count += 1
                    injected_categories.add('method_arguments')
                    if error_count >= max_errors:
                        break
        return line    

    # Method calls and instantiation
    line = replace_and_count(line, '.length', '.size()', 'method_calls')
    line = replace_and_count(line, 'new', '', 'method_calls')
    line = replace_method_arguments(line)

    # Off by one, calculation
    line = replace_and_count(line, '==', '=', 'off_by_one')
    line = replace_and_count(line, '>', '>=', 'off_by_one')
    line = replace_and_count(line, '<', '<=', 'off_by_one')
    line = replace_and_count(line, '&&', '||', 'off_by_one')
    line = replace_and_count(line, '||', '&&', 'off_by_one')
    line = replace_and_count(line, '/', '*', 'off_by_one')
    line = replace_and_count(line, '%', '/', 'off_by_one')
    line = replace_and_count(line, '+', '-', 'off_by_one')
    line = replace_and_count(line, '-', '+', 'off_by_one')
    line = replace_and_count(line, '*', '+', 'off_by_one')
    line = replace_and_count(line, '++', '--', 'off_by_one')
    line = replace_and_count(line, '--', '++', 'off_by_one')

    # Statements and returns
    line = replace_and_count(line, 'for', 'while', 'statements')
    line = replace_and_count(line, 'return true', 'return false', 'statements')
    line = replace_and_count(line, 'return false', 'return true', 'statements')
    line = replace_and_count(line, 'return', '', 'statements')

    # Types
    line = replace_and_count(line, 'String', 'char', 'types')
    line = replace_and_count(line, 'char', 'String', 'types')
    line = replace_and_count(line, 'int', 'double', 'types')
    line = replace_and_count(line, 'double', 'int', 'types')

    # Bracketing/syntax
    line = replace_and_count(line, '}', '', 'bracketing')
    line = replace_and_count(line, '{', '', 'bracketing')

    return line 

def inject_error_into_line_old(node):
    if isinstance(node, javalang.tree.BinaryOperation):
        if node.operator == '==':
            node.operator = '='
        elif node.operator == '>':
            node.operator = '>='
        elif node.operator == '<':
            node.operator = '<='
        elif node.operator == '&&':
            node.operator = '||'
        elif node.operator == '||':
            node.operator = '&&'
    return node  

def inject_error_into_ast(ast, start_line):
    # Example error injection: Swap an if with a while, or change a > to >=
    current_line = 1  # Initialize a counter for the current line number
    error_count = 0  # Initialize a counter for the number of errors injected
    max_errors = 2  # Maximum number of errors to inject

    for path, node in ast:
        # Update the current line number if the node has a position attribute
        if hasattr(node, 'position') and node.position:
            current_line = node.position.line

        # Skip nodes that are before the start line
        if current_line < start_line:
            continue

        # Stop injecting errors if the maximum number of errors has been reached
        if error_count >= max_errors:
            break

        if isinstance(node, javalang.tree.BinaryOperation):
            print(f"Found BinaryOperation with operator: {node.operator}")
            if node.operator == '>':
                node.operator = '>='
                print("Injected error: Changed > to >=")
                error_count += 1
            elif node.operator == '<':
                node.operator = '<='
                print("Injected error: Changed < to <=")
                error_count += 1
            elif node.operator == '==':
                node.operator = '='
                print("Injected error: Changed == to =")
                error_count += 1
            elif node.operator == '&&':
                node.operator = '||'
                print("Injected error: Changed && to ||")
                error_count += 1
            elif node.operator == '||':
                node.operator = '&&'
                print("Injected error: Changed || to &&")
                error_count += 1
        elif isinstance(node, javalang.tree.ReturnStatement) and isinstance(node.expression, javalang.tree.Literal) and node.expression.value == 'true':
            node.expression.value = 'false'
            print("Injected error: Changed return true to return false")
            error_count += 1
        elif isinstance(node, javalang.tree.VariableDeclarator): 
            # Change the type of the variable declaration safely
            parent = path[-2]
            if isinstance(parent, javalang.tree.VariableDeclaration) and parent.type:
                if parent.type.name == 'char':
                    parent.type.name = 'String'
                    print("Injected error: Changed type from char to String")
                elif parent.type.name == 'String':
                    parent.type.name = 'char'
                    print("Injected error: Changed type from String to char")
                elif parent.type.name == 'int':
                    parent.type.name = 'double'
                    print("Injected error: Changed type from int to double")
                elif parent.type.name == 'double':
                    parent.type.name = 'int'
                    print("Injected error: Changed type from double to int")
                else:
                    parent.type.name = 'UNKNOWN_TYPE'  # Instead of None, use a placeholder
                    print("Injected error: Changed type to UNKNOWN_TYPE")
                error_count += 1
    return ast

def ast_to_code(ast):
    # Convert the modified AST back to code
    code = []
    for path, node in ast:
        if isinstance(node, javalang.tree.ClassDeclaration):
            code.append(f"public class {node.name} {{")
            for member in node.body:
                code.append(ast_to_code_member(member))
            code.append("}")
    return '\n'.join(code)

def ast_to_code_member(node):
    if isinstance(node, javalang.tree.MethodDeclaration):
        modifiers = ' '.join(node.modifiers)
        return_type = node.return_type.name if node.return_type else 'void'
        parameters = ', '.join([f"{param.type.name} {param.name}" for param in node.parameters])
        body = '\n'.join([ast_to_code_statement(statement, 0) for statement in node.body])
        return f"{modifiers} {return_type} {node.name}({parameters}) {{\n{body}\n}}"
    elif isinstance(node, javalang.tree.FieldDeclaration):
        modifiers = ' '.join(node.modifiers)
        type_name = node.type.name
        variables = ', '.join([f"{var.name if hasattr(var, 'name') else 'UNKNOWN'} = {ast_to_code_expression(var.initializer) if var.initializer else ''}" for var in node.declarators])
        return f"{modifiers} {type_name} {variables};"
    elif isinstance(node, javalang.tree.VariableDeclaration):
        print(f"Processing VariableDeclaration: {node}")
        
        # Print out the declarators to see their structure
        print(f"Declarators: {node.declarators}")
        
        # Loop through each declarator and process it
        for var in node.declarators:
            print(f"Variable in declarator: {var}")
            # Check for name and initializer properly
            if hasattr(var, 'name'):
                print(f"Variable name: {var.name}")
            else:
                print(f"Variable does not have a 'name' attribute. Inspecting further...")
                print(f"Attributes of variable: {dir(var)}")
                print(f"Possible alternative identifier: {getattr(var, 'identifier', 'No identifier found')}")

            # Handle initializers
            if hasattr(var, 'initializer'):
                initializer = ast_to_code_expression(var.initializer)
                print(f"Initializer: {initializer}")
        type_name = node.type.name if hasattr(node, "type") and node.type else 'UNKNOWN_TYPE'
        variables = ', '.join([f"{var.name} = {ast_to_code_expression(var.initializer) if var.initializer else ''}" for var in node.declarators if hasattr(var, 'name')])
        return f"{type_name} {variables};"
    return ""

def ast_to_code_statement(node, indent_level):
    indent = ' ' * (indent_level * 4)
    if isinstance(node, javalang.tree.IfStatement):
        condition = ast_to_code_expression(node.condition)
        then_statement = ast_to_code_statement(node.then_statement, indent_level + 1)
        else_statement = ast_to_code_statement(node.else_statement, indent_level + 1) if node.else_statement else ''
        return f"{indent}if ({condition}) {{\n{then_statement}\n{indent}}}" + (f" else {{\n{else_statement}\n{indent}}}" if else_statement else '')
    elif isinstance(node, javalang.tree.ReturnStatement):
        expression = ast_to_code_expression(node.expression)
        return f"{indent}return {expression};"
    elif isinstance(node, javalang.tree.WhileStatement):
        condition = ast_to_code_expression(node.condition)
        body = '\n'.join([ast_to_code_statement(statement, indent_level + 1) for statement in node.body.statements]) if hasattr(node.body, 'statements') else ''
        return f"{indent}while ({condition}) {{\n{body}\n{indent}}}"
    elif isinstance(node, javalang.tree.ForStatement):
        if isinstance(node.control, javalang.tree.ForControl):
            init = ', '.join([ast_to_code_expression(init) for init in node.control.init]) if node.control.init else ''
            condition = ast_to_code_expression(node.control.condition) if node.control.condition else ''
            update = ', '.join([ast_to_code_expression(update) for update in node.control.update]) if node.control.update else ''
            body = '\n'.join([ast_to_code_statement(statement, indent_level + 1) for statement in node.body.statements]) if hasattr(node.body, 'statements') else ''
            return f"{indent}for ({init}; {condition}; {update}) {{\n{body}\n{indent}}}"
        elif isinstance(node.control, javalang.tree.EnhancedForControl):
            variable_type = node.control.var.type.name if node.control.var.type else ''
            variable_name = node.control.var.name if hasattr(node.control.var, 'name') else 'UNKNOWN_NAME'
            variable = f"{variable_type} {variable_name}"
            iterable = ast_to_code_expression(node.control.iterable)
            body = '\n'.join([ast_to_code_statement(statement, indent_level + 1) for statement in node.body.statements]) if hasattr(node.body, 'statements') else ''
            return f"{indent}for ({variable} : {iterable}) {{\n{body}\n{indent}}}"
    elif isinstance(node, javalang.tree.StatementExpression):
        return f"{indent}{ast_to_code_expression(node.expression)};"
    elif isinstance(node, javalang.tree.BlockStatement):
        body = '\n'.join([ast_to_code_statement(statement, indent_level) for statement in node.statements])
        return f"{body}"
    elif isinstance(node, javalang.tree.VariableDeclaration):
        print(f"Processing VariableDeclaration: {node}")
        
        # Loop through each declarator and process it
        variable_declarations = []
        for var in node.declarators:
            print(f"Variable in declarator: {var}")
            
            # Handle 'name' attribute safely
            if hasattr(var, 'name'):
                name = var.name
                print(f"Variable name: {name}")
            else:
                # If 'name' is missing, log it and proceed
                print(f"WARNING: Missing 'name' attribute in VariableDeclarator. Inspecting further...")
                print(f"Attributes of variable: {dir(var)}")
                name = "UNKNOWN_NAME"  # Fallback name
                print(f"Using fallback name: {name}")
            
            # Handle initializers
            initializer = ""
            if hasattr(var, 'initializer'):
                initializer = ast_to_code_expression(var.initializer)
                print(f"Initializer: {initializer}")
            else:
                print("No initializer found.")
            
            # Now, construct the variable code representation
            type_name = node.type.name if hasattr(node, "type") and node.type else 'UNKNOWN_TYPE'
            
            # Generate the code string for each variable
            variable_code = f"{type_name} {name}"
            if initializer:
                variable_code += f" = {initializer}"
            variable_code += ";"
            
            # Append the variable code to the list
            variable_declarations.append(variable_code)
        
        # Return the formatted result for all variable declarations
        return f"{indent}{' '.join(variable_declarations)}"
    elif isinstance(node, javalang.tree.BinaryOperation):  # Fixing i++
        left = ast_to_code_expression(node.operandl)
        right = ast_to_code_expression(node.operandr)
        return f"{left} {node.operator} {right}"
    elif isinstance(node, javalang.tree.UnaryOperation):  # Fixing unary operators like i++
        operand = ast_to_code_expression(node.operand)
        return f"{operand}{node.operator}" if node.postfix_operators else f"{node.operator}{operand}"
    return ""

def ast_to_code_expression(node):
    if isinstance(node, javalang.tree.BinaryOperation):
        left = ast_to_code_expression(node.operandl)
        right = ast_to_code_expression(node.operandr)
        return f"{left} {node.operator} {right}"
    elif isinstance(node, javalang.tree.MethodInvocation):
        qualifier = f"{ast_to_code_expression(node.qualifier)}." if node.qualifier else ""
        arguments = ', '.join([ast_to_code_expression(arg) for arg in node.arguments])
        print(f"MethodInvocation: {node.member}, Qualifier: {node.qualifier}")
        return f"{qualifier}{node.member}({arguments})"
    elif isinstance(node, javalang.tree.MemberReference):
        qualifier = f"{ast_to_code_expression(node.qualifier)}." if node.qualifier else ""
        print(f"MemberReference: {node.member}, Qualifier: {node.qualifier}")
        return f"{qualifier}{node.member}"
    elif isinstance(node, javalang.tree.Literal):
        return node.value
    elif isinstance(node, javalang.tree.Assignment):
        left = ast_to_code_expression(node.expressionl)
        right = ast_to_code_expression(node.value)
        return f"{left} {node.type} {right}"
    return ""


@app.route('/receive_text', methods=['POST'])
def receive_text():
    data = request.json
    print('Received data:', data)
    text = data.get('text')
    test_file = data.get('testFile')
    perform_accuracy_testing = data.get('performAccuracyTesting', False)
    use_correct_code = data.get('useCorrectCode', False)
    use_llm_injection = data.get('useLLMInjection', True)

    if text:
        print(f"Received text: {text}")
        print(f"Using test file: {test_file}")
        
        try:
            if perform_accuracy_testing:
                with open(test_file, 'r') as file:
                    test_cases = file.read()
            else:
                test_cases = ""

        except Exception as e:
            print(f"Error reading test file: {e}")
            log_to_file(f"Error reading test file: {e}")
            return jsonify({'status': 'error', 'message': 'Error reading test file'}), 500
    
        correct_examples = [
            {
                "prompt": "public class Greeting {\n    public static String greet(String name) {\n        // The function will greet the name with \"Hi\" and \"Bye\"\n",
                "completion": "        StringBuilder result = new StringBuilder();\n        result.append(\"Hi \").append(name).append(\"\\n\");\n        result.append(\"Bye \").append(name);\n        return result.toString();\n    }\n}"
            },
            {
                "prompt": "public class StringModifier {\n    public static String modifyString(String inp) {\n        int ni = inp.indexOf(\"not\");\n        int bi = inp.indexOf(\"bad\");\n\n        if (ni == -1) {\n            return inp;\n        } else if (bi == -1) {\n            return inp;\n        } else if (ni > bi) {\n            return inp;\n        } else {",
                "completion": "            bi = bi + \"bad\".length();\n            String op = inp.substring(0, ni) + \"good\" + inp.substring(bi);\n            return op;\n        }\n    }\n}",
            },
            {
                "prompt":  "public class BitcoinPasswordDecryptor {\n    public static int revNum(String n) {\n        return Integer.parseInt(new StringBuilder(n).reverse().toString());\n    }\n\n    public static boolean isPrime(int n) {\n        if (n == 2) {\n            return true;\n        }\n        if (n == 1 || n % 2 == 0) {\n            return false;\n        }\n        for (int i = 3; i * i <= n; i += 2) {\n            if (n % i == 0) {\n                return false;\n            }\n        }\n        return true;\n    }\n\n    public static int decryptPassword(String input) {\n        String[] parts = input.split(\",\");\n        int a = Integer.parseInt(parts[0].trim());\n        int b = Integer.parseInt(parts[1].trim());\n\n        int c = revNum(String.valueOf(a));\n        int d = revNum(String.valueOf(b));\n\n        if (isPrime(c)) {",
                "completion":  "            if (isPrime(d)) {\n                return c + d;\n            } else {\n                return a + b;\n            }\n        } else {\n            if (isPrime(d)) {\n                return a + b;\n            } else {\n                return a * b;\n            }\n        }\n    }\n}",
            }
        ] 
            
        few_shot_correct_prompt = ""
        for example in correct_examples:
            few_shot_correct_prompt += f"Example incomplete novice student code prompt:\n{example['prompt']}\nExample completion provided by you:\n{example['completion']}\n\n"
        
        incorrect_examples = [
            {
                "prompt": "public class Greeting {\n    public static String greet(String name) {\n        // The function will greet the name with \"Hi\" and \"Bye\"\n",
                "completion": "        result = new StringBuilder();\n        result.append(\"Hi \").append(name).append(\"\\n\");\n        result.append(\"Bye \").append(name);\n        return result.toString();\n    }\n}"
            },
            {
                "prompt": "public class StringModifier {\n    public static String modifyString(String inp) {\n        int ni = inp.indexOf(\"not\");\n        int bi = inp.indexOf(\"bad\");\n\n        if (ni == -1) {\n            return inp;\n",
                "completion": "        } else if (bi = -1) {\n            return inp;\n        } else if (ni > bi) {\n            return inp;\n        } else {\n             bi = bi + \"bad\".length();\n            String op = inp.substring(0, ni) + \"good\" + inp.substring(bi);\n            return op;\n        }\n    }\n}",
            },
            {
                "prompt":  "public class BitcoinPasswordDecryptor {\n    public static int revNum(String n) {\n        return Integer.parseInt(new StringBuilder(n).reverse().toString());\n    }\n\n    public static boolean isPrime(int n) {\n        if (n == 2) {\n            return true;\n        }\n        if (n == 1 || n % 2 == 0) {\n            return false;\n        }\n        for (int i = 3; i * i <= n; i += 2) {\n            if (n % i == 0) {\n                return false;\n            }\n        }\n        return true;\n    }\n\n    public static int decryptPassword(String input) {\n        String[] parts = input.split(\",\");\n        int a = Integer.parseInt(parts[0].trim());\n        int b = Integer.parseInt(parts[1].trim());\n\n        int c = revNum(String.valueOf(a));\n        int d = revNum(String.valueOf(b));\n\n        if (isPrime(c)) {",
                "completion":  "            if (isPrime(d)) {\n                return c + d;\n            } else {\n                return a + b;\n            }\n        } else {\n            if (isPrime(d)) {\n                return true;\n            } else {\n                return a * b;\n            }\n        }\n    }\n}",
            }
        ]

        few_shot_incorrect_prompt = ""
        for example in incorrect_examples:
            few_shot_incorrect_prompt += f"Example incomplete novice student code prompt:\n{example['prompt']}\nExample error injected completion provided by you:\n{example['completion']}\n\n"

        correctSystem = "You are a helpful programming assistant."
        correctUser = f"Complete the following Java code by providing me the remaining lines. Just give me the remaining lines in correct syntax. Do not give me the whole block of code. Do not add any comments, just give the remaining lines of code in correct syntax: {text}"
        
        incorrectSystem = "You are a helpful programming assistant developed to force novice students engage with code by injecting errors into your completions. You provide only the remaining lines of properly syntaxed Java code as your response but you purposely inject an error into your completion. You work by injecting one SEMANTIC error into your completion, examples of error types are: 1) use a variable without initializing it, 2)assign a variable the wrong type (type mismatch), 3) use an incorrect argument for a functional call, or 4) use comparision instead of operator or vice versa. Just give me the remaining lines with the error injected, in correct syntax. You do NOT add any comments saying what error has been injected or where as students are supposed to identify this themselves. Here are some examples of incomplete code prompts you can get and the error injected completions you can provide in json format - Obviously, you have to return the answer in Java, correctly syntaxed, not json: "+ few_shot_incorrect_prompt
        incorrectUser = f"Complete the following Java code by providing me the remaining lines in correct syntax. Purposely make a semantic error in the remaining lines of code you write. Do not add any comments.: {text}"
        
        try:
            if use_llm_injection:
                system_message = correctSystem if use_correct_code else incorrectSystem
                user_message = correctUser if use_correct_code else incorrectUser
                
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )
                # Extract the generated poem text from the response
                codeCompletion = response.choices[0].message.content
                print(f"Generated code: {codeCompletion}")

                codeCompletion = codeCompletion.replace('```java\n', '').replace('```', '').strip()
                combinedCode = text + codeCompletion

            else:
                system_message = correctSystem 
                user_message = correctUser 
                
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )
                # Extract the generated poem text from the response
                codeCompletion = response.choices[0].message.content
                print(f"Generated code: {codeCompletion}")

                codeCompletion = codeCompletion.replace('```java\n', '').replace('```', '').strip()
                # Add missing closing braces for method and class
                chosen_line = choose_random_line(codeCompletion)
                if chosen_line:
                    print(f"Chosen line for parsing: {chosen_line}")
                    codeCompletion = parse_and_replace_line(codeCompletion, chosen_line)
                    print(f"Code completion after parsing and replacing line: {codeCompletion}")

                # Add missing closing braces for method and class
                combinedCode = text + "\n" + codeCompletion
                print("Combined code for parsing:")
                print(combinedCode)
                

            if perform_accuracy_testing:
                generated_code_file = test_file.replace('Test.java', '.java')
                with open(generated_code_file, 'w') as f:
                    f.write(combinedCode)

                # Run the Python script to compile and test the code
                result = subprocess.run(['python', 'run_tests.py', test_file], capture_output=True, text=True)

                # Parse the test results
                output = result.stdout
                errors = result.stderr
                print(f"output: {output}")
                print(f"errors: {errors}")

                accuracy = calculate_accuracy(output, errors)
                print(f"accuracy: {accuracy}")

                return jsonify({'status': 'success', 'message': 'Text received', 'code': codeCompletion, 'output': output, 'errors': errors}), 200
            else:
                return jsonify({'status': 'success', 'message': 'Text received', 'code': codeCompletion}), 200
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return jsonify({'status': 'error', 'message': 'OpenAI API error'}), 500
    else:
        return jsonify({'status': 'error', 'message': 'No text received'}), 400

if __name__ == '__main__':
    app.run(port=5000)


'''
from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
import os
import logging

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Initialize OpenAI API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    logging.error("OPENAI_API_KEY environment variable not set")
    raise ValueError("OPENAI_API_KEY environment variable not set")
openai.api_key = openai_api_key

@app.route('/complete', methods=['POST'])
def complete_code():
    try:
        # Get the code context from the frontend
        data = request.json
        code_context = data.get('codeContext')
        logging.info(f"Received code context: {code_context}")

        if not code_context:
            return jsonify({'error': 'No code context provided'}), 400
        
        # Call OpenAI API for code completion
        completion = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful coding assistant."},
                {"role": "user", "content": code_context}
            ],
            max_tokens=100,
            temperature=0.5
        )

        completion_text = completion.choices[0].message['content'].strip()
        logging.info(f"Completion received: {completion_text}")
        
        return jsonify({'completions': [completion_text]})
    
    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        return jsonify({'error': 'OpenAI API error'}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
'''