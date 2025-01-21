import subprocess
import os
import sys

def run_tests():

    junit_jar = 'C:/Users/nehal/ConPilotPrototype/conpilot backend/lib/junit-4.13.2.jar'
    hamcrest_jar = 'C:/Users/nehal/ConPilotPrototype/conpilot backend/lib/hamcrest-core-1.3.jar'

    # Compile the generated code
    compile_process = subprocess.run(['javac', '-cp', f'{junit_jar};{hamcrest_jar}', 'GeneratedCode.java', 'GeneratedCodeTest.java'], capture_output=True, text=True)
    
    if compile_process.returncode != 0:
        return {'output': '', 'errors': compile_process.stderr}

    # Run the JUnit tests
    test_process = subprocess.run(['java', '-cp', f'.;{junit_jar};{hamcrest_jar}', 'org.junit.runner.JUnitCore', 'GeneratedCodeTest'], capture_output=True, text=True)
    
    return {'output': test_process.stdout, 'errors': test_process.stderr}

if __name__ == '__main__':
    result = run_tests()
    print(result)