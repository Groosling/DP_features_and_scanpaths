from Dataset import *
from Environment import *
from Sta import *
from Position_based_Weighted_Models import *

import time



if __name__ == "__main__":
    # Storage for all loaded data

    my_dataset = Dataset(
                         # 'data/template_sta/scanpaths/DOD2016_fixations_2_participants.tsv',
                         # 'data/template_sta/scanpaths/DOD2016_fixations.tsv',
                         'data/template_sta/scanpaths/DOD2016_fixations_10_participants.tsv',
                         # 'data/template_sta/scanpaths/DOD2016_fixations_5_participants.tsv',
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
    # bez simpifyingu fubnngovalo lepsie
    sta.sta_run()
    print "aaaaaaaaaaa"
    print("--- %s seconds ---" % (time.time() - start_time))
    """

    """ Position-based Weighted Models """
    """
    pbwm  = Position_based_Weighted_Models(my_dataset)
    #  po simplifikacii stale rovnako
    result = pbwm.run_PBWM()
    print result
    """

    # errorRateArea = 0
    # mySequences = Sequence.createSequences(my_dataset, errorRateArea)
    # for keys, values in mySequences.items():
    #     print(keys)
    #     print(values)
    #
    # mySequences = Sequence.getArrayRepresentationOfSequence(mySequences)
    # processed_sequence = Sequence.applyFixDurationThreshold(mySequences)






    #   TODO dorobit nech nemozu byt za sbou dve rovnake pismena v sekvencii
    #   TODO dorobit nech sa odfiltruju fixacie kratsie ako x ms

