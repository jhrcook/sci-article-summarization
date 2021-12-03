# Summarizing scientific articles

**Comparing the ability of various summarizing ML/AI methods on scientific articles. (work in progress)**

**Check out examples of summarizing the paper ["The origins and genetic interactions of *KRAS* mutations are allele- and tissue-specific"](https://www.nature.com/articles/s41467-021-22125-z) in the [examples](./examples/) directory.**

Or you can compare the results of the different summary methods using the Streamlit web app: [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/jhcook/sci-article-summarization/master/app.py)

The purpose of this project is that I wanted to play around with various AI amd ML summarization methods.
Therefore, I have created a system by which a scientific article is downloaded, parsed, and fed through various summarization models under different configurations.
I chose to use scientific articles as a medium because I thought it would present an interesting, novel, and diverse set of test-cases.
Also, there are standard practices in scientific articles that makes scoring the summary's accuracy easy such as the Abstract and Results sub-section titles.

At the moment, I have a system for parsing *Nature Communication* articles from their webpage and summarizing the paper with the three methods listed below.
My next step is to create a structured method for saving the results for easy comparison.
I will run multiple articles through the methods with various parameters for the models.
I may also standardize the system/API for getting a parsed article so that I can create parsing systems for multiple journals (though this is a low priority).

[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.2.0-FF4B4B.svg?style=flat&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![pytorch](https://img.shields.io/badge/PyTorch-1.10.0-EE4C2C.svg?style=flat&logo=pytorch)](https://pytorch.org) <br>
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![pydocstyle](https://img.shields.io/badge/pydocstyle-enabled-AD4CD3)](http://www.pydocstyle.org/en/stable/)

## Entrypoints

There are various entrypoints available as CLI commands to the article parsing and summarization functions available in the [`summarize.py`](summarize.py) script.

### Summarizing a single scientific article

Here is an example of using the CLI to summarize a single article.

```bash
./summarize.py summarize "https://www.nature.com/articles/s41467-021-22125-z" "TEXTRANK"
#> 'The origins and genetic interactions of KRAS mutations are allele- and tissue-specific'
#>   summarization method: TEXTRANK
#> ========================================================================================
#>
#> Introduction
#> ------------
#> Importantly, the activating alleles found in KRAS vary ...
#> ...
```

There are some other options for this command that you can peruse using

```bash
./summarize.py summarize --help
```

### Generate examples

I made a specific command to generate the example summarizations of my paper ["The origins and genetic interactions of *KRAS* mutations are allele- and tissue-specific"](https://www.nature.com/articles/s41467-021-22125-z).
There examples are available in the [examples](./examples/) directory.
The following command runs the paper through each summarization method with some specific configurations.

```bash
./summarize.py make-examples
```

### Run the summarization pipeline for all URLs and configurations (work-in-progress)

This is still a work-in-progress, but running this command will run a pipeline that summarizes many URLs with different summarization model configurations.
The output will be saved as pickle files so that they can be re-read into Python and displayed in an interactive application for easier comparisons.

```bash
./summarize.py summarize-all
```

### Parse article

This command just parses an article and is useful for checking if an article's webpage is processed properly.

```bash
./summarize.py parse-article "https://www.nature.com/articles/s41467-021-22125-z"
```

## Streamlit app

This project has a web application built with [Streamlit](https://streamlit.io) to make comparing two different summaries easier.
It it available online, but you can also launch the Streamlit app locally using the following command:

```bash
streamlit run app.py
```

## Setup

Because of the all the ML/AI libraries required for this project, I used [conda](https://docs.conda.io) to manage dependencies.
The environment was created using the following steps (they are a bit wonky because of some requirements for running on Streamlit's platform).

```bash
conda create --prefix ./.venv python=3.9.7
conda activate ./.venv
conda env update --prefix ./.venv --file environment.yml
```

You need an API key to use OpenAI.
This can be created by creating an account [here](https://openai.com), logging in, and going to "Personal/View API Keys".
Make a file called ".env" and add your API key as the name `OPENAI_API_KEY`.
It should look something like this:

```text
OPENAI_API_KEY="your-key-here"
```

While ".env" is in the ".gitignore", it is worth double-checking that this file is not being tracked by git.

---

## To-Do

- break down the Results section into sub-sections - it will make it easier to read the summary.
- look into different options from HuggingFace (more info [here](https://huggingface.co/transformers/task_summary.html#summarization))
  - and other parameters for the HuggingFace models
- system for:
  - different model configurations
  - multiple article URLs
  - structured output for later display and comparison results

## ML/AI methods

- the PageRank algorithm on text [`textrank`](https://github.com/summanlp/textrank)
- HuggingFace's [`BART` model](https://huggingface.co/transformers/task_summary.html#summarization)
- OpenAI's [`GPT-3`](https://beta.openai.com/docs/introduction) text completion

## Model parameters

The models all have various parameters for tuning how the model behaves and the output.
Below are the descriptions for the various parameters I have included in my experimentation.

### Textrank

### BART

### GPT-3

https://beta.openai.com/docs/api-reference/completions/create
