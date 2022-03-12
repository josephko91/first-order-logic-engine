# -------------------------------------------------------
# CSCI 561, Spring 2021
# Homework 3
# First Order Logic Resolution Engine
# Author: Joseph Ko
# Main driver
# -------------------------------------------------------
import copy
import time
from Literal import *
from Sentence import *
from KnowledgeBase import *
from resolution import *
import copy
import time

# parse input file
with open("input.txt", "r") as input_file:
    num_queries = int(input_file.readline().rstrip()) # 1st line: number of queries
    queries = [] # initialize list of queries
    for i in range(num_queries):
        queries.append(input_file.readline().rstrip()) # append to queries list 
    num_kb = int(input_file.readline().rstrip()) # number of sentences in KB
    sentence_strings = [] # initialize list of sentences in KB 
    for i in range(num_kb): # next 8 lines: 2-d list representing the board
        sentence_strings.append(input_file.readline().rstrip()) # append to list of sentences

# convert strings to Sentence objects
kb_sentences = []
for sentence_string in sentence_strings:
    kb_sentences.append(Sentence(sentence_string))

# create KnowledgeBase object with given sentences
kb = KnowledgeBase(kb_sentences)

start = time.time()
# loop through queries and run resolution on each
result_list = []
for query in queries: 
    kb_copy = copy.deepcopy(kb)
    result = resolution(query, kb_copy)
    print(result)
    result_list.append(result)
end = time.time()
print("runtime =", end-start)

# print results to output.txt
with open('output.txt', 'w') as output:
    for i in range(len(result_list)):
        if i == len(result_list)-1:
            print(result_list[i], file = output, end = "")
        else:
            print(result_list[i], file = output, end = "\n")
