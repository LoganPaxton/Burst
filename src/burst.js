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
  whitespace: "WhiteSpace"
};

let tokens = [];
let variables = {};

function tokenize(code = "") {
  code = code.split("\n");
  for (let i = 0; i < code.length; i++) {
    const line = code[i].trim();
    if (line.startsWith("==")) {
      continue; // Skip comments
    }

    let matched = false;

    if (line.startsWith("print")) {
      matched = true;
      tokens.push(token_types.print);
      const stringMatch = line.match(/"[^"]*"/);
      if (stringMatch !== null) {
        const string_value = stringMatch[0].slice(1, -1); // Remove surrounding quotes
        tokens.push("String_Value: ", string_value);
      } else {
        const varName = line.split("print")[1].trim();
        tokens.push(token_types.print_var, "Variable_Name", varName);
      }
    }

    if (line.startsWith("var")) {
      matched = true;
      let Line = line.slice(4).trim();
      Line = Line.split("=");
      const _varName = Line[0].trim();
      const _varValue = Line[1].trim();
      tokens.push(token_types.variable, _varName, token_types.equals, _varValue);
    }

    if (line.includes("+")) {
      matched = true;
      let Line = line.split("+");
      const _addName = Line[0].trim();
      const _addValue = Line[1].trim();
      tokens.push(token_types.add, _addName, _addValue);
    }

    if (line.includes("-")) {
      matched = true;
      let Line = line.split("-");
      const _subName = Line[0].trim();
      const _subValue = Line[1].trim();
      tokens.push(token_types.subtract, _subName, _subValue);
    }

    if (line.length === 0) {
      matched = true;
      tokens.push(token_types.whitespace);
    }

    if (!matched) {
      console.error("Unknown token", line);
    }
  }
  // Debug print statement to see tokens
  //console.log("Tokens:", tokens);
}

function parse(tokens = []) {
  for (let i = 0; i < tokens.length; i++) {
    if (tokens[i] === token_types.print) {
      if (tokens[i + 1] === "String_Value: ") {
        console.log(tokens[i + 2]);
      }
    } else if (tokens[i] === token_types.variable) {
      // Store variable values, removing any quotes
      variables[tokens[i + 1]] = tokens[i + 3].startsWith('"') ? tokens[i + 3].slice(1, -1) : tokens[i + 3];
    } else if (tokens[i] === token_types.print_var) {
      const varName = tokens[i + 2];
      if (variables.hasOwnProperty(varName)) {
        console.log(variables[varName]);
      } else {
        console.error("Undefined variable:", varName);
      }
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
    } else if (tokens[i] === token_types.whitespace) {
      continue;
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
    tokenize(data.toString());
    parse(tokens);
  }
});

/*
DEBUGGING
const code = `print"Hello, World!"\nvar x = 10\nprint x\nx + 5\nprint x`;
tokenize(code);
parse(tokens);
*/
