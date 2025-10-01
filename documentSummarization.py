import math
from collections import defaultdict, Counter
from nltk import sent_tokenize, word_tokenize, stem
from datetime import datetime
import numpy as np
import re
import networkx as nx



def idf_dict(sentence_sets):
     idf_dict = defaultdict(lambda:0.0)
     N = len(sentence_sets)
     all_words = []
     for sentence in sentence_sets:
          sent = list(set(sentence.split()))
          for word in sent:
               idf_dict[word] += 1
               all_words.append(word)

     all_words = list(set(all_words))
     for word in all_words:
          idf = (N/idf_dict[word])
          idf_dict[word] = math.log(idf, 10)

     return idf_dict


def idf_cosine_calc(sent_x, sent_y, idf_dict):
     x_dict, y_dict = defaultdict(lambda:0), defaultdict(lambda:0)
     # Create dict of tf each sentence
     for x_word in sent_x.split():
          x_dict[x_word] += 1
     for y_word in sent_y.split():
          y_dict[y_word] += 1
     both = sent_x.split()
     both.extend(sent_y.split())
     both = list(set(both))
     # calc numerator part of idf_cosine
     numerator = sum([((x_dict[word])*(y_dict[word])*(idf_dict[word]**2)) for word in both])
     x_denomerator = sum([(x_dict[word]*(idf_dict[word]))**2 for word in list(set(sent_x.strip().split()))])
     y_denomerator = sum([(y_dict[word]*(idf_dict[word]))**2 for word in list(set(sent_y.strip().split()))])

     if numerator == 0 or math.sqrt(x_denomerator) == 0 or math.sqrt(y_denomerator) == 0:
          return 0
     else:
          return round(numerator/(math.sqrt(x_denomerator)*math.sqrt(y_denomerator)),4)


def idfmodified_cosine_matrix(sentences, idf_dict):
    #Create Matrix
    cos_matrix = np.zeros([len(sentences),len(sentences)])
    row_num = [x for x in range(len(sentences))]
    col_num = [x for x in range(len(sentences))]
    N = len(sentences)
    for i in row_num:
        for j in col_num:
            cos_matrix[i][j] = idf_cosine_calc(sentences[i],sentences[j], idf_dict)
    return cos_matrix


def lexrank_graph(similarity_matrix, cos_th, alpha):
    rows_over_thr, cols_over_thr = np.where(similarity_matrix >= cos_th)
    graph_matrix = np.zeros(similarity_matrix.shape)
    #make degree vector 
    degree_matrix = np.zeros(similarity_matrix.shape[1])

    for i, j in zip(rows_over_thr, cols_over_thr):
        if i == j:
            continue
        else:
            graph_matrix[i][j] = 1
            degree_matrix[i]+= 1
    #CosineMatrix[i][j]/Degree[i]
    for i, j in zip(rows_over_thr, cols_over_thr):
        if i == j:
            continue
        else:
            similarity_matrix[i][j] = similarity_matrix[i][j]/degree_matrix[i]
    # using networkx
    graph = nx.Graph()
    for i, j in zip(rows_over_thr, cols_over_thr):
        if i == j:
            continue
        else:
            graph.add_edge(i, j , weight= similarity_matrix[i][j])
    lexrank = nx.pagerank(graph, alpha=0.9,  max_iter=5000)
    return lexrank


def lexrank(sentences, word_thr=100, sent_split=False, word_split=False, stemming=False, cos_th=0.05, alpha=0.9):
    # sentence_tokenize
    if sent_split:
        sentences = sent_tokenize(sentences)
    # retain original
    original_sentences = sentences
    print(original_sentences)
    # word_tokenize
    if word_split:
        sentences = [" ".join(word_tokenize(sent)) for sent in sentences]
    # stemming
    if stemming:
        stemmer = stem.PorterStemmer()
        sentences = [stemmer.stem(sent) for sent in sentences]
    # make all words lowercase for calc tf-idf & lexrank
    sentences_lower = [sent.lower() for sent in sentences]
    # construct idf dictionary
    idf_set           = idf_dict(sentences_lower)
    similarity_matrix = idfmodified_cosine_matrix(sentences_lower, idf_set)
    lexrank           = lexrank_graph(similarity_matrix, cos_th, alpha)
    lexrank_sentences = []
    word_counter = 0
    for num, score in sorted(lexrank.items(), key=lambda x:x[1], reverse=True):
        length = len(original_sentences[num].strip().split())
        if word_counter+length <= word_thr:
            word_counter += length
            lexrank_sentences.append(original_sentences[num])
        else:
            # avoid to extract nothing if 1st sentence of lexrank score is longer than word_thr
            if word_counter == 0:
                continue
            else:
                break
    return " ".join(lexrank_sentences)


def test():
    # example sentence from LexRank paper
    sents = ["Iraqi Vice President Taha Yassin Ramadan announced today, Sunday, that Iraq refuses to back down from its decision to stop cooperating with disarmament inspectors before its demands are met.",
            "Iraqi Vice president Taha Yassin Ramadan announced today, Thursday, that Iraq rejects cooperating with the United Nations except on the issue of lifting the blockade imposed upon it since the year 1990.",
            "Ramadan told reporters in Baghdad that ”Iraq cannot deal positively with whoever represents the Security Council unless there was a clear stance on the issue of lifting the blockade off of it.",
            "Baghdad had decided late last October to completely cease cooperating with the inspectors of the United Nations Special Commission (UNSCOM), in charge of disarming Iraq’s weapons, and whose work became very limited since the fifth of August, and announced it will not resume its cooperation with the Commission even if it were subjected to a military operation.",
            "The Russian Foreign Minister, Igor Ivanov, warned today, Wednesday against using force against Iraq, which will destroy, according to him, seven years of difficult diplomatic work and will complicate the regional situation in the area.",
            "Ivanov contended that carrying out air strikes against Iraq, who refuses to cooperate with the United Nations inspectors, “will end the tremendous work achieved by the international group during the past seven years and will complicate the situation in the region.”",
            "Nevertheless, Ivanov stressed that Baghdad must resume working with the Special Commission in charge of disarming the Iraqi weapons of mass destruction (UNSCOM).",
            "The Special Representative of the United Nations Secretary-General in Baghdad, Prakash Shah, announced today, Wednesday, after meeting with the Iraqi Deputy Prime Minister Tariq Aziz, that Iraq refuses to back down from its decision to cut off cooperation with the disarmament inspectors.",
            "British Prime Minister Tony Blair said today, Sunday, that the crisis between the international community and Iraq “did not end” and that Britain is still “ready, prepared, and able to strike Iraq.”",
            "In a gathering with the press held at the Prime Minister’s office, Blair contended that the crisis with Iraq “will not end until Iraq has absolutely and unconditionally respected its commitments” towards the United Nations.",
            "A spokesman for Tony Blair had indicated that the British Prime Minister gave permission to British Air Force Tornado planes stationed in Kuwait to join the aerial bombardment against Iraq."]
    print("Lexrank:\n{}".format(lexrank(sents, word_thr=100, word_split=True)))


if __name__ == '__main__':
    test()
