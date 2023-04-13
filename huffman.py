import os
from utils import UPLOAD_COMPRESSED_FILE,UPLOAD_DECOMPRESSED_FILE

class Node:
    def __init__(self,char,freq,left=None,right=None) -> None:
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

class Heap:
    def __init__(self) -> None:
        self.arr = []
        
    def shiftup(self,i):
        parent = (i-1) // 2
        
        while i > 0 and self.arr[i].freq < self.arr[parent].freq:
            self.arr[i],self.arr[parent] = self.arr[parent],self.arr[i]
            i = parent
            parent = (i-1) // 2
    
    def shiftdown(self,i):
        leftChild = 2*i+1
        rightChild = 2*i+2
        n = len(self.arr)
                
        while (leftChild < n and self.arr[leftChild].freq < self.arr[i].freq) or (rightChild < n and self.arr[rightChild].freq < self.arr[i].freq):
            smaller = leftChild if rightChild >= n or self.arr[leftChild].freq <= self.arr[rightChild].freq else rightChild
            self.arr[i],self.arr[smaller] = self.arr[smaller],self.arr[i]
            i = smaller
            leftChild = 2*i+1
            rightChild = 2*i+2         
    
    def insert(self,val):
        self.arr.append(val)
        i = len(self.arr) - 1
        self.shiftup(i)
    
    def delete(self):
        n = len(self.arr)
        self.arr[0],self.arr[n-1] = self.arr[n-1],self.arr[0]
        node = self.arr.pop()
        self.shiftdown(0)
        return node
    
    def length(self):
        return len(self.arr)
            
class HuffmanCoding:
    def __init__(self,path=""):
        self.path = path
        self.heap = Heap()
        self.root = None
        self.code = None
        self.revCode = None
    
    def __create_freq_dict(self,text):
        freq = {}
        for char in text:
            if char not in freq:
                freq[char] = 0
            freq[char]+=1
        return freq

    def __createHeap(self,freq):
        for char in freq:
            node = Node(char,freq[char])
            self.heap.insert(node)
    
    def __createBinaryTree(self):
        while self.heap.length() > 1:
            
            node1 = self.heap.delete()
            node2 = self.heap.delete()
            
            connectingNode = Node('',(node1.freq+node2.freq),node1,node2)
            
            self.heap.insert(connectingNode)
        
        self.root = self.heap.delete()
    
    def __get_char_codes(self):
        
        code = dict()
        
        def helper(node,bits):     
            if node.char:
                code[node.char] = bits
                return 
            
            helper(node.left,bits+'0')
            helper(node.right,bits+'1')

        helper(self.root,'')
        self.code = code
    
    def __get_encoded_text(self,text):
        encoded_text = ''
        
        for char in text:
            encoded_text += self.code[char]
        
        return encoded_text

    def __get_padded_text(self,encoded_text):
        padding = 8 - (len(encoded_text) % 8)
        for _ in range(padding):
            encoded_text+='0'
        padding_bits = "{0:008b}".format(padding)
        padded_text = padding_bits + encoded_text
        return padded_text

    def __get_bytes_text(self,padded_text):
        bytes = []
        
        for i in range(0,len(padded_text),8):
            byte = int(padded_text[i:i+8],2)
            bytes.append(byte)
        
        return bytes
    
    def compression(self):
        fileName,_ = os.path.splitext(self.path)
        fileName = fileName.split('/')
        output_file = UPLOAD_COMPRESSED_FILE + fileName[len(fileName)-1] + '.bin'        
        
        with open(self.path) as file, open(output_file,'wb') as output:
            text = file.read()
            text = text.rstrip()
            
            freq = self.__create_freq_dict(text)
            self.__createHeap(freq) 
            self.__createBinaryTree()
            self.__get_char_codes()
            encoded_text = self.__get_encoded_text(text)
            padded_text = self.__get_padded_text(encoded_text)
            bytes_array = self.__get_bytes_text(padded_text)
            bytes_text = bytes(bytes_array)
            
            output.write(bytes_text)
    
    def __remove_padding(self,string):
        padding = int(string[:8],2)
        removed_padding_text = string[8:len(string)-padding]
        return removed_padding_text
    
    def __create_rev_code(self):
        rev_code = dict()
        for key in self.code:
            rev_code[self.code[key]] = key
        self.revCode = rev_code

    def __get_decoded_text(self,string):
        bits = ''
        decoded_text = ''
        for bit in string:
            bits+=bit
            if bits in self.revCode:
                decoded_text+=self.revCode[bits]
                bits = ''
        return decoded_text
    
    def decompression(self,fileName):
        read_file = UPLOAD_COMPRESSED_FILE + fileName + '.bin'
        output_file =  UPLOAD_DECOMPRESSED_FILE + fileName + '_decompressed.txt'     
        string = "" 
        # 3 -> 0b11 (11) -> (000000011)
        with open(read_file,'rb') as file, open(output_file,'w+') as output:
            byte = file.read(1)
            
            while byte:
                byte = ord(byte)
                text = bin(byte)[2:].rjust(8,'0')
                string += text
                byte = file.read(1)
        
            removed_padding_text = self.__remove_padding(string)
            self.__create_rev_code()
            decoded_text = self.__get_decoded_text(removed_padding_text)
            output.write(decoded_text)
    
    
huffmanCoding = HuffmanCoding()