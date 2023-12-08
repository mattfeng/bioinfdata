#!/usr/bin/env python

import csv
import argparse
import sys

from collections import defaultdict

class Mapper():
    def __init__(self, csv_file):
        self.fwd, self.rev, self.mapping = self.read_mapping_csv(csv_file)

    def read_mapping_csv(self, csv_file):
        fwd = defaultdict(set)
        rev = defaultdict(set)

        with open(csv_file, newline="") as f:
            reader = csv.reader(f)

            from_, to = next(reader)
            mapping = f"{from_}->{to}"

            for from_, to in reader:
                if len(from_) > 0 and len(to) > 0:
                    fwd[from_].add(to)
                    rev[to].add(from_)

        return fwd, rev, mapping

    def atob(self, key):
        return self.fwd[key]

    def btoa(self, key):
        return self.rev[key]

    def bij_btoa(self, key):
        if len(self.rev[key]) == 0:
            raise Exception(f"{key} does not map to any value.")

        if len(self.rev[key]) > 1:
            raise Exception(f"{key} maps to more than one value.")

        [elt] = self.rev[key]

        if len(self.fwd[elt]) == 0:
            raise Exception(f"btoa({key}) = {elt} does not map to any value.")

        if len(self.fwd[elt]) > 1:
            raise Exception(f"btoa({key}) = {elt} maps to more than one value.")

        return elt


def main(*, mapping_csv, input_file):
    mapper = Mapper(mapping_csv)

    with open(input_file) as f:
        for line in f:
            line = line.strip()

            out = mapper.btoa(line)
            out_str = ",".join(out)

            print(f"{out_str} # {line}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "mapping_csv",
        help=""
        )
    parser.add_argument(
        "--input_file",
        help="",
        default=0 # 0 is sys.stdin
        )

    args = parser.parse_args()

    main(
        mapping_csv=args.mapping_csv,
        input_file=args.input_file
        )
