import argparse
import json
import pickle
import time
import sys
from src.models import Corpus, Document


from src.helper_functions import fetch_video_info

__author__ = "Nathan Kirk"
__credits__ = ["Nathan Kirk"]
__license__ = "GPL-3.0 license"
__email__ = "nkirk@westmont.edu"


def main() -> None:
    pars = setup_argument_parser()
    args = pars.parse_args()
    timer = Timer()

    try:
        with open(args.pickle_file_path, "rb") as pickle_file:
            corpus = timer.run_with_timer(pickle.load, [pickle_file],
                                          label="corpus load from pickle")
    except FileNotFoundError:
        with open("../data/final_data.json", "r") as file:
            final_data = json.load(file)
            corpus_documents = []
            for video in final_data:
                videoDict = Document(None, video)
                corpus_documents.append(videoDict)
        corpus = timer.run_with_timer(Corpus, [corpus_documents, args.num_threads, args.debug],
                                      label="corpus instantiation (includes TF-IDF matrix)")
        with open(args.pickle_file_path, "wb") as pickle_file:
            pickle.dump(corpus, pickle_file)

    keep_querying(corpus, 10)


def setup_argument_parser() -> argparse.ArgumentParser:
    pars = argparse.ArgumentParser(prog="python3 -m vectorspace.vector_space_runner")
    pars.add_argument("num_threads", type=int,
                      help="required integer indicating how many threads to utilize")
    pars.add_argument("pickle_file_path", type=str,
                      help="required string containing the path to a pickle (data) file")
    pars.add_argument("-d", "--debug", action="store_true",
                      help="flag to enable printing debug statements to console output")
    return pars


def keep_querying(corpus: Corpus, num_results: int) -> None:
    again_response = 'y'

    while again_response == 'y':
        raw_query = input("Your query? ")
        # puts the users query in the tags part of the doc
        query_document = Document("query", {"title": "", "description": "", "channel": "", "tags": [raw_query]})
        query_vector = corpus.compute_tf_idf_vector(query_document)

        query_result = {}
        for title, doc_vector in corpus.tf_idf.items():
            query_result[title] = doc_vector.cossim(query_vector)

        display_query_result(raw_query, query_result, corpus, num_results)
        again_response = input("Again (y/N)? ").lower()


def display_query_result(query: str, query_result: dict, corpus: Corpus, num_results) -> None:
    if num_results > len(corpus):
        num_results = len(corpus)

    sorted_result = sorted([(title, score) for title, score in query_result.items()],
                           key=lambda item: item[1], reverse=True)

    print(f"\nFor query : {query}")
    for i in range(num_results):
        title, score = sorted_result[i]
        print(f"Result {i + 1:02d} : [{score:0.6f}] {title}")
    print()


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


if __name__ == '__main__':
    main()