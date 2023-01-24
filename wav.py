from plot_sound import sound_plot as plot

def readb(b):
    return int.from_bytes(b, "little")

def readi(i, length):
    return int.to_bytes(i, length, "little")

def reads(s):
    return bytes(s, "utf-8")

class Audio:
    def __init__(self, src):
        self.src = src
        self.header = bytes()
        self.f_size = -1
        self.f_format = -1
        self.channels = -1
        self.sample_rate = -1
        self.sbc = -1
        self.bc = -1
        self.bit_depth = -1
        self.byte_depth = -1
        self.data_start = -1
        self.data_len = -1
        self.data = []
        self.b_data = bytes()

        self.load_audio()

    def load_audio(self):
        with open(self.src, "rb") as f:
            f.seek(16)
            ft_length = readb(f.read(3))

            f.seek(4)
            self.f_size = readb(f.read(4))
            
            f.seek(ft_length+4)

            self.f_format = readb(f.read(2))
            self.channels = readb(f.read(2))
            self.sample_rate = readb(f.read(4))
            self.sbc = readb(f.read(4))
            self.bc = readb(f.read(2))
            self.bit_depth = readb(f.read(2))
            self.byte_depth = self.bit_depth // 8

            i = f.tell()
            while True:
                f.seek(i)
                if f.read(4) == b'data':
                    f.seek(i+4)
                    self.data_len = readb(f.read(3))
                    self.data_start = f.tell()
                    break
                i += 1

            f.seek(0)
            self.header = f.read(self.data_start)

            f.seek(self.data_start)
            for i in range(self.data_len // self.byte_depth):
                d = readb(f.read(self.byte_depth))
                self.data.append(d) 

    def to_bytes(self):
        self.b_data = bytes()
        for s in self.data:
            self.b_data += readi(s, self.byte_depth)

    def sound_shit(self):
        new_data = []
        for i in range(0, len(self.data), 1):
            new_data.append(self.data[i])
        self.data = new_data

def save_changes(header, s_data):
    with open("edit.wav", "wb") as f:
        f.write(header + s_data)

def construct_header(f_size, ft_length, f_format, channels, sample_rate, sbc, bc, bit_depth, data_size):
    header = bytes()
    header += reads("RIFF")
    header += readi(f_size, 4)
    header += reads("WAVE")
    header += reads("fmt ")
    header += readi(ft_length, 4)
    header += readi(f_format, 2)
    header += readi(channels, 2)
    header += readi(sample_rate, 4)
    header += readi(sbc, 4)
    header += readi(bc, 2)
    header += readi(bit_depth, 2)
    header += reads("data")
    header += readi(data_size, 4)
    return header


a = Audio("weezer.wav")
h = construct_header(353126, 16, a.f_format, a.channels, a.sample_rate, a.sbc, a.bc, a.bit_depth, a.data_len)

a.to_bytes()

# 0x4D start

save_changes(h, a.b_data)

