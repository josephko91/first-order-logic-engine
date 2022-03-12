# -------------------------------------------------------
# CSCI 561, Spring 2021
# Homework 3 
# Author: Joseph Ko
# KnowledgeBase Class
# -------------------------------------------------------
from Literal import *
from Sentence import *
from collections import defaultdict

class KnowledgeBase():
    """
    set: set of sentences in KB
    dict: dict in the form e.g., {(Predicate, "positive"), Sentence}
    size: number of unique sentences
    """
    def __init__(self, sentences_kb):
        self.set = set(sentences_kb)
        self.dict = defaultdict(set)
        for sentence in self.set:
            for literal in sentence.literals:
                if literal.negated == False:
                    key = (literal.predicate, "positive")
                    self.dict[key].add(sentence)
                else:
                    key = (literal.predicate, "negative")
                    self.dict[key].add(sentence)
        self.size = len(self.set)

    def add_sentence(self, sentence):
        """
        Add sentence as Sentence object to KB.
        """
        self.size += 1
        self.set.add(sentence)
        for literal in sentence.literals:
            if literal.negated == False:
                key = (literal.predicate, "positive")
                self.dict[key].add(sentence)
            else:
                key = (literal.predicate, "negative")
                self.dict[key].add(sentence)

    def add_set(self, set_sentences):
        """
        Add set of Sentences to KB
        """
        for sentence in set_sentences:
            self.add_sentence(sentence)