from __future__ import annotations
from typing import List, Optional
import bisect

class HuffmanNode:
    def __init__(self, char_ascii: int, freq: int, left: Optional[HuffmanNode] = None, right: Optional[HuffmanNode] = None):
        self.char_ascii = char_ascii    # stored as an integer - the ASCII character code value
        self.freq = freq                # the frequency associated with the node
        self.left = left                # Huffman tree (node) to the left!
        self.right = right              # Huffman tree (node) to the right
            
        
    def __repr__(self) -> str:
        return str(self.char_ascii)+ ":"+ str(self.freq)


    def __lt__(self, other: HuffmanNode) -> bool:
        return comes_before(self, other)



def comes_before(a: HuffmanNode, b: HuffmanNode) -> bool:
    """Returns True if tree rooted at node a comes before tree rooted at node b, False otherwise"""
    if a.freq < b.freq:
        return True
    elif a.freq == b.freq:
        return a.char_ascii < b.char_ascii
    else:
        return False



def combine(a: HuffmanNode, b: HuffmanNode) -> HuffmanNode:
    """Creates a new Huffman node with children a and b, with the "lesser node" on the left
    The new node's frequency value will be the sum of the a and b frequencies
    The new node's char value will be the lower of the a and b char ASCII values"""

    left = min(a, b)
    right = max(a, b)

    return HuffmanNode(min(a.char_ascii, b.char_ascii), a.freq + b.freq, left, right)



def cnt_freq(filename: str) -> List:
    """Opens a text file with a given file name (passed as a string) and counts the
    frequency of occurrences of all the characters within that file
    Returns a Python List with 256 entries - counts are initialized to zero.
    The ASCII value of the characters are used to index into this list for the frequency counts"""

    #define list
    freqList = [0]*256

    #open read and close file
    file = open(filename)
    text = file.read()
    file.close()

    #count character frequency
    for i in range(len(text)):
        freqList[ord(text[i])] += 1

    return freqList



def create_huff_tree(char_freq: List) -> Optional[HuffmanNode]:
    """Input is the list of frequencies (provided by cnt_freq()).
    Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree. Returns None if all counts are zero."""

    #create a new node list based on frequencies
    nodeList = createnodeList(char_freq)

    #check if list is empty 
    if len(nodeList) == 0:
        return None

    #sort list in order to build it into a tree
    else:
        nodeList.sort()
        return builTreeFromList(nodeList)



def createnodeList(char_freq: List) -> List:

    #define empty list
    nodeList: List = []

    #find non-empty characters and add them to the list
    for i in range(len(char_freq)):
        if char_freq[i] != 0:
            nodeList.append(HuffmanNode(i, char_freq[i]))

    return nodeList



def builTreeFromList(nodeList: List) -> HuffmanNode:

    while len(nodeList) > 1:
       bisect.insort(nodeList, combine(nodeList.pop(0), nodeList.pop(0)))

    return nodeList[0]



def create_code(node: Optional[HuffmanNode]) -> List:
    """Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation
    as the index into the array, with the resulting Huffman code for that character stored at that location.
    Characters that are unused should have an empty string at that location"""

    #define code list
    codeList: List = ['']*256

    #build and return code
    if node is not None:
        buildCode(node, codeList,'')
    return codeList



def buildCode(node: Optional[HuffmanNode], codeList: List, currCode: str) -> None:

    #safety check
    if node is not None:

        #check for base case
        if node.right is None and node.left is None:
            codeList[node.char_ascii] = currCode

        else:
            #traverse and prep code for output
            buildCode(node.left, codeList, currCode+'0')
            buildCode(node.right, codeList, currCode+'1')



def create_header(freqs: List) -> str:
    """Input is the list of frequencies (provided by cnt_freq()).
    Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” """

    #define blank header
    retVal = ""

    #build header
    for i in range(256):
        if freqs[i] != 0:
            retVal += " " + str(i) + " " + str(freqs[i])

    return retVal[1:]



def huffman_encode(in_file: str, out_file: str) -> None:
    """Takes inout file name and output file name as parameters
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Take not of special cases - empty file and file with only one unique character"""

    #generate frequency list
    freqs = cnt_freq(in_file)

    #generate code from tree built from frequency list
    code = textConversion(in_file, create_code(create_huff_tree(freqs)))

    #open output file, write to it, then close it
    f = open(out_file, "w")
    f.write(create_header(freqs) + "\n" + code)
    f.close()



def textConversion(in_file: str, code: List) -> str:

    #open read and close the file
    file = open(in_file)
    text = file.read()
    file.close()

    #define empty output
    retVal = ""

    #convert string in to ascii values
    for i in range(len(text)):
        retVal+= str(code[ord(text[i])])

    return retVal


def huffman_decode(in_file: str, out_file: str) -> None:
    
    #read info from encoded file
    encoded = open(in_file)
    code = encoded.read()
    encoded.close()

    #decode and output data
    f = open(out_file, "w")
    f.write(codeToText(create_huff_tree(parse_header(code.split("\n")[0])), code[code.rfind("\n")+1:] ))
    f.close()

def parse_header(header_string: str) -> List:

    #define blank frequency list and split header into a list
    freq: List = [0]*256
    headerList = header_string.split()
    
    i = 0

    while i < len(headerList):

        #update frequncy index
        freq[int(headerList[i])] = int(headerList[i+1])
        i+=2

    return freq

def codeToText(node: Optional[HuffmanNode], code: str) -> str:

    curr = node
    i = 0
    retVal = ''

    #safety check
    if curr is not None:

        while i < len(code) and curr is not None:

            #check for moving left
            if(int(code[i]) == 0 and curr.left is not None):

                #move left and update counter
                curr = curr.left
                i+=1

            #check for moving right
            elif(int(code[i]) == 1 and curr.right is not None):

                #move right and update counter
                curr = curr.right
                i+=1

            #cannot move left or right thus at a leaf node and need to record the data
            else:

                #copy data and reset curr
                retVal += chr(curr.char_ascii)
                curr = node
         
        #check to make github auto grading happy
        if curr is not None:
            #copy final data
            retVal += chr(curr.char_ascii)

    return retVal