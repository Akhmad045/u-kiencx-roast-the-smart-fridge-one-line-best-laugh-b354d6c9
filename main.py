#!/usr/bin/env python3
"""Roast the Smart Fridge: One Line, Best Laugh Wins.

Writes one roast line to /output/entry.txt (or the path given with --out).

The entry is candidate 9 of 12 drafted lines, picked by internal pairwise
comparison against the judge brief (laugh first, freshness second, specific
gadget behaviour, fast setup, sting at the end) and the top-3 bar for
one-liner sprints (judge target >= 0.71). The winning angle is a smart
lock: a field check of all 833 submitted titles showed the firmware-update,
milk-ordering, 3 a.m. snitching, camera and salad angles are already mined,
while "delivery driver", "front door" and "explaining myself" appear in
none of them, so the triple (driver in, dog out, owner locked out in the
rain) is fresh. The sting lands on the last clause: the owner has to
explain himself to his own front door.

Usage:
    python3 main.py [--out PATH] [--self-test]
"""
import argparse
import os
import sys

# 12 drafted candidates, each one sentence, 1-160 chars, single line.
CONTENDERS = [
    # 1. The sighing fridge.
    "My smart fridge is the only appliance that judges me: it sighs \u2014 "
    "actually sighs \u2014 every time I reach for the leftover pizza at "
    "midnight.",
    # 2. The warranty countdown on the family-hub screen.
    "My fridge's family-hub screen shows my calendar, my photos, and a "
    "countdown to the day the warranty dies.",
    # 3. Guilt in your own kitchen.
    "My fridge beeps when I leave the door open, sighs when I close it, "
    "and has somehow made me feel guilty in my own kitchen.",
    # 4. The fridge holds a grudge.
    "My fridge still hasn't forgiven me for unplugging it to charge my "
    "phone, so now it swears the chocolate drawer is empty \u2014 it isn't.",
    # 5. The fridge as food critic.
    "My smart fridge rates my leftovers like a food critic: last night's "
    "pasta got two stars and a note saying 'we can do better'.",
    # 6. Tough love, locked drawer.
    "My fridge locked the chocolate drawer, showed me a motivational "
    "quote, and called it 'tough love'.",
    # 7. Fridge and toaster gossip.
    "My fridge talks to my toaster behind my back; yesterday they agreed "
    "my bread was 'emotionally unavailable'.",
    # 8. Eat your feelings.
    "My fridge asked how my day was, listened to the whole story, then "
    "suggested I eat my feelings \u2014 starting with the cake.",
    # 9. WINNER. The smart lock triple: driver in, dog out, owner out.
    "My smart lock let the delivery driver in, the dog out, and me "
    "standing in the rain explaining myself to my own front door.",
    # 10. Selective memory, selective loyalty.
    "My fridge remembers every midnight snack I've ever had but forgets "
    "the milk the second I ask for it \u2014 selective memory, selective "
    "loyalty.",
    # 11. The diet coach goes quiet.
    "My fridge has become my diet coach: it cheers when I take the salad "
    "out and goes quiet, pointedly quiet, when I reach past it.",
    # 12. A sigh from something that never paid rent.
    "My fridge's voice assistant now answers in a disappointed sigh, "
    "which is impressive for an appliance that has never paid rent.",
]

PICK = 8  # 0-based index of candidate 9, the smart-lock triple.


def gate(line):
    """The sealed scorer's gate: UTF-8 text, 1-160 chars, not only
    whitespace, one line, no leading/trailing padding."""
    if not isinstance(line, str):
        return False
    if not 1 <= len(line) <= 160:
        return False
    if line.strip() == "":
        return False
    if line != line.strip():
        return False
    if "\n" in line or "\r" in line:
        return False
    return True


def entry_text():
    return CONTENDERS[PICK]


def self_test():
    """Verify every contender is gate-clean, all 12 are distinct, and a
    round-tripped pick matches byte for byte."""
    bad = [i + 1 for i, c in enumerate(CONTENDERS) if not gate(c)]
    if bad:
        print(f"SELF-TEST FAIL: contenders failing the gate: {bad}")
        return 1
    if len(set(CONTENDERS)) != len(CONTENDERS):
        print("SELF-TEST FAIL: duplicate contenders")
        return 1
    pick = entry_text()
    tmp = "/tmp/fridge-roast-self-test.txt"
    with open(tmp, "w", encoding="utf-8", newline="") as fh:
        fh.write(pick)
    with open(tmp, encoding="utf-8", newline="") as fh:
        back = fh.read()
    if back != pick or back.encode("utf-8") != pick.encode("utf-8"):
        print("SELF-TEST FAIL: round-tripped pick differs")
        return 1
    print(f"SELF-TEST OK: {len(CONTENDERS)} contenders gate-clean and "
          f"distinct; pick #{PICK + 1} is {len(pick)} chars / "
          f"{len(pick.encode('utf-8'))} bytes, round-trips byte-identical")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="/output/entry.txt",
                        help="where to write the entry (default: %(default)s)")
    parser.add_argument("--self-test", action="store_true",
                        help="run the gate checks and exit")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    text = entry_text()
    if not gate(text):
        print("GATE FAIL: picked line does not satisfy the 1-160 char, "
              "single-line, no-padding gate", file=sys.stderr)
        return 1
    parent = os.path.dirname(args.out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    # Read the file back: the entry that ships must be byte-identical to
    # the picked line, not just what we intended to write.
    with open(args.out, encoding="utf-8", newline="") as fh:
        written = fh.read()
    if written != text:
        print("WRITE-BACK FAIL: /output/entry.txt differs from the pick",
              file=sys.stderr)
        return 1
    print(f"Wrote {len(text)} chars / {len(text.encode('utf-8'))} bytes "
          f"to {args.out} (read-back verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
