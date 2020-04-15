from blackbox import BlackBox
import binascii
import random
import sys
import math

seq_number = 0
reservoir = []
reservoir_max_size = 100

def main(input_file_path, stream_size, num_of_asks, output_file_path):
    global seq_number
    random.seed(553)
    
    bx = BlackBox()
    output_file = open(output_file_path, "wt")
    output_file.write("seqnum,0_id,20_id,40_id,60_id,80_id\n")

    for it in range(num_of_asks):
        stream_users = bx.ask(input_file_path, stream_size)
        
        for s in stream_users:
            seq_number += 1
            if(len(reservoir) >= 100):
                x = random.randint(0, 100)
                if(x < 10000/seq_number):
                    reservoir[x] = s
            else:
                reservoir.append(s)
        output_file.write("{},{},{},{},{},{}\n".format(seq_number, reservoir[0], reservoir[20], reservoir[40], reservoir[60], reservoir[80]))
    output_file.close()

if __name__ == '__main__':
    main(sys.argv[1].strip(), int(sys.argv[2].strip()), int(sys.argv[3].strip()), sys.argv[4].strip())