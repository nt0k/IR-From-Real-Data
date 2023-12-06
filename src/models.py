__author__ = "Nathan Kirk"
__credits__ = ["Nathan Kirk"]
__license__ = "GPL-3.0 license"
__email__ = "nkirk@westmont.edu"

from math import sqrt, log10
import sys
from typing import Callable, Iterable
import concurrent.futures
from nltk.stem import StemmerI


class Document:
    """A document is a dictionary representing a single youtube video. An example is below:
    {
    "title": "They just resurrected Call of Duty...",
    "channel": "jackfrags",
    "description": "Call of Duty and Microsoft have just made ALL of the old COD games playable on Xbox, even the Xbox 360 games, pretty cool! Let's play some MW2 for some hot nostalgia. Leave a LIKE and a comment, thanks for watching.",
    "tags": [
      "cod",
      "cod xbox",
      "xbox 360 cod",
      "cod xbox 360",
      "mw2",
      "modern warfare 2"
    ],
    "publication_date": "2023-07-24T20:54:40Z"
  }"""
    _iid = 0

    def __init__(self, title: str = None, content: dict = None):
        Document._iid += 1
        self._iid = Document._iid
        self._title = title if title else content["title"]
        self._description = content["description"]
        self._channel = content["channel"]
        self._tags = content["tags"]

    @property
    def words(self):
        """Get all words from the document content."""
        return self._title.split() + self._description.split() + self._channel.split() + [tag for tag in self._tags]

    @property
    def title(self):
        return self._title

    @property
    def iid(self):
        return self._iid

    def tf(self, term: str) -> int:
        """Compute and return the term frequency of the `term` passed in among `_words`."""
        return self.words.count(term)


class Vector:
    """Takes in a list of floats as a representation of a document as a vector in space"""

    def __init__(self, elements: list[float] | None = None):
        self._vec = elements if elements else []

    def __getitem__(self, index: int) -> float:
        if index < 0 or index >= len(self._vec):
            raise IndexError(f"Index out of range: {index}")
        else:
            return self._vec[index]

    def __setitem__(self, index: int, element: float) -> None:
        if 0 <= index < len(self._vec):
            self._vec[index] = element
        else:
            raise IndexError(f"Index out of range: {index}")

    def __eq__(self, other) -> bool:
        if other is self:
            return True
        elif other is None or not isinstance(other, Vector):
            return False
        else:
            return self._vec == other.vec

    def __str__(self) -> str:
        return str(self._vec)

    @property
    def vec(self):
        return self._vec

    @staticmethod
    def _get_cannot_compute_msg(computation: str, instance: object):
        return f"Cannot compute {computation} with an instance that is not a DocumentVector: {instance}"

    def norm(self) -> float:
        """Euclidean norm of the vector."""
        sum1 = 0
        for x in self:
            sum1 += x * x

        return sqrt(sum1)

    def dot(self, other: object) -> float:
        """Dot product of `self` and `other` vectors."""
        if not isinstance(other, Vector):
            raise ValueError(self._get_cannot_compute_msg("dot product", other))
        else:
            sum1 = 0
            for float1, float2 in zip(self, other):
                sum1 += float1 * float2
            return sum1

    def cossim(self, other: object) -> float:
        """Cosine similarity of `self` and `other` vectors."""
        if not isinstance(other, Vector):
            raise ValueError(self._get_cannot_compute_msg("cosine similarity", other))
        else:
            denominator = (self.norm() * other.norm())
            if denominator:
                return self.dot(other) / denominator
            else:
                return 0.0

    def boolean_intersect(self, other: object) -> list[tuple[float, float]]:
        """Returns a list of tuples of elements where both `self` and `other` had nonzero values."""
        if not isinstance(other, Vector):
            raise ValueError(self._get_cannot_compute_msg("boolean intersection", other))
        else:
            return [(e1, e2) for e1, e2 in zip(self._vec, other._vec) if e1 and e2]


