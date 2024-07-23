const fs = require('fs');

const token_types = {
  print: "Print",
  open_qoute: "Open_Qoute",
  string: "String",
  close_qoute: "Close_Qoute",
};

let tokens = [];

function tokenize(code = "") {
  let re = new RegExp("[A-Za-z]+");
  code = code.split("\n");
  for (let i = 0; i < code.length; i++) {
    const line = code[i].trim();
    if (line.startsWith("==")) {
      continue; // Skip comments
    }
    
    const printMatch = re.exec(line);
    if (printMatch !== null && printMatch[0] === "print") {
      tokens.push(token_types.print);
      re = new RegExp('"[^"]*"');
      const match = re.exec(line);
      if (match !== null) {
        const string_value = match[0].slice(1, -1);
        tokens.push("String_Value: ", string_value);
      }
    } else {
      console.error("Unknown token ", line);
    }
  }
}

function parse(tokens = []) {
  for (let i = 0; i < tokens.length; i++) {
    if (tokens[i] == "Print") {
      console.log(tokens[i + 2]);
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

const code = `print"Hello, World!"`;
tokenize(code)
parse(tokens)
*/
