# import spacy
#
# nlp = spacy.load("en_core_web_md")
# tokens = nlp("dog cat banana")
#
# for token in tokens:
#     print(token.text, token.has_vector)

import os
os.environ["HOME"] = "embeddings"
from embeddings import *
# g = GloveEmbedding('common_crawl_840', d_emb=300, show_progress=True)
# f = FastTextEmbedding()
k = KazumaCharEmbedding()
k.emb("Silveryustia")