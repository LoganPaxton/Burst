const fs = require('fs');

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
  else: "Else"
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

    let matched = false;

    if (line.startsWith("print")) {
      matched = true;
      tokenList.push(token_types.print);
      const stringMatch = line.match(/"[^"]*"/);
      if (stringMatch !== null) {
        const string_value = stringMatch[0].slice(1, -1); // Remove surrounding quotes
        tokenList.push("String_Value: ", string_value);
      } else {
        const varName = line.split("print")[1].trim();
        tokenList.push(token_types.print_var, varName);
      }
    }

    if (line.startsWith("var")) {
      matched = true;
      let [varName, varValue] = line.slice(4).trim().split("=");
      varName = varName.trim();
      varValue = varValue.trim();
      tokenList.push(token_types.variable, varName, token_types.equals, varValue);
    }

    if (line.includes("+")) {
      matched = true;
      let [varName, addValue] = line.split("+").map(part => part.trim());
      tokenList.push(token_types.add, varName, addValue);
    }

    if (line.includes("-")) {
      matched = true;
      let [varName, subValue] = line.split("-").map(part => part.trim());
      tokenList.push(token_types.subtract, varName, subValue);
    }

    if (line.startsWith("?")) {
      matched = true;
      // Parse the if statement
      const conditionMatch = line.match(/^\?\s*([^=\s]+)\s*(=|===)\s*([^:\s]+)\s*:\s*(.*?)\s*(?:\s*:\>\s*(.*))?$/);
      if (conditionMatch) {
        const [, arg1, op, arg2, thenPart, elsePart] = conditionMatch;
        tokenList.push(token_types.if, arg1, op, arg2, token_types.then, thenPart);
        if (elsePart) {
          tokenList.push(token_types.else, elsePart);
        }
      } else {
        console.error("Invalid if statement format", line);
      }
    }

    if (line.length === 0) {
      matched = true;
      tokenList.push(token_types.whitespace);
    }

    if (!matched) {
      console.error("Unknown token", line);
    }
  }
  return tokenList;
}

function parse(tokens = []) {
  let i = 0;
  while (i < tokens.length) {
    if (tokens[i] === token_types.print) {
      if (tokens[i + 1] === "String_Value: ") {
        console.log(tokens[i + 2]);
        i += 3;
      } else if (tokens[i + 1] === token_types.print_var) {
        const varName = tokens[i + 2];
        if (variables.hasOwnProperty(varName)) {
          console.log(variables[varName]);
        } else {
          console.error("Undefined variable:", varName);
        }
        i += 3;
      }
    } else if (tokens[i] === token_types.variable) {
      const varName = tokens[i + 1];
      const varValue = tokens[i + 3];
      variables[varName] = varValue.startsWith('"') ? varValue.slice(1, -1) : varValue;
      i += 4;
    } else if (tokens[i] === token_types.add) {
      const varName = tokens[i + 1];
      const valueToAdd = tokens[i + 2];
      if (variables.hasOwnProperty(varName)) {
        const currentValue = parseFloat(variables[varName]);
        const addValue = parseFloat(valueToAdd);
        if (!isNaN(currentValue) && !isNaN(addValue)) {
          variables[varName] = (currentValue + addValue).toString();
        } else {
          console.error("Cannot add non-numeric values");
        }
      } else {
        console.error("Undefined variable:", varName);
      }
      i += 3;
    } else if (tokens[i] === token_types.subtract) {
      const varName = tokens[i + 1];
      const valueToSub = tokens[i + 2];
      if (variables.hasOwnProperty(varName)) {
        const currentValue = parseFloat(variables[varName]);
        const subValue = parseFloat(valueToSub);
        if (!isNaN(currentValue) && !isNaN(subValue)) {
          variables[varName] = (currentValue - subValue).toString();
        } else {
          console.error("Cannot subtract non-numeric values");
        }
      } else {
        console.error("Undefined variable:", varName);
      }
      i += 3;
    } else if (tokens[i] === token_types.whitespace) {
      i += 1;
    } else if (tokens[i] === token_types.if) {
      const arg1 = tokens[i + 1];
      const op = tokens[i + 2];
      const arg2 = tokens[i + 3];
      const thenPart = tokens[i + 5];
      const elsePart = tokens[i + 7];

      // Handle the if condition
      let conditionMet = false;
      if (op === "=") {
        conditionMet = (arg1.includes('"') ? arg1.slice(1, -1) : variables[arg1]) == (arg2.includes('"') ? arg2.slice(1, -1) : arg2);
      } else if (op === "===") {
        conditionMet = (arg1.includes('"') ? arg1.slice(1, -1) : variables[arg1]) === (arg2.includes('"') ? arg2.slice(1, -1) : arg2);
      }
      
      if (conditionMet) {
        // Execute then part
        //console.log(`Condition met. Executing then part: ${thenPart}`);
        const thenTokens = tokenize(thenPart);
        parse(thenTokens);
      } else if (elsePart) {
        // Execute else part
        //console.log(`Condition not met. Executing else part: ${elsePart}`);
        const elseTokens = tokenize(elsePart);
        parse(elseTokens);
      }

      i += 8; // Adjust based on the number of tokens processed
    } else {
      i += 1;
    }
  }
  // Debug print statement to see variables
  //console.log("Variables:", variables);
}

if (process.argv.length < 3) {
  console.error("Usage: node src/burst.js <file_path>");
  process.exit(1);
}

const filePath = process.argv[2];

fs.readFile(filePath, (err, data) => {
  if (err) {
    throw err;
  } else {
    tokens = tokenize(data.toString());
    parse(tokens);
  }
});

/*
DEBUGGING
const code = `print "Hello, World!"\nvar x = 10\nprint x\nx + 5\nprint x`;
tokens = tokenize(code);
parse(tokens);
*/
