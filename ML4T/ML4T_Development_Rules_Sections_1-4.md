# Course Development Recommendations, Guidelines, and Rules

## Sections 1–4

---

# Section 1: Libraries and Code Usage

## Rule 1: Restrictions on the use of `os` and `argparse`

The `os` library provides extensive system-level capabilities, including file manipulation, process management, and interaction with the operating system. While powerful, these features can introduce risks and compatibility problems in the grading environment.

**The `os` library is prohibited.** Submission code intended for grading that uses `os` may receive a zero for part or all of the assignment.

The `argparse` library may only be used inside:

```python
if __name__ == "__main__":
```

This ensures command-line argument parsing is only executed when the file is run directly.

`argparse` must never be called, directly or indirectly, by functions, classes, or methods called by the autograder.

### Prohibited

```python
import os

data = os.path.join("data", "AAPL.csv")

with open(data, "r") as file:
    content = file.read()
```

This violates the rule because it uses `os` to construct file paths.

### Approved

```python
from util import get_data

data = get_data("AAPL.csv")

# Process the data as needed
```

This uses the course-provided `util.py` functionality instead.

**Exceptions:** None.

---

## Rule 2: Allowed Python libraries and packages

You may use:

- Any standard Python library **except `os`**
- Packages explicitly listed on the course Development Environment setup page

unless a project specifically prohibits them.

The goal is compatibility with the grading environment. Packages or versions not present in Gradescope may cause code to fail even if they work locally.

### Approved examples

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import random
```

### Prohibited examples

```python
import tensorflow as tf
import sklearn
```

These packages are not allowed unless explicitly permitted by the assignment.

**Exceptions:** Assignment instructions may prohibit specific packages, data types, or data structures.

---

## Rule 3: Course-provided or explicitly approved code

You may use code provided or explicitly allowed by the instructional staff.

Citation is not required for course-provided or explicitly approved code, although citation is encouraged as good practice.

**Exceptions:** None.

---

## Rule 4: Chart save locations

Charts may only be saved in:

```text
./
```

or:

```text
./images
```

The `./images` folder must be assumed to already exist in Gradescope. Your code must **not create it**.

Paths must be relative, not absolute.

If `./images` does not exist locally, you may create it manually, but your submitted code must not create it.

### Approved

```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3], [4, 5, 6])

plt.savefig("figure1.png")
plt.savefig("./figure1.png")
plt.savefig("./images/figure1.png")
```

### Prohibited

```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3], [4, 5, 6])

plt.savefig("./charts/figure1.png")
plt.savefig("project_folder/images/figure1.png")
plt.savefig("/users/gburdell/documents/ML4T_20XX/project_folder/images/figure1.png")
```

Only the current directory and `./images` are valid.

**Exceptions:** None.

---

## Rule 5: Maximum execution time

Scripts must execute within **10 minutes in Gradescope** unless an assignment specifies a different limit.

A chart-generating `.py` file must complete within the allowed execution window.

Timeouts may result in partial or full loss of credit.

**Exceptions:** None.

---

## Rule 6: Allowed result files

You may save only the following types of result files in the current directory:

```text
.txt
.html
.csv
```

They must follow the naming pattern:

```text
pX_results.txt
pX_results.html
pX_results.csv
```

where `X` is the project number.

For example, Project 8 may create:

```text
p8_results.txt
p8_results.html
p8_results.csv
```

You may create one of each allowed type.

Saving output to these files is recommended instead of printing large amounts of output to the terminal.

### Approved

```python
with open("p8_results.txt", "w") as txt_file:
    txt_file.write("Summary of results")

html_content = "<html><body><h1>Results</h1></body></html>"

with open("p8_results.html", "w") as html_file:
    html_file.write(html_content)

import pandas as pd

spreadsheet = pd.DataFrame({"Column1": [1, 2, 3]})
spreadsheet.to_csv("p8_results.csv", index=False)
```

### Prohibited

```python
with open("results.txt", "w") as txt_file:
    txt_file.write("Summary of results")
