#!/usr/bin/python3 -u
#
#  Determine device hw address
#  `amidi -l`
#  e.g. hw:1,0,0
#
#  request sysex (current scene) data dump (exactly 402 bytes) 
#  amidi -p hw:1,0,0 -S 'F0 42 40 00 01 13 00 1F 10 00 F7' -t 1 -r setting01.data
#
# write back updated settings file:
#  amidi -p hw:1,0,0 -s settingXX.data
#
# References:
#
# Explanation of Parameters:
# https://i.korg.com/uploads/Support/nanoKONTROL2_PG_E1_634479709631760000.pdf
# SysEx format:
# https://cdn.korg.com/us/support/download/files/aeb2862daf0cb7db826d8c62f51ec28d.txt?response-content-disposition=attachment%3Bfilename%3DnanoKONTROL2_MIDIimp.txt&response-content-type=application%2Foctet-stream%3B
#
#
#
# restore factory setting: turn on power while pressing track_cycle + track_prev + track_next

from construct import *


def Hexdump(data: bytes, stride=8):
    for i in range(0, len(data), stride):
        row = [f"{b:02x}" for b in data[i:i + stride]]
        print(f"{i:04x} {' '.join(row)}")


def Decode8to7(data: bytes) -> bytes:
    out = []
    for i in range(0, len(data), 8):
        high_bits = data[i]
        for y in data[i + 1:i + 8]:
            out.append(y | (high_bits & 1) << 7)
            high_bits >>= 1
    return bytes(out)


def Encode7to8(data: bytes) -> bytes:
    assert False, "NYI"


Header = Struct(
    Const(b"\xf0"),  # SysEx Begin
    Const(b"\x42\x40"),  # Korg
    Const(b"\x00"),  #
    Const(b"\x01\x13"),  # Device nano kontrol2
    Const(b"\x00"),  # subid
    Const(b"\x7f\x7f"),  # dump command
    Const(b"\x02"),  # two bytes forat
    Const(b"\x03\x05"),  # 3 * 128 + 5 = 389 bytes of data
)

Common = Struct(
    "channel" / Byte,
    "control_mode" / Enum(Byte, CUBASE=0, DB=1, LIVE=2, PROTOOLS=3, SONAR=4),
    "led_mode" / Enum(Byte, INTERNAL=0, EXTERNAL=1),
)

# TODO: find a way to reduce boilerplate - especially for buttons
ContollerGroup = Struct(
    "channel" / Byte,
    #
    "slider_assign_type" / Byte,
    Const(b"\x00"),
    "slider_cc" / Byte,
    "slider_min" / Byte,
    "slider_max" / Byte,
    Const(b"\x00"),
    #
    "knob_assign_tupe" / Byte,
    Const(b"\x00"),
    "knob_cc" / Byte,
    "knob_min" / Byte,
    "knob_max" / Byte,
    Const(b"\x00"),
    #
    "solo_button_assign_tupe" / Enum(Byte, ASSIGN=0, CC=1, NOTE=2),
    "solo_button_behavior" / Enum(Byte, MOMENTARY=0, TOGGLE=1),
    "solo_button_cc" / Byte,
    "solo_button_off" / Byte,
    "solo_button_on" / Byte,
    Const(b"\x00"),
    #
    "mute_button_assign_tupe" / Enum(Byte, ASSIGN=0, CC=1, NOTE=2),
    "mute_button_behavior" / Enum(Byte, MOMENTARY=0, TOGGLE=1),
    "mute_button_cc" / Byte,
    "mute_button_off" / Byte,
    "mute_button_on" / Byte,
    Const(b"\x00"),
    #
    "rec_button_assign_tupe" / Enum(Byte, ASSIGN=0, CC=1, NOTE=2),
    "rec_button_behavior" / Enum(Byte, MOMENTARY=0, TOGGLE=1),
    "rec_button_cc" / Byte,
    "rec_button_off" / Byte,
    "rec_button_on" / Byte,
    Const(b"\x00"),
)

