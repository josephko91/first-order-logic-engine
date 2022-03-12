# -------------------------------------------------------
# CSCI 561, Spring 2021
# Homework 3 
# Author: Joseph Ko
# Resolution algorithm and helper functions
# -------------------------------------------------------
from Literal import *
from Sentence import *
from KnowledgeBase import *
import copy
import time

def resolution(query, kb):
    """
    The resolution algorithm.
    input: query (string), kb (KnowledgeBase)
    output: returns "TRUE" or "FALSE" and updated kb
    """
    #new = set()
    history = set()
    # negate query and add to KB
    query_literal = Literal(query) # convert to Literal
    query_literal.negate() # negate
    negated_query_sentence = Sentence(str(query_literal)) # convert to Sentence
    kb.add_sentence(negated_query_sentence) # add to KB
    # loop until all possible sentences have been inferred or contradiction is found
    loop_count = 1
    # #with open("test_output.txt", "w") as test_output:
    # print("==================== original KB ====================")
    # print("KB size:", kb.size)
    # for sentence in kb.set:
    #     print(sentence)

    sentence1 = negated_query_sentence # initial root of resolution
    while True: 
        #new = set()
        # with open("test_output.txt", "a") as test_output:
        #     print("==================== loop", loop_count, "====================", file=test_output)
        start = time.time()
        # start with resolvent from previous iteration (initialize with negated query)
        possibly_resolvable_sentences = sentence1.get_possibly_resolvable(kb)
        sentence2_tuple = possibly_resolvable_sentences[0]
        for sentence2_tuple in possibly_resolvable_sentences:
            # sentence2_tuple = (predicate, Sentence)
            predicate = sentence2_tuple[0]
            sentence2 = sentence2_tuple[1]
            # skip to next iteration if sentences are the same
            if sentence1 == sentence2:
                continue
            # skip to next iteration if sentences already been resolved
            sentence_pair_id_1 = hash((sentence1, predicate, sentence2)) # unique id
            sentence_pair_id_2 = hash((sentence2, predicate, sentence1)) 
            if sentence_pair_id_1 in history:
                continue
            elif sentence_pair_id_2 in history:
                continue
            else:
                history.add(sentence_pair_id_1) # add to history
                history.add(sentence_pair_id_2)

            # resolve two sentences
            resolvents = sentence1.resolve(predicate, sentence2)
            if len(resolvents) == 0:
                continue
            else:
                break # if reached this point -> break loop with current sentence 2
        
        # if new KB is a subset of old KB
        if len(resolvents) == 0:
            # print("final kb size =", kb.size)
            return "FALSE"

        # if there is a contradiction encountered 
        if resolvents == "CONTRADICTION":
            # print("sentence1:", sentence1)
            # print("sentence2:", sentence2)
            # print("final kb size =", kb.size)
            return "TRUE"
        # if it was resolved, add to new
        else:
            # TESTING 
            # with open("test_output.txt", "a") as test_output:
            #     print("    -> sentence 1:", sentence1, file=test_output)
            #     print("    -> sentence 2:", sentence2, file=test_output)
            # add new resolvent to KB
            resolvent = resolvents[0] # set new resolvent
            kb.add_sentence(resolvent) # update kb

        end = time.time()
        # with open("test_output.txt", "a") as test_output:
        #     print("!!! NEW SENTENCES !!!", file=test_output)
        #     print("( size of new =", len(new), ")", file=test_output)
        #     for sentence in new:
        #         print("  ", sentence, file=test_output)
        #     print("============================================", file=test_output)
        #     print("KB size, loop", loop_count, ":", kb.size, file=test_output)
        #     print("time in loop", loop_count, "=", end-start, "seconds", file=test_output)
        
        # if loop_count == 5:
        #     test_output.close()
        #     return "False"

        loop_count += 1
        
        # update sentence1
        sentence1 = resolvent
        


