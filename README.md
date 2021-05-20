# Project AskLepios Backend


## Install

Install Python dependencies (run virtual environment before - recommended)

```bash
pip install -r requirements.txt
```

## Usage

Set up virtual environemnt:

```bash python -m venv venv```

Start the virtual environment server:

```bash
cd server cd venv cd scripts activate```

Start the uvicorn server:

```bash
uvicorn lepios_project_backend.asgi:app
```

To enable hot reload, use the `--reload` option.

The server will run at `http://localhost:8000`.


## Getting help

To get further help on Bocadillo CLI:

- Use `$ bocadillo --help`.
- Read the [Bocadillo CLI documentation][repo].

To get help on Bocadillo, visit the [Bocadillo docs site](https://bocadilloproject.github.io).

If you like Bocadillo, feel free to show some love by [starring the repo](https://github.com/bocadilloproject/bocadillo). ❣️