Transport = Struct(
    "channel" / Byte,
    #
    "track_prev_button_assign_tupe" / Enum(Byte, ASSIGN=0, CC=1, NOTE=2),
    "track_prev_button_behavior" / Enum(Byte, MOMENTARY=0, TOGGLE=1),
    "track_prev_button_cc" / Byte,
    "track_prev_button_off" / Byte,
    "track_prev_button_on" / Byte,
    Const(b"\x00"),
    #
    "track_next_button_assign_tupe" / Enum(Byte, ASSIGN=0, CC=1, NOTE=2),
    "track_next_button_behavior" / Enum(Byte, MOMENTARY=0, TOGGLE=1),
    "track_next_button_cc" / Byte,
    "track_next_button_off" / Byte,
    "track_next_button_on" / Byte,
    Const(b"\x00"),
    #
    "cycle_button_assign_tupe" / Enum(Byte, ASSIGN=0, CC=1, NOTE=2),
    "cycle_button_behavior" / Enum(Byte, MOMENTARY=0, TOGGLE=1),
    "cycle_button_cc" / Byte,
    "cycle_button_off" / Byte,
    "cycle_button_on" / Byte,
    Const(b"\x00"),
    #
    "marker_set_button_assign_tupe" / Enum(Byte, ASSIGN=0, CC=1, NOTE=2),
    "marker_set__button_behavior" / Enum(Byte, MOMENTARY=0, TOGGLE=1),
    "marker_set_button_cc" / Byte,
    "marker_set_button_off" / Byte,
    "marker_set_button_on" / Byte,
    Const(b"\x00"),
    #

    "marker_prev_button_assign_tupe" / Enum(Byte, ASSIGN=0, CC=1, NOTE=2),
    "marker_prev_button_behavior" / Enum(Byte, MOMENTARY=0, TOGGLE=1),
    "marker_prev_button_cc" / Byte,
    "marker_prev_button_off" / Byte,
    "marker_prev_button_on" / Byte,
    Const(b"\x00"),
    #
    "marker_next_button_assign_tupe" / Enum(Byte, ASSIGN=0, CC=1, NOTE=2),
    "marker_next_button_behavior" / Enum(Byte, MOMENTARY=0, TOGGLE=1),
    "marker_next_button_cc" / Byte,
    "marker_next_button_off" / Byte,
    "marker_next_button_on" / Byte,
    Const(b"\x00"),
    #
    "rew_button_assign_tupe" / Enum(Byte, ASSIGN=0, CC=1, NOTE=2),
    "rew_button_behavior" / Enum(Byte, MOMENTARY=0, TOGGLE=1),
    "rew_button_cc" / Byte,
    "rew_button_off" / Byte,
    "rew_button_on" / Byte,
    Const(b"\x00"),
    #
    "ff_button_assign_tupe" / Enum(Byte, ASSIGN=0, CC=1, NOTE=2),
    "ff_button_behavior" / Enum(Byte, MOMENTARY=0, TOGGLE=1),
    "ff_button_cc" / Byte,
    "ff_button_off" / Byte,
    "ff_button_on" / Byte,
    Const(b"\x00"),
    #
    "stop_button_assign_tupe" / Enum(Byte, ASSIGN=0, CC=1, NOTE=2),
    "stop_button_behavior" / Enum(Byte, MOMENTARY=0, TOGGLE=1),
    "stop_button_cc" / Byte,
    "stop_button_off" / Byte,
    "stop_button_on" / Byte,
    Const(b"\x00"),
    #
    "play_button_assign_tupe" / Enum(Byte, ASSIGN=0, CC=1, NOTE=2),
    "play_button_behavior" / Enum(Byte, MOMENTARY=0, TOGGLE=1),
    "play_button_cc" / Byte,
    "play_button_off" / Byte,
    "play_button_on" / Byte,
    Const(b"\x00"),
    #
    "rec_button_assign_tupe" / Enum(Byte, ASSIGN=0, CC=1, NOTE=2),
    "rec_button_behavior" / Enum(Byte, MOMENTARY=0, TOGGLE=1),
    "rec_button_cc" / Byte,
    "rec_button_off" / Byte,
    "rec_button_on" / Byte,
    Const(b"\x00"),
    #
    "custom_daw_assign_1" / Byte,
    "custom_daw_assign_2" / Byte,
    "custom_daw_assign_3" / Byte,
    "custom_daw_assign_4" / Byte,
    "custom_daw_assign_5" / Byte,
    Const(b"\x00" * 16)
)

Kontrol2Payload = Sequence(
    Common,
    Array(8, ContollerGroup),
    Transport,
)


def read(filename):
    infile = open(filename, "rb")
    data = infile.read(2000)
    infile.close()
    assert len(data) == 402
    assert data[12] == 0x40
    assert data[-1] == 0xf7
    header = data[0:12]
    payload_raw = data[13:13 + 388]
    payload = Decode8to7(payload_raw)
    assert len(payload) == 339, f"{len(payload)}"
    config = Kontrol2Payload.parse(bytes(payload))
    return header, config


def write(filename, header, config):
    # TOOD: incomplete
    outfile = open(filename, "wb")
    outfile.write(header)
    outfile.close()


if __name__ == "__main__":
    import sys

    header, config = read(sys.argv[1])
    print(config)
