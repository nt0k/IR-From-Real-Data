import unittest

from nltk import PorterStemmer


from prototype import *
from src.models import *


class TestVector(unittest.TestCase):

    def test_norm_empty_vector(self):
        vec = Vector()
        self.assertEqual(vec.norm(), 0.0, "Expected norm of an empty vector to be 0.0")

    def test_norm_vector(self):
        vec = Vector([1, 2, 3, 4, 5])
        self.assertAlmostEquals(vec.norm(), compute_euclidean_norm(vec), delta=1e-9)

    def test_dot_product_empty_vectors(self):
        vec1 = Vector()
        vec2 = Vector()
        self.assertEqual(vec1.dot(vec2), 0.0, "Expected dot product of two empty vectors to be 0.0")

    def test_dot_product(self):
        vec1 = Vector([1, 2, 3, 4, 5])
        vec2 = Vector([6, 7, 8, 9, 10])
        self.assertAlmostEquals(vec1.dot(vec2), compute_dot_product(vec1, vec2), delta=1e-9)

    def test_cossim_empty_vectors(self):
        vec1 = Vector()
        vec2 = Vector()
        self.assertEqual(vec1.cossim(vec2), 0.0, "Expected cosine similarity of two empty vectors to be 0.0")

    def test_cossim(self):
        vec1 = Vector([1, 2, 3, 4, 5])
        vec2 = Vector([6, 7, 8, 9, 10])
        self.assertAlmostEquals(vec1.cossim(vec2), compute_cosine_similarity(vec1, vec2), delta=1e-9)

    def test_dot_product_with_non_vector(self):
        vec = Vector([1, 2, 3])
        non_vec = [1, 2, 3]
        with self.assertRaises(ValueError):
            vec.dot(non_vec)

    def test_cossim_with_non_vector(self):
        vec = Vector([1, 2, 3])
        non_vec = [1, 2, 3]
        with self.assertRaises(ValueError):
            vec.cossim(non_vec)


class TestDocument(unittest.TestCase):
    def test_filter_words(self):
        words = ["Hello", "My", "Name", "is", "Nathan"]
        # may or may not match case, will ask about case normalization
        exclude_words = {"my", "is"}
        stemmer = SnowballStemmer("english")

        doc = Document(words=words, processors=(exclude_words, stemmer))
        self.assertFalse("is" in doc.words, "Word was not filtered out of doc")
        self.assertTrue("nathan" in doc.words, "word not in set")

    def test_stem_words(self):
        words = ["Hello", "My", "Name", "is", "Nathan"]
        exclude_words = {"my", "is"}
        stemmer = SnowballStemmer("english")
        words_with_exclusions = {"Hello", "Name", "Nathan"}

        doc = Document(words=words, processors=(exclude_words, stemmer))
        expected_stemmed_words = [stemmer.stem(word) for word in words_with_exclusions]
        self.assertIn(expected_stemmed_words[0], doc.words, "Not equivalent to the snowball stem")
        self.assertIn(expected_stemmed_words[1], doc.words, "Not equivalent to the snowball stem")
        self.assertIn(expected_stemmed_words[2], doc.words, "Not equivalent to the snowball stem")


    def test_tf(self):
        words = ["Hello", "My", "Name", "is", "Nathan", "Nathan", "Nathan", "Hello", "a", "a"]
        exclude_words = {"is", "a"}
        stemmer = SnowballStemmer("english")

        doc = Document(words=words, processors=(exclude_words, stemmer))
        self.assertEqual(doc.tf("nathan"), 3, "Did not get correct TF")
        self.assertEqual(doc.tf("a"), 0, "Did not get correct TF")
        self.assertEqual(doc.tf("hello"), 2, "Did not get correct TF")


class TestCorpus(unittest.TestCase):
    def setUp(self):
        words = ["Hello", "My", "Name", "is", "Nathan", "test"]
        words2 = ["This", "is", "a", "test", "list", "of", "words"]
        words3 = ["This", "is", "a", "very", "sunny", "day", "it", "is", "very", "nice"]
        exclude_words = {"test"}
        stemmer = SnowballStemmer("english")

        doc1 = Document(title="doc1", words=words, processors=(exclude_words, stemmer))
        doc2 = Document(title="doc2", words=words2, processors=(exclude_words, stemmer))
        doc3 = Document(title="doc3", words=words3, processors=(exclude_words, stemmer))
        docList = [doc1, doc2, doc3]
        self.corp = Corpus(docList)

    def test_compute_terms(self):
        self.corp._compute_terms()
        terms = self.corp.terms
        self.assertTrue(terms)
        self.assertTrue("nathan" in terms)
        self.assertFalse("test" in terms)

    def test_compute_df(self):
        self.assertEqual(self.corp._compute_df("this"), 2, "Did not get correct doc frequency")
        self.assertEqual(self.corp._compute_df("test"), 0, "Did not get correct doc frequency")
        self.assertEqual(self.corp._compute_df("is"), 3, "Did not get correct doc frequency")

    def test_compute_dfs(self):
        dict1 = self.corp._compute_dfs()
        self.assertEqual(dict1["veri"], 1, "Did not compute dfs correctly")
        self.assertEqual(dict1["is"], 3, "Did not compute dfs correctly")
        self.assertEqual(dict1["this"], 2, "Did not compute dfs correctly")

    def test_compute_tf_idf(self):
        score = self.corp._compute_tf_idf("is", None, 2)
        actualScore = compute_tf_idf(2, 3, 3)
        print("Actual Score: " + str(actualScore))
        self.assertEqual(score, actualScore, "Score did not match proto calculation")

    def test_compute_tf_idf_vector(self):
        actualScore = compute_tf_idf(2, 3, 3)
        vec = Vector(actualScore)
        self.assertEqual(self.corp.compute_tf_idf_vector(None, 2), vec, "Vectors did not match")

    def test_compute_matrix(self):
        self.assertTrue(self.corp._compute_tf_idf_matrix(), "Matrix returned false when it should be true")


if __name__ == '__main__':
    unittest.main()
