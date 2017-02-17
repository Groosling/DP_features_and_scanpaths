from algorithm.Sta import *
from algorithm.Position_based_Weighted_Models import *
from algorithm.Dotplot import *
import time
from structure import Sequence
from configparser import ConfigParser
import codecs
from featureExtraction import BasicFeatures
from featureExtraction import AgregatedFeatures
from featureExtraction.AoiFeatures import *
from featureExtraction.AngleFeatures import *
from display.ScanpathPlotter import ScanpathPlotter
if __name__ == "__main__":
    parser = ConfigParser()
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
    # """
    start_time = time.time()

    sta = Sta(my_dataset, my_env)
    # bez simpifyingu fungovalo lepsie
    res_data = sta.sta_run(mod=1)
    # print "aaaaaaaaaaa"
    print("--- %s seconds ---" % (time.time() - start_time))
    # """

    """ Position-based Weighted Models """
    """
    pbwm  = Position_based_Weighted_Models(my_dataset)
    #  po simplifikacii stale rovnako
    result = pbwm.run_PBWM(mod=1)
    print (result)
    """

    """Dotplot"""
    """
    dotplot = Dotplot(my_dataset, my_env)
    res_data = dotplot.runDotplot(simplify=True, mod=1)
    # print (common_sequence)
    """

    # sequence = Sequence.createSequences(my_dataset, mod=1)
    # sequence = Sequence.getArrayRepresentationOfSequence(sequence)
    # basicFeatures = BasicFeatures.calculateBasicFeatures(my_dataset.participants)
    # result = AgregatedFeatures.calculateAgregatedFeatures(basicFeatures)

    # vec1 = Sequence.calculateVector(0, 0, 2, 2)
    # vec2 = Sequence.calculateVector(0, 0, 0, 3)
    # angle = Sequence.calculateAngle(vec1, vec2)
    # aoisFeatures = AoiFeatures()
    # participantsWithAois = aoisFeatures.createParitcipantsWithAois(my_dataset)
    # result = aoisFeatures.getAoiFeatures(participantsWithAois)
    # angleFeatures = AngleFeatures()
    # angleFeatures.getAngleFeatures(my_dataset)
    # print ("aaa")


    # errorRateArea = 0
    # mySequences = Sequence.createSequences(my_dataset, errorRateArea)
    # for keys, values in mySequences.items():
    #     print(keys)
    #     print(values)
    #
    # mySequences = Sequence.getArrayRepresentationOfSequence(mySequences)
    # processed_sequence = Sequence.applyFixDurationThreshold(mySequences)


    scanPathPlotter = ScanpathPlotter()
    commonScanpathPositions =scanPathPlotter.scanpathToPlotRepresentation(res_data['fixations'], my_dataset.aois)
    keys = list(my_dataset.participants.keys())
    for key in keys:
        scanPath = scanPathPlotter.participantToPlotRepresentation(my_dataset.participants[key])
        scanPathPlotter.plot2D("Participant " + key,
                               "Participant " + key,
                               "d:\\diplomovka\\kod\\DP_features_and_scanpaths\\data\\template_sta\\img\\AOIs.png",
                               scanPath,
                               commonScanpathPositions,
                                firstScanpathLegend=key
                              )