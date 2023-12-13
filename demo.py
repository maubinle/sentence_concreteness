# DEMO: This file is a demonstration of the sentence_concreteness package.

import sentence_concreteness

print('***demo of word concreteness***')
print('"this":', sentence_concreteness.get_concreteness('this'))
print('"scoop":', sentence_concreteness.get_concreteness('scoop'))
print('"tomato":', sentence_concreteness.get_concreteness('tomato'))

print('***demo of sentence concretenesses***')
print("I explored an idea:", sentence_concreteness.get_sentence_concreteness("I explored an idea."))
print("I smelled the rain:", sentence_concreteness.get_sentence_concreteness("I smelled the rain."))
print("I ate a sesame bagel:", sentence_concreteness.get_sentence_concreteness("I ate a sesame bagel."))

print('***demo of verbose sentence concretenesses***')
print(sentence_concreteness.get_sentence_concreteness("I explored an idea.", verbose=True))
print(sentence_concreteness.get_sentence_concreteness("I smelled the rain.", verbose=True))
print(sentence_concreteness.get_sentence_concreteness("I ate a sesame bagel.", verbose=True))

print('***demo with allowing more or less unrecognised words***')
print("The zibberflonk bounced through the quibbly groves", sentence_concreteness.get_sentence_concreteness("The zibberflonk bounced through the quibbly groves"))
print("The zibberflonk bounced through the quibbly groves", sentence_concreteness.get_sentence_concreteness("The zibberflonk bounced through the quibbly groves", num_unmatched_words_allowed=1))