class Corpus:
    """A corpus is a list of documents. This class does the TF-IDF calculations and makes the matrix of vector values"""

    def __init__(self, documents: list[Document], threads=1, debug=False):
        self._docs: list[Document] = documents

        # Setting flags.
        self._threads: int = threads
        self._debug: bool = debug

        # Bulk of the processing (and runtime) occurs here.
        self._terms = self._compute_terms()
        self._dfs = self._compute_dfs()
        self._tf_idf = self._compute_tf_idf_matrix()

    def __getitem__(self, index) -> Document:
        if 0 <= index < len(self._docs):
            return self._docs[index]
        else:
            raise IndexError(f"Index out of range: {index}")

    def __iter__(self):
        return iter(self._docs)

    def __len__(self):
        return len(self._docs)

    @property
    def docs(self):
        return self._docs

    @property
    def terms(self):
        return self._terms

    @property
    def dfs(self):
        return self._dfs

    @property
    def tf_idf(self):
        return self._tf_idf

    def _compute_terms(self) -> dict[str, int]:
        """Computes and returns the terms (unique, stemmed, and filtered words) of the corpus."""
        list1 = []
        for doc in self._docs:
            for word in doc.words:
                if word not in list1:
                    list1.append(word)
        return self._build_index_dict(list1)

    def _compute_df(self, term) -> int:
        """Computes and returns the document frequency of the `term` in the context of this corpus (`self`)."""
        if self._debug:
            print(f"Started working on DF for '{term}'")
            sys.stdout.flush()

        def check_membership(t: str, doc: Document) -> bool:
            """An efficient method to check if the term `t` occurs in a list of words `doc`."""
            return t in doc.words

        return sum([1 if check_membership(term, doc) else 0 for doc in self._docs])

    def _compute_dfs(self) -> dict[str, int]:
        """Computes document frequencies for each term in this corpus and returns a dictionary of {term: df}s."""
        if self._threads > 1:
            return Corpus._compute_dict_multithread(self._threads, self._compute_df, self._terms.keys())
        else:
            return {t: self._compute_df(t) for t in self.terms}

    def _compute_tf_idf(self, term, doc=None, index=None):
        """Computes and returns the TF-IDF score for the term and a given document.

        An arbitrary document may be passed in directly (`doc`) or be passed as an `index` within the corpus.

        """
        dfs = self._dfs
        doc = self._get_doc(doc, index)
        # HINT: Use `dfs` declared above to eliminate redundant calculations.
        tf = 0
        for word in doc.words:
            if word == term:
                tf += 1
        # How to account for a term being in all documents (1 + df is > self.len so get a neg number)
        return (log10(1 + tf)) * log10((self.__len__() / (1 + dfs[term])))

    def compute_tf_idf_vector(self, doc=None, index=None) -> Vector:
        """Computes and returns the TF-IDF vector for the given document.

        An arbitrary document may be passed in directly (`doc`) or be passed as an `index` within the corpus.

        """
        doc = self._get_doc(doc, index)
        floats = []
        for term in self.terms:
            floats.append(self._compute_tf_idf(term, doc))
        return Vector(floats)

    def _compute_tf_idf_matrix(self) -> dict[str, Vector]:
        """Computes and returns the TF-IDF matrix for the whole corpus.

        The TF-IDF matrix is a dictionary of {document title: TF-IDF vector for the document}.

        """

        def tf_idf(document):
            if self._debug:
                print(f"Processing '{document.title}'")
                sys.stdout.flush()
            vector = self.compute_tf_idf_vector(doc=document)
            return vector

        matrix = {}
        if self._threads > 1:
            matrix = Corpus._compute_dict_multithread(self._threads, tf_idf, self._docs,
                                                      lambda d: d, lambda d: d.title)
        else:
            for doc in self._docs:
                matrix[doc.title] = tf_idf(doc)

                if self._debug:
                    print(f"Done with doc {doc.title}")
        return matrix

    def _get_doc(self, document, index):
        """A helper function to None-guard the `document` argument and fetch documents per `index` argument."""
        if document is not None and index is None:
            return document
        elif index is not None and document is None:
            if 0 <= index < len(self):
                return self._docs[index]
            else:
                raise IndexError(f"Index out of range: {index}")

        elif document is None and index is None:
            raise ValueError("Either document or index is required")
        else:
            raise ValueError("Either document or index must be passed in, not both")

    @staticmethod
    def _compute_dict_multithread(num_threads: int, op: Callable, iterable: Iterable,
                                  op_arg_func=lambda x: x, key_arg_func=lambda x: x) -> dict:
        """Experimental generic multithreading dispatcher and collector to parallelize dictionary construction.

        Args:
            num_threads (int): maximum number of threads (workers) to utilize.
            op: (Callable): operation (function or method) to execute.
            iterable: (Iterable): iterable to call the `op` on each item.
            op_arg_func: a function that maps an item of the `iterable` to an argument for the `op`.
            key_arg_func: a function that maps an item of the `iterable` to the key to use in the resulting dict.

        Returns:
            A dictionary of {key_arg_func(an item of `iterable`): op(p_arg_func(an item of `iterable`))}.

        """
        result = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            future_to_keys = {executor.submit(op, op_arg_func(item)): key_arg_func(item) for item in iterable}
            for future in concurrent.futures.as_completed(future_to_keys):
                key = future_to_keys[future]
                try:
                    result[key] = future.result()
                except Exception as e:
                    print(f"Key '{key}' generated exception:", e, file=sys.stderr)
        return result

    @staticmethod
    def _build_index_dict(lst: list) -> dict:
        """Given a list, returns a dictionary of {item from list: index of item}."""
        return {item: index for (index, item) in enumerate(lst)}
