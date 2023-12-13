# sentence_concreteness
 
This is a package for tagging sentences with their concreteness. The measure is an average of words in a sentence. Words are matched to their root form and person, place, or organizational entities are tagged with a maximum concretenes of 5. The word concreteness ratings that this package relies upon were provided by Brysbaert, Warriner & Kuperman (2013).

This method has been empirically validated in our paper. If you find it helpful, please consider using the following citation:
> Aubin Le Quéré, M., Matias, J. N. (2024). When Curiosity Gaps Backfire: Effects of Headline Concreteness on Information Selection Decisions. Under Review.

## Installation
`pip install sentence_concreteness`

## Requirements
   * `csv`
   * `string`
   * `inflect`
   * `spacy`
   * `truecase`
   * `nltk`

## Usage
See `demo.py` for an example of how to run sentence_concreteness.

## Documentation
### `get_concreteness(word)`

Returns the matched concreteness for an individual word. This method will try to match a word to a root form if able. 

| Name               | Type              | Description                      |
| ------------------ | ----------------- | -------------------------------- |
| `word`      | string   | Word that you wish to retrieve the concreteness for. |

### `get_sentence_concreteness(sentence, verbose=False, num_unmatched_words_allowed=3)`

Returns the matched concreteness for a sentence word. For each word, this method will try to calculate a concreteness and then take the average of all retrieved concretenesses. If a word is considered an entity, it will automatically be assigned a concreteness of 5.

| Name               | Type              | Description                      |
| ------------------ | ----------------- | -------------------------------- |
| `sentence`      | string   | Sentence that you wish to retrieve the concreteness for. |
| `verbose`      | boolean   | Whether you want more information. |
| `num_unmatched_words_allowed`      | int   | Number of allowable non-matched words before an error is returned. |

## Details
To calculate concreteness ratings, we first identify any person, place, or organizational entities in a headline using the spaCy package, and encode these entities with the highest concreteness score of 5. We then split our headline into a list of tokens and remove standardized stopwords from the headline. We ignore punctuation and cardinal numbers. From the remaining list of tokens, we take an iterative approach to mapping each token to its concreteness rating, checking between each step if the words maps to a concreteness rating. At each step, if we cannot yet retrieve a concreteness rating for a token, we first attempt to retrieve a singular version of the token (e.g. "elephants" &rarr; "elephant"), a present tense version (e.g. "lounged" &rarr; "lounge"), or a base adjective (e.g. "greatest" &rarr; "great").
If these steps all fail and a word is hyphenated, we take the average of both words (e.g. "super-spectacular" &rarr; "super", "spectacular"). 

## Resources used

https://maria-antoniak.github.io/2020/03/25/pip.html \
https://realpython.com/pypi-publish-python-package/#prepare-your-package-for-publication
