import re


# Sources
# 1. WordNet 3.0 - Princeton University
#    Copyright 2006 Princeton University.
#    https://wordnet.princeton.edu/
#
#    WordNet was used for preprocessing.
# 2. spaCy - Explosion AI
#    https://spacy.io/
#
#    spaCy was used for preprocessing.
# 3. OpenAI ChatGPT
#    https://chatgpt.com/
#
#    ChatGPT assisted with expanding the vocabulary lists.

NAMES = ['Ada',
 'Andrew',
 'Bobbie',
 'Cason',
 'David',
 'Farzana',
 'Frank',
 'Hannah',
 'Ida',
 'Irene',
 'Jim',
 'Jose',
 'Keith',
 'Laura',
 'Lucy',
 'Meredith',
 'Nick',
 'Serena',
 'Yan',
 'Yeeling']

LEMMAS = {'adults': 'adult',
 'am': 'be',
 'are': 'be',
 'been': 'be',
 'began': 'begin',
 'best': 'well',
 'better': 'well',
 'brought': 'bring',
 'came': 'come',
 'children': 'child',
 'did': 'do',
 'does': 'do',
 "dog's": 'dog',
 'dogs': 'dog',
 "don't": 'do',
 'done': 'do',
 'feet': 'foot',
 'flew': 'fly',
 'found': 'find',
 'gave': 'give',
 'gone': 'go',
 'got': 'get',
 'had': 'have',
 'has': 'have',
 'heard': 'hear',
 'her': 'she',
 'him': 'he',
 'is': 'be',
 'knew': 'know',
 'lay': 'lie',
 'left': 'leave',
 'made': 'make',
 'me': 'i',
 'men': 'man',
 'miles': 'mile',
 'ran': 'run',
 'said': 'say',
 'saw': 'see',
 'sings': 'sing',
 'stood': 'stand',
 'them': 'they',
 'thought': 'think',
 'told': 'tell',
 'took': 'take',
 'us': 'we',
 'walked': 'walk',
 'was': 'be',
 'went': 'go',
 'were': 'be',
 'wrote': 'write'}

