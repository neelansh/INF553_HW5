from blackbox import BlackBox
import binascii
import random
import sys


bloom_filter = [False]*69997

p = 13591
m = 69997
number_of_hashes = 3
random.seed(a=123)
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

def main(input_file_path, stream_size, num_of_asks, output_file_path):
    global bloom_filter
    bx = BlackBox()
    gt_set = set()
    fp = 0
    output_file = open(output_file_path, "wt")
    output_file.write("Time,FPR\n")
    for it in range(num_of_asks):
        stream_users = bx.ask(input_file_path, stream_size)
        for s in stream_users:
            indices = myhashs(s)
            is_not_present = False
            
            for i in indices:
                if(not bloom_filter[i]):
                    is_not_present = True
                    break
            
            if(is_not_present):
                for i in indices:
                    bloom_filter[i] = True
                
            if(not s in gt_set and not is_not_present):
                fp += 1
                
            gt_set.add(s)
        output_file.write("{},{}\n".format(it, fp/((it+1)*stream_size)))
    output_file.close()
    return


if __name__ == '__main__':
    main(sys.argv[1].strip(), int(sys.argv[2].strip()), int(sys.argv[3].strip()), sys.argv[4].strip())