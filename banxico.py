import requests
import datetime
from typing import List
import yaml

class BanxicoApi:

    def __init__(self, config):
        self.config = self._load_yaml_file(config)
        self.token = self.config["api"]["token"]
        self.base = self.config["api"]["_base"]

    def _load_yaml_file(self, file_path):
        with open(file_path, 'r') as file:
            try:
                data = yaml.safe_load(file)
                return data
            except yaml.YAMLError as exc:
                print(f"Error reading YAML file: {exc}")
                return None

    def _call(self, endpoint):
        url = f"{self.base}/{endpoint}?token={self.token}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['bmx']['series']
        
    def _combine_metadata_with_data(self, data, metadata):
            dict1 = {item['idSerie']: item for item in data}
            for item in metadata:
                dict1[item['idSerie']].update(item)
            return list(dict1.values())
        
    def _get(self, series: List[str], oportuno = False, metadata = False):
        series_ids = ",".join(series)
        if oportuno:
            endpoint = f"{series_ids}/datos/oportuno"
        else:
            endpoint = f"{series_ids}/datos"
        data = self._call(endpoint)
        if metadata:
            metadata = self._call(series_ids)
            merged_list = self._combine_metadata_with_data(data, metadata)
            return merged_list
        return data

    def _get_range(self, series: List[str], start_date:datetime, end_date:datetime, metadata = False):
        series_ids = ",".join(series)
        if start_date > end_date:
            raise ValueError("Start date must be before end date")
        endpoint = f"{series_ids}/datos/{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}"
        data = self._call(endpoint)
        if metadata:
            metadata = self._call(series_ids)
            merged_list = self._combine_metadata_with_data(data, metadata)
            for item in merged_list:
                item["fechaInicio"] = start_date.strftime('%Y-%m-%d')
                item["fechaFin"] = end_date.strftime('%Y-%m-%d')
            return merged_list
        return data

    def get(self, series: List[str], start_date:datetime = None, end_date:datetime = None, oportuno = False, metadata = False):
        if (start_date is None) != (end_date is None):
            raise ValueError("Either both dates must be None or both must be not None")
        if start_date and end_date:
            return self._get_range(series, start_date, end_date, metadata)
        return self._get(series, oportuno, metadata)
    
    def getMetadata(self, series: List[str]):
        series_ids = ",".join(series)
        return self._call(series_ids)
    
    def getByCode(self, code):
        code_series = self.config["codes"][code]
        return self.get(code_series)
    
    
