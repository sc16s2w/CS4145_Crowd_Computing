from nltk.stem import SnowballStemmer


def parsing_baseline(path):
    entity_start_id = 3
    entity_num = 8

    feature_start_id = 11
    feature_num = 8

    entity_list = {}
    feature_list = {}

    entity_list_single = {}
    feature_list_single = {}

    stemmer = SnowballStemmer("english")

    with open(path, 'r', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            if 'https' not in line:
                continue

            items = line.split('\t')
            url = items[0]

            for i in range(entity_start_id, entity_start_id + entity_num):
                words = items[i].strip().lower().split(',')
                for word in words:
                    if word != '':
                        word = stemmer.stem(word).strip()
                        entity_list[word] = ''

                        if url not in entity_list_single.keys():
                            entity_list_single[url] = {}
                        entity_list_single[url][word] = 0

            for i in range(feature_start_id, feature_start_id + feature_num):
                words = items[i].strip().lower().split(',')
                for word in words:
                    if word != '':
                        word = stemmer.stem(word).strip()
                        feature_list[word] = ''

                        if url not in feature_list_single.keys():
                            feature_list_single[url] = {}
                        feature_list_single[url][word] = 0


    print('\n\n\nEntities {}:\n'.format(len(entity_list.keys())))
    print(entity_list.keys())
    print('\n\n\nFeatures {}:\n'.format(len(entity_list.keys())))
    print(feature_list.keys())

    return entity_list.keys(), feature_list.keys(), entity_list_single, feature_list_single


def parsing_improved(path):
    entity_start_id = 2
    entity_num = 8 + 8

    feature_start_id = 18
    feature_num = 8 + 8

    entity_list = {}
    feature_list = {}

    entity_list_single = {}
    feature_list_single = {}

    stemmer = SnowballStemmer("english")
    tmp = {}
    counter = 0
    with open(path, 'r', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            items = line.replace('"', '').split('\t')
            if 'https' not in line:
                continue
            counter += 1
            items = line.replace('"','').split('\t')
            url = items[0]



            tmp[url] = ''

            for i in range(entity_start_id, entity_start_id + entity_num):
                words = items[i].strip().lower().split(',')
                for word in words:
                    if word != '':
                        word = stemmer.stem(word).strip()
                        entity_list[word] = ''

                        if url not in entity_list_single.keys():
                            entity_list_single[url] = {}
                        entity_list_single[url][word] = 0

            for i in range(feature_start_id, feature_start_id + feature_num):
                words = items[i].strip().lower().split(',')
                for word in words:
                    if word != '':
                        word = stemmer.stem(word).strip()
                        feature_list[word] = ''

                        if url not in feature_list_single.keys():
                            feature_list_single[url] = {}
                        feature_list_single[url][word] = 0


    print('\n\n\nEntities {}:\n'.format(len(entity_list.keys())))
    print(entity_list.keys())
    print('\n\n\nFeatures {}:\n'.format(len(feature_list.keys())))
    print(feature_list.keys())

    return entity_list.keys(), feature_list.keys(), entity_list_single, feature_list_single


def writeTSV(path, content):
    with open(path, 'w+') as write_tsv:
        line = '{}\t{}\t{}\n'.format('picId', 'diversity', 'words')
        write_tsv.write(line)
        for url in content:
            key = int(url.replace('https://raw.githubusercontent.com/sc16s2w/CS4145_Crowd_Computing/main/', '').replace('.jpg', ''))
            diversity = len(content[url])
            line = '{}\t{}\t{}\n'.format(key, diversity, list(content[url].keys()))
            write_tsv.write(line)


if __name__ == '__main__':
    #print('Baseline\n')
    b1,b2,b3,b4 = parsing_baseline('baseline.tsv')

    #print('Improved\n')
    i1, i2, i3, i4 = parsing_improved('improved_answer.tsv')

    writeTSV('diversity_single_baseline_entity', b3)
    writeTSV('diversity_single_baseline_feature', b4)
    writeTSV('diversity_single_improved_entity', i3)
    writeTSV('diversity_single_improved_feature', i4)


    #print('Baseline_train\n')
    b1,b2,b3,b4 = parsing_baseline('baseline_train_answer.tsv')

    #print('Improved\n')
    i1, i2, i3, i4 = parsing_improved('improved_train_answer.tsv')

    writeTSV('diversity_single_baseline_train_entity', b3)
    writeTSV('diversity_single_baseline_train_feature', b4)
    writeTSV('diversity_single_improved_train_entity', i3)
    writeTSV('diversity_single_improved_train_feature', i4)