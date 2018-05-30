# Creation/building and evaluation of 'LimeSurvey' surveys

Python scripts for creating and evaluating [LimeSurvey surveys](https://www.limesurvey.org/). Works on python 3+.



## Scripts

# create_survey.py:

create_survey.py is a simple Command Line Interface (CLI) tool to read and extract data from a semicolon-separated CSV file and to
write it into the [LimeSurvey-XML-format]. The script has two options as input, '-f' and '-d'. The '-f' option takes the path
to the CSV file as input. A folder named 'lsg_files' - in which all LimeSurvey-XML files are saved - is automatically created in
the same directory as the CSV file during the process. The '-d' option deletes this 'lsg_files' folder if it already exist. If a
folder named 'lsg_files' already exists but the '-d' option isn't set, the program will print an error message to remove this folder
from this directory or set the '-d' option and abort.

# Example usage:

```shell
#Go to the directoy where the create_survey.py script is saved and type:

python create_survey.py -f biodiv_questions.csv -d
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


# analyze_results.py:

analyze_results.py is a simple CLI tool to read and extract data from a [LimeSurvey-Result]-CSV file and to write and evaluate its
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
#Go to the directoy where the analyze_results.py script is saved and type:

python analyze_results.py -f first.csv second.csv third.csv -c 2
```



### Remarks

The analyze_results.py require the [Fleiss' Kappa](in the 'modules' folder) and the
[pandas](https://pandas.pydata.org/) packages for data evaluation and easy-data-extraction of CSV files.
