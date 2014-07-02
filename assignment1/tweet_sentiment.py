import json
import sys


def lines(fp):
    print str(len(fp.readlines()))


def build_sentiment_scores(sentiment_file):
    scores = {} # initialize an empty dictionary

    with open(sentiment_file) as f:
        for line in f:
            term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
            scores[term] = int(score)  # Convert the score to an integer.

    return scores


def main():
    sentiment_scores = build_sentiment_scores(sys.argv[1])

    with open(sys.argv[2]) as f:
        for line in f:
            score = 0
            tweet = json.loads(line)

            for term in tweet.get("text", "").split():
                score += sentiment_scores.get(term, 0)

            print score


if __name__ == '__main__':
    main()
