# Fleiss' Kappa, GWET and other statistical calculations

Computation of several statistics needed for the evaluation of survey data, including calculations of the [Fleiss' Kappa] and [GWET] values.

Based on the caluclations by [Joseph L. Fleiss](https://en.wikipedia.org/wiki/Fleiss%27_kappa) and [Kilem Li Gwet](http://www.agreestat.com/research_papers/bjmsp2008_interrater.pdf). Works on Python 3+.



## Code usage

```python
import fleisskappa as kp


-----------------------------
#Calculation of the sum over all n(ij)
#Given a list or dictionary containing the scores of each category for one noun (e.g. dict[category1]=5, dict[category2]=2, dict[category3]=9, etc.), run:

kp.calculateSumN(score_list)


-----------------------------
#Calculation of the P(i) value
#Given the sum over all n(ij) and the number of participants, run:

kp.calculatePI(participantNumber, sumN)


-----------------------------
#Caluclation of the P value
#Given a list of P(i) values and the number of nouns used in the survey, run:

kp.caluclateP(pi_value_list, nounNumber)


-----------------------------
#Calculation of the Pe value, the Pe(I) value, the p(j) values for each category and the p(j)(I) values for each category
#Given a list or dictionary containing the overall scores of each category for all nouns, the number of nouns, the number of categories and the number of participants, run:

kp.calculatePE_PEI(overall_score_list, participantNumber, nounNumber, categoryNumber)

#The method returns a list containing all four values:

Pe value: kp.calculatePE_PEI(overall_score_list, participantNumber, nounNumber, categoryNumber)[0]
Pe(I) value: kp.calculatePE_PEI(overall_score_list, participantNumber, nounNumber, categoryNumber)[1]
p(j) values: kp.calculatePE_PEI(overall_score_list, participantNumber, nounNumber, categoryNumber)[2]
p(j)(I) values: kp.calculatePE_PEI(overall_score_list, participantNumber, nounNumber, categoryNumber)[3]


-----------------------------
#Non-matrix calculation of the Fleiss' Kappa and GWET values
#Given the P and the Pe or Pe(I) values, run:

kp.calculateFleissKappa_GWET(p_value, pei_value)

#Depending on the second parameter the method calculates the Fleiss' Kappa or GWET value:
Fleiss' Kappa: kp.calculateFleissKappa_GWET(p_value, pe_value)
GWET: kp.calculateFleissKappa_GWET(p_value, peI_value)


-----------------------------
#Matrix calculation fo the Fleiss' Kappa and GWET values.
#Given a two-dimensional matrix containing each score of each category for all nouns, run:

kp.calculateFleissKappa_GWET_Matrix(dataMatrix)

#The method returns a list containing the Fleiss' Kappa and GWET values:

Fleiss' Kappa: calculateFleissKappa_GWET_Matrix(dataMatrix)[0]
GWET: calculateFleissKappa_GWET_Matrix(dataMatrix)[1]

#Example matrix with five categories, three nouns and four participants:

dataMatrix = [[2,2,0,0,0],[1,0,1,1,1],[0,1,0,1,2]]
```


### Installation

```shell
#Go to the 'modules' directory with the 'setup.py' script and type:

python setup.py install
```


#### Remarks

This module requires the [NumPy](http://www.numpy.org/) and [Pypandoc](https://pypi.org/project/pypandoc/) packages to function properly.
