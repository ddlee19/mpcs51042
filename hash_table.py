'''
MPCS 51042 S'20: Markov models and hash tables

DANIEL LEE
'''
from map import Map

class Hashtable(Map):
    
    def __init__(self, capacity, defVal, loadfactor, growthFactor):
        '''
        Constructor of Hashtable.

        Params:
            capacity: the initial number of cells to use. It must create a list of empty cells with 
                the specified length. You can assume the value passed in for the initial number of 
                cells will be greater than 0.
            defVal: a value to return when looking up a key that has not been inserted
            loadfactor: a floating point number ((0, 1]). If the fraction of occupied cells grows
                beyond the loadfactor after an update, then you must perform a rehashing of the table.
                Rehashing is described below
            growthFactor: an integer greater than or 1 that represents how much to grow the table by 
                when rehashing. For example, if growthFactor = 2 then the size of the hash table will 
                double each time we rehash.
        '''
        self._capacity = capacity

        self._defval = defVal

        self._loadfactor = loadfactor

        self._growthfactor = growthFactor

        #Create list of empty cells with specified capacity
        self._lst = [()]*capacity


    def __getitem__(self, key):
        '''
        Similiar to the __getitem__ method for a Python dictionary, this will 
        return the value associated with key in the map.

        Params:
            key: key of cell to look up and return value associated 
        '''
    
        #If key is not contained in hash table, return defval
        if key not in self:
            return self._defval
            
        else:
            #Calculate hash value of key
            hash_val = self._hash(key)

            cell = self._lst[hash_val]

            #If keys match, return value
            if cell[0] == key:
                return cell[1]

            #Else, increment hash_val to look for key after collision
            while self._lst[hash_val]:

                #If keys match, return value
                if self._lst[hash_val][0] == key:
                    return self._lst[hash_val][1]
                
                hash_val += 1
                if hash_val >= self._capacity:
                    hash_val = 0
            
    
    def __delitem__(self, key):
        '''
        "Logically delete" the key-value pairing inside the map.

        Params:
            key: key of cell to delete
        '''
        
        #Return defval if key not in table
        if key not in self:
            return self._defval

        else:
            #Calculate hash value of key
            hash_val = self._hash(key)

            #Replace cell of key with empty cell if keys match
            if self._lst[hash_val][0] == key:
                self._lst[hash_val] = (self._lst[hash_val][0], self._lst[hash_val][1], False)

            else:
                while self._lst[hash_val]:
                    #If keys match, logically delete cell
                    if self._lst[hash_val][0] == key:
                        self._lst[hash_val] = (self._lst[hash_val][0], self._lst[hash_val][1], False)
                        break
                    
                    hash_val += 1
                    if hash_val >= self._capacity:
                        hash_val = 0

        


    def __setitem__(self, key, value):
        '''
        Adds or update the key-value pairing inside the map.

        Params:
            key: key of cell to add or update
        '''

        #Calculate hash val
        hash_val = self._hash(key)

        #If key not in table, insert key-val pairing
        if key not in self:
            
            #If fraction of occupied cells grow beyond loadfactor with insert, rehash
            if ((len(self) + 1) / self._capacity) > self._loadfactor:
                self.rehash()

                #Recalculate hash_val
                hash_val = self._hash(key)

            #If cell at hash_val is empty, insert
            if not self._lst[hash_val]:
                self._lst[hash_val] = (key, value, True)

            #Else, collision happened so increment hash_val
            else:
                while self._lst[hash_val]:
                    hash_val += 1
                    if hash_val >= self._capacity:
                        hash_val = 0
                
                self._lst[hash_val] = (key, value, True)


            self._lst[hash_val] = (key, value, True)

        #If key in table, update value
        else:

            #Update value at hash val if keys match
            if self._lst[hash_val][0] == key:
                self._lst[hash_val] = (key, value, True)
            
            #Else, check for collision and increment hash_val
            else:
                while self._lst[hash_val]:
                    
                    #If keys match, update value
                    if self._lst[hash_val][0] == key:
                        self._lst[hash_val] = (key, value, True)
                        break
                    
                    hash_val += 1
                    if hash_val >= self._capacity:
                        hash_val = 0
          


    def __contains__(self, key):
        '''
        Returns True if the key-value pairing is inside the map; otherwise, if not
        then returns False.

        Params:
            key: key to lookup
        '''

        #Calculate hash_val
        hash_val = self._hash(key)

        cell = self._lst[hash_val]

        #If cell at hash_val is empty, return False
        if not cell:
            return False

        else:
            #If key at hash_val matches, return True
            if key == cell[0]:
                return True

            #Else, increment hash_val while cells are not empty and check if keys match
            else:
                while self._lst[hash_val]:
                    #Check if keys match
                    if self._lst[hash_val][0] == key:
                        return True

                    hash_val += 1
                    if hash_val >= self._capacity:
                        hash_val = 0

                return False
            

    def keys(self):
        '''
        Returns an iterable object (of your choosing) with all the keys inside 
        the map.
        '''

        keys = []

        for tup in self._lst:
            if tup and tup[2]:
                keys.append(tup[0])

        return keys

    
    def values(self):
        '''
        Returns an iterable object (of your choosing) with all the values inside
        the map. 
        '''

        values = []
        for tup in self._lst:
            if tup and tup[2]:
                values.append(tup[1])

        return values

    def __len__(self):
        '''
        Returns the number of items in the map. 
        It needs no parameters and returns an integer.
        '''
        count = 0

        for tup in self._lst:
            if tup and tup[2]:
                count += 1

        return count

    def __bool__(self):
        '''  
        Returns whether the map is empty or not. 
        it needs no parameters and returns a bool.
        ''' 

        if len(self) == 0:
            return False

        else:
            return True

    def __iter__(self):
        '''
        Returns an iterator of key-val pairs in map.
        '''

        pairs = []

        for tup in self._lst:
            if tup:
                pairs.append(tup[:2])

        return iter(pairs)


    def _hash(self, key):
        '''
        Takes in a string and returns a hash value. Uses the standard hashing function (i.e. Horner's method).
        Returns hash value of string key

        Params:
            key: string to hash
        '''

        #Relatively prime number for multiplier
        multiplier = 37

        #Initial hash_val is ord of first character in key
        hash_val = 0

        #Horner's method to calculate hash_val using rest of chars in key
        for char in key:
            hash_val = (hash_val * multiplier + ord(char)) % self._capacity            
        
        return hash_val


    def rehash(self):
        '''
        Rehash table when called. Expands size of hash table and migrates all the existing data into 
        their proper locations in newly-expanded hash table.
        Grows size of new table by growthfactor.
        '''
        
        #If old table's list is not empty, create copy of existing data
        old_lst = []

        if len(self) > 0:
            for tup in self._lst:
                if tup and tup[2]:
                    old_lst.append(tup)

        #Expand size of new hash table by growthfactor
        self._capacity = self._capacity * self._growthfactor
        self._lst = [()] * self._capacity
        
        #Migrate pre-existing data into proper location in new hash table if old_lst is not empty
        if old_lst:    
            for item in old_lst:
               
                #Get new hash vals
                hash_val = self._hash(item[0])

                #If cell at hash_val is empty, insert
                if not self._lst[hash_val]:
                    self._lst[hash_val] = (item[0], item[1], True)

                #Else, collision happened so increment hash_val
                else:
                    while self._lst[hash_val]:
                        hash_val += 1
                        if hash_val >= self._capacity:
                            hash_val = 0
                    
                    self._lst[hash_val] = (item[0], item[1], True)

            