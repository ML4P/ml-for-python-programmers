import json
import pandas as pd

def get_text_sentiment(words):
    count = float(len(words))
    return {
        "pandas": sum("pandas" in word for word in words) / count,
        "excitement": sum("!" in word for word in words) / count,
        "twitter": sum("birthday" in word or "10" in word for word in words) / count,
    }

def obtain_tweets(data, metadata):
    return (
        pd.DataFrame([
            json.loads(l) for l in open("tweets.jsons")
        ]),
        {"source": "tweets.jsons"},
    )

def scrub_stopwords(data, metadata, col):
    return data[col].apply(lambda x: [x for x in x.lower().split() if len(x) > 3])

def classify_sentiment(data, metadata, col):
    return data[col].apply(get_text_sentiment)

def get_sentiment_by_language(data, metadata):
    def average_sentiment(rows):
        # DataFrame with columns ["pandas", "excitement", "twitter"]
        sentiments = pd.DataFrame.from_records(rows["sentiment"].values)
        # Returns a series:
        #     excitement    0.024415
        #     pandas        0.124067
        #     twitter       0.016040
        return sentiments.mean()
    return data, {
        "sentiment_by_language": data.groupby("lang").apply(average_sentiment),
    }

def run(steps):
    data = None
    metadata = {}
    for step in steps:
        func, _, target = step.partition(" -> ")
        func = func.replace("(", "(data, metadata, ")

        print "Running:", step

        res = eval(func, globals(), locals())
        if isinstance(res, tuple):
            new_data, new_metadata = res
        else:
            new_data = res
            new_metadata = {}

        if target:
            assert isinstance(new_data, pd.Series)
            new_data.name = target
            data[target] = new_data
        else:
            data = new_data
        metadata.update(new_metadata)

    print "Done!"
    print
    print "Final metadata:"
    for k, v in metadata.items():
        print k
        print "-" * len(k)
        print v
        print


run([
    "obtain_tweets()",
    "scrub_stopwords('text') -> words_no_stopwords",
    "classify_sentiment('words_no_stopwords') -> sentiment",
    "get_sentiment_by_language()",
])