```

Incorrect filename.

```python
with open("project8_results.html", "w") as html_file:
    html_file.write("<html><body><h1>Results</h1></body></html>")
```

Incorrect filename.

```python
with open("p8_data.json", "w") as json_file:
    json_file.write('{"data": [1, 2, 3]}')
```

Incorrect file type and filename.

**Exceptions:** None.

---

# Section 2: Code Behavior and Output

## Rule 7: Do not print or display information in submitted code

Code submitted for grading must not print or display information to the console, screen, or terminal.

Gradescope runs submissions automatically without human interaction. Printing and interactive input can degrade performance or cause execution to hang.

### Approved

```python
with open("p3_results.txt", "w") as file:
    file.write("Results: 123\n")
```

### Prohibited

```python
print("Enter a number:")
number = input()
print(f"You entered: {number}")
```

This can cause the grading process to wait indefinitely for user input.

**Exceptions:** Assignment instructions may explicitly allow terminal output.

---

## Rule 8: Do not display charts

Submitted code must not cause charts to appear in a window.

For example, do **not** use:

```python
plt.show()
```

A chart window can cause execution to wait indefinitely for user interaction.

Instead, save charts to an approved location.

### Approved

```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3], [4, 5, 6])
plt.savefig("./figure1.png")
```

### Prohibited

```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3], [4, 5, 6])
plt.show()
```

**Exceptions:** None.

---

## Rule 9: Warning messages

Warning messages are acceptable and do not automatically result in point deductions.

However, students should investigate and address warnings when possible because they may indicate:

- Correctness issues
- Performance problems
- Potential bugs
- Poor coding practices

Suppressing warnings is not required.

**Exceptions:** None.

---

# Section 3: File Handling and Structure

## Rule 10: Do not create directories

Code must not create new directories.

You must maintain the course-provided directory hierarchy.

Although folder names may differ between environments, their relative relationships must remain unchanged.

Creating subfolders or changing the working directory structure may cause code to fail in Gradescope.

**Exceptions:** None.

---

## Rule 11: Stock symbols must be read using `util.py`

Stock symbol data must be read only through functions provided in the course-supplied `util.py`.

Other files may be read only using approaches allowed by the specific project instructions.

### Prohibited

```python
import os

data = os.path.join("data", "AAPL.csv")

with open(data, "r") as file:
    content = file.read()
```

### Approved

```python
from util import get_data

data = get_data("AAPL.csv")

# Process the data as needed
```

**Exceptions:** None.

---

## Rule 12: Do not move, edit, or copy environment files

You must not move, edit, or copy course environment files such as:

```text
util.py
grading/
```

into new locations.

You also may not recreate the file-reading functionality found in `util.py`.

The provided environment depends on its existing relative directory structure.

**Exceptions:** None.

---

## Rule 13: Do not use absolute imports for your own project folders

Your implementation must not use absolute import statements that reference your own project folder structure.

### Approved

```python
import DTLearner as dtl

def main():
    learner = dtl()
    print("DTLearner initialized.")

if __name__ == "__main__":
    main()
```

### Prohibited

```python
from assess_learners.DTLearner import DTLearner as dtl

def main():
    learner = dtl()
    print("DTLearner initialized.")

if __name__ == "__main__":
    main()
```

Imports such as:

```python
from matplotlib.pyplot import plot
```

are acceptable because they refer to the defined package structure of an external library rather than your own folder layout.

**Exceptions:** None.

---

# Section 4: Coding Standards and Practices

## Rule 14: No global variables

Code must not use global variables.

All code and variables should exist within:

- Functions
- Classes
- Methods

Global variables can create naming conflicts with the grading environment and make code harder to debug and test.

### Prohibited

```python
def increment():
    global x
    x += 1

def main():
    increment()
    print(x)

