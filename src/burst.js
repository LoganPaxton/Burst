const token_types = {
  print: "Print",
  open_qoute: "Open_Qoute",
  string: "String",
  "close_qoute:": "Close_Qoute",
};

let tokens = [];

function tokenize(code = "") {
  let re = new RegExp("[A-Za-z]+");
  code = code.split("\n");
  for (let i = 0; i !== code.length; i++) {
    const print = re.test(code[i]);
    if (print === true) {
      tokens.push(token_types.print);
      re = new RegExp('"[^"]*"');
      const match = re.exec(code[i]);
      if (match !== null) {
        const string_value = match[0].slice(1, -1);
        tokens.push("String_Value: ", string_value);
      }
    }
    //console.log(tokens); Used for debugging
  }
}

function parse(tokens=[]) {
  for (let i = 0; i < tokens.length; i++) {
    if (tokens[i] == "Print") {
      console.log(tokens[i + 2])
    }
  }
}

/*
DEBUGGING

const code = `print"Hello, World!"\n`;
tokenize(code)
parse(tokens)
*/
