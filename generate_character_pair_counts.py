###############################################
# This script computes char co-occurence within
# alexa's top 1-million web domains.
# The co-occurence counts, probability and 
# log(probability) and stored in a json doc.
###############################################

import json
import math

file = 'alexa-top-1m.csv'


def bigrams(input_list):
    return zip(input_list, input_list[1:])


pairs = {}
line_count = 0

with open(file, 'r') as fi:
    for line in fi:
        # keep track of progress
        line_count += 1

        # extract ranking
        arr = line.split(',')
        ranking = arr[0]

        # extract basedomain
        basedomain = arr[1].split('.')[0]

        # sometimes basedomain is made up of 2 or more words with hyphens between, we split them on the hyphen to obtain 'words'
        # e.g. my-malicious-domain.com, x-site.com etc.
        words = basedomain.split('-')

        # for each domain 'word' greater than 1 character
        # obtain character pairs
        for word in words:
            if len(word) > 1:
                b = bigrams(word)

                # combine bigram char pairs and maintain count 
                for char_tuple in b:
                    pair = char_tuple[0] + char_tuple[1]
                    if pair in pairs:
                        pairs[pair] += 1
                    else:
                        pairs[pair] = 1

# now that we have pairs, compute sum of all pair combinations
# for example:
# if pairs['go'] = 4, pairs['im'] = 5, pairs['to'] = 9 then total_pairs = 18.
total_pairs = sum(pairs.values())
print(total_pairs)

# calculate probability for each pair of letters update the dict value with a dict of following format
# we use logarithm base 10 because later we would need to multiple pairwise to obtain an overall probability
# however, instead of multiplying small floats we add their logarithms as
# log(xy) = log(x) + log(y)
#
# key = { count: 2000, 
#         probability: 0.00008580898447093862, 
#         log: -4.605170185988091
#       }

for k, v in pairs.items():
    # probability = val / total_pairs
    probability = float(v) / total_pairs
    pairs[k] = {
        'count': v,
        'probability': probability,
        'log': round(math.log10(probability), 5)
    }

# finally add total_pairs to dict. useful to calculate pair counts later
pairs['total_pairs'] = total_pairs

j = json.dumps(pairs)

with open('character_pair_probabilities.json', 'w') as fo:
    fo.write(j)

exit()