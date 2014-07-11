import json
import sys


def main():
    all_term_occurrences = 0
    term_occurrences     = dict()

    with open(sys.argv[1]) as f:
        for line in f:
            tweet = json.loads(line)

            for term in tweet.get("text", "").split():
                all_term_occurrences += 1
                term_occurrences[term] = 1 + term_occurrences.get(term, 0)

    for term, occurrences in term_occurrences.iteritems():
        print term, (float(occurrences) / all_term_occurrences)


if __name__ == '__main__':
    main()
