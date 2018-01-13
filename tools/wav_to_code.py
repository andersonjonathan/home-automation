import glob
import wave


def parse_wav_file(file_name):
    print(file_name.rsplit("/", 1)[1][:-4])
    wave_file = wave.open(file_name, 'r')

    length = wave_file.getnframes()
    fr = wave_file.getframerate()
    frames = 0
    temp = 2
    raw = []
    for i in range(0, length):
        wave_data = wave_file.readframes(1)
        d = int(str(bin(int(wave_data.hex(), 16))[2:].zfill(16))[8:9])
        if d == temp:
            frames += 1
        elif temp == 2:
            temp = d
            frames = 1
        else:
            raw.append([temp, frames/fr])
            temp = d
            frames = 1

    low = raw[2][1]
    for r in raw[1:-1]:
        if r[1] < low:
            low = r[1]
    avg_low_list = []
    for r in raw[1:-1]:
        if r[1] < low * 1.7:
            avg_low_list.append(r[1])
    avg = float(sum(avg_low_list)) / len(avg_low_list)
    print("T = " + str(int(avg*1000000)) + "ms")

    types = set()
    sequence = []
    for r in range(1, len(raw)):
        if raw[r][0] == 0:
            continue
        try:
            identifier = str(round(raw[r][1] / avg)).zfill(2) + "-" + str(round(raw[r+1][1] / avg)).zfill(2)
            types.add(identifier)
            sequence.append(identifier)
        except IndexError:
            pass
    s_types = sorted(types)
    char = ord('A')
    d_types = {}
    for t in range(0, len(s_types)):
        print(chr(char+t) + " = " + s_types[t])
        d_types[s_types[t]] = chr(char+t)
    tmp = []
    for r in sequence:
        tmp.append(d_types[r])

    print("".join(tmp).split(chr(char+len(s_types)-1))[1]+chr(char+len(s_types)-1))


file_list = sorted(glob.glob("/home/jonathan/Desktop/Stugan 433/*.wav"))
for file in file_list:
    parse_wav_file(file)
    print("")
