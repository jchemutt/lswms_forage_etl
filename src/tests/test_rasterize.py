import unittest
import sys,os
import pandas as pd
import geopandas as gpd
import rasterio
import numpy as np
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from codes.rasterize import *

class TestRasterize(unittest.TestCase):

    def setUp(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.outputs_path = os.path.join(self.project_root, 'outputs')
        self.temp_raster_files=os.path.join(self.outputs_path, 'temp_raster_files')
        self.test_results= os.path.join(self.outputs_path,  "test_results.csv")
        self.test_raster= os.path.join(self.outputs_path,  "test_raster.tif")
        # Create a temporary results CSV file with test data
        self.test_data = pd.DataFrame({'lon': [39.41, 39.445, 39.492], 'lat': [3.271, 3.261, 3.254], 'date': [20240101,20240101,20240101],'year': [2024, 2024, 2024],
                                       'month': [1, 1, 1], 'day': [1, 1, 1],
                                        'biom': [1.79040380360565, 1.78896823494216, 1.79198639098456]})
        self.test_data.to_csv(self.test_results, index=False)

    

    def test_process_data(self):
        # Test if process_data function correctly converts CSV to GeoDataFrame
        processed_data = process_data(self.test_results)
        self.assertIsInstance(processed_data, gpd.GeoDataFrame)
        self.assertEqual(len(processed_data), 3)  # Assuming 3 rows of test data

    def test_create_raster_files(self):
        # Test if create_raster_files function correctly generates raster files
        raster = rasterio.open(self.test_raster, 'w', driver='GTiff', height=300, width=260, count=1,dtype='float32', crs='EPSG:4326', transform=rasterio.transform.from_origin(36, 15, 0.05, 0.05))
        processed_data = process_data(self.test_results)
        create_raster_files(processed_data, self.temp_raster_files, raster)
        raster.close()
        raster_files = os.listdir(self.temp_raster_files)
        self.assertEqual(len(raster_files), 1)  # Assuming only one raster file is created
        self.assertTrue(raster_files[0].startswith('biomass_20240101'))  # Assuming the file name follows a certain pattern
    
    def tearDown(self):
        # Clean up temporary files after each test
        os.remove(self.test_results)
        for file in os.listdir(self.temp_raster_files):
            os.remove(os.path.join(self.temp_raster_files, file))

if __name__ == '__main__':
    unittest.main()
