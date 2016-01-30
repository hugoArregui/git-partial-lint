Small utility to run a linter on the repo current changes

(requires python 3.5+)

#Usage

```
usage: git-partial-lint.py [-h] [--format FORMAT] rule file [file ...]

run linter only on the repo current changes

positional arguments:
rule             rule name
file             file or wildcard

optional arguments:
-h, --help       show this help message and exit
--format FORMAT  format
```
#Customization

- Use Rules static variables (fmt, flags)
- Write your own main script, and import the pieces you would like to reuse
