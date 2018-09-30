import sys
import re
import argparse

ratis = []
DICT_DELIMITER = '\t'
WORD_POS_SEPARATOR = '/'


def parse():

    parser = argparse.ArgumentParser()
    parser.add_argument('bigram_prob_dict',
                        help='bigram Probability dictionaly')
    parser.add_argument('lex_prob_dict',
                        help='Lexical Generation Probability dictionary')

    args = parser.parse_args()

    return args


def load_bigram_prob_dict(fname):

    bigram_prob = {}

    with open(fname, 'r') as fp:
        for line in fp:
            line = line.rstrip()
            bigram, prob = line.split(DICT_DELIMITER)
            bigram_prob[bigram] = float(prob)

    return bigram_prob


def load_lex_prob_dict(fname):

    lex_prob = {'F': {'F': 1.0}}

    with open(fname, 'r') as fp:
        for line in fp:
            line = line.rstrip()
            word_pos, prob = line.split(DICT_DELIMITER)
            word, pos = word_pos.split(WORD_POS_SEPARATOR)
            dic = lex_prob.get(word)
            if dic == None:
                lex_prob[word] = {pos: float(prob)}
            else:
                lex_prob[word].update({pos: float(prob)})

    return lex_prob


def update_ratis(max_prob, word, before_word):
    
    ratis.append([max_prob, word, before_word])
    return 0


def back(ratis, max_word_class):
    tmp = max_word_class
    answer = []

    for l in reversed(ratis):
        if l[1] == tmp:
            answer.append(l[1])
            tmp = l[2]
    return list(reversed(answer))


def calc(sentence, lex_prob, bigram_prob):
    words = sentence.split()
    words.insert(0,'F')
    for i in range(1, len(words)):
        for word_class in lex_prob[words[i]]:
            max_prob = -1
            max_word_class = ''
            for before_word_class in lex_prob[words[i-1]]:
                bigram_name = before_word_class+'-'+word_class
                value = 0
                tmp = lex_prob[words[i-1]]
                if bigram_prob.get(bigram_name):
                    value = bigram_prob[bigram_name] * tmp[before_word_class] * lex_prob[words[i]][word_class]#ここで現在の出現確立をかける
                else:
                    value = 0

                if max_prob <= value:
                    max_prob = value
                    max_word_class = before_word_class
                    max_now_word_class = word_class
            """
            print('max_prob:', max_prob)
            print('now_word:', words[i])
            print('maxword_class', max_word_class)
            print('now_max_word_class', max_now_word_class)
            """
            lex_prob[words[i]][word_class] = max_prob
            update_ratis(max_prob, words[i]+'/'+word_class, words[i-1]+'/'+max_word_class)
    return words[i]+'/'+max_now_word_class


def main():
    args = parse()
    lex_prob = load_lex_prob_dict(args.lex_prob_dict)
    bigram_prob = load_bigram_prob_dict(args.bigram_prob_dict)

    sentence = 'Time flies like an arrow'
    max_word_class = calc(sentence, lex_prob, bigram_prob)
    answer = back(ratis, max_word_class)
    print()
    print(answer)
    return 0

main()