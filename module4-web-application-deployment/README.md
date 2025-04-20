# Web Application Deployment

You have a cool web application going - but it's not really on the *web* yet.
Linking to a GitHub repo is your portfolio is nice, but linking to a live
working application is better as it has a broader audience. Anybody, whether
they are technical or not, can click and enjoy!

## Learning Objectives

- Deploy a basic (single-server) web application to common cloud services
- Securely connect a deployed web application to a relational database back-end

## Before Lecture

Sign up for a free [Render.com](https://render.com/) account - you shouldn't
need to provide credit card information. Then read their [getting started on
Render.com with
Python](https://render.com/docs/deploy-python) 
guide, and optionally follow along (the example app is Django, but the process
will be similar with Flask).

Also, do your best to get your app in a good working (or at least stable) state,
so you can follow along with deploying in lecture.

## Live Lecture Task

See [guided-project.md](https://github.com/LambdaSchool/DS-Unit-3-Sprint-3-Productization-and-Cloud/blob/master/module4-web-application-deployment/guided-project.md)

## Assignment

See [assignment.md](https://github.com/LambdaSchool/DS-Unit-3-Sprint-3-Productization-and-Cloud/blob/master/module4-web-application-deployment/assignment.md)

## Resources and Stretch Goals

- If you really run into issues with Render.com, you can check out
  [ngrok](https://ngrok.com/) as a way to set up a tunnel that lets you run the
  server locally but serve it to the world - but it isn't really a replacement
  for cloud deployment, as it's only up when you're running it on your computer
- `render run` is super powerful - you can use it to run code on your hosted
  application, including shell commands to access your application
- Push the app! See if you can break it, and if you do, if you can fix it
- Try to see how the app scales - free Render.com service will have some limitations
- Incorporate [Redis](https://redislabs.com/) as a cache to mitigate performance
  issues
- An alternative to Render.com for hosting Flask is
  [PythonAnywhere](https://www.pythonanywhere.com/)
  - In some ways it is simpler, and it can even persist a SQLite database file
  - But, it doesn't provide PostgreSQL (you can use
    [ElephantSQL](https://www.elephantsql.com/) instead) and is less widely used
  - Overall: stick with Render.com first, but check out PythonAnywhere if you'd like
- Another alternative (in the other direction) is [AWS](https://aws.amazon.com/)
  - Render.com is nice for prototyping and fairly standard applications (it
    abstracts away a lot of the details, so as long as you fit their use case it
    "just works")
  - But larger more complicated services are often deployed via more powerful
    services like AWS, Google Cloud, and Microsoft Azure
  - Again: Render.com first, and then explore alternatives
- Add some basic permissions or possibly even an account system, so not everyone
  can just add users, pull Tweets, or reset data
