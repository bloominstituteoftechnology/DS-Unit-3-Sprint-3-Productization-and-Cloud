This file contains basic instructions for replacing Basilica with SpaCy within the twitoff app. This starts by assuming you already have an, essentially complete, implementation of twitoff build using Basilica.

-------------------------------------

First, install spacy and a pretrained model.

```
>pipenv uninstall basilica
>pipenv install spacy
>pipenv install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.5/en_core_web_sm-2.2.5.tar.gz
```

Note that I'm using the small model since it's fast to download (11 MB). There's also medium (en_core_web_md-2.2.5, 91 MB) and large (en_core_web_lg-2.2.5, 789 MB), which are more accurate. Note that the large model is too large to be put on Heroku, but the medium model can still be used.

-------------------------------------

In `twitter.py`, remove the basilica import and import the following;

```
import spacy
import en_core_web_sm
```

Delete the line defining `BASILICA = ...`, and replace it with

```
nlp = en_core_web_sm.load()
```

Instead of defining `embedding = BASILICA...`, define it as 

```
embedding = nlp(tweet.full_text).vector
```

-------------------------------------

In `predict.py`, instead of importing `BASILICA`, import `nlp` from `.twitter`.

Instead of defining `tweet_embedding = BASILICA...`, define it as

```
tweet_embedding = nlp(tweet_text).vector
```

-------------------------------------

The app should work at this point without further modification. It will not be as accurate, but it will give you results, and you can try the larger models if you want. Since additional calls to an external API don't need to be made, adding users is much faster.

If you had Basilica working before, you'll need to reset your SQL database to flush out the old embeddings which are not compatible with our new model.

In principal, this same procedure with only slight variation should work for any word library with embeding models, such as gensim, mxnet, etc.