WORD_TYPES = {'a': ['DET'],
 'able': ['ADJ'],
 'about': ['ADJ', 'ADV'],
 'above': ['ADJ', 'ADV', 'NOUN'],
 'act': ['NOUN', 'VERB'],
 'add': ['NOUN', 'VERB'],
 'adult': ['ADJ', 'NOUN'],
 'adults': ['NOUN'],
 'after': ['ADP', 'ADV'],
 'again': ['ADV'],
 'against': ['ADP'],
 'age': ['NOUN', 'VERB'],
 'ago': ['ADJ', 'ADV'],
 'air': ['NOUN', 'VERB'],
 'all': ['DET', 'PRON'],
 'also': ['ADV'],
 'always': ['ADV'],
 'am': ['AUX', 'VERB'],
 'among': ['ADP'],
 'an': ['DET'],
 'and': ['CCONJ'],
 'animal': ['ADJ', 'NOUN'],
 'answer': ['NOUN', 'VERB'],
 'any': ['ADJ', 'ADV'],
 'appear': ['VERB'],
 'are': ['AUX', 'VERB'],
 'area': ['NOUN'],
 'as': ['ADV', 'NOUN'],
 'ask': ['VERB'],
 'at': ['ADP'],
 'back': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'base': ['ADJ', 'NOUN', 'VERB'],
 'be': ['AUX', 'VERB'],
 'beauty': ['NOUN'],
 'bed': ['NOUN', 'VERB'],
 'been': ['AUX', 'VERB'],
 'before': ['ADP', 'ADV'],
 'began': ['VERB'],
 'begin': ['NOUN', 'VERB'],
 'behind': ['ADJ', 'ADV', 'NOUN'],
 'best': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'better': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'between': ['ADP'],
 'big': ['ADJ', 'ADV'],
 'bird': ['NOUN', 'VERB'],
 'black': ['ADJ', 'NOUN', 'VERB'],
 'blue': ['ADJ', 'NOUN', 'VERB'],
 'boat': ['NOUN', 'VERB'],
 'body': ['NOUN', 'VERB'],
 'book': ['NOUN', 'VERB'],
 'both': ['ADJ'],
 'box': ['NOUN', 'VERB'],
 'boy': ['NOUN'],
 'bring': ['VERB'],
 'brought': ['VERB'],
 'build': ['NOUN', 'VERB'],
 'busy': ['ADJ', 'VERB'],
 'but': ['CCONJ'],
 'by': ['ADP'],
 'call': ['NOUN', 'VERB'],
 'came': ['VERB'],
 'can': ['AUX', 'NOUN', 'VERB'],
 'car': ['NOUN'],
 'care': ['NOUN', 'VERB'],
 'carry': ['NOUN', 'VERB'],
 'cause': ['NOUN', 'VERB'],
 'center': ['ADJ', 'NOUN', 'VERB'],
 'certain': ['ADJ'],
 'change': ['NOUN', 'VERB'],
 'check': ['NOUN', 'VERB'],
 'children': ['NOUN'],
 'city': ['NOUN'],
 'class': ['NOUN', 'VERB'],
 'clear': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'close': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'cold': ['ADJ', 'NOUN'],
 'color': ['ADJ', 'NOUN', 'VERB'],
 'come': ['NOUN', 'VERB'],
 'common': ['ADJ', 'NOUN'],
 'complete': ['ADJ', 'VERB'],
 'contain': ['VERB'],
 'cool': ['ADJ', 'NOUN', 'VERB'],
 'correct': ['ADJ', 'VERB'],
 'could': ['AUX'],
 'country': ['NOUN'],
 'course': ['ADV', 'NOUN', 'VERB'],
 'cover': ['NOUN', 'VERB'],
 'cross': ['ADJ', 'NOUN', 'VERB'],
 'cry': ['NOUN', 'VERB'],
 'cut': ['ADJ', 'NOUN', 'VERB'],
 'dark': ['ADJ', 'NOUN'],
 'day': ['NOUN'],
 'decide': ['VERB'],
 'deep': ['ADJ', 'ADV', 'NOUN'],
 'develop': ['VERB'],
 'did': ['AUX', 'VERB'],
 'differ': ['VERB'],
 'direct': ['ADJ', 'ADV', 'VERB'],
 'do': ['AUX', 'VERB'],
 'does': ['AUX', 'VERB'],
 'dog': ['NOUN', 'VERB'],
 "dog's": ['NOUN', 'POSS'],
 'dogs': ['NOUN', 'VERB'],
 "don't": ['AUX'],
 'done': ['ADJ', 'VERB'],
 'door': ['NOUN'],
 'down': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'draw': ['NOUN', 'VERB'],
 'drive': ['NOUN', 'VERB'],
 'dry': ['ADJ', 'NOUN', 'VERB'],
 'during': ['ADP'],
 'each': ['DET', 'PRON'],
 'early': ['ADJ', 'ADV'],
 'earth': ['NOUN', 'VERB'],
 'ease': ['NOUN', 'VERB'],
 'east': ['ADJ', 'ADV', 'NOUN'],
 'eat': ['VERB'],
 'end': ['NOUN', 'VERB'],
 'enough': ['ADJ', 'ADV', 'NOUN'],
 'even': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'ever': ['ADV'],
 'every': ['DET'],
 'example': ['NOUN'],
 'eye': ['NOUN', 'VERB'],
 'face': ['NOUN', 'VERB'],
 'fact': ['NOUN'],
 'fall': ['NOUN', 'VERB'],
 'family': ['NOUN'],
 'far': ['ADJ', 'ADV', 'NOUN'],
 'farm': ['NOUN', 'VERB'],
 'fast': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'father': ['NOUN', 'VERB'],
 'feel': ['NOUN', 'VERB'],
 'feet': ['NOUN'],
 'few': ['ADJ', 'NOUN'],
 'field': ['NOUN', 'VERB'],
 'figure': ['NOUN', 'VERB'],
 'fill': ['NOUN', 'VERB'],
 'final': ['ADJ', 'NOUN'],
 'find': ['NOUN', 'VERB'],
 'fine': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'fire': ['NOUN', 'VERB'],
 'first': ['ADJ', 'ADV', 'NOUN'],
 'fish': ['NOUN', 'VERB'],
 'five': ['ADJ', 'NOUN', 'NUM'],
 'flew': ['VERB'],
 'fly': ['ADJ', 'NOUN', 'VERB'],
 'follow': ['VERB'],
 'food': ['NOUN'],
 'foot': ['NOUN', 'VERB'],
 'for': ['ADP'],
 'force': ['NOUN', 'VERB'],
 'form': ['NOUN', 'VERB'],
 'found': ['ADJ', 'NOUN', 'VERB'],
 'four': ['ADJ', 'NOUN', 'NUM'],
 'free': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'friend': ['NOUN'],
 'from': ['ADP'],
 'front': ['ADJ', 'NOUN', 'VERB'],
 'full': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'game': ['ADJ', 'NOUN', 'VERB'],
 'gave': ['VERB'],
 'get': ['NOUN', 'VERB'],
 'girl': ['NOUN'],
 'give': ['NOUN', 'VERB'],
 'go': ['ADJ', 'NOUN', 'VERB'],
 'gold': ['ADJ', 'NOUN'],
 'gone': ['ADJ', 'VERB'],
 'good': ['ADJ', 'ADV', 'NOUN'],
 'got': ['VERB'],
 'govern': ['VERB'],
 'great': ['ADJ', 'NOUN'],
 'green': ['ADJ', 'NOUN', 'VERB'],
 'ground': ['NOUN', 'VERB'],
 'group': ['NOUN', 'VERB'],
 'grow': ['VERB'],
 'had': ['AUX', 'VERB'],
 'half': ['ADJ', 'ADV', 'NOUN'],
 'hand': ['NOUN', 'VERB'],
 'happen': ['VERB'],
 'hard': ['ADJ', 'ADV'],
 'has': ['AUX', 'VERB'],
 'have': ['AUX', 'VERB'],
 'he': ['PRON'],
 'head': ['NOUN', 'VERB'],
 'hear': ['VERB'],
 'heard': ['ADJ', 'VERB'],
 'heat': ['NOUN', 'VERB'],
 'help': ['NOUN', 'VERB'],
 'her': ['DET', 'PRON'],
 'here': ['ADJ', 'ADV', 'NOUN'],
 'high': ['ADJ', 'ADV', 'NOUN'],
 'him': ['PRON'],
 'his': ['DET', 'PRON'],
 'hold': ['NOUN', 'VERB'],
 'home': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'horse': ['NOUN', 'VERB'],
 'hot': ['ADJ'],
 'hour': ['NOUN'],
 'house': ['NOUN', 'VERB'],
 'how': ['ADV'],
 'hundred': ['ADJ', 'NOUN', 'NUM'],
 'i': ['PRON'],
 'idea': ['NOUN'],
 'if': ['SCONJ'],
 'in': ['ADP', 'ADV'],
 'inch': ['NOUN', 'VERB'],
 'interest': ['NOUN', 'VERB'],
 'is': ['AUX', 'VERB'],
 'island': ['NOUN'],
 'it': ['PRON'],
 'just': ['ADJ', 'ADV'],
 'keep': ['NOUN', 'VERB'],
 'kind': ['ADJ', 'NOUN'],
 'king': ['NOUN'],
 'knew': ['VERB'],
 'know': ['NOUN', 'VERB'],
 'land': ['NOUN', 'VERB'],
 'language': ['NOUN'],
 'large': ['ADJ', 'ADV', 'NOUN'],
 'last': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'late': ['ADJ', 'ADV'],
 'laugh': ['NOUN', 'VERB'],
 'lay': ['ADJ', 'NOUN', 'VERB'],
 'lead': ['NOUN', 'VERB'],
 'learn': ['VERB'],
 'leave': ['NOUN', 'VERB'],
 'left': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'less': ['ADJ', 'ADV'],
 'let': ['NOUN', 'VERB'],
 'letter': ['NOUN', 'VERB'],
 'life': ['NOUN'],
 'light': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'like': ['ADJ', 'NOUN', 'VERB'],
 'line': ['NOUN', 'VERB'],
 'list': ['NOUN', 'VERB'],
 'listen': ['VERB'],
 'little': ['ADJ', 'ADV', 'NOUN'],
 'live': ['ADJ', 'ADV', 'VERB'],
 'long': ['ADJ', 'ADV', 'VERB'],
 'look': ['NOUN', 'VERB'],
 'lot': ['NOUN', 'VERB'],
 'love': ['NOUN', 'VERB'],
 'low': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'machine': ['NOUN', 'VERB'],
 'made': ['ADJ', 'VERB'],
 'main': ['ADJ', 'NOUN'],
 'make': ['NOUN', 'VERB'],
 'man': ['NOUN', 'VERB'],
 'many': ['ADJ'],
 'map': ['NOUN', 'VERB'],
 'mark': ['NOUN', 'VERB'],
 'may': ['AUX'],
 'me': ['PRON'],
 'mean': ['ADJ', 'NOUN', 'VERB'],
 'measure': ['NOUN', 'VERB'],
 'men': ['NOUN'],
 'might': ['AUX'],
 'mile': ['NOUN'],
 'miles': ['NOUN'],
 'mind': ['NOUN', 'VERB'],
 'minute': ['ADJ', 'NOUN'],
 'miss': ['NOUN', 'VERB'],
 'money': ['NOUN'],
 'moon': ['NOUN', 'VERB'],
 'more': ['ADJ', 'ADV', 'NOUN'],
 'morning': ['NOUN'],
 'most': ['ADJ', 'ADV'],
 'mother': ['NOUN', 'VERB'],
 'mountain': ['NOUN'],
 'move': ['NOUN', 'VERB'],
 'much': ['ADJ', 'ADV', 'NOUN'],
 'music': ['NOUN'],
 'must': ['AUX'],
 'my': ['DET'],
 'name': ['NOUN', 'VERB'],
 'near': ['ADJ', 'ADV', 'VERB'],
 'need': ['NOUN', 'VERB'],
 'never': ['ADV'],
 'new': ['ADJ', 'ADV'],
 'next': ['ADJ', 'ADV'],
 'night': ['NOUN'],
 'no': ['ADV', 'DET'],
 'north': ['ADJ', 'ADV', 'NOUN'],
 'not': ['PART'],
 'note': ['NOUN', 'VERB'],
 'nothing': ['ADV', 'NOUN'],
 'notice': ['NOUN', 'VERB'],
 'noun': ['NOUN'],
 'now': ['ADV', 'NOUN'],
 'number': ['NOUN', 'VERB'],
 'numeral': ['ADJ', 'NOUN'],
 'object': ['NOUN', 'VERB'],
 'of': ['ADP'],
 'off': ['ADJ', 'ADV', 'VERB'],
 'often': ['ADV'],
 'oh': ['NOUN'],
 'old': ['ADJ', 'NOUN'],
 'on': ['ADP', 'ADV'],
 'once': ['ADV'],
 'one': ['ADJ', 'NOUN', 'NUM'],
 'only': ['ADJ', 'ADV'],
 'open': ['ADJ', 'NOUN', 'VERB'],
 'or': ['CCONJ'],
 'order': ['NOUN', 'VERB'],
 'other': ['ADJ'],
 'our': ['DET'],
 'out': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'over': ['ADP', 'ADV'],
 'own': ['ADJ', 'VERB'],
 'page': ['NOUN', 'VERB'],
 'paper': ['NOUN', 'VERB'],
 'part': ['ADV', 'NOUN', 'VERB'],
 'pass': ['ADJ', 'NOUN', 'VERB'],
 'pattern': ['NOUN', 'VERB'],
 'people': ['NOUN', 'VERB'],
 'perhaps': ['ADV'],
 'person': ['NOUN'],
 'picture': ['NOUN', 'VERB'],
 'piece': ['NOUN', 'VERB'],
 'place': ['NOUN', 'VERB'],
 'plain': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'plan': ['NOUN', 'VERB'],
 'plane': ['ADJ', 'NOUN', 'VERB'],
 'plant': ['NOUN', 'VERB'],
 'play': ['NOUN', 'VERB'],
 'point': ['NOUN', 'VERB'],
 'port': ['ADJ', 'NOUN', 'VERB'],
 'pose': ['NOUN', 'VERB'],
 'possible': ['ADJ', 'NOUN'],
 'pound': ['NOUN', 'VERB'],
 'power': ['NOUN', 'VERB'],
 'press': ['NOUN', 'VERB'],
 'problem': ['NOUN'],
 'produce': ['NOUN', 'VERB'],
 'product': ['NOUN'],
 'pull': ['NOUN', 'VERB'],
 'put': ['NOUN', 'VERB'],
 'question': ['NOUN', 'VERB'],
 'quick': ['ADJ', 'ADV', 'NOUN'],
 'rain': ['NOUN', 'VERB'],
 'ran': ['VERB'],
 'reach': ['NOUN', 'VERB'],
 'read': ['NOUN', 'VERB'],
 'ready': ['ADJ', 'NOUN', 'VERB'],
 'real': ['ADJ', 'ADV', 'NOUN'],
 'record': ['NOUN', 'VERB'],
 'red': ['ADJ', 'NOUN'],
 'remember': ['VERB'],
 'rest': ['NOUN', 'VERB'],
 'right': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'river': ['NOUN'],
 'road': ['NOUN'],
 'rock': ['NOUN', 'VERB'],
 'room': ['NOUN', 'VERB'],
 'round': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'rule': ['NOUN', 'VERB'],
 'run': ['NOUN', 'VERB'],
 'said': ['ADJ', 'VERB'],
 'same': ['ADJ', 'NOUN'],
 'saw': ['NOUN', 'VERB'],
 'say': ['NOUN', 'VERB'],
 'school': ['NOUN', 'VERB'],
 'science': ['NOUN'],
 'sea': ['NOUN'],
 'second': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'see': ['NOUN', 'VERB'],
 'seem': ['VERB'],
 'self': ['ADJ', 'NOUN'],
 'sentence': ['NOUN', 'VERB'],
 'serve': ['NOUN', 'VERB'],
 'set': ['ADJ', 'NOUN', 'VERB'],
 'several': ['ADJ'],
 'shape': ['NOUN', 'VERB'],
 'she': ['PRON'],
 'ship': ['NOUN', 'VERB'],
 'short': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'should': ['AUX'],
 'show': ['NOUN', 'VERB'],
 'side': ['ADJ', 'NOUN', 'VERB'],
 'simple': ['ADJ', 'NOUN'],
 'since': ['ADP', 'ADV', 'SCONJ'],
 'sing': ['VERB'],
 'sings': ['VERB'],
 'sit': ['VERB'],
 'six': ['ADJ', 'NOUN', 'NUM'],
 'size': ['ADJ', 'NOUN', 'VERB'],
 'sleep': ['NOUN', 'VERB'],
 'slow': ['ADJ', 'ADV', 'VERB'],
 'small': ['ADJ', 'ADV', 'NOUN'],
 'snow': ['NOUN', 'VERB'],
 'so': ['ADV', 'NOUN'],
 'some': ['DET', 'PRON'],
 'song': ['NOUN'],
 'soon': ['ADV'],
 'sound': ['ADJ', 'NOUN', 'VERB'],
 'south': ['ADJ', 'ADV', 'NOUN'],
 'special': ['ADJ', 'NOUN'],
 'spell': ['NOUN', 'VERB'],
 'stand': ['NOUN', 'VERB'],
 'star': ['ADJ', 'NOUN', 'VERB'],
 'start': ['NOUN', 'VERB'],
 'state': ['NOUN', 'VERB'],
 'stay': ['NOUN', 'VERB'],
 'step': ['NOUN', 'VERB'],
 'still': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'stood': ['VERB'],
 'stop': ['NOUN', 'VERB'],
 'store': ['NOUN', 'VERB'],
 'story': ['NOUN'],
 'street': ['NOUN'],
 'strong': ['ADJ'],
 'study': ['NOUN', 'VERB'],
 'such': ['ADJ', 'ADV'],
 'sun': ['NOUN', 'VERB'],
 'sure': ['ADJ', 'ADV'],
 'surface': ['ADJ', 'NOUN', 'VERB'],
 'table': ['NOUN', 'VERB'],
 'tail': ['NOUN', 'VERB'],
 'take': ['NOUN', 'VERB'],
 'talk': ['NOUN', 'VERB'],
 'teach': ['NOUN', 'VERB'],
 'tell': ['NOUN', 'VERB'],
 'ten': ['ADJ', 'NOUN', 'NUM'],
 'test': ['NOUN', 'VERB'],
 'than': ['ADP', 'SCONJ'],
 'that': ['DET', 'PRON', 'SCONJ'],
 'the': ['DET'],
 'their': ['DET'],
 'them': ['PRON'],
 'then': ['ADJ', 'ADV', 'NOUN'],
 'there': ['ADV', 'NOUN'],
 'these': ['DET', 'PRON'],
 'they': ['PRON'],
 'thing': ['NOUN'],
 'think': ['NOUN', 'VERB'],
 'this': ['DET', 'PRON'],
 'those': ['DET', 'PRON'],
 'though': ['SCONJ'],
 'thought': ['NOUN', 'VERB'],
 'thousand': ['ADJ', 'NOUN', 'NUM'],
 'three': ['ADJ', 'NOUN', 'NUM'],
 'through': ['ADP', 'ADV'],
 'time': ['NOUN', 'VERB'],
 'to': ['ADP', 'PART'],
 'together': ['ADJ', 'ADV'],
 'told': ['VERB'],
 'too': ['ADV'],
 'took': ['VERB'],
 'top': ['ADJ', 'NOUN', 'VERB'],
 'toward': ['ADP'],
 'town': ['NOUN'],
 'travel': ['NOUN', 'VERB'],
 'tree': ['NOUN', 'VERB'],
 'true': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'try': ['NOUN', 'VERB'],
 'turn': ['NOUN', 'VERB'],
 'two': ['ADJ', 'NOUN', 'NUM'],
 'under': ['ADP', 'ADV'],
 'unit': ['NOUN'],
 'until': ['ADP', 'SCONJ'],
 'up': ['ADJ', 'ADV', 'VERB'],
 'us': ['PRON'],
 'use': ['NOUN', 'VERB'],
 'usual': ['ADJ'],
 'very': ['ADJ', 'ADV'],
 'voice': ['NOUN', 'VERB'],
 'vowel': ['NOUN'],
 'wait': ['NOUN', 'VERB'],
 'walk': ['NOUN', 'VERB'],
 'walked': ['VERB'],
 'want': ['NOUN', 'VERB'],
 'war': ['NOUN', 'VERB'],
 'warm': ['ADJ', 'ADV', 'VERB'],
 'was': ['AUX', 'VERB'],
 'watch': ['NOUN', 'VERB'],
 'water': ['NOUN', 'VERB'],
 'way': ['ADV', 'NOUN'],
 'we': ['PRON'],
 'week': ['NOUN'],
 'weight': ['NOUN', 'VERB'],
 'well': ['ADJ', 'ADV', 'NOUN', 'VERB'],
 'went': ['VERB'],
 'were': ['AUX', 'VERB'],
 'west': ['ADJ', 'ADV', 'NOUN'],
 'what': ['PRON'],
 'wheel': ['NOUN', 'VERB'],
 'when': ['ADV', 'SCONJ'],
 'where': ['ADV'],
 'which': ['DET', 'PRON'],
 'while': ['SCONJ'],
 'white': ['ADJ', 'NOUN', 'VERB'],
 'who': ['PRON'],
 'whole': ['ADJ', 'ADV', 'NOUN'],
 'why': ['ADV'],
 'will': ['AUX', 'NOUN', 'VERB'],
 'wind': ['NOUN', 'VERB'],
 'with': ['ADP'],
 'wonder': ['NOUN', 'VERB'],
 'wood': ['NOUN'],
 'word': ['NOUN', 'VERB'],
 'work': ['NOUN', 'VERB'],
 'world': ['ADJ', 'NOUN'],
 'would': ['AUX'],
 'write': ['VERB'],
 'wrote': ['VERB'],
 'year': ['NOUN'],
 'yes': ['NOUN'],
 'yet': ['ADV'],
 'you': ['PRON'],
 'young': ['ADJ', 'NOUN'],
 'your': ['DET']}

