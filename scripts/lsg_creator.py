# -*- coding: utf-8 -*-
import argparse
import csv
import os
import shutil
import sys
from random import randint

#number of the current row starting at 1
rowNumber = 1

#dictionary containing another dictionary with the information of the CSV file. First key: row number; second key: title, question, noun
rowDic = {}


#Method for command line interface, arguments: -f (input file) and -d (decides whether to delete an already existing folder named 'lsg_files' or not)
#return: The path to the input file of the -f option
def commandLine():
	
	
    parser = argparse.ArgumentParser(description="Convert a CSV file to a LSG file.")
    parser.add_argument("-f", "--file", help="Input path to CSV file", required=True)
    parser.add_argument("-d", "--delete", action="store_true", help="Deletes the folder 'lsg_files' in the current directory")

    args = parser.parse_args()
    csv_file = args.file
    
    #creates an folder named 'lsg_files' if it doesn't exist. If it exists, an exception will be thrown (folder already exists)
    #except the -d option is set true
    if(not os.path.exists("lsg_files")):
        os.makedirs("lsg_files")
    else:
        if(args.delete):
            shutil.rmtree("lsg_files")
            os.makedirs("lsg_files")
        else:
            raise IOError("There already exists a directory 'lsg_files' in the current directory. Please remove the folder 'lsg_files' from the current directory. Use the -d option if you want to delete this folder automatically.")



    return csv_file


#Method for reading a semicolon separated CSV file
#csv_file: The path to the CSV file as a String
def readCSVFile(csv_file):

    global rowNumber
    global rowDic

	#reading the semicolon separated CSV file line for line. 
    with open(csv_file, "r") as csvfile:
        content = csv.reader(csvfile, delimiter=";")
        firstLine = True
        for row in content:
			#the first line is ignored since it only contains the names of each column
            if(firstLine):
                firstLine = False
            #the content of each line is saved in a local dictionary (columnDic) which in return is saved in a global dictionary (rowDic).
            #The first column contains the title of the question (key: title).
            #The second column contains the question (key: question).
            #The fourth and all subsequent columns contain the nouns of the question (key: nouns)
            elif(not firstLine):
                columnDic = {}
                columnDic["title"] = row[0]
                columnDic["question"] = row[1]
                columnDic["nouns"] = row[4:]
                rowDic[rowNumber] = columnDic
                rowNumber = rowNumber + 1




#Method containing the first part of the header of the survey format
#gid: The global ID as an Integer
#sid: The survey ID as an Integer
#return: The first part of the header as a String
def getHeaderOne(gid, sid):

    lsg_header = """<?xml version="1.0" encoding="UTF-8"?>
<document>
 <LimeSurveyDocType>Group</LimeSurveyDocType>
 <DBVersion>346</DBVersion>
 <languages>
  <language>en</language>
 </languages>
 <groups>
  <fields>
   <fieldname>gid</fieldname>
   <fieldname>sid</fieldname>
   <fieldname>group_name</fieldname>
   <fieldname>group_order</fieldname>
   <fieldname>description</fieldname>
   <fieldname>language</fieldname>
   <fieldname>randomization_group</fieldname>
   <fieldname>grelevance</fieldname>
  </fields>
  <rows>
   <row>
    <gid><![CDATA[""" + str(gid) + """]]></gid>
    <sid><![CDATA[""" + str(sid) + """]]></sid>\n"""

    return lsg_header


