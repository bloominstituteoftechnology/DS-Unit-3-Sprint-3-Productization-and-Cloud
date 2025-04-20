# Guided Project Walkthrough

We'll deploy the app! We'll step through all of the following:

- Creating the app on Render.com
- Adding Render.com as a git remote (Render.com deploys using git)
- Making sure we have an appropriate build configuration (tells Render.com the process to
  run when starting up our app)
- Setting environment variables (the Render.com equivalent of environment variables)

## Turning an existing folder into a git repository

If you didn't start your project out as a Git Repository there's a simple way to do this and get the commands that you need.

Go to GitHub.com, make sure you're logged in and create a new repository with the same name as the folder on your computer. It's not necessary that it be named the same as the folder on your computer, but I find that it makes things less confusing.

When you create the repository if you don't select any of the pre-defined options (besides making the repository public) you'll be presented with a list of commands that you can use to initialize your repository as a git repo and to push it to github for the first time. This list of commands includes setting GitHub as a "remote" for the repository which is the most important step. Setting the "remote" is what creates the connection between your local folder and the repository on GitHub.

### Make sure you don't push your `.env` file

Navigate to the project folder that you want to add to github from the command line and add check to see if you have a `.gitignore` file and make sure that file includes your `.env` file. You DO NOT want to push your `.env` file to GitHub on accident.

See if your repository has a `.gitignore` file

`ls -a`

If it doesn't create one and make sure to add `.env` as its own row in the `.gitignore`

After you've done this, you'rw ready to use the Git commands shown on the screen after you've created this new repository to push your repository up to Git. You can even just copy them all as one chunk and paste them into your command line tool.

![New GitHub Repository](/images/new-repo.png)

I was going to put a copy of the commands here, but I won't because the commands will be customized to your repository, so it's best to get them from GitHub directly.

## Pushing an existing repo to GitHub

If your app has already been created as a git repository or if you've made additional changes to your files since connecting it with GitHub, go ahead and make sure that the latest changes have been pushed to GitHub. From the command line run:

Tells us if any files or folders have been modified since we last pushed changes to GitHub

`git status`

Adds any new or changed files to the "git staging" (get's it ready to be committed.)

`git add .`

I like to run git status again just to see the colors of my files change, this lets me know that indeed everything has been added to staging. This command is not necessary and literally does nothing, but somehow it's comforting to me to see the colors change to know that I haven't missed something.

`git status`

Saves the current snapshot of our directory and packages it up as a "commit" that is ready to be pushed to GitHub. We'll always include a commit message along with our commit, that's what the `-m` flag stands for is "message." Inside of the parentheses leave a short note to future-you that summarizes the changes that you're making to the repository files with this commit.

`git commit -m "your commit message here"`

Send the changes across the wire to GitHub. If you have an old repository you might need to say `master` instead of `main`.

`git push origin main`

And that's it. You should now be able to see all of the updated files on GitHub!

## Making a new app on Render.com

If you haven't already. Sign up for an account at [Render.com](https://render.com). Once you have an account, create a new Web Service. Give this app a unique name for your project.

Once you have created the new web service, connect it to your GitHub repository. Once you do this you'll be prompted to connect Render.com to your GitHub account. Go ahead and follow the instructions as indicated to give Render.com permissions to access your account. Then select the specific repository that you want to link to this Render.com Web Service. Once you've linked the repository to the Render.com service, this will allow Render.com to grab all of the files in the GitHub repository and use them when launching the app. This has the benefit of making it very easy to update your app on Render.com. You simply need to push your changes to GitHub and then Render.com will automatically redeploy. It's a pretty slick system!

Once you've connected your app to GitHub, configure your build settings and click the "Create Web Service" button. This will start up the deployment process where you'll see Render.com installing the dependencies listed in your requirements file. When it's done it should give you a URL for your deployed app!

Go ahead and try and navigate to your deployed app once the build has completed. You may find that you get a screen saying you have an application error. That's ok! We'll work to debug what might be going on.

![Render.com Application Error](/images/application-error.png)

## Debugging application errors

To view the error logs for your app. Come back to Render.com and navigate to your web service dashboard. Click on the "Logs" tab to view the application logs.

![View Render.com Application Logs](/images/view-logs.png)

You might see a couple of telling messages in these logs.

1) You might see some messages about Twitter authentication failing. Hmmm... Why might that be?

2) If you navigate to your application or refresh the page on the Application Error screen you'll see new error messages in the logs.

One common issue is that Render.com might not know how to start your app. Unlike Heroku which uses a Procfile, Render.com uses a Start Command configuration.

From the Render.com dashboard, go to your web service settings and update the Start Command. For a Flask application, you might use something like:

`gunicorn twitoff:APP -t 120`

Next, we'll install a more deployment-friendly way of starting up our Flask web server. We'll install a tool called `gunicorn` and configure Render.com to use it to start our app. Please note: gunicorn does not work on Windows. Windows users should skip the installation.

`pipenv install gunicorn`

After gunicorn has finished installing, make sure to update your Start Command in the Render.com settings as shown above.

This tells Render.com to use `gunicorn` to start up our app and tells it where it can find the APP variable. We'll also give this a timeout of 120 seconds because our app may take a little while to startup. We don't want it to stop trying to startup simply because the instance isn't very powerful, so this timeout is extra generous to allow plenty of time for Render.com to try and launch the app before erring out with a "gateway timeout" message.

Once you've installed `gunicorn` and configured the Start Command, be sure to push your changes back to GitHub and Render.com will automatically redeploy the app.

## Setting up environment variables

When you redeploy the app, you may see new errors in the Render.com Logs. One thing that can trigger error messages is missing environment variables. Remember that we used our `.gitignore` to make sure that our `.env` file would never be pushed to GitHub? Well Render.com can't see the `.env` file so it doesn't have our Twitter API keys and it doesn't know where to find the database within our app.

Go ahead and add your environment variables to Render.com. You can add these under the "Environment" tab in your web service settings. The required env vars are as follows:

```
DATABASE_URL=sqlite:///db.sqlite3
NOT_TWITTER_URL=https://twitoff-be.onrender.com/
```

![Render.com Environment Variables](/images/config-vars.png)

After you've added those environment variables, Render.com will automatically redeploy your app.

## Creating the Database

Once you've deployed your app, navigate to its Render.com URL. If all has gone according to plan, you will see a different screen. If you see a screen that says `Internal Server Error`. That means that the app has at least launched! Now we're getting an error within our flask application. 

![Internal Server Error](/images/internal-server-error.png)

We'll always get this error the very first time we deploy our app because our database hasn't been created yet. Go ahead and navigate to the `/reset` route on your app and that should generate the sqlite3 database and your app should be working after that. (It will also work for any other users who come to it).

And that's it! You're app should now be up and running on Render.com!
