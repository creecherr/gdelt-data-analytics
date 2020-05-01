import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from api.firebase import Firebase


def report_generator():
    """
    This is the dynamic report generator. The charts generated are:
    1. Descriptive Statistics
    2. Correlation Chart
    3. Goldstein Summary Statistics Grouped by Class1
    4. Average Tone Summary Statistics Grouped by Class1
    5. Average Tone vs. ML Results: Class2 Scatterplot
    6. Goldstein Score vs. ML Results: Class2 Scatterplot
    """
    firebase = Firebase()
    data = firebase.get_data()

    gdelt_df = pd.DataFrame(data)
    matplotlib.use('agg')

    descriptive_stats = gdelt_df.describe()
    descriptive_chart = plt.figure(figsize=(9, 2))
    ax = plt.subplot(111)
    ax.axis('off')
    ax.table(cellText=descriptive_stats.values, colLabels=descriptive_stats.columns,
             rowLabels=['count', ' mean', 'std', 'min', '25%', '50%', '75%', 'max'], bbox=[0, 0, 1, 1])
    txt = '''
        Descriptive Statistics'''
    descriptive_chart.text(.35, .92, txt)

    correlations = gdelt_df.corr()
    correlation_chart = plt.figure(figsize=(9, 2))
    ax = plt.subplot(111)
    ax.axis('off')
    ax.table(cellText=correlations.values, colLabels=correlations.columns,
             rowLabels=correlations.columns, bbox=[0, 0, 1, 1])
    txt = '''
        Correlation Chart'''
    correlation_chart.text(.35, .92, txt)

    class1_goldstein_relation = gdelt_df.groupby('class1')['goldstein'].describe()
    class1_goldstein_chart = plt.figure(figsize=(9, 2))
    ax = plt.subplot(111)
    ax.axis('off')
    ax.table(cellText=class1_goldstein_relation.values, colLabels=class1_goldstein_relation.columns,
             rowLabels=['True', ' False'], bbox=[0, 0, 1, 1])
    txt = '''
            Goldstein Statistics Grouped by Class1'''
    class1_goldstein_chart.text(.30, .92, txt)

    class1_tone_relation = gdelt_df.groupby('class1')['average_tone'].describe()
    class1_tone_chart = plt.figure(figsize=(9, 2))
    ax = plt.subplot(111)
    ax.axis('off')
    ax.table(cellText=class1_tone_relation.values, colLabels=class1_tone_relation.columns,
             rowLabels=['True', ' False'], bbox=[0, 0, 1, 1])
    txt = '''
            Average Tone Statistics Grouped by Class1'''
    class1_tone_chart.text(.30, .92, txt)

    tone_chart = gdelt_df.plot(kind='scatter', x='average_tone', y='class2',
                            title='Average Tone vs. ML Results: Class2').get_figure()
    goldstien_chart = gdelt_df.plot(kind='scatter', x='goldstein', y='class2',
                            title='Goldstein Score vs. ML Results: Class2').get_figure()

    with PdfPages('report.pdf') as pdf:
        pdf.savefig(descriptive_chart)
        pdf.savefig(correlation_chart)
        pdf.savefig(class1_tone_chart)
        pdf.savefig(class1_goldstein_chart)
        pdf.savefig(tone_chart)
        pdf.savefig(goldstien_chart)
