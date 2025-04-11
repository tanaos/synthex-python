# Synthex

[![Static Badge](https://img.shields.io/pypi/v/synthex?logo=pypi&logoColor=%23fff&color=%23006dad)](https://pypi.org/project/synthex/)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/tanaos/synthex/python-publish.yml?logo=github&logoColor=%23fff&label=CI)](https://github.com/tanaos/synthex-python/actions/workflows/python-publish.yml)


Synthex is a Python library for high-quality, large-scale synthetic dataset generation 📊🧪, powered by the [Tanaos Platform](https://tanaos.com) API.

## Installation

You only need acces to this source code if you want to modify the package. We do welcome contributions. To find out how you can contribute, see [CONTRIBUTING.md](CONTRIBUTING.md).

If you just want to **use** the package, simply run

```bash
pip install --upgrade synthex
```

## Requirements

- Python >= 3.7

## Usage

The library needs to be configured with an API Key. You can generate an API Key by creating a free account on the [Tanaos Platform](https://platform.tanaos.com) and navigating to the [API Keys](https://platform.tanaos.com/api-keys) section. 

Once you have your API Key, you can pass it to the library in one of two ways:

1. Create a `.env` file **in your project's root directory** and add a `API_KEY` entry:

    ```bash
    API_KEY="dKri286...264Yb9rH"
    ```

    The API Key will be automatically picked up when you instantate the `Synthex` class.

    ```python
    from synthex import Synthex

    client = Synthex()
    ```

2. Explicitly pass the `api_key` parameter when instantiating the `Synthex` class:

    ```python
    from synthex import Synthex

    client = Synthex(api_key="dKri286...264Yb9rH")
    ```

In all code snippets below, we will assume that you have a `.env` file in your project's root directory with your `API_KEY` written on it.

### Creating a new dataset

To create a new dataset, use `Synthex.jobs.generate_data()`

```python
from synthex import Synthex

client = Synthex()

client.jobs.generate_data(
    schema_definition, # Your output dataset's schema
    examples, # A few sample output datapoints
    requirements, # The requirements for your data generation job
    output_path # The path for the generated dataset
    number_of_samples, # How many datapoints you want in your output dataset
    output_type, # The format of your output dataset
)
```

where the parameters are as follows:

- `schema_definition`: A dictionary which specifies the output dataset's schema. It must have the following format:
    ```python
    {
        "<name_of_column_1>": {"type": "<datatype_of_column_1>"},
        "<name_of_column_2>": {"type": "<datatype_of_column_2>"},
        ...
        "<name_of_column_n>": {"type": "<datatype_of_column_n>"}
    }
    ```

    the possible values of `"type"` are `"string"`, `"integer"` and `"float"`.

    For instance, if you want to generate a of real estate listings dataset, a possible value for the `schema_definition` parameter could be the following:

    ```python
    schema_definition = {
        "surface": {"type": "float"},
        "number_of_rooms": {"type": "integer"},
        "construction_year": {"type": "integer"},
        "city": {"type": "string"},
        "market_price": {"type": "float"}
    },
    ```

- `examples`: A list of dictionaries, which specifies a few (3 to 5 are enough) sample datapoints that will help the data generation model understand what the output data should look like. They must have the same schema as the one specified in the `schema_definition` parameter, or an exception will be raised.

    In the "real estate listing dataset" scenario, a possible value for the `examples` parameter could be the following:

    ```python
    examples = [
        {
            "surface": 104.00,
            "number_of_rooms": 3,
            "construction_year": 1985,
            "city": "Nashville",
            "market_price": 218000.00
        },
        {
            "surface": 98.00,
            "number_of_rooms": 2,
            "construction_year": 1999,
            "city": "Springfield",
            "market_price": 177000.00
        },
        {
            "surface": 52.00,
            "number_of_rooms": 1,
            "construction_year": 2014,
            "city": "Denver",
            "market_price": 230000.00
        },
    ]
    ```

- `requirements`: a list of strings, where each string specifies a requirement or constraint for the job. It can be an empty list if no specific requirements are present.

    In the "real estate listings dataset" scenario, a possible value for the `requirements` parameter is the following:

    ```python
    requirements = [
        "The 'market price' field should be realistic and should depend on the characteristics of the property.",
        "The 'city' field should specify cities in the USA, and the USA only"
    ]
    ```

- `output_path`: a string which specifies the path where the output dataset will be generated. It does not need to contain a file name, as this will be added automatically if one is not provided. If `output_path` does contain a file name, its extension must be consistent with the `output_type` parameter. If this is the case, the provided `output_path` is used in its entirety. Otherwise, the provided extension is replaced with one that is consistent with `output_type`.

- `number_of_samples`: an integer which specifies the number of datapoints that the model should generate. Keep in mind that the maximum number of datapoints you can generate with a single job depends on whether you are on a free or paid plan.

- `output_type`: a string which specifies the format of the output dataset. Only `"csv"` (meaning a .csv file will be generated) is supported at this time, but we will soon add more options.