AUXILIARIES = ['am',
 'are',
 'be',
 'been',
 'can',
 'could',
 'did',
 'do',
 'does',
 'had',
 'has',
 'have',
 'is',
 'may',
 'might',
 'must',
 'should',
 'was',
 'were',
 'will',
 'would']

ADVERBS = ['again',
 'always',
 'early',
 'fast',
 'just',
 'late',
 'never',
 'often',
 'soon',
 'still',
 'together',
 'well']

NEGATIVES = ["don't", 'never', 'no', 'not']

MODIFIER_TYPES = {
    'color': {'black', 'blue', 'brown', 'gold', 'gray', 'green', 'grey', 'orange', 'pink', 'purple', 'red', 'silver', 'white', 'yellow'},
    'size': {'big', 'giant', 'huge', 'large', 'little', 'long', 'narrow', 'short', 'small', 'tall', 'thick', 'thin', 'tiny', 'wide'},
    'quantity': {'eight', 'eleven', 'few', 'five', 'four', 'hundred', 'many', 'nine', 'one', 'seven', 'several', 'six', 'ten', 'three', 'twelve', 'twenty', 'two', 'zero'},
    'shape': {'circle', 'circular', 'curved', 'flat', 'oval', 'rectangular', 'round', 'square', 'straight', 'triangle', 'triangular'},
    'age': {'ancient', 'modern', 'new', 'old', 'young'},
    'speed': {'fast', 'quick', 'rapid', 'slow'},
}



