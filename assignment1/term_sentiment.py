import json
import sys

from tweet_sentiment import build_sentiment_scores

def main():
    sentiment_scores = build_sentiment_scores(sys.argv[1])
    derived_scores   = dict()

    with open(sys.argv[2]) as f:
        for line in f:
            # print line
            new_terms = []
            score     = 0
            tweet     = json.loads(line)

            for term in tweet.get("text", "").split():
                if term in sentiment_scores:
                    score += sentiment_scores.get(term, 0)

                elif not term in new_terms:
                    new_terms.append(term)

            for term in new_terms:
                derived_scores[term] = score + derived_scores.get(term, 0)

    for term, score in derived_scores.iteritems():
        print term, score

if __name__ == '__main__':
    main()
