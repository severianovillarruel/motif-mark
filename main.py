#!/usr/bin/env python3

"""
Severiano Villarruel
03/03/20

Program to parse fasta files and diagram motifs
"""

from classes import *
from functions import *
import cairo
import re
import sys
import random

#open files
args = get_args()
fasta_f = open(args.fasta_file, 'r')
motifs_f = open(args.motifs_file, 'r')

#make fa to one line
fasta_f = mk_oneline(fasta_f, 'one_line.fa')

#get motifs
motif_d = motif_f_parser(motifs_f)

#get attributes
record_obj_l = []
for line in fasta_f:
    if '>' in line:
        header = line.strip()
    else:
        seq = line.strip()
        len_seq = len(seq)

        #get exon coords
        exon_coords = []
        for idx, char in enumerate(seq):
            if char.isupper() == True:
                exon_coords.append(idx)
        exon_coords = (exon_coords[0], exon_coords[-1])

        #initiate record object
        record_obj = record(header, len_seq, exon_coords)

        #find the start/stop of each motif
        for motif in motif_d:
            for i in range(len(seq)):
                len_motif = motif_d[motif][0] #length of original motif
                re_motif = motif_d[motif][1] #regex expression
                window = seq[i:len_motif + i]
                if re.findall(re_motif, window):
                    record_obj.append_dict(motif, (i, i+len(motif)))

        #pass motif and start/stop to record class
        record_obj_l.append(record_obj)

#draw motif diagrams

#page setup
margin = 20
header = 50
spacing = 100
footer = 50

textbox = 250
tb_margin = 100

#find longest sequence
for record_obj in record_obj_l:
    longest_seq = record_obj.len_seq
    if record_obj.len_seq > longest_seq:
        longest_seq = record_obj.len_seq

#initialize cairo
surface = cairo.PDFSurface("plot.pdf", margin + longest_seq + margin + textbox, header + (len(record_obj_l) * spacing) + footer) #width, height
context = cairo.Context(surface)

#draw
counter = 1
color_d = {}
for record_obj in record_obj_l:

    # print(record_obj.header)

    #set text attributes
    context.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL,cairo.FONT_WEIGHT_NORMAL)
    context.set_font_size(12)

    #set motif colors and make legend
    for motif in record_obj.motif_d.keys(): #dict_keys(['ygcy', 'catag'])
        if motif not in color_d:
            color_d[motif] = [random.random(), random.random(), random.random()]

    #mk seq line
    context.set_line_width(2)
    context.set_source_rgb(0.0, 0.0, 0.0)
    context.move_to( margin, header + (spacing * counter) ) #x,y
    context.line_to( margin + record_obj.len_seq, header + spacing * (counter) ) #x,y
    context.move_to( margin, header + (spacing * counter) - spacing/2 ) #x,y
    context.show_text(record_obj.header[1:])
    context.stroke()

    #draw exon
    context.set_line_width(20)
    context.set_source_rgb(0.0, 0.0, 0.0)
    context.move_to( margin + record_obj.exon_coords[0], header + (spacing * counter) ) #x,y
    context.line_to( margin + record_obj.exon_coords[1], header + (spacing * counter) ) #x,y
    context.stroke()

    #draw motifs
    for motif in record_obj.motif_d:
        context.set_source_rgb(color_d[motif][0], color_d[motif][1], color_d[motif][2])
        for coords in record_obj.motif_d[motif]:
            context.set_line_width(20)
            context.move_to( margin + coords[0], header + (spacing * counter) ) #x,y
            context.line_to( margin + coords[1], header + (spacing * counter) ) #x,y
            context.stroke()

    #increment
    counter += 1

#make legend
counter = 1
context.set_line_width(10)
context.set_source_rgb(0, 0, 0)
context.move_to( longest_seq + margin + tb_margin, header + 20 * counter ) #x,y
context.line_to( longest_seq + margin + tb_margin, (header + 20 * counter) + 10 ) #x,y
context.stroke()
context.set_source_rgb(0.0, 0.0, 0.0)
context.move_to(longest_seq + margin + tb_margin + 15, (header + 20 * counter) + 10 - 2)
context.show_text('exon')
context.stroke()

counter = 2
for motif in color_d:
    context.set_line_width(10)
    context.set_source_rgb(color_d[motif][0], color_d[motif][1], color_d[motif][2])
    context.move_to( longest_seq + margin + tb_margin, header + 20 * counter ) #x,y
    context.line_to( longest_seq + margin + tb_margin, (header + 20 * counter) + 10 ) #x,y
    context.stroke()
    context.set_source_rgb(0.0, 0.0, 0.0)
    context.move_to(longest_seq + margin + tb_margin + 15, (header + 20 * counter) + 10 - 2)
    context.show_text(motif)
    context.stroke()
    counter += 1

#finish
surface.finish()
