from algorithm.Sta import *
from algorithm.Position_based_Weighted_Models import *
from algorithm.Dotplot import *
import time
from structure import Sequence
from ConfigParser import SafeConfigParser
import codecs
from featureExtraction import BasicFeatures



if __name__ == "__main__":
    parser = SafeConfigParser()
    # Open the file with the correct encoding
    with codecs.open('config.ini', 'r', encoding='utf-8') as f:
        parser.readfp(f)

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
    # bez simpifyingu fungovalo lepsie
    sta.sta_run(mod = 5)
    print "aaaaaaaaaaa"
    print("--- %s seconds ---" % (time.time() - start_time))
    """

    """ Position-based Weighted Models """
    """
    pbwm  = Position_based_Weighted_Models(my_dataset)
    #  po simplifikacii stale rovnako
    result = pbwm.run_PBWM(mod=5)
    print result
    """

    """Dotplot"""
    """
    dotplot = Dotplot(my_dataset, my_env)
    common_sequence = dotplot.runDotplot(mod=5)
    print common_sequence
    """

    sequence = Sequence.createSequences(my_dataset, mod=1)
    sequence = Sequence.getArrayRepresentationOfSequence(sequence)
    result = BasicFeatures.calculateBasicFeatures(my_dataset.participants)

    # vec1 = Sequence.calculateVector(0, 0, 2, 2)
    # vec2 = Sequence.calculateVector(0, 0, 0, 3)
    # angle = Sequence.calculateAngle(vec1, vec2)

    print "aaa"


    # errorRateArea = 0
    # mySequences = Sequence.createSequences(my_dataset, errorRateArea)
    # for keys, values in mySequences.items():
    #     print(keys)
    #     print(values)
    #
    # mySequences = Sequence.getArrayRepresentationOfSequence(mySequences)
    # processed_sequence = Sequence.applyFixDurationThreshold(mySequences)


