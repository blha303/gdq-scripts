#!/usr/bin/env python
import json,sys,argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()
    with open(args.file) as f:
        tracker = json.load(f)
    out = []
    out.append("pk\t" + "\t".join(k for k in tracker[0]["fields"]))
    for t in tracker:
        outp = ""
        for field in out[0].split("\t"):
            if field == "pk":
                outp += str(t[field]) + "\t"
            else:
                if type(t["fields"][field]) is list:
                    outp += ",".join(str(t["fields"][field])) + "\t"
                else:
                    outp += str(t["fields"][field]) + "\t"
        outp = outp.strip()
        out.append(outp)
    with open(args.file.split(".", 1)[0] + ".tsv", "w") as f:
        f.write("\n".join(out))
    return 0

if __name__ == "__main__":
    sys.exit(main())
