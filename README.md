# Synthex

![Static Badge](https://img.shields.io/pypi/v/synthex?logo=pypi&logoColor=%23fff&color=%23006dad&link=https%3A%2F%2Fpypi.org%2Fproject%2Fsynthex%2F)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/tanaos/synthex/python-publish.yml?logo=github&logoColor=%23fff&label=CI&link=https%3A%2F%2Fgithub.com%2Ftanaos%2Fsynthex-python%2Factions%2Fworkflows%2Fpython-publish.yml)


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
    number_of_samples, # How many datapoints you want in your output dataset
    output_type, # The format of your output dataset
    output_path # The path for the generated dataset
)
```


