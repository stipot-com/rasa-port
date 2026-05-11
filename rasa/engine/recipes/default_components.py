from __future__ import annotations

from importlib import import_module
from typing import Dict, Text


DEFAULT_COMPONENTS: Dict[Text, Text] = {
    # Message classifiers
    "DIETClassifier": "rasa.nlu.classifiers.diet_classifier:DIETClassifier",
    "FallbackClassifier": "rasa.nlu.classifiers.fallback_classifier:FallbackClassifier",
    "KeywordIntentClassifier": "rasa.nlu.classifiers.keyword_intent_classifier:KeywordIntentClassifier",
    "MitieIntentClassifier": "rasa.nlu.classifiers.mitie_intent_classifier:MitieIntentClassifier",
    "SklearnIntentClassifier": "rasa.nlu.classifiers.sklearn_intent_classifier:SklearnIntentClassifier",
    "LogisticRegressionClassifier": "rasa.nlu.classifiers.logistic_regression_classifier:LogisticRegressionClassifier",
    # Response selectors
    "ResponseSelector": "rasa.nlu.selectors.response_selector:ResponseSelector",
    # Message entity extractors
    "CRFEntityExtractor": "rasa.nlu.extractors.crf_entity_extractor:CRFEntityExtractor",
    "EntitySynonymMapper": "rasa.nlu.extractors.entity_synonyms:EntitySynonymMapper",
    "MitieEntityExtractor": "rasa.nlu.extractors.mitie_entity_extractor:MitieEntityExtractor",
    "SpacyEntityExtractor": "rasa.nlu.extractors.spacy_entity_extractor:SpacyEntityExtractor",
    "RegexEntityExtractor": "rasa.nlu.extractors.regex_entity_extractor:RegexEntityExtractor",
    # Message featurizers
    "LexicalSyntacticFeaturizer": "rasa.nlu.featurizers.sparse_featurizer.lexical_syntactic_featurizer:LexicalSyntacticFeaturizer",
    "MitieFeaturizer": "rasa.nlu.featurizers.dense_featurizer.mitie_featurizer:MitieFeaturizer",
    "SpacyFeaturizer": "rasa.nlu.featurizers.dense_featurizer.spacy_featurizer:SpacyFeaturizer",
    "CountVectorsFeaturizer": "rasa.nlu.featurizers.sparse_featurizer.count_vectors_featurizer:CountVectorsFeaturizer",
    "LanguageModelFeaturizer": "rasa.nlu.featurizers.dense_featurizer.lm_featurizer:LanguageModelFeaturizer",
    "RegexFeaturizer": "rasa.nlu.featurizers.sparse_featurizer.regex_featurizer:RegexFeaturizer",
    # Tokenizers
    "JiebaTokenizer": "rasa.nlu.tokenizers.jieba_tokenizer:JiebaTokenizer",
    "MitieTokenizer": "rasa.nlu.tokenizers.mitie_tokenizer:MitieTokenizer",
    "SpacyTokenizer": "rasa.nlu.tokenizers.spacy_tokenizer:SpacyTokenizer",
    "WhitespaceTokenizer": "rasa.nlu.tokenizers.whitespace_tokenizer:WhitespaceTokenizer",
    # Language model providers
    "MitieNLP": "rasa.nlu.utils.mitie_utils:MitieNLP",
    "SpacyNLP": "rasa.nlu.utils.spacy_utils:SpacyNLP",
}


def import_default_component(name: Text) -> None:
    """Import one default component so its recipe decorator can register it."""
    target = DEFAULT_COMPONENTS.get(name)
    if not target:
        return
    module_name, _, _class_name = target.partition(":")
    import_module(module_name)
