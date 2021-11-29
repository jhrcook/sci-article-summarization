# Summarizing scientific articles

**Comparing the ability of various summarizing ML/AI methods on scientific articles. (work in progress)**

The goal of this project is to play around with various AI amd ML summarization methods.
I chose to use scientific articles as a medium because I thought it would present an interesting, novel, and diverse set of test-cases.
At the moment, I have a system for parsing *Nature Communication* articles from their webpage and summarizing the paper with the three methods listed below.
My next step is to create a structured method for saving the results for easy comparison.
I will run multiple articles through the methods with various parameters for the models.
I may also standardize the system/API for getting a parsed article so that I can create parsing systems for multiple journals (though this is a low priority).

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
