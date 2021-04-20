from nltk import pos_tag, RegexpParser, word_tokenize

vp = r"""
    VP: {<PRP\$><NN><NNS>}
        {<PRP>?<RBS>?<JJ>?<VBP>?<DT>?<JJ>?<NN><IN><PRP\$><NN>}
    """

np = r"""
    NP: {<NN>+}
        {<PRP>?<VBD>?<VBG|IN>?<DT>?<JJ>*<NN>+}
"""


