
## What went well (in the context of working on the assignment) today?

Frankly, not much. It was a big slog and I felt like I was missing some 'glue' to fit together the pieces of my flask app. What was positive is that I broadly understand the concepts that we're working towards:

-flask is a web framework for our python module that can support extentsions to allow us to interact wtih databases, libaries and APIs

-a models.py module defines our database structures and how they relate to each other

-an app.py module executes functions and routes them to our web addresses, it imports functionality from our other modules

-a twitter.py module handles our twitter thin client interface. It defines functions that communicate our needs to twitter and then handles twitter's output so it can be passed into our SQL database

-finally we have a predict module. This is our machine learning implementation and uses bascilica embedings (generated from each tweet) as the data to train our model

In general, I think I comprehend the structure of our project, but the complexity of all these interacting systems leaves me wondering where to even start asking questions at times.

## What was particularly interesting or surprising about the topic(s) today?

I think that this exercise in describing the highlevel implementation of what we're doing is probably the most enjoyable part. Also, working collaboratively on bug fixing is very rewarding and fulfills some social/cooperative needs.

What's truly shocking is just how much tech it takes to deploy any app and the giants who have developed Flask, Horoku, etc and upon whose shoulders we stand.

## What was the most challenging part of the work today, and why?

I hadn't quite gotten use to the idea of debugging for more than 5 hours straight, trying to pass errors to the FLASK shell log so I could figure out where my code was dying. I ended up staying up almost the entire night, iterating on bugs and it was weirdly satisfying. Probably because I had been intimidated by the complexity of the problem but it turned out ok.
