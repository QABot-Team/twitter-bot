from allennlp.models.archival import load_archive
from allennlp.service.predictors import Predictor

# a mapping from model `type` to the default Predictor for that type
predictors = {
        'srl': 'semantic-role-labeling',
        'decomposable_attention': 'textual-entailment',
        'bidaf': 'machine-comprehension',
        'simple_tagger': 'sentence-tagger',
        'crf_tagger': 'sentence-tagger',
        'coref': 'coreference-resolution'
}

archive = load_archive("https://s3-us-west-2.amazonaws.com/allennlp/models/bidaf-model-2017.09.15-charpad.tar.gz")

model_type = archive.config.get("model").get("type")

if model_type not in predictors:
    raise ValueError("no known predictor for model type {}".format(model_type))


predictor = Predictor.from_archive(archive, predictors[model_type])

passage = "A reusable launch system (RLS, or reusable launch vehicle, RLV) is a launch system which is capable " \
          "of launching a payload into space more than once. This contrasts with expendable launch systems, where " \
          "each launch vehicle is launched once and then discarded. No completely reusable orbital launch system has " \
          "ever been created. Two partially reusable launch systems were developed, the Space Shuttle and Falcon 9. " \
          "The Space Shuttle was partially reusable: the orbiter (which included the Space Shuttle main engines and " \
          "the Orbital Maneuvering System engines), and the two solid rocket boosters were reused after several " \
          "months of refitting work for each launch. The external tank was discarded after each flight."
question = "How many partially reusable launch systems were developed?"

res = predictor.predict_json({"passage": passage, "question": question})
print(res['best_span_str'])
