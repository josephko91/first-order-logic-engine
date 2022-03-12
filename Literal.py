# -------------------------------------------------------
# CSCI 561, Spring 2021
# Homework 3
# Author: Joseph Ko
# Literal Class
# -------------------------------------------------------
from unification import *

class Literal():
    """
    This class defines a literal, which is 
    composed of the predicate and its arguments.
    as_string: literal as a string
    predicate: predicate as a string
    negated: True if predicate is negated
    arguments: [arg1, arg2, ...]
    """
    def __init__(self, literal_string):
        """
        has_constants: Boolean
        invalid: Boolean (turns True if there are repeated parameters)
        as_string: literal string (String)
        predicate: predicate (String)
        negated: (Boolean)
        parameters: list of parameters as Strings (List)
        """
        #self.as_string = literal_string
        self.num_constants = 0
        self.invalid = False
        split_literal = literal_string.split("(")
        if split_literal[0][0] == "~":
            self.predicate = split_literal[0][1:]
            self.negated = True
        else:
            self.predicate = split_literal[0][0:]
            self.negated = False 
        parameters_string = split_literal[1][:-1]
        #self.parameters = [x.strip() for x in parameters_string.split(",")]
        self.parameters = []
        parameter_set = set()
        for x in parameters_string.split(","):
            parameter = x.strip()
            if parameter in parameter_set:
                self.invalid = True
            parameter_set.add(parameter)
            self.parameters.append(parameter)
            if parameter[0].isupper():
                self.num_constants += 1
        self.as_string = str(self)

    def __hash__(self):
        return hash(self.as_string)

    def __eq__(self, other):
        return self.as_string == other.as_string

    def __str__(self):
        """
        Reconstruct literal as string from attributes
        """
        literal_string = ""
        if self.negated:
            literal_string = "~" + self.predicate
        else:
            literal_string = self.predicate
        literal_string += "("
        for parameters in self.parameters:
            literal_string += " " + parameters + " "
            literal_string += ","
        literal_string = literal_string[:-1]
        literal_string += ")"
        return literal_string

    def negate(self):
        """
        Negates a literal
        """
        if self.negated: # negative to positive
            self.as_string = self.as_string[1:]
        else: # positive to negative
            self.as_string = "~" + self.as_string
        self.negated = not self.negated

    def unify_literals(self, literal2):
        """
        unifies two literals
        returns MGU (theta) or false if unification is not possible
        """
        if self.predicate != literal2.predicate:
            return False
        elif self.negated^literal2.negated == False:
            return False
        elif self.num_constants == len(self.parameters) or literal2.num_constants == len(literal2.parameters):
            theta_dict = unify(self.parameters, literal2.parameters, {})
            if theta_dict == False:
                return False
            if len(theta_dict) == 0: # if empty dictionary
                for parameter in self.parameters:
                    if parameter[0].islower():
                        return False # if a variable is found in the parameters, return False
                return [] # if all parameters are constant, return empty list
            # ================= TESTING ================= 
            # only unify if all variables are unifed to constant
            for substitution in theta_dict.values():
                if substitution[0].islower(): # substitution is a variable
                    return False
            # =================        
            theta_list = list(theta_dict.items()) # convert from dict to list
            return theta_list
        else:
            return False