from models import Corpus, Document
import time
from pyspark.sql import SparkSession
import pickle
import sys


class Timer:
    def __init__(self):
        self._start = 0.0
        self._stop = 0.0

    def run_with_timer(self, op, op_args=None, label="operation"):
        if not op_args:
            op_args = []

        self.start()
        result = op(*op_args)
        self.stop()

        self.print_elapsed(label=label)
        return result

    def print_elapsed(self, label: str = "operation", file=sys.stdout):
        print(f"Elapsed time for {label}: {self.get_elapsed():0.4f} seconds", file=file)

    def get_elapsed(self) -> float:
        return self._stop - self._start

    def start(self) -> None:
        self._start = time.time()

    def stop(self) -> None:
        self._stop = time.time()


spark = SparkSession.builder.getOrCreate()

# Read JSON data into a DataFrame
json_data = spark.read.option("multiline", "true").json(
    "gs://dataproc-staging-us-west1-1054165745548-ex76tnob/IR-From-Real-Data/data/final_data.json")

# Collect the DataFrame as a list of rows
rows = json_data.collect()

# Create a list of Document objects
corpus_documents = [Document(None, row.asDict()) for row in rows]

# Now you have a list of Document objects, and you can proceed with the rest of your code
timer = Timer()
corpus = timer.run_with_timer(
    Corpus, [corpus_documents, 1],
    label="corpus instantiation (includes TF-IDF matrix)"
)

# Save the corpus to a pickle file
with open("gs://dataproc-staging-us-west1-1054165745548-ex76tnob/IR-From-Real-Data/data/my_corpus", 'wb') as file:
    # Serialize and write an object (e.g., a Python dictionary) to the file
    pickle.dump(corpus, file)
