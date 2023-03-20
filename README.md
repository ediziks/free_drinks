# free_drinks

Free drinks promotion estimator for vending machines. The estimator considers the config file provided including day(s) and time ranges to see if free drinks can be received at the current time. Although, the estimator suggests user to buy a drink if can't receive a free drink at the time as a part of tricky marketing strategy.

## Project Structure
```
.
├── README.md
├── free_drinks
│   ├── __init__.py
│   ├── config
│   └── main.py
├── tests
    ├── __init__.py
    └── tests.py
├── .gitignore
├── poetry.lock
└── pyproject.toml
```

## How to Use?

First, clone the repository and change directory to repo folder. Afterwards, create the dependenci
```bash
git clone https://github.com/ediziks/free_drinks.git
cd free_drinks
poetry install
```
Then set the `config` file provided under `free_drinks` folder with a sample `config_string` in it. Afterwards, free drinks estimation can be run to see if you could get a free drink in the current time. To do so;
```bash
poetry run python free_drinks/main.py
```
Indeed, the estimator script can be tested with the current test file provided. To run the tests;
```bash
poetry run python tests/tests.py
```

## Assumptions Made
- Poetry is used as the dependency manager since a production ready code is requested. It is more effective to manage environment, packages, project settings while making it easier to build and ship the code at the same time.
- Considered that time ranges will be from start-time until the end-time (not including exact ending-time) due to making it easy for the user to configure. (e.g. Mon: 2200-2400 would have fallen into Tuesday 00:00 as well which would be less likely to desire when setting the config)
- Multi time range for the same day is allowed (such as Fri: 1000-1200 Fri: 1400-1600) thinking that the user would most probably like to set two different promotions for the same day, instead of fixing the first time range with the coming ones.
- Config string is requested from a separate config file unlike asking a user input or leaving as a string variable within the code, since it's mentioned that "Time intervals are configured by using a string that the machine owner can set in config." in the project description.
