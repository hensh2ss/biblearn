# Web based resources for inspiration / data

https://christopherjayminson.medium.com/ai-meets-the-bible-e70febc38b47
https://cursor.pubpub.org/pub/hemenway-bible-interface/release/3
https://app.inferkit.com/demo
https://towardsdatascience.com/artificial-intelligence-genesis-literally-947c1935752d
https://docs.api.bible/
https://hackathon.bible/data/
http://www.crosswire.org/sword/modules/ModDisp.jsp?modType=Bibles

# Various SWORD Bible Versions
https://tgc-dk.gitlab.io/pysword/examples.html
http://www.crosswire.org/sword/modules/ModDisp.jsp?modType=Bibles


# Christopher Minson

Let's recreate this [blog](https://www.christopherminson.com/articles/aibible.html) from this [repo](https://github.com/cminson/embeddedbible)

## Build the model

### Quick corrections to get the model

before you run textinput,py, load this

```
import nltk
nltk.download('punkt')
```

change the size parameter in ```gensim.models.Word2Vec``` from ```size``` to ```vector_size```

fixed typos in lines 56 and 58 by adding wv from model.mostsimilar to model.wv.mostsimilar



