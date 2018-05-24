import pandas as pd
from pandas import Series
import seaborn as sns
from sklearn import preprocessing as pp
from configparser import ConfigParser
import codecs

config = ConfigParser()
# Open the file with the correct encoding
with codecs.open('config.ini', 'r', encoding='utf-8') as f:
    config.readfp(f)

class Correlations:
    def __init__(self):
        self.dfData = pd.DataFrame()
        self.correlations = pd.Series()
        self.sortedCorrelationsName = []

    def deleteHighlyCorrelatedAttributes(self, dfInterAttributesCorrelation, dictCorrTopredicted):
        resultColumns = dict(dictCorrTopredicted)
        threshold = float(config.get("correlations", "interAttributesCorrThreshold"))
        print("Inter correlation threshold")
        print("----------------------------")
        print(str(threshold))

        for index, row in dfInterAttributesCorrelation.iterrows():
            for column in dfInterAttributesCorrelation:
                # if comapring same attributes... skip
                if dfInterAttributesCorrelation.columns.get_loc(column) == dfInterAttributesCorrelation.index.get_loc(index):
                    continue
                # pop less correlatet attribute
                if row[column] > threshold:
                    resultColumns.pop(column, None) if dictCorrTopredicted[index] > dictCorrTopredicted[column] else resultColumns.pop(index, None)
        return list(resultColumns.keys())

    def keepJustParticularColumnsInAllData(self, dataframes, columns):
        for i in range(0, len(dataframes)):
            dataframes[i]["data"] = dataframes[i]["data"][columns]
        return dataframes

    def calculateInterAttributesCorrelations(self, df):
        correlations = df.corr(method='spearman').abs();
        # for i in range(0, correlations.shape[0]):
            # print(correlations.index.values[i] + ": " + str(correlations.values[i]))
        return correlations

    def calculateCorrelationsToPredicted(self, dfData, dfPredicted):
        self.sortedCorrelationsName = []
        length = len(dfData.index.values.tolist())
        dfData = dfData.reset_index()
        dfPredicted = dfPredicted.reset_index()
        self.dfData = pd.concat([dfData, dfPredicted], axis=1)
        tmp = self.dfData.corr(method='spearman')["predicted"]
        self.correlations = tmp.drop("predicted").abs().sort_values(ascending=False)
        result = {}
        i = 0
        for i in range(self.correlations.size):
            # print(self.correlations.index.values[i] + ": " + str(self.correlations.values[i]))
            self.sortedCorrelationsName.append(self.correlations.index.values[i])
            result[self.correlations.index.values[i]] = self.correlations.values[i]
        return result


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

    def featureEngineering(self, dataframes):
        poly = pp.PolynomialFeatures(2)
        for i in range(0, len(dataframes)):
            rowNames = dataframes[i]["data"].index.values.tolist()
            res = poly.fit_transform(dataframes[i]["data"])
            columns = poly.get_feature_names(dataframes[i]["data"].columns.values.tolist())
            dataframes[i]["data"] = pd.DataFrame(res, index=rowNames)
            dataframes[i]["data"].columns = columns
            dataframes[i]["data"].drop("1",  axis=1, inplace=True)