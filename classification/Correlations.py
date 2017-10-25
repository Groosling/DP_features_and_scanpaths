import pandas as pd
from pandas import Series
import seaborn as sns

class Correlations:
    def __init__(self):
        self.dfData = pd.DataFrame()
        self.correlations = pd.Series()
        self.sortedCorrelationsName = []


    def calculateCorrelations(self, dfData, dfPredicted):
        self.sortedCorrelationsName = []
        length = len(dfData.index.values.tolist())
        dfData = dfData.reset_index()
        dfPredicted = dfPredicted.reset_index()
        self.dfData = pd.concat([dfData, dfPredicted], axis=1)
        tmp = self.dfData.corr(method='spearman')["predicted"]
        self.correlations = tmp.drop("predicted").abs().sort_values(ascending=False)
        i = 0
        for i in range(self.correlations.size):
            print(self.correlations.index.values[i] + ": " + str(self.correlations.values[i]))
            self.sortedCorrelationsName.append(self.correlations.index.values[i])


    def plotBoxplot(self):
        # normalize data - except target variable
        columnNames = self.sortedCorrelationsName[:10]

        newDf =  self.dfData[columnNames].copy()
        df_norm = (newDf - newDf.mean()) / (newDf.max() - newDf.min())
        df_norm['predicted'] = self.dfData['predicted']

        ax = sns.boxplot(data=df_norm, orient="v", palette="Set3", whis=3)
        ax.get_figure().savefig('boxplot_seaborn.png')

    def plotPairsSeaborn(self):
        columnNames = self.sortedCorrelationsName[:10]
        columnNames.append("predicted")
        sns_plot = sns.pairplot(self.dfData[columnNames], hue="predicted", diag_kind="kde")
        sns_plot.savefig('scatter_matrix_seaborn.png')

    def getBestColumnNames(self, n):
        return self.sortedCorrelationsName[:n]