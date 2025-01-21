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

@app.route('/receive_text', methods=['POST'])
def receive_text():
    data = request.json
    print('Received data:', data)
    text = data.get('text')
    if text:
        print(f"Received text: {text}")
            # Send the text to OpenAI to generate a poem
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful programming assistant."},
                    {"role": "user", "content": f"Complete the following Java code by providing me the remaining lines. Just give me the remaining lines in correct syntax. Do not give me the whole block of code: {text}"}
                ],
                max_tokens=300,
                temperature=0.7
            )
            # Extract the generated poem text from the response
            codeCompletion = response.choices[0].message.content
            print(f"Generated code: {codeCompletion}")
                        # Save the generated code to a file

            codeCompletion = codeCompletion.replace('```java\n', '').replace('```', '').strip()
            combinedCode = text + codeCompletion
            with open('GeneratedCode.java', 'w') as f:
                f.write(combinedCode)

            # Run the Python script to compile and test the code
            result = subprocess.run(['python', 'run_tests.py'], capture_output=True, text=True)

            # Parse the test results
            output = result.stdout
            errors = result.stderr
            print(f"output: {output}")
            print(f"errors: {errors}")

            accuracy = calculate_accuracy(output, errors)
            print(f"accuracy: {accuracy}")

            return jsonify({'status': 'success', 'message': 'Text received', 'code': codeCompletion, 'output': output, 'errors': errors}), 200
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