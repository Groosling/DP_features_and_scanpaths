from os import listdir


# TODO class should store all the sequences/scanpaths instead of receiving them via function arguments
# TODO the same goes for error area - once calculated set it as property
class Dataset:
    """Common class for grouping a set of scanpaths together"""

    def __init__(self, file_path_scanpaths, file_path_aoi, file_path_visual, website_name):
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
        # Fetch all files in specified folder
        # files_list = listdir(self.file_path_scanpaths)

        # for filename in files_list:
        if self.file_path_scanpaths.endswith(self.data_file_format):
            try:
                fo = open(self.file_path_scanpaths, "r")
            except:
                print "Failed to open specified file - skipping to next one"
                return
            act_file_content = fo.read()

            act_file_lines = act_file_content.split('\n')
            act_file_data = []

            # Read the file by lines (skip the first one with description)
            for y in range(0, len(act_file_lines) - 1):
                # if y = 0 get column of particular information we need
                if y ==0:
                    # find indeces of required columns
                    column_captions =act_file_lines[y].split('\t')
                    self.FIXATION_INDEX = column_captions.index("FixationIndex")
                    self.TIME_INDEX = column_captions.index("RecordingTimestamp")
                    self.DUR_INDEX = column_captions.index("GazeEventDuration")
                    self.XPOINT_INDEX = column_captions.index("FixationPointX (MCSpx)")
                    self.YPOINT_INDEX = column_captions.index("FixationPointY (MCSpx)")
                    self.PAGE_NAME_INDEX = column_captions.index("MediaName")
                    self.PARTICIPANT_NAME_INDEX = column_captions.index("ParticipantName")
                    #  TODO find specific column this way a contruct needed structure
                else:

                    try:
                        temp_act_file_line = ""
                        # If the page name argument matches the page name specified in file
                        if act_file_lines[y].index(self.website_name) > 0:
                            # Read the data in columns by splitting via tab character
                            temp_act_file_line = act_file_lines[y].split('\t')

                            # clear data on visit of first line of new participant
                            if self.last_participant_name != temp_act_file_line[self.PARTICIPANT_NAME_INDEX]:
                                act_file_data = []
                                self.last_participant_name = temp_act_file_line[self.PARTICIPANT_NAME_INDEX]

                            act_file_data.append([str(int(temp_act_file_line[self.FIXATION_INDEX]) - 1),
                                                  temp_act_file_line[self.TIME_INDEX],
                                                  temp_act_file_line[self.DUR_INDEX],
                                                  temp_act_file_line[self.XPOINT_INDEX],
                                                  temp_act_file_line[self.YPOINT_INDEX],
                                                  temp_act_file_line[self.PAGE_NAME_INDEX],
                            ])
                    except:
                        print "Invalid data format - line will be skipped"
                        continue

                    # Return object containing array of fixations (each fixation is also an array)
                    participant_identifier = temp_act_file_line[self.PARTICIPANT_NAME_INDEX]
                    self.participants[participant_identifier] = act_file_data
            fo.close()

    def load_aois(self):
        """
        Format macitavaneho suboru:
        nazov ,x. x-offset, y, y-offset, AOI_char
        """
        try:
            fo = open(self.file_path_aoi, "r")
        except:
            print "Failed to open file containing areas of interest"
        aoi_file = fo.read()
        file_lines = aoi_file.split('\n')

        # Read the file by lines and remember Identifier, X-from, X-length, Y-from, Y-length, ShortID
        for x in range(0, len(file_lines)):
            temp = file_lines[x].split(' ')
            self.aois.append([temp[0], temp[1], temp[2], temp[3], temp[4], temp[5]])

    def load_visuals(self):
        print 'hello'

    def get_formatted_sequences(self, sequences):
        """
        {'01': [[A, 150], [B, 250]], '02': ...} gets transformed into:
        [{'identifier': '01', 'fixations': [[A, 150], [B, 250]]}, {'identifier': '02' ... }]
        """
        formatted_sequences = []
        keys = sequences.keys()
        for it in range(0, len(sequences)):
            act_rec = {
                'identifier': keys[it],
                'fixations': sequences[keys[it]]
            }
            formatted_sequences.append(act_rec)

        return formatted_sequences

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
