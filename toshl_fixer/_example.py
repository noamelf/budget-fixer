import glob, os, nltk, pickle, math
from nltk.corpus import stopwords
import seaborn as sns
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


# Utilities -----


def strip_spaces(text):
    return " ".join(text.split())


def to_float(text):
    return float(text)


def to_date(text):
    return datetime.strptime(text, "%d/%m/%Y")


def to_dict(description):
    return dict(
        [
            (word, True)
            for word in description.upper().split()
            if word not in stopwords.words("english")
        ]
    )


def train_classifier(file_list, converters):
    training_data = pd.concat(
        pd.read_csv(f, converters=converters) for f in file_list
    )  # Read the .csv files
    training_set = [
        (to_dict(row["Description"]), row["Category"])
        for i, row in training_data[training_data["Category"].notnull()].iterrows()
    ]  # Convert the data to NLTK format
    classifier = nltk.NaiveBayesClassifier.train(training_set)  # Train the classifier
    print(len(training_data))

    return classifier


# Main program -----

converters = {
    "Date": to_date,
    "Description": strip_spaces,
    "Amount": to_float,
    "Balance": to_float,
}
train_classifier_flag = True
test_classifier_flag = True
classify_flag = False

# Train classifier -----

if train_classifier_flag == True:
    training_file_list = glob.glob(
        os.path.join("2011", "*.CSV")
    )  # Use 2011 as training set
    # training_file_list.append(os.path.join("2016", "Historical20160124_68832978.CSV"))
    classifier = train_classifier(
        training_file_list, converters
    )  # Get a trained classifier
    f = open("classifier.pickle", "wb")
    pickle.dump(classifier, f)
    f.close()

# Test classifier -----

if test_classifier_flag == True:
    f = open("classifier.pickle", "rb")
    classifier = pickle.load(f)
    f.close()
    test_file_list = glob.glob(os.path.join("2012", "*.CSV"))  # Use 2011 as testing set
    test_data = pd.concat(
        (pd.read_csv(f, converters=converters) for f in test_file_list),
        ignore_index=True,
    )
    categories_all = sorted(
        set(
            classifier.labels()
            + test_data[test_data["Category"].notnull()]["Category"].tolist()
        )
    )
    matrix = pd.DataFrame(data=0, columns=categories_all, index=categories_all)
    for i, row in test_data[test_data["Category"].notnull()].iterrows():
        category = classifier.classify(to_dict(row["Description"]))
        probs = classifier.prob_classify(to_dict(row["Description"]))
        probability = probs.prob(category)
        if probability > 0:
            if row["Category"] == category:
                test_data.loc[i, "Probability"] = probability
                test_data.loc[i, "Estimated Category"] = category
            else:
                test_data.loc[i, "Probability"] = probability
                test_data.loc[i, "Estimated Category"] = category
                # print(classifier.show_most_informative_features(5))
        if row["Category"] in categories_all and category in categories_all:
            matrix.loc[row.Category, category] += 1
        else:
            print(row["Category"], category)

    correct = test_data.loc[(test_data["Category"] == test_data["Estimated Category"])]
    incorrect = test_data.loc[
        (test_data["Category"].notnull())
        & (test_data["Estimated Category"] != test_data["Category"])
    ]
    unclassified = test_data.loc[(test_data["Estimated Category"].isnull())]
    print(
        len(correct),
        len(incorrect),
        len(unclassified),
        len(test_data),
        "{:.1%}".format(len(correct) / len(test_data)),
    )

    petrol = test_data.loc[
        (test_data["Category"] == "Groceries")
        & (test_data["Estimated Category"] == "Petrol")
    ]
    for i, row in petrol.iterrows():
        print(row["Description"], row["Probability"], row["Amount"])
    print(len(petrol))

    sns.set()

    ax = plt.subplot()
    sns.distplot(
        correct["Probability"],
        bins=25,
        hist=True,
        kde=False,
        label="Correctly classified",
    )
    sns.distplot(
        incorrect["Probability"],
        bins=25,
        hist=True,
        kde=False,
        label="Incorrectly classified",
    )
    ax.set_xlim(0, 1)
    ax.set_xlabel("Probability of estimated category")
    ax.set_ylabel("Number of transactions")
    ax.legend(loc="upper left")
    sns.plt.tight_layout()
    sns.plt.savefig("acc_hist.png")
    sns.plt.clf()

    ax = plt.subplot()
    sns.heatmap(
        matrix,
        annot=False,
        linewidths=0.5,
        cbar=True,
        square=True,
        annot_kws={"size": "xx-small"},
    )
    ax.set_xlabel("Estimated Category", size="x-small", labelpad=10)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, size="x-small")
    ax.set_ylabel("True Category", size="x-small", labelpad=10)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, size="x-small")
    ax.invert_yaxis()
    sns.plt.tight_layout()
    sns.plt.savefig("acc_occ.png")
    # sns.plt.show()

    """
    #plt.figure()
    fig, ax = plt.subplots()
    ax.set_yticks([y + .5 for y in range(0, len(matrix.index))], minor = False)
    ax.set_yticklabels(matrix.index, size = "small")
    ax.set_xticks([y + .5 for y in range(0, len(matrix.index))], minor = False)
    ax.set_xticklabels(matrix.columns, minor = False, rotation = 90, size = "small")
    plt.pcolor(matrix, cmap = plt.cm.Greys, alpha = 0.8)
    plt.show()
    """

    # true_category = test_data[["Category"]].groupby([test_data["Category"]]).count()
    # estimated_category = test_data[["Estimated Category"]].groupby([test_data["Estimated Category"]]).count()

# Classify files -----

if classify_flag == True:
    f = open("classifier.pickle", "rb")
    classifier = pickle.load(f)
    f.close()
    test_file_list = glob.glob(os.path.join("2016", "*.CSV"))  # Use 2016 as test set
    test_data = pd.concat(pd.read_csv(f, converters=converters) for f in test_file_list)
    over_50, under_50 = 0, 0
    categories = []
    probabilities = []
    for i, row in test_data.iterrows():
        category = classifier.classify(to_dict(row["Description"]))
        categories.append(category)
        probs = classifier.prob_classify(to_dict(row["Description"]))
        probability = probs.prob(category)
        probabilities.append(probability)
        print("{}, {}, {:.1%}".format(row.Description, category, probability))
        if probability > 0.5:
            over_50 += 1
        else:
            under_50 += 1
    print(over_50, under_50)
    test_data["Category"] = categories
    test_data["Probability"] = probabilities

    count = test_data[["Category"]].groupby([test_data["Category"]]).count()
    sums = []
    for category in count.iterrows():
        sums.append(test_data.loc[test_data["Category"] == category[0], "Amount"].sum())
    count["Sum"] = sums

    plt.figure()
    count.plot(kind="bar")
    plt.show()
    print(count)
