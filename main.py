from Dataset import *
from Environment import *
from Sta import *

import time
import operator


if __name__ == "__main__":
    # Storage for all loaded data

    my_dataset = Dataset(
                         # 'data/template_sta/scanpaths/DOD2016_fixations_2_participants.tsv',
                         # 'data/template_sta/scanpaths/DOD2016_fixations.tsv',
                         # 'data/template_sta/scanpaths/DOD2016_fixations_10_participants.tsv',
                         'data/template_sta/scanpaths/DOD2016_fixations_5_participants.tsv',
                         # 'data/template_sta/regions/seg_FIIT_page.txt',
                         'data/template_sta/regions/seg_FIIT_page_simplified.txt',
                         'static/images/datasets/template_sta/placeholder.png',
                         'http://www.fiit.stuba.sk/')
    # Environment in which the eye tracking experiment was performed
    my_env = Environment(0.5, 60, 1920, 1200, 17)


    """ STA part"""
    """
    start_time = time.time()

    sta = Sta(my_dataset, my_env)
    sta.sta_run()
    print "aaaaaaaaaaa"
    print("--- %s seconds ---" % (time.time() - start_time))
    """

    """ Position-based Weighted Models """
    sta = Sta(my_dataset, my_env)

    mySequences = sta.createSequences(0)
    for keys, values in mySequences.items():
        print(keys)
        print(values)


    keys = mySequences.keys()

    # odstranenie bodky na konci
    for y in range(0, len(keys)):
        mySequences[keys[y]] = mySequences[keys[y]].split('.')
        del mySequences[keys[y]][len(mySequences[keys[y]]) - 1]

    #  rozdeli D-100 na pole z dvomi prvkami D a 100
    for y in range(0, len(keys)):
        for z in range(0, len(mySequences[keys[y]])):
            mySequences[keys[y]][z] = mySequences[keys[y]][z].split('-')

    # crating dictionary of AOIS
    aois = {}
    for item in my_dataset.aois:
        aois[item[5]] = 0.0

    # vytvorenie histogramu
    for y in range(0, len(keys)):
         aois[mySequences[keys[y]][0][0]] = aois[mySequences[keys[y]][0][0]] + 1
         aois[mySequences[keys[y]][1][0]] = aois[mySequences[keys[y]][1][0]] + 0.5
         aois[mySequences[keys[y]][2][0]] = aois[mySequences[keys[y]][2][0]] + 0.2

    # zoradi dictionary do pola
    sorted = sorted(aois.items(), reverse=True, key=operator.itemgetter(1))

    # create printable result
    result = ""
    for i in range (0, 3):
        result =  result + sorted[i][0] +","

    print result[:len(result)-1]

    #   TODO  dorobit nech je to samostatna trieda
    #   TODO dorobit nech nemozu byt za sbou dve rovnake pismena v sekvencii
    #   TODO dorobit nech sa odfiltruju fixacie kratsie ako x ms
    #   TODO sekvencia by mala mat vlastnu triedu s tym ze by tam bolo to create sequence + by sa dala nastavit na minimalna dlzka trvania fixacie
