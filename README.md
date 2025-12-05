## 🚀 Burst Coding Language

Burst is a new **statically-typed** coding language, initially developed in July 2024, with a core philosophy centered on **simplicity and low-level capability**.

Unlike many high-level "simple" languages (like Python or JavaScript), Burst aims to provide an accessible learning curve while still offering the control and power required for more intricate tasks, similar to languages like C/C++/C\#.

-----

> [\!IMPORTANT]
> Burst has migrated from **dynamic typing** to **static typing**. This is a **backwards-incompatible** change.
>
> You must now prefix every variable declaration with its type (e.g., `bool`, `int`, `str`, `input`).

### ✨ Key Features (Based on `compiler.py`)

Burst supports the following core language constructs:

  * **Static Variable Declaration:** Define variables with explicit types (`int`, `str`, `bool`, `input`).
  * **Printing & String Interpolation:** Output values and easily embed variables into strings.
  * **Conditional Logic (If/Else):** Execute different code blocks based on conditions.
  * **Arithmetic Expressions:** Perform basic math operations on integer variables.
  * **Function Definition and Calls:** Structure code using custom functions.
  * **File Inclusion:** Import code and exported variables from other Burst files.

-----

## 💻 Documentation

### 1\. Installation & Setup

To get started with Burst, you'll need to clone the repository and navigate to the testing directory.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/LoganPaxton/Burst.git
    ```
2.  **Navigate to the test environment:**
    ```bash
    cd Burst && cd tests
    ```
3.  You can now modify the sample file, `tests/test.br`.

### 2\. Running Burst Code

Burst is currently compiled using a Python interpreter.

1.  **Navigate to the source directory:**
    ```bash
    cd .. && cd src
    ```
2.  **Run the compiler:**
    ```bash
    python3 burst.py tests/test.br
    ```

-----

## 💡 Examples

Here are some comprehensive examples demonstrating the core syntax:

### 1\. Hello, World\! (Basic Output)

```burst
print("Hello, World!");
```

### 2\. Static Typing and Arithmetic

This example showcases declaring an integer variable and performing arithmetic.

```burst
int var num1 = 10;
int var num2 = 5;

// Increase num1 by num2
num1 + num2;

print("New value of num1 is:");
print(num1); // Output: 15
```

### 3\. User Input and String Interpolation

Use the `input()` call and the `i""` prefix for interpolation.

```burst
str var name = input(); // Prompts the user for a string
print(i"Hello, ${name}! Welcome to Burst.");
```

### 4\. Conditional (If/Else) Statement

The syntax requires the condition in `[]` and the bodies in `()`.

```burst
int var age = 20;

if [age >= 18] => (
    print("You are an adult!");
) else => (
    print("You are a minor.");
);
```

### 5\. Function Definition and Call

Define a function with `func` and call it by its name.

```burst
func greet(username) => (
    print(i"Function called: Hello, ${username}!");
);

// Call the function
greet("Example");
```

-----

## 🤝 Credits

**[@SalladShooter](https://github.com/SalladShooter)** - Prompts / Input (Javascript Version)
