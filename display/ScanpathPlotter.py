from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.path import Path
import matplotlib.patches as patches
import pylab
import numpy as np
from random import randint

from configparser import ConfigParser
import codecs


parser = ConfigParser()
# Open the file with the correct encoding
with codecs.open('config.ini', 'r', encoding='utf-8') as f:
    parser.readfp(f)


class ScanpathPlotter:

    def participantToPlotRepresentation(self,participant):
        """
        Transfrom from participants representation to dictionaries of lists

        Returns:
        {
            x: []
            y : []
            dur: []
        }
        """
        minFixDurationThreshold = parser.get('display', 'minFixDurationThreshold')

        result = {}
        result['x'] = []
        result['y'] = []
        result['dur'] = []
        for fixation in participant:
            if int(fixation[2]) > int(minFixDurationThreshold):
                result['x'].append(fixation[3])
                result['y'].append(fixation[4])
                result['dur'].append(fixation[2])
        return result

    def scanpathToPlotRepresentation(self,scanpath, aois):
        """

        Args:
            scanpath: array of characters
            aois: aois from dataset

        Returns:
        {
            x: []
            y : []
            dur: []
        }
        """
        print("aaa")
        result = {}
        result['x'] = []
        result['y'] = []
        result['dur'] = []
        for area in scanpath:
            aoi = None
            for i in range(0, len(aois)):
                if area == aois[i][5]:
                    aoi = aois[i]
                    break
            if aois is not None:
                result['x'].append(randint(int(aoi[1]), int(aoi[1]) + int(aoi[2])) )
                result['y'].append(randint(int(aoi[3]), int(aoi[3]) + int(aoi[4])) )
                result['dur'].append(400)
        return result



    def plot2D(self, plotFileName, title, image_path, firstScanpath, secondScanpath = None , firstScanpathLegend=None, secondScanpathLegend=None ):
        """

        Args:
            plotFileName: file name without extension
            title: name of the plot
            image_path: path of background image
            firstScanpath:        {
                                x: []
                                y : []
                                dur: []
                            }
            secondScanpath:        {
                        x: []
                        y : []
                        dur: []
                    }
        Returns:

        """
        ax = plt.axes()

        # imige
        # img = Image.open(image_path).rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
        img = Image.open(image_path)
        (imw, imh) = img.size
        x0 = 0
        y0 = 0
        x1 = x0+imw
        y1 = y0+imh
        plt.imshow(np.asarray(img),alpha=1,
                 origin='None',aspect='auto',extent=(x0,x1,y0,y1))

        ax.set_ylim(ax.get_ylim()[::-1])


        # firstScanpath
        opt = {'antialiased':True,\
             'alpha':.6,\
             'color':"red",\
             'lw':1,\
             'marker':"o",\
             'markersize':2,\
             'markeredgecolor':"red",\
             'markeredgewidth':1}
        line = plt.Line2D(firstScanpath['x'], firstScanpath['y'], **opt)
        ax.add_artist(line)

        # texts next to fixations
        for i in range(len(firstScanpath['x'])):

            ax.annotate(str(i), (int(firstScanpath['x'][i]), int(firstScanpath['y'][i])), color='white', horizontalalignment='center', verticalalignment='center')
            r = int(firstScanpath['dur'][i]) / 10
            circ = plt.Circle((int(firstScanpath['x'][i]), int(firstScanpath['y'][i])), radius=r, fc='red', ec='white', alpha=0.6)
            ax.add_patch(circ)

        #-------------------------------------

        # secondScanpath
        opt = {'antialiased':True,\
             'alpha':.6,\
             'color':"blue",\
             'lw':1,\
             'marker':"o",\
             'markersize':2,\
             'markeredgecolor':"blue",\
             'markeredgewidth':1}
        line = plt.Line2D(secondScanpath['x'], secondScanpath['y'], **opt)
        ax.add_artist(line)

        # calclulate r base on image size
        r =  np.average([imw, imh]) / 50
        # texts next to fixations
        for i in range(len(secondScanpath['x'])):

            ax.annotate(str(i), (int(secondScanpath['x'][i]), int(secondScanpath['y'][i])), color='white', horizontalalignment='center', verticalalignment='center')

            circ = plt.Circle((int(secondScanpath['x'][i]), int(secondScanpath['y'][i])), radius=r, fc='blue', ec='white', alpha=0.6)
            ax.add_patch(circ)

        # ---------------------------------------
        # Legend
        handles, labels = ax.get_legend_handles_labels()
        display = (0,1,2)
        #Create custom artists
        simArtist = plt.Line2D((0,1),(0,0), color='r', marker='o', linestyle='', markersize='15')
        anyArtist = plt.Line2D((0,1),(0,0), color='b', marker='o', linestyle='', markersize='15')

        legendLabels = ['Single participant', 'Common scanpath']
        if firstScanpathLegend is not None:
            legendLabels[0] = firstScanpathLegend
        if secondScanpathLegend is not None:
            legendLabels[1] = secondScanpathLegend


        #Create legend from custom artist/label lists
        ax.legend([handle for i,handle in enumerate(handles) if i in display]+[simArtist,anyArtist],
                  [label for i,label in enumerate(labels) if i in display]+['Single participant', 'Common scanpath'],
                  loc='lower left',
                  fontsize = 'xx-large')
        # -------------------------------------
        # title and labels
        plt.title(title)
        plt.ylabel("$y$-coordinate (pixels)",family="sans-serif")
        plt.xlabel("$x$-coordinate (pixels)",family="sans-serif")
        plt.grid(True,'major',ls='solid',alpha=.1)
        # margins
        plt.tight_layout()



        fig = plt.gcf()
        fig.set_size_inches(imw / 100, imh / 100)
        fig.savefig('output\\plots\\'+ plotFileName + '.png', dpi=100)
        print(plotFileName)

