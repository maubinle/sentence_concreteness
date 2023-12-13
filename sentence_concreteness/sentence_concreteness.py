import csv
import string
import inflect
import spacy
import truecase
from string import punctuation
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

nlp = spacy.load("en_core_web_sm")
inf = inflect.engine()
lemma = WordNetLemmatizer()

concreteness_file='concreteness_ratings.csv'
concreteness_dict = {}

ner_entity_types = ['GPE', 'PERSON', 'ORG']

stop_words = stopwords.words('english')

# remove some words from the stopword list that upworthy uses to create curiosity gaps
stop_words_to_remove = ['these', 'this', 'it', 'what', 'he', 'she', 
                        'her', 'him', 'his', 'they', 'them', 'this',
                        'what', 'here', 'how']

stop_words = [stop_word for stop_word in stop_words if stop_word not in stop_words_to_remove]
exclusion_list = ['an', 'a', 'the', 'when', 'who', 'where', ',', '.', "'",'...','i', 'me', 'you']
        
i=0
with open(concreteness_file,'r') as data:
    for line in csv.reader(data):        
        if line[1] == 'Bigram':
            continue
        # converting to be the inverse
        concreteness_dict[line[0]] = float(line[2])

# def print_word_concreteness(word):
#     print('the word "' + word + '" has a concreteness score of ' + str(concreteness_dict[word]))

def get_singular(word):
    try:  
        return inf.singular_noun(word)
    except:
        return None
    
def get_present_tense(word):
    try:
        return lemma.lemmatize(word,'v')
    except: 
        return None
    
def get_base_adjective(word):
    try: return lemma.lemmatize(word,'a')
    except: return None
        
def match_word_to_dict(word, d):
    try:
        return d[word]
    except:
        #try singular
        try:
            return d[get_singular(word)]
        except:
            #as a final attempt, try converting to present tense
            try:
                return d[get_present_tense(word)]
            except: 
                try:
                    return d[get_base_adjective(word)]
                except:
                    return None

def get_concreteness(word):

    try1 = match_word_to_dict(word, concreteness_dict)
    if try1 != None:
        return try1
    
    # one attempt is to try it with removal of punctuation marks
    else:
        try2 = match_word_to_dict(word.translate(str.maketrans('', '', string.punctuation)), concreteness_dict)
        if try2 != None:
            return try2
        # finally, if there are two words separated by a hyphen which are both recognised, take the average
        split_words = word.split('-')
        if len(split_words) == 2:
            abs1 = match_word_to_dict(split_words[0], concreteness_dict)
            abs2 = match_word_to_dict(split_words[1], concreteness_dict)
            if abs1 != None and abs2 != None:
                return (abs1 + abs2) / 2
    
    return None

assert get_concreteness('elephants') == get_concreteness('elephant')
assert get_concreteness('lounged') == get_concreteness('lounge')
assert get_concreteness('greatest') == get_concreteness('great')
assert get_concreteness('non-profit') == get_concreteness('non-profit')
assert get_concreteness('mind-bending') == (get_concreteness('mind') + get_concreteness('bending'))/2

def get_non_stopwords(tokens):
    words = set()
    for token in tokens:
        if token.lower() not in stop_words:
            words.add(token)
    return list(words)

def return_single_entities(doc):
    
    entity_indexes = []
    
    # pointer
    j = 0
    
    for i in range(0,len(doc)):

        if i == j:
            curr_token = doc[i]
            curr_entity_type = doc[i].ent_type_
            
            # found the beginning of an entity
            if curr_entity_type in ner_entity_types:
                
                if j!= len(doc)-1:

                    # search for the end of the entity
                    while doc[j+1].ent_type_ == curr_entity_type:
                        j+=1

                        if j == len(doc)-1:
                            break
                        
                entity_indexes.append((i,j))
            j+=1
    entities = []
    
    for entity in entity_indexes:
        entities.append(doc[entity[0]:entity[1]+1])
    
    return entities

def run_NER(headline):
    
    doc = nlp(truecase.get_true_case(headline))
    cleaned = [t.text if t.ent_type_ not in ['GPE', 'PERSON', 'ORG'] else t.ent_type_ for t in doc]
    
    entities_raw = []    
    entities_raw = return_single_entities(doc)
    
    # second pass is to check the single length entities
    # if they have an abstraction, we'll count that instead
    
    entities = []
    
    for entity in entities_raw:
        if len(entity) == 1:
            if get_concreteness(str(entity).lower()) == None:
                entities.append(entity)
        else:
            entities.append(entity)
    
    num_entities = len(entities)

    return entities, num_entities

def has_long_none(words_none):
    for word in words_none:
        word = word.translate(str.maketrans('', '', string.punctuation))
        if len(word) >= 3:
            return True
    return False

has_long_none([',tr,,,he'])

def get_sentence_concreteness(sentence, verbose=False, num_unmatched_words_allowed=3):
    sentence = sentence.lower()
    entities, num_entities = run_NER(sentence.replace('-', ' '))
    entities_tokens = [words for seg in entities for words in str(seg).lower().split()]

    words = word_tokenize(sentence)
    words = get_non_stopwords(words)
    words = [w for w in words if w not in entities_tokens]
    words = [w for w in words if not w.isnumeric()]

    words_none = [x for x in words if get_concreteness(x) == None]
    words_none = [x for x in words_none if x not in punctuation]
    if len(words_none) > num_unmatched_words_allowed:
        return "Sentence has more than "+ str(num_unmatched_words_allowed) + " words with no matched concreteness. To allow more unmatched words, set `num_unmatched_words_allowed` to your desired threshold."
    words_not_none = [x for x in words if get_concreteness(x) != None]

    concreteness_values_all = [get_concreteness(x) for x in words_not_none]
    concreteness_values_all = concreteness_values_all + [5]*num_entities

    if len(concreteness_values_all) == 0:
        return "This sentence had no recognized words and no concreteness rating can be provided."
    concreteness_all = sum(concreteness_values_all)/len(concreteness_values_all)
    if verbose==True:
        print('SENTENCE IS:', sentence)
        print('overall sentence concreteness:', concreteness_all)
        # print('overall headline concreteness:', 5-concreteness_all)
        print('breakdown of concreteness value for each word:', 
            [x for x in zip(list(words_not_none + entities),concreteness_values_all)])
    return concreteness_all