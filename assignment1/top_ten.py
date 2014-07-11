import json
import sys


def main():
    hashtag_occurences = {}

    with open(sys.argv[1]) as f:
        for line in f:
            try:
                tweet = json.loads(line)

                entities = tweet["entities"]
                hashtags = entities["hashtags"]

                for raw_hashtag in hashtags:
                    hashtag = raw_hashtag["text"]
                    hashtag_occurences[hashtag] = 1 + hashtag_occurences.get(hashtag, 0)

            except Exception, e:
                # ignore failed parsing
                pass

    sorted_hastag_occurences = [(v, k) for k, v in hashtag_occurences.iteritems()]
    sorted_hastag_occurences.sort(reverse=True)

    for occurences, hashtag in sorted_hastag_occurences[:10]:
        print hashtag, occurences


if __name__ == '__main__':
    main()
