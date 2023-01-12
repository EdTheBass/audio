from plot_sound import sound_plot as plot

def readb(b):
    return int.from_bytes(b, "little")

def save_changes(header, s_data):
    with open("edit.wav", "wb") as f:
        f.write(header + s_data)

with open("weezer.wav", "rb") as f:
    f.seek(16)
    ft_length = readb(f.read(3))

    f.seek(4)
    f_size = readb(f.read(3))
    
    f.seek(ft_length+4) 

    f_format = readb(f.read(2))
    channels = readb(f.read(2))
    sample_rate = readb(f.read(4))
    sbc = readb(f.read(4))
    bc = readb(f.read(2))
    bit_depth = readb(f.read(2))
    byte_depth = bit_depth // 8

    data_size = -1
    data_start = -1
    i = f.tell()
    while True:
        f.seek(i)
        if f.read(4) == b'data':
            f.seek(i+4)
            data_size = readb(f.read(3))
            data_start = f.tell()+4
            break
        i += 1

    f.seek(0)
    header = f.read(data_start)
    print(header)

    sound_data = []
    f.seek(data_start)
    for i in range(data_size // byte_depth):
        d = readb(f.read(byte_depth))
        sound_data.append(d) 

