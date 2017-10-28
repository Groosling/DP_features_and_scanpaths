from os import listdir
import copy
import pandas as pd
from configparser import ConfigParser
import codecs
import csv
import numpy as np

# TODO class should store all the sequences/scanpaths instead of receiving them via function arguments
# TODO the same goes for error area - once calculated set it as property
class Dataset:
    """Common class for grouping a set of scanpaths together"""

    def __init__(self, file_path_scanpaths, file_path_aoi, file_path_visual, website_name):
        self.parser = ConfigParser()
        # Open the file with the correct encoding
        with codecs.open('config.ini', 'r', encoding='utf-8') as f:
            self.parser.readfp(f)
        # Initialize attributes
        self.FIXATION_INDEX = 0
        self.TIME_INDEX = 0
        self.DUR_INDEX = 0
        self.XPOINT_INDEX = 0
        self.YPOINT_INDEX = 0
        self.PARTICIPANT_NAME_INDEX = 0
        self.PAGE_NAME_INDEX = 0
        self.file_path_aoi = file_path_aoi
        self.file_path_visual = file_path_visual
        self.file_path_scanpaths = file_path_scanpaths
        self.data_file_format = '.tsv'
        self.website_name = website_name
        self.last_participant_name = ""
        # Data holding objects
        self.participants = {}
        self.aois = []
        # Fill the data holding objects
        self.load_participants()
        self.load_aois()


    def load_participants(self):
        act_file_data = []
        currentfix = 0
        with open(self.file_path_scanpaths, 'r') as f:
            currentfix = 0
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                if row["MediaName"].split(" ")[0] != self.website_name:  # ignore non-recording data point
                    continue
                if not row["ValidityLeft"] or not row["ValidityRight"] or not row["FixationPointX (MCSpx)"] or not \
                row["FixationPointY (MCSpx)"]:  # ignore data point with no information
                    continue
                if row["GazeEventType"] != "Fixation" or currentfix == currentfix == int(row["FixationIndex"]):
                    # if not a fixation or the current fixation
                    continue
                # clear data on visit of first line of new participant
                if self.last_participant_name !=row["ParticipantName"]:
                    act_file_data = []
                    self.last_participant_name = row["ParticipantName"]
                act_file_data.append([str(int(row["FixationIndex"]) - 1),
                                      row["RecordingTimestamp"],
                                      row["GazeEventDuration"],
                                      row["FixationPointX (MCSpx)"],
                                      row["FixationPointY (MCSpx)"],
                                      row["MediaName"].split(" ")[0],
                                      ])
                participant_identifier = row["ParticipantName"]
                self.participants[participant_identifier] = act_file_data
                currentfix = int(row["FixationIndex"])
        f.close()

    def load_aois(self):
        """
        Format macitavaneho suboru:
        nazov ,x. x-offset, y, y-offset, AOI_char
        """
        try:
            fo = open(self.file_path_aoi, "r")
        except:
            print ("Failed to open file containing areas of interest")
        aoi_file = fo.read()
        file_lines = aoi_file.split('\n')

        # Read the file by lines and remember Identifier, X-from, X-length, Y-from, Y-length, ShortID
        for x in range(0, len(file_lines)):
            temp = file_lines[x].split(' ')
            self.aois.append([temp[0], temp[1], temp[2], temp[3], temp[4], temp[5]])

    def load_visuals(self):
        print ('hello')



    def get_max_similarity(self, scanpaths):
        """ Function calculates most similiar double for each scanpath in the set """
        for scanpath in scanpaths:
            # Create empty max_similarity object
            max_similar = {}
            max_similar['identifier'] = ''
            max_similar['value'] = -1
            # Iterate through previously calculated similarity values of given scanpath
            for similarity_iter in scanpath['similarity']:
                similarity_val = scanpath['similarity'][similarity_iter]
                if similarity_val > max_similar['value']:
                    max_similar['value'] = similarity_val
                    max_similar['identifier'] = similarity_iter
            # Assign max_similarity object to scanpath (in JSON-style)
            scanpath['maxSimilarity'] = max_similar

    def get_min_similarity(self, scanpaths):
        """ Function calculates most similiar double for each scanpath in the set """
        for scanpath in scanpaths:
            # Create empty max_similarity object
            min_similar = {}
            min_similar['identifier'] = ''
            min_similar['value'] = 101
            # Iterate through previously calculated similarity values of given scanpath
            for similarity_iter in scanpath['similarity']:
                similarity_val = scanpath['similarity'][similarity_iter]
                if similarity_val < min_similar['value']:
                    min_similar['value'] = similarity_val
                    min_similar['identifier'] = similarity_iter
            # Assign max_similarity object to scanpath (in JSON-style)
            scanpath['minSimilarity'] = min_similar

    def getListOfGroups(self):
        listOfGroups = []
        counter = 1
        while counter:
            try:
                listOfGroups.append(self.parser.get('participants', 'group' + str(counter)).split('\n'))
                counter += 1
            except:
                break
        return listOfGroups

    def getDatasetDividedIntoGroups(self):
        # load separation of participant into groups
        listOfGroups= self.getListOfGroups()
        # create copies of loaded dataset with particular participants of the groups
        listOfDatasets = []
        for group in listOfGroups:
            tempDataset = copy.copy(self)
            tempDataset.participants = {}
            for participant in group:
                if participant in self.participants:
                    tempDataset.participants[participant] = self.participants[participant]
            listOfDatasets.append(tempDataset)
        return listOfDatasets

    def getPredictedColumnValues(self):
        listOfGroups = self.getListOfGroups()
        counter = 0
        dataframe = pd.DataFrame()
        for group in listOfGroups:
            d = pd.DataFrame(counter, index=group, columns=['predicted'])
            dataframe = pd.concat([dataframe, d], axis=0)
            counter += 1
        dataframe.drop(["tester18"], inplace=True)
        return dataframe