#Method containing the second part of the header of the survey format (after the 'gid' and 'sid')
#return: The second part of the header as a String
def getHeaderTwo():
  
    lsg_header = """    <description><![CDATA[<div class="panel-group" id="accordionParent">
<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title"><a data-parent="#accordionParent" data-toggle="collapse" href="#legend">Explanation (Please click here to expand/fold up the instructions !)</a></h4>
</div>

<div class="panel-collapse collapse" id="legend">
<div class="panel-body">
<p>Each question group contains 20 questions. Please choose a proper information category for each of the highlighted phrases.</p>

<p><strong>Example:</strong> What <em>insects</em> (Organism) occur in the <em>shrub layer</em> (Environment)?</p>

<p>Please note that only one category can be applied per phrase. If no category fits, select 'other' and add a new category into the field that will appear below. If you have any further comments use the general comment field below each question.</p>

<p>If you don't know a term you can either look it up or skip it. Compound nouns, such as 'benthis oxygen update rates' are splitted up into individual terms. Please categorize the individual terms with respect to their context in the compound noun.</p>

<p>You can stop the survey in between and resume later. Please click 'Resume later' in the upper right corner, provide an email address and a password to save your current state and to go on at a later time.</p>

<div class="panel-group" id="accordion">
<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title"><a data-parent="#accordion" data-toggle="collapse" href="#organism">Organism</a> <img alt="" src="http://gfbio-git.inf-bb.uni-jena.de/images/org.png" /></h4>
</div>

<div class="panel-collapse collapse in" id="organism">
<div class="panel-body"><em>Organism </em>comprises all individual life forms, including plants, fungi, bacteria, animals and microorganisms, e.g., quercus, cyclothone, globigerina bulloides</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title"><a data-parent="#accordion" data-toggle="collapse" href="#environment">Environment</a> <img alt="" src="http://gfbio-git.inf-bb.uni-jena.de/images/env.png" /></h4>
</div>

<div class="panel-collapse collapse" id="environment">
<div class="panel-body">All species live in certain local and global <em>Environments</em> such as habitats, biome (e.g., below 4000m, ground water, city)</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title"><a data-parent="#accordion" data-toggle="collapse" href="#quality">Quality</a> <img alt="" src="http://gfbio-git.inf-bb.uni-jena.de/images/quality.png" /></h4>
</div>

<div class="panel-collapse collapse" id="quality">
<div class="panel-body">Organisms have certain characteristics (traits, phenotypes) that are summarized with <em>Quality and Phenotype</em>, e.g., length, growth rate, reproduction rate, traits</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title"><a data-parent="#accordion" data-toggle="collapse" href="#material">Mat & Subst - Material and Substances</a> <img alt="" src="http://gfbio-git.inf-bb.uni-jena.de/images/material.png" /></h4>
</div>

<div class="panel-collapse collapse" id="material">
<div class="panel-body">Chemical compounds, rocks, sand and sediments can be grouped as <em>Materials and Substances</em>, e.g., sediment, rock, CO2</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title"><a data-parent="#accordion" data-toggle="collapse" href="#method">Method</a> <img alt="" src="http://gfbio-git.inf-bb.uni-jena.de/images/meth.png" /></h4>
</div>

<div class="panel-collapse collapse" id="method">
<div class="panel-body">The term <em>Method</em> describes all operations and experiments that have to be conducted to lead to a certain result, e.g., lidar measurements, observation, remote sensing</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title"><a data-parent="#accordion" data-toggle="collapse" href="#dataType">Data Type</a> <img alt="" src="http://gfbio-git.inf-bb.uni-jena.de/images/dataType.png" /></h4>
</div>

<div class="panel-collapse collapse" id="dataType">
<div class="panel-body">Outcomes of research methods are delivered in <em>Data Types</em>, e.g., DNA data or sequence data is the result of genome sequencing, lidar data is the result of lidar measurements (active remote sensing)</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title"><a data-parent="#accordion" data-toggle="collapse" href="#process">Process</a> <img alt="" src="http://gfbio-git.inf-bb.uni-jena.de/images/process.png" /></h4>
</div>

<div class="panel-collapse collapse" id="process">
<div class="panel-body">Biological, chemical and physical <em>Processes</em> are re-occurring and transform materials or organisms due to chemical reactions or other influencing factors, e.g., climate change, nitrogen transformation</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title"><a data-parent="#accordion" data-toggle="collapse" href="#anatomy">Anatomy</a> <img alt="" src="http://gfbio-git.inf-bb.uni-jena.de/images/anat.png" /></h4>
</div>

<div class="panel-collapse collapse" id="anatomy">
<div class="panel-body"><em>Anatomical Entities</em> comprise the structure of organisms, e.g., body or plant parts, organs, cells and genes, e.g., DNA, proteome, root</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title"><a data-parent="#accordion" data-toggle="collapse" href="#location">Location</a> <img alt="" src="http://gfbio-git.inf-bb.uni-jena.de/images/loc.png" /></h4>
</div>

<div class="panel-collapse collapse" id="location">
<div class="panel-body">All kinds of geographic information is summarized with <em>Location</em>, e.g., Germany, Hainich, Atlantic Ocean</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title"><a data-parent="#accordion" data-toggle="collapse" href="#time">Time</a> <img alt="" src="http://gfbio-git.inf-bb.uni-jena.de/images/time.png" /></h4>
</div>

<div class="panel-collapse collapse" id="time">
<div class="panel-body">Time data including geological eras are described with <em>Time</em>, e.g., current, over time, triassic</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title"><a data-parent="#accordion" data-toggle="collapse" href="#event">Event</a> <img alt="" src="http://gfbio-git.inf-bb.uni-jena.de/images/event.png" /></h4>
</div>

<div class="panel-collapse collapse" id="event">
<div class="panel-body"><em>Events</em> are processes that appear only once at a specific time, such as environmental disasters, e.g., Deepwater Horizon oil spill, Tree of the Year 2016</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title"><a data-parent="#accordion" data-toggle="collapse" href="#person">Person & Org - Person and Organization</a> <img alt="" src="http://gfbio-git.inf-bb.uni-jena.de/images/pers.png" /></h4>
</div>

<div class="panel-collapse collapse" id="person">
<div class="panel-body"><em>Person and Organization</em> are either projects or authors of data, e.g., Deep Sea Drilling Project, author’s or collector’s names</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title"><a data-parent="#accordion" data-toggle="collapse" href="#humanInt">Human Inter - Human Intervention</a> <img alt="" src="http://gfbio-git.inf-bb.uni-jena.de/images/human.png" /></h4>
</div>

<div class="panel-collapse collapse" id="humanInt">
<div class="panel-body"><em>Human Intervention</em> on landscape and environment, e.g., agriculture, land use, crop yield increase</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
]]></description>
    <language><![CDATA[en]]></language>
    <randomization_group/>
    <grelevance/>
   </row>
  </rows>
 </groups>
 <questions>
  <fields>
   <fieldname>qid</fieldname>
   <fieldname>parent_qid</fieldname>
   <fieldname>sid</fieldname>
   <fieldname>gid</fieldname>
   <fieldname>type</fieldname>
   <fieldname>title</fieldname>
   <fieldname>question</fieldname>
   <fieldname>preg</fieldname>
   <fieldname>help</fieldname>
   <fieldname>other</fieldname>
   <fieldname>mandatory</fieldname>
   <fieldname>question_order</fieldname>
   <fieldname>language</fieldname>
   <fieldname>scale_id</fieldname>
   <fieldname>same_default</fieldname>
   <fieldname>relevance</fieldname>
   <fieldname>modulename</fieldname>
  </fields>
  <rows>\n"""


    return lsg_header



