# Summarizing scientific articles

Compare the ability of various summarizing ML/AI methods on scientific articles.

Make a pipeline to download the text of an article from a website (web-scrape) and feed into various summarizaiton methods.
Then compare to the abstract of the paper (not given to the machine).

ML/AI methods:

- `textrank` (PageRank algorithm)
- `HuggingFace` has some models
- OpenAI `GPT-3`  text completion

HuggingFace summarization pipeline: https://huggingface.co/transformers/task_summary.html#summarization

OpenAI examples (search "summ"): https://beta.openai.com/examples

textrank from 'summa' library: https://github.com/summanlp/textrank
