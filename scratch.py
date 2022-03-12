from Literal import *
from Sentence import *
import time
import copy

# empty dict
empty_dict = {}
print(len(empty_dict)==0)

substitution = 'Teddy'
print(substitution[0].islower)
print(substitution[0].islower())
# # Issue 1: test resolve function
# sentence1 = Sentence("~Learn( Come , x ) | ~Learn( Sit , x ) | Train( Down , x )")
# sentence2 = Sentence("~Healthy( Hayley ) | ~Train( Sit , Hayley ) | Train( Down , Hayley )")
# predicate = "Train"
# resolvents = sentence1.resolve(predicate, sentence2)

# Issue 2: repeated literala
# sentence_test = Sentence("~Socialize( Teddy , Teddy ) | ~Socialize( Teddy , Teddy ) | Play( Teddy , Teddy ) | ~Start( Teddy ) | ~Vaccinated( Teddy )")

# Issue 3: repeated parameters 
# sentence1 = Sentence("~Ready( y ) | ~Socialize( Teddy , y ) | ~Socialize( y , Teddy ) | Play( Teddy , y ) | ~Start( Teddy )")
# sentence2 = Sentence("~Vaccinated( Teddy ) | Ready( Teddy )")
# predicate = "Ready"
# resolvents = sentence1.resolve(predicate, sentence2)

# Issue 4: different ordering of same sentence

# set1 = frozenset(["a", "b", "c"])
# set2 = frozenset(["b", "a", "c"])
# print(set1)
# print(set2)
# print(hash(set1))
# print(hash(set2))
# print(set1 == set2)

# original
sentence1 = Sentence("~Ready( y ) | ~Socialize( Teddy , y ) | ~Socialize( y , Teddy ) | Play( Teddy , y ) | ~Start( Teddy )")
sentence2 = Sentence("~Start( Teddy ) | Ready( Teddy )")
predicate = "Ready"
tuple = (sentence1, predicate, sentence2)
print("tuple:", tuple)
hash_v1 = hash(tuple)
print("sentence1:", sentence1)
print("sentence2:", sentence2)
print("hash_v1 =", hash_v1)
# shuffled 
sentence1 = Sentence("~Socialize( y , Teddy ) | ~Ready( y ) | ~Start( Teddy ) | Play( Teddy , y ) | ~Socialize( Teddy , y )")
sentence2 = Sentence("Ready( Teddy ) | ~Start( Teddy )")
predicate = "Ready"
tuple = (sentence1, predicate, sentence2)
print("tuple:", tuple)
hash_v2 = hash(tuple)
print("sentence1:", sentence1)
print("sentence2:", sentence2)
print("hash_v2 =", hash_v2)
# are they equal?
print("equal?", hash_v1==hash_v2)

sentence_string = '~Healthy( x ) | ~Train( y , x ) | Learn( y , x )'
sub = ' Come '
var = ' y '
theta = [('y', 'Come')]


theta = []
print(theta==False)


sentence_string = "~Learn( Come , x )"
sentence = Sentence(sentence_string)
print(sentence.as_string)

literal_string = "~Learn( Sit , x )"
literal = Literal(literal_string)
print(literal)

sentence_copy = copy.deepcopy(sentence)
literal1 = sentence_copy.literals[0]
sentence_copy.literals.remove(literal1)
new_sentence_string = str(sentence_copy)
new_sentence = Sentence(new_sentence_string)

list = [1, 2, 3, 4]
if 5 in list:
    print("found it")
else:
    print("not found")

# parse input file
with open("input.txt", "r") as input_file:
    num_queries = int(input_file.readline().rstrip()) # 1st line: number of queries
    queries = [] # initialize list of queries
    for i in range(num_queries):
        queries.append(input_file.readline().rstrip()) # append to queries list 
    num_kb = int(input_file.readline().rstrip()) # number of sentences in KB
    sentences_kb = [] # initialize list of sentences in KB 
    for i in range(num_kb): # next 8 lines: 2-d list representing the board
        sentences_kb.append(input_file.readline().rstrip()) # append to list of sentences

start = time.time()
# test hash and eq for Sentence class
test_sentence = Sentence(sentences_kb[3])
test_sentence2 = Sentence("~Learn(Come,x) | ~Learn(Sit,x) | Train(Down,x)")
print(test_sentence)
print(test_sentence2)
print(hash(test_sentence))
print(test_sentence == test_sentence2)
end = time.time()
print("runtime", end-start)

# testing hash()
test_sentence = Sentence(sentences_kb[3])
test_literal = test_sentence.literals[0]
print(test_literal)
test_literal2 = Literal("~Learn(Come,x)")
print(hash(test_literal))
print(hash(test_literal2))
print(test_literal == test_literal2)

sentence_string = sentences_kb[3]
print(sentence_string)
sentence_split = [x.strip() for x in sentence_string.split("=>")]
print(sentence_split)

test_sentence = Sentence(sentence_string)
test_literals = test_sentence.literals
for literal in test_literals: 
    print(literal)
print(test_sentence)

# for sentence in sentences_kb:
#     print(sentence)
#     if "=>" in sentence:
#         print("implication found")
#     else:
#         print("no implication found")