#Method containing the subquestion header of the survey format
#return: The subquestion header as a String
def getSubquestionHeader():

    lsg_subquestion_header = """ <subquestions>
  <fields>
   <fieldname>qid</fieldname>
   <fieldname>parent_qid</fieldname>
   <fieldname>sid</fieldname>
   <fieldname>gid</fieldname>
   <fieldname>type</fieldname>
   <fieldname>title</fieldname>
   <fieldname>question</fieldname>
   <fieldname>preg</fieldname>
   <fieldname>help</fieldname>
   <fieldname>other</fieldname>
   <fieldname>mandatory</fieldname>
   <fieldname>question_order</fieldname>
   <fieldname>language</fieldname>
   <fieldname>scale_id</fieldname>
   <fieldname>same_default</fieldname>
   <fieldname>relevance</fieldname>
   <fieldname>modulename</fieldname>
  </fields>
  <rows>\n"""

    return lsg_subquestion_header


#Method containing the answer header of the survey format
#return: The answer header as a String
def getAnswerHeader():

    lsg_answer_header = """ <answers>
  <fields>
   <fieldname>qid</fieldname>
   <fieldname>code</fieldname>
   <fieldname>answer</fieldname>
   <fieldname>sortorder</fieldname>
   <fieldname>assessment_value</fieldname>
   <fieldname>language</fieldname>
   <fieldname>scale_id</fieldname>
  </fields>
  <rows>\n"""

    return lsg_answer_header



