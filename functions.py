import cairo
import re
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="motif marker")
    parser.add_argument("-fasta", "--fasta_file", help="fasta sequence that will be searched to find motifs", required=True, type = str)
    parser.add_argument("-motifs", "--motifs_file", help="the motifs that will be used in the search through the fasta file", required=True, type = str)
    return parser.parse_args()

def mk_oneline(fasta_f, name):
    '''
    pass in fp and name of oneline fa
    returns fp of oneline fa
    '''
    new_fasta_f = open(name,'w')
    counter = 0
    for line in fasta_f:
        line = line.strip()
        if '>' in line:
            if counter == 0:
                new_fasta_f.write(line + '\n')
            else:
                new_fasta_f.write('\n' + line + '\n')
        else:
            new_fasta_f.write(line)
        counter += 1
    return open(name,'r')

def motif_f_parser(motifs_f):
    '''
    mk dict where key is motif and list with original len and re motif is value
    '''
    ref_d = {'a':'[aA]','t':'[tT]','c':'[cC]','g':'[gG]','y':'[cCtT]','u':'[tT]'} #u could be c?
    motif_d = {} #{ori_motif:[len_motif, re_motif]}
    for line in motifs_f:
        motif = line.lower().strip()
        len_motif = len(motif)
        info = []
        info.append(len_motif)

        re_motif = ''
        for char in motif:
            re_motif += ref_d[char]

        info.append(re_motif)
        motif_d[motif] = info
    return motif_d
