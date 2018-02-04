from random import randint


def generate_telldus_code(c_s="C", c_0="BA", c_1="AB", c_p="D", nexa=False):
    def _convert(value):
        if value == "0":
            return c_0
        if value == "1":
            return c_1

    uniqe_code = "{0:b}".format(randint(0, 67108863)).zfill(26)
    channel = "00"
    unit = "{0:b}".format(randint(0, 2)).zfill(2)
    if nexa:
        channel = "11"
        unit = "{0:b}".format(randint(1, 3)).zfill(2)
    return {
        "ON": "{sync}{uniqe_code}{group}{state}{channel}{unit}{pause}".format(
            sync=c_s,
            uniqe_code="".join(list(map(_convert, uniqe_code))),
            group=c_1,
            state=c_0,  # ON
            channel="".join(list(map(_convert, channel))),
            unit="".join(list(map(_convert, unit))),
            pause=c_p,
        ),
        "OFF": "{sync}{uniqe_code}{group}{state}{channel}{unit}{pause}".format(
            sync=c_s,
            uniqe_code="".join(list(map(_convert, uniqe_code))),
            group=c_1,
            state=c_1,  # ON
            channel="".join(list(map(_convert, channel))),
            unit="".join(list(map(_convert, unit))),
            pause=c_p,
        ),
    }


if __name__ == '__main__':
    print(generate_telldus_code(nexa=True))
