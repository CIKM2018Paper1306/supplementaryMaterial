# Creation/building and evaluation of 'LimeSurvey' surveys

Python scripts for creating and evaluating [LimeSurvey surveys](https://www.limesurvey.org/). Works on python 3+.



## Scripts

# lsg_creator.py:

lsg_creator.py is a simple Command Line Interface (CLI) tool to read and extract data from a semicolon-separated CSV file and to
write it into the [LimeSurvey-XML-format]. The script has two options as input, '-f' and '-d'. The '-f' option takes the path
to the CSV file as input. A folder named 'lsg_files' - in which all LimeSurvey-XML files are saved - is automatically created in
the same directory as the CSV file during the process. The '-d' option deletes this 'lsg_files' folder if it already exist. If a
folder named 'lsg_files' already exists but the '-d' option isn't set, the program will print an error message to remove this folder
from this directory or set the '-d' option and abort.

# Example usage:

```shell
#Go to the directoy where the lsg_creator.py script is saved and type:

python lsg_creator.py -f biodiv_questions.csv -d
```

The [LimeSurvey-XML] file can have a maximum of 20 questions. If a CSV file has more than 20 questions it will separated in two, three,
four, etc. number of [LimeSurvey-XML] files that will be saved in the 'lsg_files' folder. So, if a CSV file has 55 questions, the first
20 questions will be saved in a [LimeSurvey-XML] file, the next 20 questions will be saved in another [LimeSurvey-XML] file and the last
15 questions will be saved, again, in another [LimeSurvey-XML] file (-> three [LimeSurvey-XML] files).

The CSV file should be semicolon-separated and have the following format:

- 1st column: Title
    -> each question has to have an unique title
    
- 2nd column: Question/statement

- 3rd column: custom usage

- 4th column: custom usage

- 5th and all following columns: Terms to be annotated


# lsg_evaluator.py:

lsg_evaluator.py is a simple CLI tool to read and extract data from a [LimeSurvey-Result]-CSV file and to write and evaluate its
results into a new CSV file, called 'lsg__/survey_names/.csv'. The script has two options as input, '-f' and '-c'. The '-f' option
can take the paths of multiple [LimeSurvey-Result]-CSV files and combine the results into a single CSV file. However, each of these
files have to have the same questions and nouns, i.e. have to be identical except for their question order. Most likely won't most
participants answer each question and noun (especially in particulary long surveys). Therefore, it can be useful to let each participant
run through one survey multiple times - each time with a different question order -, to make sure that each noun is actually annotated
at least once. The '-c' option let's you choose at which column in the [LimeSurvey-Result]-CSV file the actually data starts, so at which
column the first question (and noun) and answer is. Only the start column of the first input [LimeSurvey-Result]-CSV file is needed since
the data of all following [LimeSurvey-Result]-CSV files is extracted by using the question titles and nouns of the first
[LimeSurvey-Result]-CSV file.

# Example usage:

```shell
#Go to the directoy where the lsg_evaluator.py script is saved and type:

python lsg_evaluator.py -f first-lsg-results.csv second-lsg-results.csv third-lsg-results.csv -c 9
```


# lsg_krippendorff.py:

lsg_krippendorff is a simple CLI tool to read and extract data from a [LimeSurvey-Result]-CSV file and to write its results in a 
two-dimensional Krippendorff matrix (as a CSV file, called 'lsg__krippendorff__/survey_names/.csv') for further evaluation by the
[Krippendorff’s alpha agreement measure.](https://pypi.org/project/krippendorff/0.2.2/). The script has two options as input, '-f'
and '-c'. Both options are identical in their function to the options in the 'lsg_evaluator.py' script.

# Example usage:

```shell
#Go to the directoy where the lsg_krippendorff.py script is saved and type:

python lsg_krippendorff.py -f first-lsg-results.csv second-lsg-results.csv third-lsg-results.csv -c 5
```



### Remarks

The lsg_evaluator.py and lsg_krippendorff.py scripts require the [Fleiss' Kappa](in the 'modules' folder) and the
[pandas](https://pandas.pydata.org/) packages for data evaluation and easy-data-extraction of CSV files.
