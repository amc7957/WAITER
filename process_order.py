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
    request: {<MD><PRP><VB>?<VB>}                   #'can I get'
             {<VB><PRP><VB>?<VB>}                   #'let me get'
    extras: {<IN><NN>+<CC>?<NN>?}                   #'with lettuce, tomato, cheese, and mayo'
               }<IN>{                                   #remove 'with'
               }<CC>{                                   #remove 'and'
    item: {<NN>+}                                   #grabs all remaining items
    """
    parser = nltk.RegexpParser(grammar)         #build parser
    orderTree = parser.parse(POStagged)         #parse

    return orderTree


def assemble_order(number, numberSize, numberMulti, numberSizedMulti, items, menu ):
    """Retrieve order information from chunks and assemble into summary 
    for output to GUI.
    """

    # Initialize variable
    order = []
    
    # Single number orders, no size idicator
    for i in range(len(number)):
        numberString = number[i]
        numberToken = nltk.word_tokenize(numberString)
        numberEntry = 'MD ' + numberToken[0].capitalize() + ' ' + numberToken[1].capitalize()
        if numberEntry:
            order.append(numberEntry)

    # Multi order - first item is amount, second and third are order number
    for i in range(len(numberMulti)):
        multiString = numberMulti[i]
        multiToken = nltk.word_tokenize(multiString)
        amount = multiToken[0]                                                                        #first item is amount
        multiOrderEntry = 'MD ' + multiToken[1].capitalize() + ' ' + multiToken[2].capitalize()       #remaining items cover the order number

        # Add appropriate number of orders to the menu
        if amount == 'one':
            j = 1
        elif amount == 'two':
            j = 2
        elif amount == 'three':
            j = 3
        elif amount == 'four':
            j = 4

        # Add orders
        for i in range(j):
            order.append(multiOrderEntry)

    # Sized order - first item is size, second and third are order number
    for i in range(len(numberSize)):
        sizeString = numberSize[i]
        sizeToken = nltk.word_tokenize(sizeString)
        size = sizeToken[0]
        
        # Get appropriate size signifier
        if size == 'small':
            size = 'SM'
        elif size == 'medium':
            size = 'MD'
        elif size == 'large':
            size = 'LG'
        
        # Add orders
        sizeOrderEntry = size + ' ' + sizeToken[1].capitalize() + ' ' + sizeToken[2].capitalize()
        order.append(sizeOrderEntry)

    # Sized multi-orders - first item is number of orders, second item is size, third and fourth are order number
    for i in range(len(numberSizedMulti)):
        sizedMultiString = numberSizedMulti[i]
        sizedMultiToken = nltk.word_tokenize(sizedMultiString)
        amount = sizedMultiToken[0]
        size = sizedMultiToken[1]

        # Add appropriate number of orders to the menu
        if amount == 'one':
            j = 1
        elif amount == 'two':
            j = 2
        elif amount == 'three':
            j = 3
        elif amount == 'four':
            j = 4

        # Get appropriate size signifier
        if size == 'small':
            size = 'SM'
        elif size == 'medium':
            size = 'MD'
        elif size == 'large':
            size = 'LG'

        # Add orders
        for i in range(j):
            sizedMultiOrderEntry = size + ' ' + sizedMultiToken[2].capitalize() + ' ' + sizedMultiToken[3].capitalize()
            order.append(sizedMultiOrderEntry)

    # Individual items
    for i in range(len(items)):
        item = items[i]
        order.append(item)

    return order
        


def process_order(string, menu):
    """Function to take order, process with NLTK to determine what user is asking for, and 
    summarize output as list of"""

    # Create list of stop words to remove from processing
    stopWords = set(stopwords.words('english'))         #stopwords
    stopWords.add('please')         #add words to be included
    stopWords.add('get')            #as stopwords
    stopWords.add('let')
    stopWords.remove('a')
    stopWords.remove('with')
    stopWords.remove('and')
    stopWords.remove('no')

    # Receive input string and use NLTK to chunk
    orderTree = take_order(string, stopWords)
    orderTree.draw()

    # See which chunks were present
    orderNumber = get_chunk(orderTree, 'orderNumber')
    orderNumberSize = get_chunk(orderTree, 'orderNumberSize')
    orderNumberMulti = get_chunk(orderTree, 'orderNumberMulti')
    orderNumberSizedMulti = get_chunk(orderTree, 'orderNumberSizedMulti')
    extras = get_chunk(orderTree, 'extras')
    items = get_chunk(orderTree,'item')

    # Assemble output list of strings
    orderOutput = assemble_order(orderNumber, orderNumberSize, orderNumberMulti, orderNumberSizedMulti, items, menu)

    return orderOutput