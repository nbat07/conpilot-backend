import subprocess
import os
import sys

def run_tests(test_file):

    junit_jar = 'C:/Users/nehal/ConPilotPrototype/conpilot backend/lib/junit-4.13.2.jar'
    hamcrest_jar = 'C:/Users/nehal/ConPilotPrototype/conpilot backend/lib/hamcrest-core-1.3.jar'

    # Determine the name of the generated code file
    generated_code_file = test_file.replace('Test.java', '.java')

    # Compile the generated code
    compile_process = subprocess.run(['javac', '-cp', f'{junit_jar};{hamcrest_jar}', generated_code_file, test_file], capture_output=True, text=True)
    
    if compile_process.returncode != 0:
        return {'output': '', 'errors': compile_process.stderr}

    test_class = test_file.replace('.java', '')
    # Run the JUnit tests
    test_process = subprocess.run(['java', '-cp', f'.;{junit_jar};{hamcrest_jar}', 'org.junit.runner.JUnitCore', test_class], capture_output=True, text=True)
    
    return {'output': test_process.stdout, 'errors': test_process.stderr}

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python run_tests.py <test_file>")
        sys.exit(1)
    test_file = sys.argv[1]
    result = run_tests(test_file)
    print(result)