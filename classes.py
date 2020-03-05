class record:
    #this section can be used for allocating memory
    def __init__(self, header, len_seq, exon_coords):
        self.header = header
        self.len_seq = len_seq
        self.exon_coords = exon_coords
        self.motif_d = {}

    def append_dict(self, key, value):
        if key not in self.motif_d:
            self.motif_d[key] = [value] #{motif a: [(start, stop), (start, stop)], motif b: [(start, stop)]}
        else:
            self.motif_d[key].append(value)

class drawer:
    pass
