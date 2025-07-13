# -*- coding: utf-8 -*-


any_letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
itu_prefix = {
    "203": ("OE", any_letter),  # Austria
    "205": ("O", "NOPQRST"),  # Belgium
    "207": ("LZ", any_letter),  # Bulgaria
    "211": ("D", "ABCDEFGHIJKLMNOPQR"),  # Germany
    "214": ("E", "R"),  # Moldova (MMSI = ATIS)
    "226": ("F", any_letter),  # France
    "227": ("F", any_letter),  # France
    "228": ("F", any_letter),  # France
    # "238": ("9", "A"),  # Croatia (scheme unclear)
    "243": ("HG", any_letter),  # Hungary
    "244": ("P", "ABCDEFGHI"),  # Netherlands
    "245": ("P", "ABCDEFGHI"),  # Netherlands
    "246": ("P", "ABCDEFGHI"),  # Netherlands
    "253": ("L", "X"),  # Luxembourg (MMSI = ATIS)
    # "261": ("S", "NOPQR"),  # Poland (scheme unclear)
    "262": ("4", "O"),  # Montenegro
    "264": ("Y", "OPQR"),  # Romania (MMSI = ATIS)
    # "267": ("O", "M"),  # Slovakia (scheme unclear)
    "269": ("H", "E"),  # Switzerland (MMSI = ATIS)
    "270": ("O", "KL"),  # Czechia
    "279": ("Y", "T"),  # Serbia (MMSI = ATIS)
}


def num_to_letter(num):
    return str(chr(0x40 + int(num)))


def determine_etsi(atis):
    # see ETSI EN 300 698 annex C
    callsign = []
    mid = atis[1:4]

    callsign.append(itu_prefix[mid][0])

    callsign.append(num_to_letter(atis[4:6]))
    if callsign[1] not in itu_prefix[mid][1]:
        return None

    callsign.append(atis[6])
    if callsign[2] not in "23456789":
        return None

    for i in range(7, 10):
        callsign.append(atis[i])
        if callsign[-1] not in "0123456789":
            return None

    return callsign


def determine(atis):
    try:
        callsign = determine_etsi(atis)
        return "".join(callsign)
    except Error:
        return ""
    except TypeError:
        return ""
    except ValueError:
        return ""
