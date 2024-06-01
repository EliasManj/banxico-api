import unittest
import datetime
from banxico import BanxicoApi

class TestBanxicoApi(unittest.TestCase):
    def setUp(self):
        self.api = BanxicoApi("config.yaml")
    
    def _contains_ids(self, dict_list, target_ids):
        dict_ids = {d.get('idSerie') for d in dict_list}

        # Check if all target IDs are in the set of dictionary IDs
        return all(target_id in dict_ids for target_id in target_ids)

    def test_get_series(self):
        series =  ['SF43695','SF43702','SF43696']
        data = self.api.get(series)
        self.assertTrue(data, "The JSON response is empty")
        self.assertTrue(len(data) == len(series), "The JSON response does not contain all series")
        self.assertTrue(self._contains_ids(data, series), "The JSON response does not contain all series")

    def test_get_series_with_metadata(self):
        series =  ['SF43695','SF43702','SF43696']
        data = self.api.get(series, metadata=True)
        self.assertTrue(data, "The JSON response is empty")
        self.assertTrue(len(data) == len(series), "The JSON response does not contain all series")
        self.assertTrue(self._contains_ids(data, series), "The JSON response does not contain all series")
        for serie in data:
            self.assertIn('titulo', serie, "The JSON response does not contain metadata")
            self.assertIn('periodicidad', serie, "The JSON response does not contain metadata")
            self.assertIn('cifra', serie, "The JSON response does not contain metadata")
            self.assertIn('unidad', serie, "The JSON response does not contain metadata")

    def test_get_series_oportuno(self):
        series =  ['SF43695','SF43702','SF43696']
        data = self.api.get(series = series, oportuno=True)
        self.assertTrue(data, "The JSON response is empty")
        self.assertTrue(len(data) == len(series), "The JSON response does not contain all series")
        self.assertTrue(self._contains_ids(data, series), "The JSON response does not contain all series")
        for serie in data:
            self.assertTrue(len(serie['datos']) == 1, "The JSON response does not contain only one data point")

    def test_get_series_range(self):
        series =  ['SF43695','SF43702','SF43696']
        start_date = datetime.datetime(2021, 1, 1)
        end_date = datetime.datetime(2024, 2, 1)
        data = self.api.get(series = series, start_date=start_date, end_date=end_date)
        self.assertTrue(data, "The JSON response is empty")
        self.assertTrue(len(data) == len(series), "The JSON response does not contain all series")
        self.assertTrue(self._contains_ids(data, series), "The JSON response does not contain all series")
        for serie in data:
            for dato in serie['datos']:
                date = datetime.datetime.strptime(dato['fecha'], '%d/%m/%Y')
                self.assertTrue(start_date <= date <= end_date, "The JSON response contains data out of the range")


    def test_get_metadata(self):
        series =  ['SF43695','SF43702','SF43696']
        data = self.api.getMetadata(series)
        self.assertTrue(data, "The JSON response is empty")
        self.assertTrue(len(data) == len(series), "The JSON response does not contain all series")
        self.assertTrue(self._contains_ids(data, series), "The JSON response does not contain all series")

if __name__ == '__main__':
    unittest.main()
