import requests
from typing import List

class BanxicoApi:

    def __init__(self, token):
        self.token = token
        self.base = "https://www.banxico.org.mx/SieAPIRest/service/v1/series"
        self.code_mappings = {
            "CF120": [
                "SF43695",
                "SF43702",
                "SF43696"
            ],
            "CF104": [
                "SF43671",
                "SF43672",
                "SF43673",
                "SF43671",
                "SF43658",
                "SF43686",
                "SF43687",
                "SF63315",
                "SF43688",
                "SF43689",
                "SF43968",
                "SF43690",
                "SF43691",
                "SF43692",
                "SF43693",
                "SF43657",
                "SF267992",
                "SF44081",
                "SF65183",
                "SF4403"
            ],
            "CF106": [
                "SF43703",
                "SF43704",
                "SF43705",
                "SF43706",
                "SF43707",
                "SF43708",
                "SF43709",
                "SF43710",
                "SF43711"
            ],
            "CF894": [
                "SF336106",
                "SF336107",
                "SF336108",
                "SF336109",
                "SF336110",
                "SF336111",
                "SF336112",
                "SF336113",
                "SF336114",
                "SF336338"
            ],
            "CF169": [
                "SF38460",
                "SF38461",
                "SF38462",
                "SF38463",
                "SF38464",
                "SF38465",
                "SF38466"
            ]
        }

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

    def _get_range(self, series: List[str], start_date:str, end_date:str, metadata = False):
        series_ids = ",".join(series)
        if start_date > end_date:
            raise ValueError("Start date must be before end date")
        endpoint = f"{series_ids}/datos/{start_date}/{end_date}"
        data = self._call(endpoint)
        if metadata:
            metadata = self._call(series_ids)
            merged_list = self._combine_metadata_with_data(data, metadata)
            for item in merged_list:
                item["fechaInicio"] = start_date
                item["fechaFin"] = end_date
            return merged_list
        return data

    def get(self, series: List[str], start_date:str = None, end_date:str = None, oportuno = False, metadata = False):
        if (start_date is None) != (end_date is None):
            raise ValueError("Either both dates must be None or both must be not None")
        if start_date and end_date:
            return self._get_range(series, start_date, end_date, metadata)
        return self._get(series, oportuno, metadata)
    
    def getMetadata(self, series: List[str]):
        series_ids = ",".join(series)
        return self._call(series_ids)
    
    def getByCode(self, code):
        code_series = self.code_mappings[code]
        return self.get(code_series)
    
    
