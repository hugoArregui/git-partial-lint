Small utility to run a linter on the repo current changes

#Usage

    git-partial-lint rule_file file
  
The rule file is also a bash script defining three functions:

```
    run(input_file, output_file)
    extract_error_linenum(line)
    print_output(line)
```

Check rules dir for examples
