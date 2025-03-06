import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from openai import OpenAI

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

@app.route('/receive_text', methods=['POST'])
def receive_text():
    data = request.json
    print('Received data:', data)
    text = data.get('text')
    test_file = data.get('testFile')
    perform_accuracy_testing = data.get('performAccuracyTesting', False)
    use_correct_code = data.get('useCorrectCode', False)

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