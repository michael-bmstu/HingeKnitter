# Hinge Knitter
___
## Description

##Usage
___
- run the script(main.py) in your python(3.6+) interpreter
- run HingeKnitter.exe file
___

![](img/main.jpg)

**Parameters:**
- mode(radiobutton):
  - folder: program will process folder with task files
  - file: program will process only one given file
- paths(3 buttons):
    - to the task folder/file
    - to the folder where processed file(-s) will be saved
    - to the file with hinge sequences
- prefix(default=file):
  - prefix for the processed file(-s), will use for naming processed file(-s)
- pattern(default=QVTVSS):
  - sequences with _pattern_ at the end will be processed
- minimum length of sequence(default=90 symbols):
  - reads in the processed file(-s) will divide into two 
  groups(1. length of read < min_len and 2. length of read >= min_len)
  and after processing will be writen in two 
  files(prefix_short_num and prefix_long_num)