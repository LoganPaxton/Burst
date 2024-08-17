/*
BURST - COMPILER / TOKENIZER - Version 1.2.2

THIS HAS BEEN DEPRECAITED USE THE burst.py FILE TO RUN YOUR CODE!

You hear this a lot, but I'll say it anyways 
DO NOT CONFIGURE UNLESS YOU KNOW WHAT YOU ARE DOING!

*/
/*
// CONFIG START

const filePath = "main.br" // Set this to the Burst file you want to run.

// CONFIG END

const fs = require('fs');
const readline = require('readline');

const token_types = {
  print: "Print",
  open_qoute: "Open_Qoute",
  string: "String",
  close_qoute: "Close_Qoute",
  variable: "Variable",
  equals: "Equals",
  print_var: "Print_var",
  add: "Add",
  subtract: "Subtract",
  whitespace: "WhiteSpace",
  if: "If",
  exactly_equals: "Exactly_Equals",
  then: "Then",
  else: "Else",
  prompt: "Prompt" // Add prompt token type here
};

let tokens = [];
let variables = {};

function tokenize(code = "") {
  let tokenList = [];
  code = code.split("\n");
  for (let i = 0; i < code.length; i++) {
    const line = code[i].trim();
    if (line.startsWith("==")) {
      continue; // Skip comments
    }

    // Regular expression to check for print statements
    const printMatch = /^print\s+(.*)$/.exec(line);
    if (printMatch) {
      tokenList.push(token_types.print);
      const parts = printMatch[1].split("+").map(part => part.trim());
      for (const part of parts) {
        if (part.startsWith('"') && part.endsWith('"')) {
          // This is a string
          const stringValue = part.slice(1, -1); // Remove quotes
          tokenList.push("String_Value: ", stringValue);
        } else {
          // This is a variable or expression
          tokenList.push(token_types.print_var, part);
        }
      }
      continue;
    }

    // Match variable declarations
    if (line.startsWith("var")) {
      const varDeclParts = line.split("=");
      if (varDeclParts.length === 2) {
        const varName = varDeclParts[0].trim().slice(4); // Get variable name
        const varValue = varDeclParts[1].trim(); // Get the value after '='

        if (varValue.startsWith('"') && varValue.endsWith('"')) {
          tokenList.push(token_types.variable, varName, token_types.equals, varValue.slice(1, -1)); // Store without quotes
        } else {
          tokenList.push(token_types.variable, varName, token_types.equals, varValue);
        }
      }
      continue;
    }

    // Handle prompt command with message in the same line
    if (line.startsWith("prompt")) {
      const parts = line.split("=");
      const varName = parts[0].split(" ")[1].trim(); // Get the variable name
      const message = parts[1].trim().replace(/^"(.*)"$/, '$1'); // Extract the message after '='
      tokenList.push(token_types.prompt, varName, message);
      continue;
    }

    // Handle empty lines and whitespace
    if (line.length === 0) {
      tokenList.push(token_types.whitespace);
      continue;
    }

    console.error("Unknown statement:", line); // Handle unknown lines
  }
  return tokenList;
}

// Set up readline interface
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

// Function to wait for user input
function askQuestion(query) {
  return new Promise((resolve) => rl.question(query, resolve));
}

async function parse(tokens = []) {
  let i = 0;
  while (i < tokens.length) {
    if (tokens[i] === token_types.prompt) {
      const varName = tokens[i + 1];
      const message = tokens[i + 2];
      const answer = await askQuestion(`${message} `); // Wait for user input
      variables[varName] = answer; // Set the variable to user input
      i += 3; // Move past the prompt token, variable name, and message
      continue; // Skip to the next iteration
    }

    if (tokens[i] === token_types.print) {
      let output = '';
      i += 1;

      // Collecting strings and variables for concatenation
      while (i < tokens.length && (tokens[i] === "String_Value: " || tokens[i] === token_types.print_var)) {
        if (tokens[i] === "String_Value: ") {
          output += tokens[i + 1]; // Concatenate string value
          i += 2;
        } else if (tokens[i] === token_types.print_var) {
          const varName = tokens[i + 1];
          if (variables.hasOwnProperty(varName)) {
            output += variables[varName]; // Concatenate variable value
          } else {
            console.error("Undefined variable:", varName);
          }
          i += 2;
        }
      }

      console.log(output); // Print the final concatenated output
    } else if (tokens[i] === token_types.variable) {
      const varName = tokens[i + 1];
      const varValue = tokens[i + 3];
      variables[varName] = varValue.startsWith('"') ? varValue : varValue; // Store as string if in quotes
      i += 4;
    } else if (tokens[i] === token_types.whitespace) {
      i += 1;
    } else {
      console.error("Unknown token in parse:", tokens[i]);
      i += 1;
    }
  }
}

// Main program execution
fs.readFile(filePath, async (err, data) => {
  if (err) {
    throw err;
  } else {
    tokens = tokenize(data.toString());
    await parse(tokens); // Wait for the complete execution of all tokens
    rl.close(); // Close the readline interface after processing
  }
});
*/


/*
DEBUGGING
const code = `prompt name = "What is your name?"
print "Hello, " + name
var result = "Final message: " + name
print result
`;
tokens = tokenize(code);
parse(tokens);
*/
