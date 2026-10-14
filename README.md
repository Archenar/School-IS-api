# Information Systems: from UML and JSON to a running API

**Running example: Student / Course / Enrolment.** Continue the school model from our modelling class: Alice (1001), Noah (1002), IS101 and DB101. All records are fictional. A Course represents one offering in this small example; an enrolment is identified by the **student/course pair**.

**Optional worked reference.** For the first classroom exercise, start with [Student-API-Basic](https://github.com/DevidMontecchiari/Student-API-Basic): one entity, three routes and one application file. This reference extends the same school model to courses, enrolments, Python objects and optional registration. Explore the parts that help explain your own model; the additional files are not an assignment checklist.

Start by running the application and inspecting its responses. Then follow the learning path to understand and adapt it. This repository is a small worked reference with activities alongside the code. There is one implementation; you do not need to switch branches or compare two running servers. Activities support the assignment; they do not introduce additional assessment requirements.

## Start the application

### In your own GitHub Codespace

Open this repository on GitHub and choose **Code → Codespaces → Create codespace on main** (or its displayed default branch). This creates your own environment; it does not join the lecturer's Codespace. To keep and push your changes, work from your own fork if you have no write access to the teaching repository.

Wait for the container setup to finish. It installs Python dependencies automatically. Open a terminal in the repository root, then enter just this command:

```sh
python run.py
```

Open **Ports → 8000 → Open in Browser**, then append `/docs` to the forwarded address. Keep the port private for this exercise. Leave the terminal running. **Ctrl+C** stops the application.

No local Python or Docker installation is needed for this browser route. Codespaces access depends on your GitHub account and any institutional restrictions.

### On your computer

Use Python 3.12 or newer and a terminal in this folder. Create an environment once:

```sh
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or in macOS/Linux:

```sh
source .venv/bin/activate
```

Then:

```sh
python -m pip install -r requirements.txt
python run.py
```

Open <http://127.0.0.1:8000/docs>. If PowerShell prevents activation, use `.\.venv\Scripts\python.exe` instead of `python` for the install and run commands. In VS Code select this environment with **Python: Select Interpreter**.

`requirements.txt` lists just two direct dependencies: **FastAPI**, the web framework, and **Uvicorn**, the server that runs it. Installing these also installs the libraries they depend on. Python already includes `json` and `pathlib`. `requirements-test.txt` is only for running the optional checks.

## How the examples fit together

| Example | Use it for |
| --- | --- |
| [Student-API-Basic](https://github.com/DevidMontecchiari/Student-API-Basic) | Your first IS exercise and a small starting point to adapt. |
| This school reference | Follow Student / Course / Enrolment, inspect Python objects, and explore the optional registration example. |
| [Station Bar API](https://github.com/DevidMontecchiari/Station-bar-api) | Optional further examples from Web-based Applications. It will grow over the semester, including more backend and data-layer material. |

The examples have different teaching scopes. Use the IS assignment description to decide what your project needs; the larger repositories do not add requirements.

## Learning path

[1. Run and observe](docs/01-run-and-observe.md) → [2. A small FastAPI example](docs/02-first-api.md) → [3. Trace a request](docs/03-trace-a-request.md) → [4. UML, objects and JSON](docs/04-models-and-objects.md) → [5. Change and adapt](docs/05-change-and-adapt.md)

| Step | What you will do | Open these files |
| --- | --- | --- |
| 1 | Run the school API; compare success and missing-record responses | `main.py`, `/docs` in your browser |
| 2 | Explain a route, function, parameter and return value | `tutorial.py` |
| 3 | Follow one request from the URL to a JSON file and back | `main.py`, `storage.py`, `data/` |
| 4 | Instantiate the classes from our model and call `enrol(course)` | `domain.py`, `objects_demo.py` |
| 5 | Change one record, verify it, then adapt a read operation to your project | Your own copy; optional `registration_demo.py` |

**Python rusty?** Keep the [Python reading guide](docs/python-reading-guide.md) beside the code. It explains the exact constructs used here, including indentation, dictionaries, loops, functions, classes and type hints. [Troubleshooting](docs/troubleshooting.md) covers common setup and runtime problems.

## Find your way around

```text
main.py                 HTTP routes: read all / read one
storage.py              load and save JSON files
data/                   fictional students, courses and enrolments
tutorial.py             small isolated introduction to FastAPI
domain.py               ordinary Student, Course and Enrolment classes
objects_demo.py         UML operation -> object -> JSON, without saving
registration_demo.py    optional command-line registration with checks and saving
run.py                  starts the development server
requirements.txt        the two direct runtime dependencies
docs/                   learning path and Python help
tests/                  automated behaviour checks
.devcontainer/          browser environment setup
```

Start by reading `main.py`, not the environment configuration. The API reads lists/dictionaries from JSON; it does not automatically turn them into domain-class instances. Step 4 makes that conversion explicit. The optional write demo is a command-line program, not an HTTP POST route. The API remains a read-only starting point.

## Boundaries and references

This example has no login or authorisation checks. Typing a student ID is a lookup, not proof of identity. JSON files here are local teaching storage, without database transactions or protection against concurrent writers. Use fictional records; deployment and a full database are separate topics.

The guide adapts the module's earlier *IS Demo – Details* and read-all/read-one demonstration to the current school model. Technical references: [FastAPI First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/), [path parameters](https://fastapi.tiangolo.com/tutorial/path-params/), [errors](https://fastapi.tiangolo.com/tutorial/handling-errors/), [Python classes](https://docs.python.org/3.14/tutorial/classes.html), [Python JSON](https://docs.python.org/3.14/library/json.html), [Codespaces port forwarding](https://docs.github.com/en/codespaces/developing-in-a-codespace/forwarding-ports-in-your-codespace).

Optional automated checks, from this folder:

```sh
python -m pip install -r requirements-test.txt
python -m unittest discover -s tests -v
```

**Begin → [1. Run and observe](docs/01-run-and-observe.md)**
