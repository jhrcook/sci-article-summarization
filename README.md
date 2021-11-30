# Summarizing scientific articles

**Comparing the ability of various summarizing ML/AI methods on scientific articles. (work in progress)**

[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![pytorch](https://img.shields.io/badge/PyTorch-1.10.0-EE4C2C.svg?style=flat&logo=pytorch)](https://pytorch.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![pydocstyle](https://img.shields.io/badge/pydocstyle-enabled-AD4CD3)](http://www.pydocstyle.org/en/stable/)

The goal of this project is to play around with various AI amd ML summarization methods.
I chose to use scientific articles as a medium because I thought it would present an interesting, novel, and diverse set of test-cases.
At the moment, I have a system for parsing *Nature Communication* articles from their webpage and summarizing the paper with the three methods listed below.
My next step is to create a structured method for saving the results for easy comparison.
I will run multiple articles through the methods with various parameters for the models.
I may also standardize the system/API for getting a parsed article so that I can create parsing systems for multiple journals (though this is a low priority).

## Example uses

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

## To-Do

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