#Method containing the answer body of the survey format
#return: The answer body as a String
def getAnswerBody():

    lsg_answer_body = """   <row>
    <qid><![CDATA[!?!]]></qid>
    <code><![CDATA[A1]]></code>
    <answer><![CDATA[<div><span style="color:#bdc3c7;">Anatomy</span></div>]]></answer>
    <sortorder><![CDATA[8]]></sortorder>
    <assessment_value><![CDATA[0]]></assessment_value>
    <language><![CDATA[en]]></language>
    <scale_id><![CDATA[0]]></scale_id>
   </row>
   <row>
    <qid><![CDATA[!?!]]></qid>
    <code><![CDATA[D1]]></code>
    <answer><![CDATA[<div><span style="color:#8e44ad;">Data Type</span></div>]]></answer>
    <sortorder><![CDATA[7]]></sortorder>
    <assessment_value><![CDATA[0]]></assessment_value>
    <language><![CDATA[en]]></language>
    <scale_id><![CDATA[0]]></scale_id>
   </row>
   <row>
    <qid><![CDATA[!?!]]></qid>
    <code><![CDATA[E1]]></code>
    <answer><![CDATA[<div><span style="color:#2ecc71;">Environment</span></div>]]></answer>
    <sortorder><![CDATA[2]]></sortorder>
    <assessment_value><![CDATA[0]]></assessment_value>
    <language><![CDATA[en]]></language>
    <scale_id><![CDATA[0]]></scale_id>
   </row>
   <row>
    <qid><![CDATA[!?!]]></qid>
    <code><![CDATA[E2]]></code>
    <answer><![CDATA[<div><span style="color:#cccc33;">Event</span></div>]]></answer>
    <sortorder><![CDATA[11]]></sortorder>
    <assessment_value><![CDATA[0]]></assessment_value>
    <language><![CDATA[en]]></language>
    <scale_id><![CDATA[0]]></scale_id>
   </row>
   <row>
    <qid><![CDATA[!?!]]></qid>
    <code><![CDATA[H1]]></code>
    <answer><![CDATA[<div><span style="color:#7f8c8d;">Human Inter</span></div>]]></answer>
    <sortorder><![CDATA[13]]></sortorder>
    <assessment_value><![CDATA[0]]></assessment_value>
    <language><![CDATA[en]]></language>
    <scale_id><![CDATA[0]]></scale_id>
   </row>
   <row>
    <qid><![CDATA[!?!]]></qid>
    <code><![CDATA[L1]]></code>
    <answer><![CDATA[<div><span style="color:#33cccc;">Location</span></div>]]></answer>
    <sortorder><![CDATA[9]]></sortorder>
    <assessment_value><![CDATA[0]]></assessment_value>
    <language><![CDATA[en]]></language>
    <scale_id><![CDATA[0]]></scale_id>
   </row>
   <row>
    <qid><![CDATA[!?!]]></qid>
    <code><![CDATA[M1]]></code>
    <answer><![CDATA[<div><span style="color:#f1c40f;">Method</span></div>]]></answer>
    <sortorder><![CDATA[6]]></sortorder>
    <assessment_value><![CDATA[0]]></assessment_value>
    <language><![CDATA[en]]></language>
    <scale_id><![CDATA[0]]></scale_id>
   </row>
   <row>
    <qid><![CDATA[!?!]]></qid>
    <code><![CDATA[MS1]]></code>
    <answer><![CDATA[<div><span style="color:#3498db;">Mat & Subst</span></div>]]></answer>
    <sortorder><![CDATA[4]]></sortorder>
    <assessment_value><![CDATA[0]]></assessment_value>
    <language><![CDATA[en]]></language>
    <scale_id><![CDATA[0]]></scale_id>
   </row>
   <row>
    <qid><![CDATA[!?!]]></qid>
    <code><![CDATA[O1]]></code>
    <answer><![CDATA[<div><span style="color:#d35400;">Organism</span></div>]]></answer>
    <sortorder><![CDATA[1]]></sortorder>
    <assessment_value><![CDATA[0]]></assessment_value>
    <language><![CDATA[en]]></language>
    <scale_id><![CDATA[0]]></scale_id>
   </row>
   <row>
    <qid><![CDATA[!?!]]></qid>
    <code><![CDATA[OT1]]></code>
    <answer><![CDATA[<div>other</div>]]></answer>
    <sortorder><![CDATA[14]]></sortorder>
    <assessment_value><![CDATA[0]]></assessment_value>
    <language><![CDATA[en]]></language>
    <scale_id><![CDATA[0]]></scale_id>
   </row>
   <row>
    <qid><![CDATA[!?!]]></qid>
    <code><![CDATA[P1]]></code>
    <answer><![CDATA[<div><span style="color:#ffccff;">Person & Org</span></div>]]></answer>
    <sortorder><![CDATA[12]]></sortorder>
    <assessment_value><![CDATA[0]]></assessment_value>
    <language><![CDATA[en]]></language>
    <scale_id><![CDATA[0]]></scale_id>
   </row>
   <row>
    <qid><![CDATA[!?!]]></qid>
    <code><![CDATA[PQ1]]></code>
    <answer><![CDATA[<div><span style="color:#f39c12;">Quality</span></div>]]></answer>
    <sortorder><![CDATA[3]]></sortorder>
    <assessment_value><![CDATA[0]]></assessment_value>
    <language><![CDATA[en]]></language>
    <scale_id><![CDATA[0]]></scale_id>
   </row>
   <row>
    <qid><![CDATA[!?!]]></qid>
    <code><![CDATA[Pr1]]></code>
    <answer><![CDATA[<div><span style="color:#663300;">Process</span></div>]]></answer>
    <sortorder><![CDATA[5]]></sortorder>
    <assessment_value><![CDATA[0]]></assessment_value>
    <language><![CDATA[en]]></language>
    <scale_id><![CDATA[0]]></scale_id>
   </row>
   <row>
    <qid><![CDATA[!?!]]></qid>
    <code><![CDATA[T1]]></code>
    <answer><![CDATA[<div><span style="color:#003399;">Time</span></div>]]></answer>
    <sortorder><![CDATA[10]]></sortorder>
    <assessment_value><![CDATA[0]]></assessment_value>
    <language><![CDATA[en]]></language>
    <scale_id><![CDATA[0]]></scale_id>
   </row>\n"""

    return lsg_answer_body


