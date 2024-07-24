const fs = require('fs');

const token_types = {
  print: "Print",
  open_qoute: "Open_Qoute",
  string: "String",
  close_qoute: "Close_Qoute",
  variable: "Variable",
  equals: "Equals",
  print_var: "Print_var"
};

let tokens = [];
let variables = {};

function tokenize(code = "") {
  let re = new RegExp("[A-Za-z]+");
  code = code.split("\n");
  for (let i = 0; i < code.length; i++) {
    const line = code[i].trim();
    if (line.startsWith("==")) {
      continue; // Skip comments
    }

    const varMatch = line.startsWith("var");
    const printMatch = line.startsWith("print");

    if (printMatch) {
      tokens.push(token_types.print);
      re = new RegExp('"[^"]*"');
      const match = re.exec(line);
      if (match !== null) {
        const string_value = match[0].slice(1, -1); // Remove surrounding quotes
        tokens.push("String_Value: ", string_value);
      } else {
        const varName = line.split("print")[1].trim();
        tokens.push(token_types.print_var, "Variable_Name", varName);
      }
    } else if (varMatch) {
      let Line = line.slice(4).trim();
      Line = Line.split("=");
      const _varName = Line[0].trim();
      const _varValue = Line[1].trim();
      tokens.push(token_types.variable, _varName, token_types.equals, _varValue);
    } else {
      console.error("Unknown token ", line);
    }
  }
}

function parse(tokens = []) {
  for (let i = 0; i < tokens.length; i++) {
    if (tokens[i] === "Print") {
      if (tokens[i + 1] === "String_Value: ") {
        console.log(tokens[i + 2]);
      }
    } else if (tokens[i] === "Variable") {
      // Store variable values, removing any quotes
      variables[tokens[i + 1]] = tokens[i + 3].startsWith('"') ? tokens[i + 3].slice(1, -1) : tokens[i + 3];
    } else if (tokens[i] === "Print_var") {
      const varName = tokens[i + 2];
      if (variables.hasOwnProperty(varName)) {
        console.log(variables[varName]);
      } else {
        console.error("Undefined variable: ", varName);
      }
    }
  }
}

fs.readFile('tests/basic.br', (err, data) => {
  if (err) {
    throw err;
  } else {
    tokenize(data.toString());
    parse(tokens);
  }
});

/*
DEBUGGING

const code = `print"Hello, World!"\nvar x = 10\nprint x`;
tokenize(code)
parse(tokens)
*/
