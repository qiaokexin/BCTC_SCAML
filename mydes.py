import sys
import numpy as np

# _pythonMajorVersion is used to handle Python2 and Python3 differences.
_pythonMajorVersion = sys.version_info[0]


    
    
#############################################################################
#                     DES                        #
#############################################################################
class mydes:


    # Permutation and translation tables for DES
    __pc1 = [56, 48, 40, 32, 24, 16,  8,
          0, 57, 49, 41, 33, 25, 17,
          9,  1, 58, 50, 42, 34, 26,
         18, 10,  2, 59, 51, 43, 35,
         62, 54, 46, 38, 30, 22, 14,
          6, 61, 53, 45, 37, 29, 21,
         13,  5, 60, 52, 44, 36, 28,
         20, 12,  4, 27, 19, 11,  3
    ]

    # number left rotations of pc1
    __left_rotations = [
        1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
    ]

    # permuted choice key (table 2)
    __pc2 = [
        13, 16, 10, 23,  0,  4,
         2, 27, 14,  5, 20,  9,
        22, 18, 11,  3, 25,  7,
        15,  6, 26, 19, 12,  1,
        40, 51, 30, 36, 46, 54,
        29, 39, 50, 44, 32, 47,
        43, 48, 38, 55, 33, 52,
        45, 41, 49, 35, 28, 31
    ]

    # initial permutation IP
    __ip = [57, 49, 41, 33, 25, 17, 9,  1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7,
        56, 48, 40, 32, 24, 16, 8,  0,
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6
    ]

    # Expansion table for turning 32 bit blocks into 48 bits
    __expansion_table = [
        31,  0,  1,  2,  3,  4,
         3,  4,  5,  6,  7,  8,
         7,  8,  9, 10, 11, 12,
        11, 12, 13, 14, 15, 16,
        15, 16, 17, 18, 19, 20,
        19, 20, 21, 22, 23, 24,
        23, 24, 25, 26, 27, 28,
        27, 28, 29, 30, 31,  0
    ]

    # The (in)famous S-boxes
    __sbox = [
        # S1
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
         0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
         4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
         15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

        # S2
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
         3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
         0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
         13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

        # S3
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
         13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
         13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
         1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

        # S4
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
         13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
         10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
         3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

        # S5
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
         14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
         4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
         11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

        # S6
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
         10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
         9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
         4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

        # S7
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
         13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
         1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
         6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

        # S8
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
         1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
         7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
         2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
    ]


    # 32-bit permutation function P used on the output of the S-boxes
    __p = [
        15, 6, 19, 20, 28, 11,
        27, 16, 0, 14, 22, 25,
        4, 17, 30, 9, 1, 7,
        23,13, 31, 26, 2, 8,
        18, 12, 29, 5, 21, 10,
        3, 24
    ]

    # final permutation IP^-1
    __fp = [
        39,  7, 47, 15, 55, 23, 63, 31,
        38,  6, 46, 14, 54, 22, 62, 30,
        37,  5, 45, 13, 53, 21, 61, 29,
        36,  4, 44, 12, 52, 20, 60, 28,
        35,  3, 43, 11, 51, 19, 59, 27,
        34,  2, 42, 10, 50, 18, 58, 26,
        33,  1, 41,  9, 49, 17, 57, 25,
        32,  0, 40,  8, 48, 16, 56, 24
    ]

    # Type of crypting being done
    ENCRYPT =    0x00
    DECRYPT =    0x01

    # Initialisation
    def __init__(self, key):
        # Sanity checking of arguments.
        
        if len(key) != 8:
            raise ValueError("Invalid DES key size. Key must be exactly 8 bytes long.")
        self.block_size = 8
        self.key_size = 8

        self.L = []
        self.R = []
        self.Kn = [ [0] * 48 ] * 16    # 16 48-bit keys (K1 - K16)
        self.final = []
        self.Sbox_output = []

        self.setKey(key)

    def setKey(self, key):
        """Will set the crypting key for this object. Must be 8 bytes."""
        
        self.__key = key

        self.__create_sub_keys()

    def getKey(self):
        """getKey() -> bytes"""
        return self.__key
    def getSubKey(self):
        return self.__Kn


    def __int_to_BitList(self, data):
        """Turn the np.array([...],dtype=np.uint8) data, into a list of bits (1, 0)'s"""
        
        l = len(data) * 8
        result = [0] * l
        pos = 0
        for ch in data:
            i = 7
            while i >= 0:
                if ch & (1 << i) != 0:
                    result[pos] = 1
                else:
                    result[pos] = 0
                pos += 1
                i -= 1

        return result

    def __BitList_to_int(self, data):
        """Turn the list of bits -> data, into a np.array([...],dtype=np.uint8)"""
        result = []
        pos = 0
        c = 0
        while pos < len(data):
            c += data[pos] << (7 - (pos % 8))
            if (pos % 8) == 7:
                result.append(c)
                c = 0
            pos += 1

        
        return np.array(result,dtype=np.uint8)

    def __permutate(self, table, block):
        """Permutate this block with the specified table"""
        return list(map(lambda x: block[x], table))
    
    # Transform the secret key, so that it is ready for data processing
    # Create the 16 subkeys, K[1] - K[16]
    def __create_sub_keys(self):
        """Create the 16 subkeys K[1] to K[16] from the given key"""
        key = self.__permutate(self.__pc1, self.__int_to_BitList(self.getKey()))
        i = 0
        # Split into Left and Right sections
        self.L = key[:28]
        self.R = key[28:]
        while i < 16:
            j = 0
            # Perform circular left shifts
            while j < self.__left_rotations[i]:
                self.L.append(self.L[0])
                del self.L[0]

                self.R.append(self.R[0])
                del self.R[0]

                j += 1

            # Create one of the 16 subkeys through pc2 permutation
            self.Kn[i] = self.__permutate(self.__pc2, self.L + self.R)

            i += 1

    # Main part of the encryption algorithm, the number cruncher :)
    def __des_crypt(self, block, crypt_type):
        """Crypt the block of data through DES bit-manipulation"""
        block = self.__permutate(self.__ip, block)
        self.L = block[:32]
        self.R = block[32:]

        # Encryption starts from Kn[1] through to Kn[16]
        if crypt_type == self.ENCRYPT:
            iteration = 0
            iteration_adjustment = 1
        # Decryption starts from Kn[16] down to Kn[1]
        else:
            iteration = 15
            iteration_adjustment = -1

        i = 0
        while i < 16:
            # Make a copy of R[i-1], this will later become L[i]
            tempR = self.R[:]

            # Permutate R[i - 1] to start creating R[i]
            self.R = self.__permutate(self.__expansion_table, self.R)

            # Exclusive or R[i - 1] with K[i], create B[1] to B[8] whilst here
            self.R = list(map(lambda x, y: x ^ y, self.R, self.Kn[iteration]))
            B = [self.R[:6], self.R[6:12], self.R[12:18], self.R[18:24], self.R[24:30], self.R[30:36], self.R[36:42], self.R[42:]]
            # Optimization: Replaced below commented code with above
            #j = 0
            #B = []
            #while j < len(self.R):
            #    self.R[j] = self.R[j] ^ self.Kn[iteration][j]
            #    j += 1
            #    if j % 6 == 0:
            #        B.append(self.R[j-6:j])

            # Permutate B[1] to B[8] using the S-Boxes
            j = 0
            Bn = [0] * 32
            pos = 0
            while j < 8:
                # Work out the offsets
                m = (B[j][0] << 1) + B[j][5]
                n = (B[j][1] << 3) + (B[j][2] << 2) + (B[j][3] << 1) + B[j][4]

                # Find the permutation value
                v = self.__sbox[j][(m << 4) + n]

                # Turn value into bits, add it to result: Bn
                Bn[pos] = (v & 8) >> 3
                Bn[pos + 1] = (v & 4) >> 2
                Bn[pos + 2] = (v & 2) >> 1
                Bn[pos + 3] = v & 1

                pos += 4
                j += 1

            # Permutate the concatination of B[1] to B[8] (Bn)
            self.R = self.__permutate(self.__p, Bn)

            # Xor with L[i - 1]
            self.R = list(map(lambda x, y: x ^ y, self.R, self.L))
            # Optimization: This now replaces the below commented code
            #j = 0
            #while j < len(self.R):
            #    self.R[j] = self.R[j] ^ self.L[j]
            #    j += 1

            # L[i] becomes R[i - 1]
            self.L = tempR

            i += 1
            iteration += iteration_adjustment
        
        # Final permutation of R[16]L[16]
        self.final = self.__permutate(self.__fp, self.R + self.L)
        return self.final
    
    # get IntermediateValue during des,for example Sbox output in first round
    def des_getIntermediateValue(self, plaintext, crypt_type):
        
        self.Sbox_output=[]
        block = self.__int_to_BitList(plaintext)
        """Crypt the block of data through DES bit-manipulation"""
        block = self.__permutate(self.__ip, block)
        self.L = block[:32]
        self.R = block[32:]

        # Encryption starts from Kn[1] through to Kn[16]
        if crypt_type == self.ENCRYPT:
            iteration = 0
            iteration_adjustment = 1
        # Decryption starts from Kn[16] down to Kn[1]
        else:
            iteration = 15
            iteration_adjustment = -1

        i = 0
        while i < 1:
            # Make a copy of R[i-1], this will later become L[i]
            tempR = self.R[:]

            # Permutate R[i - 1] to start creating R[i]
            self.R = self.__permutate(self.__expansion_table, self.R)

            # Exclusive or R[i - 1] with K[i], create B[1] to B[8] whilst here
            self.R = list(map(lambda x, y: x ^ y, self.R, self.Kn[iteration]))
            B = [self.R[:6], self.R[6:12], self.R[12:18], self.R[18:24], self.R[24:30], self.R[30:36], self.R[36:42], self.R[42:]]
            # Optimization: Replaced below commented code with above
            #j = 0
            #B = []
            #while j < len(self.R):
            #    self.R[j] = self.R[j] ^ self.Kn[iteration][j]
            #    j += 1
            #    if j % 6 == 0:
            #        B.append(self.R[j-6:j])

            # Permutate B[1] to B[8] using the S-Boxes
            j = 0
            Bn = [0] * 32
            pos = 0
            while j < 8:
                # Work out the offsets
                m = (B[j][0] << 1) + B[j][5]
                n = (B[j][1] << 3) + (B[j][2] << 2) + (B[j][3] << 1) + B[j][4]

                # Find the permutation value
                v = self.__sbox[j][(m << 4) + n]

                self.Sbox_output.append(v)
                # Turn value into bits, add it to result: Bn
                Bn[pos] = (v & 8) >> 3
                Bn[pos + 1] = (v & 4) >> 2
                Bn[pos + 2] = (v & 2) >> 1
                Bn[pos + 3] = v & 1

                pos += 4
                j += 1

            # Permutate the concatination of B[1] to B[8] (Bn)
            self.R = self.__permutate(self.__p, Bn)

            # Xor with L[i - 1]
            self.R = list(map(lambda x, y: x ^ y, self.R, self.L))
            # Optimization: This now replaces the below commented code
            #j = 0
            #while j < len(self.R):
            #    self.R[j] = self.R[j] ^ self.L[j]
            #    j += 1

            # L[i] becomes R[i - 1]
            self.L = tempR

            i += 1
            iteration += iteration_adjustment
        
        # Final permutation of R[16]L[16]
        self.final = self.__permutate(self.__fp, self.R + self.L)
        return self.Sbox_output


    # Data to be encrypted/decrypted
    def crypt(self, data, crypt_type):
        """Crypt the data in blocks, running it through des_crypt()"""

        # Error check the data
        if not data:
            return ''
        if len(data) % self.block_size != 0:
            # Decryption must work on 8 byte blocks
            raise ValueError("Invalid data length, data must be a multiple of " + str(self.block_size) + " bytes\n.")
            


        # Split the data into blocks, crypting each one seperately
        i = 0
        dict = {}
        result = []
        #cached = 0
        #lines = 0
        while i < len(data):
            # Test code for caching encryption results
            #lines += 1
            #if dict.has_key(data[i:i+8]):
                #print "Cached result for: %s" % data[i:i+8]
            #    cached += 1
            #    result.append(dict[data[i:i+8]])
            #    i += 8
            #    continue
                
            block = self.__int_to_BitList(data[i:i+8])

            # ECB mode
            processed_block = self.__des_crypt(block, crypt_type)


            # Add the resulting crypted block to our list
            #d = self.__BitList_to_String(processed_block)
            #result.append(d)
            result.append(self.__BitList_to_int(processed_block))
            #dict[data[i:i+8]] = d
            i += 8

        # print "Lines: %d, cached: %d" % (lines, cached)

        # Return the full crypted uint
        return np.array(result,dtype=np.uint8)

