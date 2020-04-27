import os
import random
import string
import unittest
import numpy as np

from ..ml.cv import ind_to_class, topk, extract_feature

class ImageFeatureExtractionTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        self.file_path = os.path.join(os.getcwd(), 'application/static/images', 'test_image.jpg')

    # executed after each test
    def tearDown(self):
        pass

    ########################
    #### helper methods ####
    ########################

    ###############
    #### tests ####
    ###############

    def test_feature_extraction(self):
        features, output_label = extract_feature(self.file_path)
        self.assertEqual(features.dtype, np.float32)
        self.assertEqual(features.shape[0], 1280)
        self.assertEqual(isinstance(output_label, str), True)

    def test_label_to_class_conversion(self):
        indexes, original_classes = [1, 10, 100], \
                                    ['goldfish carassius auratus', \
                                     'brambling fringilla montifringilla',\
                                      'black swan cygnus atratus']
        classes = ind_to_class(indexes)
        self.assertEqual(isinstance(classes, list), True)
        self.assertEqual(len(classes), len(indexes))
        for current_class in classes:
            self.assertEqual(isinstance(current_class, str), True)
        self.assertEqual(classes, original_classes)


    def test_topk_predictions(self):
        predictions = 8;
        probabilities, classes = topk(self.file_path, predictions)
        self.assertEqual(isinstance(probabilities, list), True)
        self.assertEqual(len(probabilities), predictions)
        self.assertEqual(isinstance(classes, list), True)
        self.assertEqual(len(classes), predictions)
        for i in range(1, predictions):
            self.assertEqual(probabilities[i] <= probabilities[i - 1], True)


    def test_topk_max_classes(self):
        self.assertRaises(AssertionError, topk, self.file_path, -1)
        self.assertRaises(AssertionError, topk, self.file_path, 0)
        _, _ = topk(self.file_path, 1)
        _, _ = topk(self.file_path, 10)
        _, _ = topk(self.file_path, 1000)
        self.assertRaises(AssertionError, topk, self.file_path, 1001)

if __name__ == "__main__":
    unittest.main()