#Method containing the default values header of the survey format
#return: The default values header as a String
def getDefaultHeader():

    lsg_default_header = """ <defaultvalues>
  <fields>
   <fieldname>qid</fieldname>
   <fieldname>scale_id</fieldname>
   <fieldname>sqid</fieldname>
   <fieldname>language</fieldname>
   <fieldname>specialtype</fieldname>
   <fieldname>defaultvalue</fieldname>
  </fields>
  <rows>\n"""

    return lsg_default_header


#Method containing the default values body the survey format
#return: The default values body as a String
def getDefaultBody():

    lsg_default_body = """   <row>
    <qid><![CDATA[!?!]]></qid>
    <scale_id><![CDATA[0]]></scale_id>
    <sqid><![CDATA[?!?]]></sqid>
    <language><![CDATA[en]]></language>
    <specialtype/>
    <defaultvalue><![CDATA[new category]]></defaultvalue>
   </row>\n"""

    return lsg_default_body


#Method containing the question attributes header of the survey format
#return: The question attributes of the survey format
def getQuestionAttributesHeader():

    lsg_question_attributes_header = """ <question_attributes>
   <fields>
    <fieldname>qid</fieldname>
    <fieldname>attribute</fieldname>
    <fieldname>value</fieldname>
    <fieldname>language</fieldname>
   </fields>
   <rows>\n"""
 
    return lsg_question_attributes_header


#Method containing the question attibutes body of the survey format
#return: The question attributes body as a String
def getQuestionAttributesBody():

    lsg_question_attributes_body = """   <row>
    <qid><![CDATA[!?!]]></qid>
    <attribute><![CDATA[cssclass]]></attribute>
    <value><![CDATA[comment]]></value>
   </row>\n"""
 
    return lsg_question_attributes_body