if __name__ == "__main__":
    x = 10
    main()
```

`x` is global because it is defined outside a function.

### Approved

```python
def increment(value):
    return value + 1

def main():
    x = 10
    x = increment(x)
    print(x)

if __name__ == "__main__":
    main()
```

**Exceptions:** None.

---

## Rule 15: No nested functions

Functions may not be defined inside other functions.

### Prohibited

```python
def outer_function():

    def inner_function():
        print("This is a nested function.")

    inner_function()
```

Methods inside classes are allowed:

```python
class ExampleClass:

    def valid_method(self):
        print("This is allowed.")
```

But methods may not contain nested functions:

```python
class ExampleClass:

    def invalid_method(self):

        def nested_function():
            print("This is not allowed.")

        nested_function()
```

Nested functions can complicate testing, debugging, and serialization/pickling.

**Exceptions:** None.

---

## Rule 16: No explicit multithreading or multiprocessing

Code must not explicitly use:

- `threading`
- `multiprocessing`
- Similar explicit parallel-processing mechanisms

These may interfere with the grading environment.

### Prohibited — threading

```python
import threading

def worker():
    print("Thread is running")

threads = []

for i in range(5):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()
```

### Prohibited — multiprocessing

```python
import multiprocessing

def worker():
    print("Process is running")

if __name__ == "__main__":

    processes = []

    for i in range(5):
        p = multiprocessing.Process(target=worker)
        processes.append(p)
        p.start()
```

**Exceptions:** None.

---

## Rule 17: Random seeds

Random seeds may not be set unless the project instructions explicitly allow them.

They must **never** be set inside a learner.

If a project permits a seed:

- Set it only once per package
- Use your Georgia Tech ID as the seed value
- Follow any project-specific requirements

Example seed:

```python
import random
random.seed(901234567)

import numpy as np
np.random.seed(901234567)
```

### Approved

```python
import random

random.seed(901234567)

# Continue with the rest of the program
```

### Prohibited — seed inside a learner

```python
class DTLearner:

    def __init__(self):
        pass

    def add_evidence(self, data):
        import random
        random.seed(901234567)
```

### Prohibited — resetting the seed repeatedly

```python
import random

for i in range(10):
    random.seed(901234567)
    print(random.randint(0, 100))
```

**Exceptions:** Assignment instructions may establish different seed requirements.

---

## Rule 18: Do not modify protected starter code

Code above the line:

```text
-----do not edit anything above this line---
```

must remain unchanged.

You may modify or delete code below that line.

Formatting tools such as Black may be used only if everything above the protected line—including non-printable characters—remains unchanged.

**Exceptions:** Assignment instructions may modify this rule.

---

# Quick Reference — Sections 1–4

## Libraries

- [ ] Do not use `os`
- [ ] Use `argparse` only inside `if __name__ == "__main__":`
- [ ] Use only standard Python libraries and approved course packages
- [ ] Course-provided code is allowed

## Files and Charts

- [ ] Save charts only to `./` or `./images`
- [ ] Do not create `./images` in submitted code
- [ ] Use only approved `pX_results.txt`, `.html`, or `.csv` result filenames
- [ ] Do not create directories
- [ ] Do not move/edit/copy `util.py` or grading files

## Runtime / Output

- [ ] Finish within 10 minutes unless the project says otherwise
- [ ] Do not print/display submitted output
- [ ] Do not use interactive `input()`
- [ ] Do not use `plt.show()`
- [ ] Save charts instead

## Imports / Data

- [ ] Read stock symbols through `util.py`
- [ ] Do not use absolute imports that reference your own project folder structure

## Code Structure

- [ ] No global variables
- [ ] No nested functions
- [ ] No explicit multithreading
- [ ] No explicit multiprocessing
- [ ] Set a random seed only if the project explicitly permits it
- [ ] Never set a seed inside a learner
- [ ] Do not modify code above the protected starter-code line

