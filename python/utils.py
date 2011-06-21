color_seqs = dict(
    purple = '\033[95m',
    blue = '\033[94m',
    green = '\033[92m',
    yellow = '\033[93m',
    red = '\033[91m',
    end = '\033[0m')
    
def cprint(string,color="red"):
    print(color_seqs[color]+string+color_seqs["end"])
