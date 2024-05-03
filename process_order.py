import nltk
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords

def get_chunk(tree, label):
    """Retrieve chunk from output tree object."""

    chunk = []
    if hasattr(tree, 'label') and tree.label() == label:
        chunk.append(' '.join([element[0] for element in tree]))
    for element in tree:
        if isinstance(element, nltk.Tree):
            chunk.extend(get_chunk(element, label))
    return chunk


def take_order(string,stopWords):
    """Determine what user is trying to order by following 
    these steps:
        -tokenize string
        -filter out stop words
        -lemmatize to reduce varying forms
        -part-of-speech (POS) tag
        -assign grammar rules and form NP-chunks
    """

    # Tokenize sentence
    tokenized = nltk.word_tokenize(string)

    # Filter out stop words as these won't be useful to the order    
    filtered = [word.lower() for word in tokenized if not word.lower() in stopWords]

    # Lemmatize sentence to remove plurals
    lemma = WordNetLemmatizer() 
    lemmatized = [lemma.lemmatize(word) for word in filtered]

    # POS Tag sentence
    POStagged = nltk.pos_tag(lemmatized)

    # Chunk POS Tagged Sentence
    # Assign grammar rules
    grammar = """                           
    orderNumberSizedMulti: {<CD><NN|JJ><NN><CD>}    #'three small number ones'
    orderNumberMulti: {<CD><NN><CD>}                #'three number ones'
    orderNumberSize: {<NN|JJ><NN><CD>}              #'medium number two'
    orderNumber: {<NN><CD>}                         #'number three'
    extras: {<NN>+<IN><NN>+<CC>?<NN>?}              #'with lettuce, tomato, cheese, and mayo'
    item: {<NN>+}                                   #grabs all remaining items
    """
    parser = nltk.RegexpParser(grammar)         #build parser
    orderTree = parser.parse(POStagged)         #parse

    return orderTree


def assemble_order(number, numberSize, numberMulti, numberSizedMulti, items, extras):
    """Retrieve order information from chunks and assemble into summary 
    for output to GUI.
    """

    # Initialize variable
    orderList = []
    
    # Single number orders, no size idicator
    for i in range(len(number)):
        numberString = number[i]
        orderList.append(numberString)

    # Multi order - first item is amount, second and third are order number
    for i in range(len(numberMulti)):
        multiString = numberMulti[i]
        orderList.append(multiString)

    # Sized order - first item is size, second and third are order number
    for i in range(len(numberSize)):
        sizeString = numberSize[i]
        orderList.append(sizeString)

    # Sized multi-orders - first item is number of orders, second item is size, third and fourth are order number
    for i in range(len(numberSizedMulti)):
        sizedMultiString = numberSizedMulti[i]
        orderList.append(sizedMultiString)

    # Individual items
    for i in range(len(items)):
        item = items[i]
        orderList.append(item)

    # Output extras
    for i in range(len(extras)):
        extra = extras[i]
        orderList.append(extra)

    return orderList


def check_menu(orderList, menu):
    
    # Initialize variable
    orderOutput = []

    # Loop through each item ordered and check if it is on the menu
    for entry in orderList:
        onMenu = False
        for item in menu:                       #see if any item on the menu matches what was ordered
            if item in entry:
                onMenu = True
        if onMenu==True:
            orderOutput.append(entry)

    return orderOutput


def process_order(string,menu):
    """Function to take order, process with NLTK to determine what user is asking for, and 
    summarize output as list of"""

    # Create list of stop words to remove from processing
    stopWords = set(stopwords.words('english'))     
    stopWords.add('please')                             #add words to be included in list
    stopWords.add('get')            
    stopWords.add('let')
    stopWords.remove('a')                               #remove some words so they aren't ignored
    stopWords.remove('with')
    stopWords.remove('and')
    stopWords.remove('no')

    # Receive input string and use NLTK to chunk
    orderTree = take_order(string, stopWords)

    # See which chunks were present
    orderNumber = get_chunk(orderTree, 'orderNumber')
    orderNumberSize = get_chunk(orderTree, 'orderNumberSize')
    orderNumberMulti = get_chunk(orderTree, 'orderNumberMulti')
    orderNumberSizedMulti = get_chunk(orderTree, 'orderNumberSizedMulti')
    extras = get_chunk(orderTree, 'extras')
    items = get_chunk(orderTree,'item')

    # Assemble output list of strings
    orderList = assemble_order(orderNumber, orderNumberSize, orderNumberMulti, orderNumberSizedMulti, items, extras)

    # Check if items are on menu
    orderOutput = check_menu(orderList, menu) 

    return orderOutput, orderTree