#Method for building and writing the LSG survey file
def buildLSGFile():
	
	#sets the max length of the question title
    maxlen = 18
    
    #sets the starting question ID
    qid = 0
    #sets the starting question order
    qorder = 0
    #sets the starting question number
    questionsNumber = 1
    #sets the starting survey number
    surveyNumber = 1

    #Strings for each survey section (question, subquestion, answers, default values and question attributes)
    lsg_questions = ""
    lsg_subquestions = ""
    lsg_answers = ""
    lsg_defaults = ""
    lsg_question_attributes = ""

    #creates a random global ID (between 0 and the max Integer value)
    gid = randint(0, sys.maxsize)
    #creates a random survey ID (between 0 and the max Integer value)
    sid = randint(0, sys.maxsize)

    #sets the first header part
    lsg_header_one = getHeaderOne(gid, sid)
    #sets the second header part
    lsg_header_two = getHeaderTwo()

    #sets the subquestion header
    lsg_subquestion_header = getSubquestionHeader()

    #sets the answer header
    lsg_answer_header = getAnswerHeader()
    #sets the answer body
    lsg_answer_body = getAnswerBody()

    #sets the default header
    lsg_default_header = getDefaultHeader()
    #sets the default body
    lsg_default_body = getDefaultBody()
    
    #sets the question attributes header
    lsg_question_attributes_header = getQuestionAttributesHeader()
    #sets the question attributes body
    lsg_question_attributes_body = getQuestionAttributesBody()

    sid_s = "    <sid><![CDATA[" + str(sid) + "]]></sid>"
    gid_s = "    <gid><![CDATA[" + str(gid) + "]]></gid>"
    
    #loops through each row (key) of the rowDic dictionary
    for row in range(1, rowNumber):
        columnDic = rowDic[row]

        #builds the complete question body
        #loop = 0: question
        #loop = 1: other
        #loop = 2: comment
        for loop in range(0, 3):
            qid_s = "    <qid><![CDATA[" + str(qid) + "]]></qid>"
            qorder_s = "    <question_order><![CDATA[" + str(qorder) + "]]></question_order>"
            #sets the starting subquestion number
            sqnum = 1
            type = ""
            mandatory = ""
            title = ""
            question = ""
            #sets the arguments for the main question body
            if(loop == 0):
                mandatory = "N"
                type = "F"
                #if the title length is longer than 18, then the title is trimmed to the max length of 18 
                if(len(columnDic["title"]) > maxlen):
                    columnDic["title"] = columnDic["title"][:18]
                title = columnDic["title"]
                question = columnDic["question"]
                for noun in columnDic["nouns"]:
                    if(noun):
                        question = question.replace(noun, "<em>" + noun + "</em>")
            #sets the arguments for the 'other' question body
            elif(loop == 1):
                mandatory = "N"
                type = "Q"
                title = columnDic["title"] + "C"
                question = "Please provide a new category if you selected 'other'!"
            #sets the arguments for the comment question body
            elif(loop == 2):
                mandatory = "N"
                type = "T"
                title = columnDic["title"] + "CQ"
                question = "For general comments on this question, please use the field below."

            mandatory_s = "    <mandatory><![CDATA[" + str(mandatory) + "]]></mandatory>"
            type_s =  "    <type><![CDATA[" + str(type) + "]]></type>"
            title_s = "    <title><![CDATA[" + str(title) + "]]></title>"
            question_s = "    <question><![CDATA[" + str(question) + "]]></question>"
			
			#sets the String of the question body
            lsg_questions = lsg_questions + ("   <row>\n" + qid_s + "\n" + "    <parent_qid><![CDATA[0]]></parent_qid>\n" +
                                             sid_s + "\n" + gid_s + "\n" + type_s + "\n" + title_s + "\n" + question_s + "\n"
                                             + "    <preg/>\n    <help/>\n" + "    <other><![CDATA[N]]></other>\n" + mandatory_s +
                                             "\n" + qorder_s + "\n" +
                                             "    <language><![CDATA[en]]></language>\n    <scale_id><![CDATA[0]]></scale_id>\n" +
                                             "    <same_default><![CDATA[0]]></same_default>\n    <relevance><![CDATA[1]]></relevance>\n" +
                                             "    <modulename/>\n   </row>\n")

            #sets the starting subquestion order
            sqorder = 0
            #sets the subquestion ID to the question ID
            sqid = qid
            
            #if the main or 'other' question body is built
            #adds the nouns to the questions
            if(loop != 2):
                for noun in columnDic["nouns"]:
                    if(noun):
                        sqid = sqid + 1
                        subquestion = "    <question><![CDATA[" + noun + "]]></question>"
                        parent = "    <parent_qid><![CDATA[" + str(qid) + "]]></parent_qid>"
                        sqid_s = "    <qid><![CDATA[" + str(sqid) + "]]></qid>"
                        sqorder_s = "    <question_order><![CDATA["+ str(sqorder) + "]]></question_order>"
                        #sets the subquestion body
                        lsg_subquestions = lsg_subquestions + ("   <row>\n" + sqid_s + "\n" + parent + "\n" + sid_s + "\n" + gid_s + "\n" +
                                       "    <type><![CDATA[T]]></type>\n" + "    <title><![CDATA[SQ" + str(sqnum) + "]]></title>" + "\n" +
                                       subquestion + "\n" + "    <help/>\n    <other><![CDATA[N]]></other>\n" + sqorder_s + "\n" +
                                       "    <language><![CDATA[en]]></language>\n    <scale_id><![CDATA[0]]></scale_id>\n" +
                                       "    <same_default><![CDATA[0]]></same_default>\n    <relevance><![CDATA[1]]></relevance>\n" +
                                       "    <modulename/>\n   </row>\n")

                        #increases the subquestion number by one
                        sqnum = sqnum + 1
                        #increases the subquestion order by one
                        sqorder = sqorder + 1

            #sets the question ID to the subquestion ID
            qid = sqid


            #if the main question body is built
            if(loop == 0):
				#sets the answer body
                lsg_answers = lsg_answers + lsg_answer_body.replace("    <qid><![CDATA[!?!]]></qid>", qid_s)

            #if the 'other' question body is built
            if(loop == 1):
                dqid_s = "    <sqid><![CDATA[" + str(qid + 400) + "]]></sqid>"
                #sets the default values body
                lsg_defaults = lsg_defaults + lsg_default_body.replace("    <qid><![CDATA[!?!]]></qid>", qid_s).replace("    <sqid><![CDATA[?!?]]></sqid>", dqid_s)
                #sets the question attributes body
                lsg_question_attributes = lsg_question_attributes + lsg_question_attributes_body.replace("    <qid><![CDATA[!?!]]></qid>", qid_s)
                

            #increses question ID by one
            qid = qid + 1
            #increases the question order by one
            qorder = qorder + 1
            
        #each survey group contains 20 questions. If this number is exceeded or there are no questions left,
        #the LSG file is built and all survey Strings, IDs and order numbers are set to the starting values
        if(questionsNumber%20 == 0 or (rowNumber-1)-questionsNumber == 0):
            #resets the question ID
            qid = 0
            #resets the question order
            qorder = 0

            #sets the survey name (limesurvey_page_"surveyNumber".lsg)
            lsg_name = "lsg_files/limesurvey_page_" + str(surveyNumber) + ".lsg"
            #sets the survey number
            lsg_question_number = "    <group_name><![CDATA[BioDiv Question Page " + str(surveyNumber) + "]]></group_name>\n"
            #sets the complete survey header
            lsg_header = lsg_header_one + lsg_question_number + lsg_header_two

            #sets the complete question section
            lsg_questions = lsg_questions + "  </rows>\n </questions>\n"
            #sets the complete subquestion section
            lsg_subquestions = lsg_subquestion_header + lsg_subquestions + "  </rows>\n </subquestions>\n"
            #sets the complete answer section
            lsg_answers = lsg_answer_header + lsg_answers + "  </rows>\n </answers>\n"
            #sets the complete question attributes section
            lsg_question_attributes = lsg_question_attributes_header + lsg_question_attributes + "   </rows>\n</question_attributes>\n"
            #sets the complete default values section
            lsg_defaults = lsg_default_header + lsg_defaults + "  </rows>\n </defaultvalues>\n</document>"
            
            #writes the complete LSG file to the lsg_files folder
            with open(lsg_name, "w") as lsg:
                lsg.write(lsg_header + lsg_questions + lsg_subquestions + lsg_answers + lsg_question_attributes + lsg_defaults)
			
			#resets the question String
            lsg_questions = ""
            #resets the subquestion String
            lsg_subquestions = ""
            #resets the answer String
            lsg_answers = ""
            #resets the default values String
            lsg_defaults = ""
            #increases the survey number by one
            surveyNumber = surveyNumber + 1

            #creates a new random global ID
            gid = randint(0, sys.maxsize)
            #creates an new random survey ID
            sid = randint(0, sys.maxsize)

            #sets the new first header part
            lsg_header_one = getHeaderOne(gid, sid)

            sid_s = "    <sid><![CDATA[" + str(sid) + "]]></sid>"
            gid_s = "    <gid><![CDATA[" + str(gid) + "]]></gid>"


        #increases the question by one
        questionsNumber = questionsNumber + 1


#Main method for building the LSG file.
#Throws an error if the CSV file can't be accessed or an incorrect formatted file was used as an input
def startLSGWriter():

    try:
        csv = commandLine()
        readCSVFile(csv)
        buildLSGFile()
    except IOError as ioe:
        print(ioe)
    except OSError:
        print("Permission denied.")
    except IndexError as ie:
        print("Couldn't parse the CSV file. Did you select the correct file and is the file correctly formatted?")


#starts the main method of the script
startLSGWriter()
