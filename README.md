## Overview

BanxicoApi is a Python class designed to interact with the Banxico (Banco de México) API. It allows users to fetch economic and financial series data, including metadata, and provides methods to handle data ranges and specific series codes.


## Usage

### Initialization

You need to initialize the BanxicoApi class with your API token:

```
from BanxicoApi import BanxicoApi

api_token = 'YOUR_API_TOKEN'
banxico_api = BanxicoApi(api_token)
```

### Fetching Series Data

You can fetch series data using the get method. This method allows for various parameters to customize the data retrieval.

**Basic Usage**

Fetch data for a list of series:

```
series = ['SF43718', 'SF46410']
data = banxico_api.get(series)
print(data)
```

**Fetching Data with Metadata**

To include metadata in the response:

```
data_with_metadata = banxico_api.get(series, metadata=True)
print(data_with_metadata)
```

**Fetching Opportuno Data**

To fetch the most recent data available:

```
opportuno_data = banxico_api.get(series, oportuno=True)
print(opportuno_data)
```

**Fetching Data for a Specific Date Range**

You can specify a date range to fetch data:

```
start_date = '2022-01-01'
end_date = '2022-12-31'
data_in_range = banxico_api.get(series, start_date=start_date, end_date=end_date)
print(data_in_range)
```

To include metadata with date range data:

```
data_in_range_with_metadata = banxico_api.get(series, start_date=start_date, end_date=end_date, metadata=True)
print(data_in_range_with_metadata)
```

**Fetching Metadata Only**

If you only need the metadata for a list of series:

```
metadata = banxico_api.getMetadata(series)
print(metadata)
```

**Fetching Data by Code instead of series ID**

If you have predefined codes mapped to series, you can fetch data by code:

```
code = 'CF120'
data_by_code = banxico_api.getByCode(code)
print(data_by_code)
```


## Methods Summary

`get(series: List[str], start_date: str = None, end_date: str = None, oportuno: bool = False, metadata: bool = False)` 
Fetches data for the specified series, optionally within a date range, and with metadata.

`getMetadata(series: List[str])` 
Fetches metadata for the specified series.