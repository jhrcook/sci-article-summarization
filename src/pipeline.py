"""Functions for the pipeline of summarizations."""


from src.summarize_utils import SummarizationConfiguration, SummarizationMethod


def get_urls() -> set[str]:
    """Get the URLs for the articles to summarize.

    Returns:
        set[str]: Set of URLs.
    """
    return {
        "https://www.nature.com/articles/s41467-021-22125-z",  # KRAS alleles
        "https://www.nature.com/articles/s41467-021-26703-z",  # DL Alzheimer’s
        "https://www.nature.com/articles/s41467-021-26788-6",  # CRISPR selection
        "https://www.nature.com/articles/s41467-020-15552-x",  # cardio Myc
    }


def _textrank_pipeline_configs() -> list[SummarizationConfiguration]:
    _ratios = [0.01, 0.05, 0.1, 0.2]
    return [
        SummarizationConfiguration(
            method=SummarizationMethod.TEXTRANK, config_kwargs={"ratio": ratio}
        )
        for ratio in _ratios
    ]


def _bart_pipeline_configs() -> list[SummarizationConfiguration]:
    _min_ratios = [0.05, 0.1, 0.2]
    _max_ratios = [0.1, 0.2, 0.3]
    return [
        SummarizationConfiguration(
            method=SummarizationMethod.BART,
            config_kwargs={"min_ratio": min_ratio, "max_ratio": max_ratio},
        )
        for min_ratio, max_ratio in zip(_min_ratios, _max_ratios)
    ]


def generate_configurations() -> list[SummarizationConfiguration]:
    """Get configurations to use for the summarizations.

    Returns:
        list[SummarizationConfiguration]: List of summarization configurations.
    """
    configs: list[SummarizationConfiguration] = []
    configs += _textrank_pipeline_configs()
    configs += _bart_pipeline_configs()
    return configs
