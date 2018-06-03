# Supplementary Material for CIKM2018 paper 1306

## Overview
This repository contains scripts and example files for setting up a survey to assign categories to given information artifacts. This will result in an annotated question corpus that can be used as training data in research fields such as question answering or semantic search.  
We conducted our research in the biodiversity domain, a research field where (to the best of our knowledge) no question corpus has been established yet. The original question corpus and the identified terms to label are provided in a csv file --> 'biodiv_questions.csv' 
We also provide supplementary material to the annotation guidelines, the template files that have been generated with scripts to set up a survey and scripts to analyze the exported results.

For further information, in particular the annotation guidelines, please have a look at our publication.


## How to reproduce the result?
 

```shell
#Go to the scripts folder and install python and the necessary modules as stated. Copy the biodiv-questions.csv file to the scripts folder and run

python create_survey.py -f biodiv-questions.csv
```
That will create a new folder 'lsg_files' that contains files which can be imported into *Limesurvey* (https://www.limesurvey.org/) as question groups. Further information can be found in the scripts folder.
The exported result files are under *surveys* --> *result*. We established three survey with the same number of questions but different orderings in order to increase the likelihood that every question gets a rating. To retrieve the final result file with the statistics 

```shell
# Please copy the three individual result files into the scripts folder and run+
python analyze_result.py -f first.csv second.csv third.csv -c 1
```

The result file lsg____first__second__third.csv will contain the statistics including the overall inter-rater-agreement determined with Fleiss-Kappa and GWET's AC.

## How to use it for a new domain?

In order to use these scripts for a new domain, you would need to

1. collect questions in your domain and store it in a csv file
2. inspect the questions concerning suitable categories
3. develop annotation guidelines (What to label? What are relevant terms and phrases?) in close collaboration with domain experts
4. identify terms and phrases (artifacts) in the questions according to the guidelines and write the artifacts into the row of the related question
5. adapt the create_survey.py script to your needs (e.g., change the categories)
6. run the create_survey.py script to generate Limesurvey structure files
7. setup Limesurvey and import the lsg files into a new survey
8. send the survey to domain experts (including a short description of the categories and what to do in this evaluation!) who will assign categories to the given terms and phrases
9. export the survey results from Limesurvey into a csv file
10. run the analyze_result.py script to generate the statistics and the inter-rater-agreement

## How to further use these results?
As you can see from our *lsg____first__second__third.csv file*, the artifacts have different *P(i)* values, which is the observed agreement over all raters. It is up to you to define a threshold at which agreement you consider a rating as a valid category assignment. Usually, a *P(i)* > 0,6 can be considered as a good agreement.

## License
ToDo
