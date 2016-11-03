# file: stega.py
# updated by Duncan Fisher
# 10/18/16 


from PIL import Image



# bit mask for extracting 2 bits per byte
bit_mask = b'\xc0\x30\x0c\x03'


def available_bytes(carrier):
    '''
    returns number of bytes that can be stored inside carrier
    using lsb substitution (2 bits per byte)
    '''
    img = Image.open(carrier)
    img_bytes = img.tobytes()
    return len(img_bytes)//4
    

def inject_bytes(bs1, bs2):
    '''
    accepts two bytes objects bs1 and bs2 and injects the bytes of 
    bs2 2 bits at a time into the least significant bits of each
    byte of bs1. Checks to ensure bs1 is large enough to hold the
    bits of bs2
    '''
    if len(bs1) < 4*len(bs2):
        return
    ba = bytearray(bs1)
    for i, byte in enumerate(bs2):
        for j in range(4):
            ba[4*i+j] = (ba[4*i+j] & 252) | ((bit_mask[j] & byte) >> 2*(3-j))
    return bytes(ba)


def extract_n_bytes(data, n):
    '''
    returns a bytes object that is n bytes long and consists
    of the least significant bits of data
    '''
    if len(data) < 4*n :
        return
    ba = bytearray(n)
    for i in range(4*n):
        ba[i//4] = ba[i//4] | ((data[i] & 3) << 2*(3 - (i%4)))
    return bytes(ba)


def pack(data):
    '''
    appends a 4 byte field specifying the length of data
    '''
    length = len(data).to_bytes(4, byteorder='big')
    return length + data


def unpack(data):
    '''
    parses a bytes object
    returns a tuple with the length and the data segment
    '''
    length = int.from_bytes(extract_n_bytes(data, 4), byteorder='big')
    data_segment = extract_n_bytes(data[16:], length)
    return length , data_segment
 

def inject_file(carrier, hidden, output):
    '''
    recieves 3 file objects
    stores data from hidden in carrier and saves result to output
    '''
    img = Image.open(carrier)  
    hidden_bytes = hidden.read()
    output_bytes = inject_bytes(img.tobytes(), pack(hidden_bytes))
    img = Image.frombytes(img.mode, img.size, output_bytes)
    img.save(output, format='PNG')


def inject_text(carrier, text, output):
    '''
    stores unicode text inside carrier and saves result to output
    '''
    img = Image.open(carrier)
    text_bytes = text.encode()
    output_bytes = inject_bytes(img.tobytes(), pack(text_bytes))
    img = Image.frombytes(img.mode, img.size, output_bytes)
    img.save(output, format='PNG')


def extract_file(carrier, output):
    img = Image.open(carrier)
    length, output_bytes = unpack(img.tobytes())
    output.write(output_bytes)


def extract_text(carrier):
    '''
    given an image with a hidden unicode string
    returns the string
    '''
    img = Image.open(carrier)
    length, text_bytes = unpack(img.tobytes())
    text = text_bytes.decode()
    return text



# test functions via command line    

if __name__ == "__main__" :

    print('1 -> inject text', '2 -> inject file', '3 -> extract text', '4 -> extract file', sep='\n')
    choice = int(input('choice: '))

    if choice == 1:
        carrier = open(input('carrier path: '), 'rb')
        text = input('enter a string: ')
        output = open('pings/output.png', 'wb')
        inject_text(carrier, text, output)
    elif choice == 2:
        carrier = open(input('carrier path: '), 'rb')
        hidden = open(input('hidden path: '), 'rb')
        output = open('pings/output.png', 'wb')
        inject_file(carrier, hidden, output)
    elif choice == 3:
        carrier = open(input('carrier path: '), 'rb')
        text = extract_text(carrier)
        print(text)   
    elif choice == 4:
        carrier = open(input('carrier path: '), 'rb')
        output = open(input('output path: '), 'wb')
        extract_file(carrier, output)  
    else:
        exit(1)


