# -------------------------------------------------------
# CSCI 561, Spring 2021
# Homework 3
# Author: Joseph Ko
# Sentence Class
# -------------------------------------------------------
from Literal import *
import copy
from collections import defaultdict

class Sentence():
    """
    Defines a Sentence object, which is composed of 
    literals connected by "|"
    Sentences in CNF.
    """
    def __init__(self, sentence_string):
        """
        invalid: Boolean (repeated parameters in Literal)
        literals: List of Strings
        predicate_dict: Dictionary, {"Predicate":[List of Literals]}
        as_string: sentence as String
        """
        self.invalid = False
        #self.literals = []
        self.literals = set()
        self.predicate_dict = defaultdict(list)
        if "=>" in sentence_string: 
            split_sentence = [x.strip() for x in sentence_string.split("=>")]
            pre_implication = split_sentence[0]
            post_implication = split_sentence[1]
            split_pre_implication = [x.strip() for x in pre_implication.split("&")]
            # before "=>"
            for literal_string in split_pre_implication:
                literal = Literal(literal_string)
                literal.negate()
                #self.literals.append(literal)
                self.literals.add(literal)
                self.predicate_dict[literal.predicate].append(literal)
            # after "=>"
            literal = Literal(post_implication)
            #self.literals.append(literal)
            self.literals.add(literal)
            self.predicate_dict[literal.predicate].append(literal)
        elif "|" in sentence_string:
            split_sentence = [x.strip() for x in sentence_string.split("|")]
            literal_set = set()
            for literal_string in split_sentence:
                # check for repeated literals
                if literal_string in literal_set:
                    continue
                literal_set.add(literal_string)
                literal = Literal(literal_string)
                if literal.invalid:
                    self.invalid = True
                    break
                #self.literals.append(literal)
                self.literals.add(literal)
                self.predicate_dict[literal.predicate].append(literal)
        elif not sentence_string: # if empty string
            pass
        else:
            literal = Literal(sentence_string)
            if literal.invalid:
                self.invalid = True
            #self.literals.append(literal)
            self.literals.add(literal)
            self.predicate_dict[literal.predicate].append(literal)
        self.as_string = str(self)
        self.literals_frozen = frozenset(self.literals)

    def __hash__(self):
        #return hash(self.as_string)
        return hash(self.literals_frozen)

    def __eq__(self, other):
        #return self.as_string == other.as_string
        return self.literals == other.literals

    def __str__(self):
        """
        reconstruct CNF sentence as string
        """
        sentence_string = ""
        for literal in self.literals:
            sentence_string += str(literal)
            sentence_string += " | "
        sentence_string = sentence_string[:-3]
        return sentence_string

    def resolve(self, predicate, sentence2):
        """
        Resolves two sentences if possible
        output: returns set of resolvents, OR 
        returns "CONTRADICTION" if contradiction is found
        """
        resolvents = []
        literal_list1 = self.predicate_dict[predicate]
        literal_list2 = sentence2.predicate_dict[predicate]
        for literal1 in literal_list1:
            for literal2 in literal_list2:
                theta = literal1.unify_literals(literal2) # finds most general unifier, else returns False
                if theta == False: # cannot unify
                    continue
                else:
                    # remove literal containing unified predicate 
                    s1_removed = self.remove_literal(literal1)
                    s2_removed = sentence2.remove_literal(literal2)
                    if not s1_removed.literals and not s2_removed.literals: # if contradiction encountered
                        return "CONTRADICTION"
                    # make substitutions 
                    s1_subbed = s1_removed.substitute(theta)
                    s2_subbed = s2_removed.substitute(theta)

                    # if either sentence invalid after substitution 
                    if s1_subbed.invalid or s2_subbed.invalid:
                        continue

                    # form resolvent as a string
                    if not s1_subbed.literals: # if s1 is empty
                        resolvent_string = s2_subbed.as_string
                    elif not s2_subbed.literals: # elif s2 is empty
                        resolvent_string = s1_subbed.as_string
                    else:
                        resolvent_string = s1_subbed.as_string + " | " + s2_subbed.as_string

                    resolvent = Sentence(resolvent_string)
                    # # TESTING
                    # with open("test_output.txt", "a") as test_output:
                    #     print("resolvent:", resolvent, file=test_output)
                    #     print("  *predicate:", predicate, file=test_output)
                    # if resolvent_string == "~Learn( Sit , Hayley ) | ~Learn( Sit , Hayley )":
                    #     print("!!! sentences that resolved to ~Learn( Sit , Hayley ) | ~Learn( Sit , Hayley ) !!!")
                    #     print(self)
                    #     print(sentence2)
                    # convert resolvent string to Sentence object
                    
                    # add resolvent to list of resolvents
                    resolvents.append(resolvent)
        return resolvents
    
    def remove_literal(self, literal):
        """
        Remove literal from sentence and return new sentence object
        """            
        sentence_copy = copy.deepcopy(self)
        sentence_copy.literals.remove(literal)
        new_sentence_string = str(sentence_copy)
        new_sentence = Sentence(new_sentence_string)
        return new_sentence
    
    def substitute(self, theta):
        """
        Make substitutions (theta)
        input: theta = list of tuples, e.g., [(x, John), (y, Bill), ...]
        literal = literal to remove from sentence
        output: new sentence with substitutes made
        """
        sentence_string = self.as_string
        for tuple in theta:
            var = " " + tuple[0] + " "
            sub = " " + tuple[1] + " "
            sentence_string = sentence_string.replace(var, sub)
        new_sentence = Sentence(sentence_string)
        return new_sentence

    def get_possibly_resolvable(self, kb):
        """
        Get all sentences in KB with same predicate and opposite sign.
        output: list of tuples with form (predicate, sentence)
        """
        output = []
        for literal in self.literals:
            if literal.negated:
                key = (literal.predicate, "positive")
            else:
                key = (literal.predicate, "negative")
            for sentence in kb.dict[key]:
                output.append((literal.predicate, sentence))
        return output
