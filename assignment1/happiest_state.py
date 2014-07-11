import json
import sys


STATES = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}


def build_sentiment_scores(sentiment_file):
    scores = {} # initialize an empty dictionary

    with open(sentiment_file) as f:
        for line in f:
            term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
            scores[term] = int(score)  # Convert the score to an integer.

    return scores


def main():
    sentiment_scores = build_sentiment_scores(sys.argv[1])
    state_scores = dict()

    with open(sys.argv[2]) as f:
        for line in f:
            try:
                score = 0
                state = None
                tweet = json.loads(line)

                place = tweet.get("place", False)

                if place and place["country_code"] == u"US":
                    first_name, last_name = place["full_name"].split(", ")

                    if place["place_type"] == u"city":
                        if last_name in STATES:
                            state = last_name

                    elif place["place_type"] == u"admin":
                        for abbr, name in STATES.iteritems():
                            if name.lower() == first_name.lower():
                                state = abbr

                    if state:
                        for term in tweet.get("text", "").split():
                            score += sentiment_scores.get(term, 0)

                        state_scores[state] = score + state_scores.get(state, 0)

            except Exception, e:
                print "Exception ignored!", e

    sorted_state_scores = [(v, k) for k, v in state_scores.iteritems()]
    sorted_state_scores.sort(reverse=True)

    print sorted_state_scores[0][1]


if __name__ == '__main__':
    main()
