from blackbox import BlackBox
import binascii
import random
import sys
import math

p = 13591
m = 69997
number_of_hashes = 30
len_of_group = 2
random.seed(a=10)
a = random.sample(range(1, p), number_of_hashes)
b = random.sample(range(0, p), number_of_hashes)

def convert_str_int(s):
    return int(binascii.hexlify(s.encode('utf8')),16)

def myhashs(s):
    global a, b, m
    x = convert_str_int(s)
    result = []
    for (ai, bi) in zip(a, b):
        result.append((ai*x+bi)%m)
    return result


def calculate_count(num_trailing_zeros):
    global number_of_hashes, len_of_group
    avgs_groups = []
    for i in range(0, number_of_hashes, len_of_group):
        group = num_trailing_zeros[i: (i+1)*len_of_group]
        group = [math.pow(2, r) for r in group]
        avg = sum(group)/len(group)
        avgs_groups.append(avg)
        
    return sorted(avgs_groups)[len(avgs_groups)//2]

def flajolet_martin(input_file_path, stream_size, num_of_asks, output_file_path):
    global number_of_hashes
    bx = BlackBox()
    output_file = open(output_file_path, "wt")
    output_file.write("Time,Ground Truth,Estimation\n")
    predicted_sum = 0
    actual_sum = 0
    for it in range(num_of_asks):
        stream_users = bx.ask(input_file_path, stream_size)
        max_number_of_trainling_zeros = [-sys.maxsize]*number_of_hashes
        for s in stream_users:
            hashes = myhashs(s)
            for i, h in enumerate(hashes):
                h = format(h, '016b')
                number_of_trailing_zeros = len(h) - len(h.rstrip('0'))
                    
                if(number_of_trailing_zeros > max_number_of_trainling_zeros[i]):
                    max_number_of_trainling_zeros[i] = number_of_trailing_zeros
        count = calculate_count(max_number_of_trainling_zeros)
        output_file.write("{},{},{}\n".format(it, stream_size, int(count)))
        predicted_sum += count
        actual_sum += stream_size
    print(predicted_sum/actual_sum)
    output_file.close()
    return
        
if __name__ == '__main__':
    flajolet_martin(sys.argv[1].strip(), int(sys.argv[2].strip()), int(sys.argv[3].strip()), sys.argv[4].strip())