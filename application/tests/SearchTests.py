import os
import unittest
import numpy as np

from ..ml.cv import ind_to_class, topk, extract_feature
from ..routes.indexRoutes import distance, filter_items

class SearchTests(unittest.TestCase):

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

    def test_distance_function(self):
        features, output_label = extract_feature(self.file_path)
        self.assertEqual(distance([(features, features)]), 0)
        self.assertEqual(distance([(features, None)]), np.inf)

    def test_filter_items(self):
        items = filter_items(types=[])
        self.assertEqual(len(items), 0)



if __name__ == "__main__":
    unittest.main()
