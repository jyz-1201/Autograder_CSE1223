import csv
import subprocess
import os
import tempfile

# Define the student name and java CSV file index
JAVA_CSV_INDEX = [14, 18, 26]

# Define the user input
user_input = ["81\n4\nYuze\n",
              "81\n4\nYuze\n",
              "81\n4\nYuze\n"]  # Simulate user input, including a newline

# Define the expected output
expected_output = [["Enter the first:", "Enter the second:", "Enter your name:", "Yuze, the product is 324"],
                   ["Enter the first:", "Enter the second:", "Enter your name:", "Yuze, the sum is 85"],
                   ["Enter the first:", "Enter the second:", "Enter your name:", "Yuze, the difference is 77"],
                   ]

STU_CSV_INDEX = 0

JAVA_CLASS_NAME = "Main"

# Define the CSV file name
csv_file = "quiz_week2.csv"

# Create a directory to store temporary Java files
temp_dir = "temp_java_files"
os.makedirs(temp_dir, exist_ok=True)


# Function to compile and run Java code with fixed user input
def compile_and_run_java(java_code, user_input, expected_output):
    new_java_code = ""
    for char in java_code:
        if char == "\n":
            new_java_code += char
        else:
            new_java_code += " " if char.isspace() else char

    if new_java_code.find("import") == -1:
        new_java_code = "import java.util.Scanner;\npublic class Main {\n" + \
                        new_java_code + \
                        "\n}"

    # Generate a unique Java file name
    java_file = os.path.join(temp_dir, f"{JAVA_CLASS_NAME}.java")

    # Write the Java code to the temporary file
    with open(java_file, "w", encoding="utf-8") as f:
        f.write(new_java_code)

    # Remove Byte File if exists
    byte_file = os.path.join(temp_dir, f"{JAVA_CLASS_NAME}.class")

    if os.path.exists(byte_file):
        os.remove(byte_file)

    # Compile the Java program
    compile_command = f"javac {java_file}"
    compile_result = subprocess.run(compile_command, shell=True, stderr=subprocess.PIPE)

    # Check if compilation was successful
    if compile_result.returncode == 0:
        print("Java compilation successful!")

        # Run the Java program
        run_command = f"java -cp {temp_dir} {JAVA_CLASS_NAME}"
        run_result = subprocess.run(run_command, shell=True, input=user_input,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Print the Java program's output
        print("Java program output:")
        print(run_result.stdout)

        # Check correctness of students program
        correct = True
        for e in expected_output:
            if run_result.stdout.find(e) == -1:
                correct = False

        # Print test results
        if run_result.stdout is not "":
            if correct:
                print("GOOD ANSWER")
            else:
                print("WRONG ANSWER")

        # Check for errors
        if "Error" in run_result.stderr:
            print("Java program ENCOUNTERED AN ERROR:")
            print(run_result.stderr)
    else:
        print("Java COMPILATION FAILED.")
        print("Error message:")
        print(compile_result.stderr)

# Read the CSV file and process each row
with open(csv_file, mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row

    for row in csv_reader:
        # Extract the student name from the "STU_CSV_INDEX"-th column (assuming 0-based index)
        stu_name = row[STU_CSV_INDEX]

        for prog_id, input, output in zip(JAVA_CSV_INDEX, user_input, expected_output):
            # Extract the Java code from the "JAVA_CSV_INDEX"-th column (assuming 0-based index)
            java_code = row[prog_id]

            if java_code is not "":
                # Call the compile_and_run_java_with_fixed_input function to compile and run the Java code
                compile_and_run_java(java_code, input, output)

        print(f"Grading info above is for: {stu_name}")


# Clean up temporary Java files and directory
for file_name in os.listdir(temp_dir):
    file_path = os.path.join(temp_dir, file_name)
    os.remove(file_path)
os.rmdir(temp_dir)
