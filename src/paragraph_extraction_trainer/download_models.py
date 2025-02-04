#from huggingface_hub import hf_hub_download
import hf_resources 
from importlib_resources import files # for reading files from the local_resources folder 

paragraph_extraction_model_path = files(hf_resources).joinpath('paragraph_extraction_model.model')

#paragraph_extraction_model_path = hf_hub_download(
#    repo_id="HURIDOCS/pdf-segmentation",
#    filename="paragraph_extraction_model.model",
#    revision="ffc4f1753ac1ca55981be06c29f1e73787e611b5",
#)

letter_corpus_path = files(hf_resources).joinpath('letter_corpus.txt')

#letter_corpus_path = hf_hub_download(
#    repo_id="HURIDOCS/pdf-segmentation", filename="letter_corpus.txt", revision="da00a69c8d6a84493712e819580c0148757f466c"
#)

toc_model_path = files(hf_resources).joinpath('TwoModelsV3SegmentsContext2Len.model')

#toc_model_path = hf_hub_download(
#    repo_id="HURIDOCS/pdf-segmentation",
#    filename="TwoModelsV3SegmentsContext2Len.model",
#    revision="d66b49062439d6283464edadd9428a186c553f64",
#)