class SentenceReadingAgent:
    def __init__(self):
        self.names = set(NAMES)
        self.lemmas = LEMMAS
        self.word_types = WORD_TYPES
        self.auxiliaries = set(AUXILIARIES)
        self.adverbs = set(ADVERBS)
        self.negatives = set(NEGATIVES)
        self.determiners = {
            "a", "an", "the", "this", "that",
            "these", "those", "each", "every",
            "some", "all", "my", "your",
            "his", "her", "our", "their"
        }


    def tokenize_text(self, text):
        pattern = r"\d{1,2}:\d{2}(?:AM|PM)?|[A-Za-z]+(?:'[A-Za-z]+)?"
        return re.findall(pattern, text, flags=re.IGNORECASE)

    def normalize_word(self, word):
        word = word.lower()
        return self.lemmas.get(word, word)

    def classify_word(self, word):
        if (word in self.names):
            return["PROPN"]

        if re.fullmatch(r"\d{1,2}:\d{2}(?:AM|PM)?",word,flags=re.IGNORECASE):
            return ["TIME"]

        if word.lower() in self.determiners:
          types = self.word_types.get(word.lower(), [])
          return sorted(set(types) | {"DET"})

        return self.word_types.get(word.lower(), ["UNKNOWN"])

    
    def get_noun_segments(self, text, tokens):
        segments = []
        current_index = 0

        while( current_index < len(tokens)):
            word = tokens[current_index]
            types = self.classify_word(word)

            if ("NOUN" not in types and "PROPN" not in types and "PRON" not in types):
                current_index += 1
                continue

            start = current_index
            determiner = None
            modifiers = []

            previous_index = current_index - 1

            while( previous_index >= 0):
                previous_word = tokens[previous_index]
                previous_types = self.classify_word(previous_word)

                if ("ADJ" in previous_types or "NUM" in previous_types or "POSS" in previous_types):
                    modifiers.insert(0, previous_word)
                    start = previous_index
                    previous_index -= 1
                    continue

                if("DET" in previous_types):
                    determiner = previous_word
                    start = previous_index
                    break

                break

            segments.append({
                "start": start,
                "end": current_index,
                "key_index": current_index,
                "base": self.normalize_word(word),
                "original": word,
                "determiner": determiner,
                "modifiers": modifiers
            })

            current_index += 1

        return segments         


    def get_verb_segments(self, text, tokens):
        segments = []
        current_index = 0

        while (current_index < len(tokens)):
            word = tokens[current_index]
            types = self.classify_word(word)

            if("VERB" not in types and "AUX" not in types):
                current_index +=1
                continue

            start = current_index
            auxiliaries = []
            modifiers = []
            negative= False

            previous_index = current_index-1

            while(previous_index >=0):
                previous_word = tokens[previous_index]
                previous_types = self.classify_word(previous_word)

                if(previous_word.lower() in self.negatives):
                    negative = True

                    if "AUX" in previous_types:
                      auxiliaries.insert(0, previous_word)

                    start = previous_index
                    previous_index -=1
                    continue

                if("ADV" in previous_types):
                    modifiers.insert(0, previous_word)
                    start = previous_index
                    previous_index -= 1
                    continue

                if("AUX" in previous_types):
                    auxiliaries.insert(0, previous_word)
                    start = previous_index
                    previous_index -= 1
                    continue

                break

            # don't forget that verbs can have following moidifiers
            end = current_index
            next_index = current_index+1

            while(next_index < len(tokens)):
                 next_word = tokens[next_index]
                 next_types = self.classify_word(next_word)
                 if("ADV" in next_types):
                     modifiers.append(next_word)
                     end = next_index
                     next_index+=1
                     continue

                 break

            segments.append({
                  "start": start,
                  "end": end,
                  "key_index": current_index,
                  "base": self.normalize_word(word),
                  "original": word,
                  "auxiliaries": auxiliaries,
                  'modifiers': modifiers,
                  "negative": negative
              })


            current_index += 1

        return segments

    
    def get_preposition_segments(self, text, tokens, noun_segments):
        segments = []
        current_index = 0

        while(current_index <len(tokens)):
            word = tokens[current_index]
            types = self.classify_word(word)

            if("ADP" not in types):
                current_index +=1
                continue

            for noun_segment in noun_segments:
                if(noun_segment["start"] != current_index+1):
                    continue
                
                segments.append({
                    "start": current_index,
                    "end": noun_segment["end"],
                    "key_index": current_index,
                    "base": self.normalize_word(word),
                    "original": word,
                    "object_index": noun_segment["key_index"]
                  })
            
            current_index +=1

        return segments


    def get_infinitive_segments(self, tokens, verb_segments):
        segments = []

        for verb in verb_segments:
            verb_index = verb["key_index"]

            if(verb_index ==0):
                continue

            previous_index = verb_index -1
            previous_word = tokens[previous_index]

            if (previous_word.lower() != "to"):
                continue

            if (self.normalize_word(tokens[verb_index]) != tokens[verb_index].lower()):
                continue

            segments.append({"start": previous_index, "end": verb["end"], "key_index": verb_index, "base": verb["base"], "original": verb["original"]})

        return segments


    def filter_segments(self, tokens, noun_segments, verb_segments, preposition_segments):
        prep_object_indices = set()

        for preposition in preposition_segments:
            prep_object_indices.add(preposition["object_index"])

        filtered_nouns = []

        for noun in noun_segments:
            if(noun["key_index"] not in prep_object_indices):
                filtered_nouns.append(noun)

        resolved_nouns = []

        for noun in filtered_nouns:
            is_contained = False

            for other in filtered_nouns:
                if noun is other:
                    continue

                if(other["start"] <= noun["start"] and other["end"] >= noun["end"] and (other["start"] < noun["start"] or other["end"] > noun["end"])):
                    is_contained = True
                    break

            if not is_contained:
                resolved_nouns.append(noun)

        filtered_verbs = []
        

        for verb in verb_segments:
            verb_index = verb["key_index"]
            is_noun_phrase = False

            for noun in noun_segments:
                if(noun["key_index"] == verb_index and noun["determiner"] is not None):
                    is_noun_phrase = True
                    break

            if not is_noun_phrase and verb_index not in prep_object_indices:
                filtered_verbs.append(verb)

        resolved_verbs = []

        for verb in filtered_verbs:
            verb_index = verb["key_index"]
            is_aux_candidate = "AUX" in self.classify_word(tokens[verb_index])

            if(is_aux_candidate):
                used_as_aux = False

                for other in filtered_verbs:
                    if(other is verb):
                        continue

                    if(other["key_index"] > verb_index) and other["start"] <= verb_index and tokens[verb_index] in other["auxiliaries"]:
                        used_as_aux = True
                        break
                if used_as_aux:
                    is_linking_verb = ( verb["base"] == "be"
                        and any(other["key_index"] > verb_index and other["start"] <= verb_index and 
                                tokens[verb_index] in other["auxiliaries"] and "ADJ" in self.classify_word( tokens[other["key_index"]] )
                            for other in filtered_verbs
                        )
                    )

                    if not is_linking_verb:
                        continue

            resolved_verbs.append(verb)

        resolved_prepositions = []

        for preposition in preposition_segments:
            is_contained = False

            for other in preposition_segments:
                if preposition is other:
                  continue

                if(other["start"] <= preposition["start"] and other["end"] >= preposition["end"] and (other["start"] < preposition["start"] or other["end"] > preposition["end"])):
                    is_contained = True
                    break

            if not is_contained:
                resolved_prepositions.append(preposition)

        return resolved_nouns, resolved_verbs, resolved_prepositions

    def find_predicate(self, tokens, resolved_nouns, resolved_verbs, preposition_segments):
        if not resolved_verbs:
            return None


        candidates = []

        for verb in resolved_verbs:
            score = 0
            verb_index = verb["key_index"]

            for noun in resolved_nouns:
                if (noun["end"] < verb['start']):
                    score +=2
                    break 

            for noun in resolved_nouns:
                if noun["key_index"] == verb_index:
                    if noun["determiner"] is not None or noun["modifiers"]:
                        score -= 3
                        break

            if (verb["auxiliaries"]):
                score +=2

            if (verb["end"] > verb_index):
                score +=1

            for other in resolved_verbs:
                if other is verb:
                    continue

                if(other["start"] <= verb_index and verb_index <= other['end'] and verb["original"] in other["modifiers"]):
                    score -= 3
                    break

            if (verb["base"] == "be" ):
                for other in resolved_verbs:
                    if other is verb:
                        continue

                    if (other["key_index"] > verb_index and "ADJ" in self.classify_word(tokens[other["key_index"]]) and other['start'] <= verb_index):
                        score += 3
                        break

            candidates.append({
                  "verb": verb,
                  "score": score
              })

        best_score = max(candidate["score"] for candidate in candidates)

      
        minimum_score = best_score - 2
        best_candidate = None

        for candidate in candidates:
            if (candidate["score"] < minimum_score):
                continue

            verb = candidate["verb"]

            if (best_candidate is None or verb["key_index"] < best_candidate["key_index"]):
                best_candidate = verb

        return best_candidate

    def find_subject(self, tokens, resolved_nouns, predicate):
        if predicate is None:
            return None

        subject = None
        predicate_start = predicate["start"]

        for noun in resolved_nouns:
            if(noun["end"] >= predicate_start):
                continue

            if (subject is None or noun["end"] > subject["end"]):
                subject = noun

        if subject is None:
            return None

        subjects = [subject]
        conjunction = None

        while True:
            con_index = subjects[0]["start"]-1

            if con_index < 0:
              break

            word = tokens[con_index].lower()

            if word not in ("and", 'or', "nor"):
                break

            previous_noun = None

            for noun in resolved_nouns:
                if noun["end"] == con_index -1:
                    previous_noun = noun
                    break

            if previous_noun is None:
                break

            subjects.insert(0, previous_noun)
            conjunction = word

        return {"nouns": subjects, "conjunction": conjunction}

    
    def find_object_relationships(self,resolved_nouns,noun_segments,resolved_prepositions,predicate):
        if predicate is None:
            return None

        objects = []
        prepositions = []

        for noun in resolved_nouns:
            if noun["start"] > predicate["end"]:
                objects.append(noun)

        
        for preposition in resolved_prepositions:
            object_noun = None

            for noun in noun_segments:
                if (noun["key_index"] == preposition["object_index"]):
                    object_noun = noun
                    break

            if object_noun is not None:
                prepositions.append({"preposition": preposition,"object": object_noun})

        return {
            "objects": objects,
            "prepositions": prepositions
        }


    def analyze_question(self, question_tokens):
        if not question_tokens:
            return None

        words = []

        for token in question_tokens:
            words.append(token.lower())

        question_type = words[0].upper()
        preposition = None

        if question_type == "WHEN":
            question_type = "TIME"

        elif (question_type == "WHAT" and len(words) > 1 and words[1] == "time"):
            question_type = "TIME"

        elif (len(words) >= 3 and (words[0] == "at" and words[1] == "what" and words[2] == "time")):
            question_type = "TIME"
            preposition = None

        if (question_type == "HOW" and len(words) >1):
            if(words[1] in ("long", "far", "many")):
                question_type = "HOW_"+ words[1].upper()

        for word in words:
            if ("ADP" in self.classify_word(word)):
                preposition = word

        return {"type": question_type, "preposition": preposition}

    def answer_question(self, question_tokens, question_info, subject, object_relationships, predicate, sentence_tokens, resolved_nouns):
        if (question_info == None or object_relationships == None):
            return None

        if (question_info["type"] == "WHO"):
            question_words = []

            for word in question_tokens:
                question_words.append(word.lower())

            if ("was" in question_words or "were" in question_words):
                if (len(object_relationships["objects"]) > 1):
                    return object_relationships["objects"][0]["original"]
                
            if subject is not None and object_relationships["objects"]:

                subject_mentioned = False

                for noun in subject["nouns"]:
                    for word in question_tokens:
                        if (self.normalize_word(word) == noun["base"]):
                            subject_mentioned = True
                            break

                if not subject_mentioned and len(object_relationships["objects"]) > 1:
                    recipient = object_relationships["objects"][0]

                    if("NOUN" in self.classify_word(recipient["original"]) or "PRON" in self.classify_word(recipient["original"])):
                        return recipient["original"]
                    
            if question_info["preposition"] in ("in", "at", "on"):
              if subject is not None and subject["nouns"]:
                  return subject["nouns"][0]["original"]

            if (subject is not None and len(subject["nouns"]) > 1):
                if (subject["conjunction"] == "and"):

                    mentioned_subjects = []
                    other_subjects = []

                    for noun in subject["nouns"]:
                        mentioned = False

                        for word in question_tokens:
                            if (self.normalize_word(word) == noun["base"]):
                                mentioned = True
                                break

                        if mentioned:
                            mentioned_subjects.append(noun)
                        else:
                            other_subjects.append(noun)

                    if (question_info["preposition"] == "with" and mentioned_subjects and other_subjects):
                        return other_subjects[0]["original"]

            
            preposition = question_info["preposition"]

            if preposition is not None:

              for relationship in object_relationships["prepositions"]:

                  if (relationship["preposition"]["base"] != preposition):
                      continue

                  object_name = relationship["object"]["base"]

                  if (preposition == "with" and subject is not None):
                      for word in question_tokens:
                          if self.normalize_word(word) == object_name:
                              return subject["nouns"][0]["original"]

                  return relationship["object"]["original"]

              return None

            words = []

            for token in question_tokens:
                words.append(token.lower())

            if subject is not None:
                for noun in subject["nouns"]:
                    if noun["original"].lower() in words:

                        for object in object_relationships["objects"]:
                            if "PROPN" in self.classify_word(object["original"]):
                                return object["original"]

                        return None

            if subject is not None and subject["nouns"]:
                return subject["nouns"][0]['original']

        if (question_info["type"] == "WHAT"):
          if (subject is not None and predicate is not None and predicate["base"] == "be"):
            question_words = [word.lower() for word in question_tokens]

            for modifier in predicate["modifiers"]:
                if modifier.lower() in question_words:
                    return subject["nouns"][0]["original"]

            for noun in object_relationships["objects"]:
                if ( "ADJ" in self.classify_word(noun["original"]) and noun["original"].lower() in question_words):
                    return subject["nouns"][0]["original"]
                  
          if subject is not None:
              for noun in subject["nouns"]:

                  noun_mentioned = False

                  for word in question_tokens:
                      if self.normalize_word(word) == noun["base"]:
                          noun_mentioned = True
                          break

                  if not noun_mentioned:
                      continue
                  
                  for word in question_tokens:
                      modifier_type = word.lower()

                      if modifier_type not in MODIFIER_TYPES:
                          continue

                      for modifier in noun["modifiers"]:
                          if modifier.lower() in MODIFIER_TYPES[modifier_type]:
                              return modifier

          if subject is not None:
            for person_or_name in subject["nouns"]:

                if person_or_name["base"] not in [self.normalize_word(word) for word in question_tokens]:
                    continue

                for noun in resolved_nouns:
                    if (noun["end"] == person_or_name["start"] - 1 and (object_relationships is None or not object_relationships["objects"])):
                        if ("NOUN" in self.classify_word(noun["original"])):
                            return noun["original"]

          if subject is not None:
            subject_mentioned = False

            for noun in subject["nouns"]:
                for word in question_tokens:
                    if (self.normalize_word(word) == noun["base"]):
                        subject_mentioned = True
                        break

            if not subject_mentioned and not object_relationships["objects"]:
                return subject["nouns"][0]["original"]

          for noun in object_relationships["objects"]:

              if "PRON" in self.classify_word(noun["original"]):
                  continue

              answer = noun["original"]

          return answer if "answer" in locals() else None

        if (question_info["type"] == "HOW_LONG"):

          for noun in object_relationships["objects"]:

              for word in question_tokens:
                  if (self.normalize_word(word) == noun["base"]):
                      if noun["modifiers"]:
                          return noun["modifiers"][0]

          return None

        if (question_info["type"] == "HOW_MANY"):
                  for noun in resolved_nouns:
                      for modifier in reversed(noun["modifiers"]):
                          if ("NUM" in self.classify_word(modifier)):
                              return modifier

                          
        if (question_info["type"] == "WHERE"):

            if object_relationships is None:
                return None

            destination = None

            for relationship in object_relationships["prepositions"]:

                preposition = relationship["preposition"]
                noun = relationship["object"]

                if preposition["base"] in ("to", "in", "at", "on"):
                    destination = noun["original"]

            return destination

        if (question_info["type"] == "HOW_FAR"):

          if object_relationships is None:
              return None

          distance_units = {"mile", "foot", "yard", "meter", "kilometer"}

          for noun in object_relationships["objects"]:
              if noun["base"] in distance_units:
                  return noun["original"]

          return None

        
        if (question_info["type"] == "HOW"):

            for word in question_tokens:
              word = word.lower()

              for category, values in MODIFIER_TYPES.items():
                  if word in values:

                      if predicate is not None:
                          for modifier in predicate["modifiers"]:
                              if modifier.lower() in values:
                                  return modifier

            if predicate is not None:
                return predicate["original"]

            return None

        if (question_info["type"] == "TIME"):

          for word in sentence_tokens:
              if "TIME" in self.classify_word(word):
                  return word

          return None



        return None

                
        
    def solve(self, sentence, question):
    
        '''
          You can use a library like spacy (https://spacy.io/usage/linguistic-features) to preprocess the
            mostcommon.txt file. There are others that could be used but you must use them in preprocessing only.
            You CANNOT import the library into Gradescope.
          
          You must include whatever preprocessing you've done into your SentenceReadingAgent.py.
          
          DO NOT use another file .txt or .csv. Hard code your DICTS | LISTS into this .py file
          
          While the supplied mostcommon.txt contains most of the common words you will need
            you can (and SHOULD) expand the file as you find cases that the agent has problems
            processing. 
            
          Also not all words will be processed using the correct lexing for every possible problem the 
            agent might encounter and you are ENCOURAGED to expand these in your agents knowledge representation.
        '''
        try:
            sentence_tokens = self.tokenize_text(sentence)
            question_tokens = self.tokenize_text(question)

            noun_segments = self.get_noun_segments(sentence, sentence_tokens)
            verb_segments = self.get_verb_segments(sentence, sentence_tokens)
            infinitive_segments = self.get_infinitive_segments(sentence_tokens,verb_segments)
            preposition_segments = self.get_preposition_segments(
                sentence,
                sentence_tokens,
                noun_segments
            )

            resolved_nouns, resolved_verbs, resolved_prepositions = (
                self.filter_segments(
                    sentence_tokens,
                    noun_segments,
                    verb_segments,
                    preposition_segments
                )
            )

            predicate = self.find_predicate(
                sentence_tokens,
                resolved_nouns,
                resolved_verbs,
                preposition_segments
            )

            subject = self.find_subject(
                sentence_tokens,
                resolved_nouns,
                predicate
            )


            object_relationships = self.find_object_relationships(
                resolved_nouns,
                noun_segments,
                resolved_prepositions,
                predicate
            )

            question_info = self.analyze_question(question_tokens)

            answer = self.answer_question(
                question_tokens,
                question_info,
                subject,
                object_relationships,
                predicate,
                sentence_tokens,
                resolved_nouns
            )

            return answer if answer is not None else ""
        except Exception:
          return ""




if __name__ == "__main__":
    agent = SentenceReadingAgent()

    examples = [
        ("Ada brought a short note to Irene.", [
            "Who brought the note?",
            "What did Ada bring?",
            "Who did Ada bring the note to?",
            "How long was the note?"
        ]),
        ("David and Lucy walk one mile to school at 8:00AM.", [
            "Who does Lucy walk with?",
            "Where do David and Lucy walk?",
            "How far do David and Lucy walk?",
            "At what time do David and Lucy walk to school?"
        ]),
        ("The blue bird will sing in the morning.", [
            "What color is the bird?"
        ]),
        ("My dog Red is very large.", [
            "What animal is Red?",
            "How big is Red?"
        ])
    ]

    for sentence, questions in examples:
        print(f"\n{'=' * 60}")
        print(f"SENTENCE: {sentence}")
        print("-" * 60)

        for question in questions:
            answer = agent.solve(sentence, question)
            print(f"Q: {question}")
            print(f"A: {answer}\n")