# Burst
Burst is a new coding language made in July of 2024. I was a project I decided to take on for one reason, simplicity. Most coding languages these days are either fast and complex (Steep learning curve) or slow and simple (Shallower learning curve). Most "simple" coding languages like Python, or Javascript are high-level languages, and you can't really do stuff like you would in C/C++/C# which are low-level.

## Credits
**[@SalladShooter](https://github.com/SalladShooter)** - Prompts / Input (Javascript Version)

## Docs

1. **Installation:**
   To install, run `git clone https://github.com/LoganPaxton/Burst.git`,
   Then, run `cd Burst && cd tests`
   Now, you can modify the `basic.br` file!
2. **Running:**
   To run your basic.br file, run this command `cd .. && cd src`
   Then, run `python3 burst.py` or, `python3 burst.min.py`


### Examples

> [!CAUTION]
> Burst 2.0.0 has **BACKWARDS INCOMPATABLE** changes! To migrate to 2.0.0, please read the [Migration Guide](#Migration)

1. **Hello, World!**
```burst
print "Hello, World!"
```
2. **PI**
```burst
var PI = 3.141592653
print("The rough value of PI is " + PI)
```
4. **Prompt**
```burst
var name = prompt("What is your name?)
print(i"Hello, {name}")
```

## Migration
To migrate to the latest 2.0.0 version, please change your current code to match the above in the documentation.
