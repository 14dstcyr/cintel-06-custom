# cintel-06-custom
# Objectives
 - This module gives you a chance to add a unique interactive app to your online portfolio. 

 - You should have already created a project repo named cintel-06-custom with 4 files: 

    -- README.md
    -- .gitignore
    -- requirements.txt
    -- app.py (OR dashboard/app.py if working locally and deploying to GitHub pages - see more below).
      -- If you decide to try the local development, you'll be able to deploy your live date site using GitHub Pages. To make it easy to build our app from a folder and export the app into the docs folder (for Pages), please move your app.py file into a folder. I named my folder "dashboard", so I have a dashboard/app.py file and no app.py in the root folder. This is a more common organization for Python projects. 

### You may develop your app in the browser (recommended if you have NOT had 44-608) or develop your app on your machine locally (recommended if you have had 44-608 and/or prior practice with project virtual environments). 

### Your app.py or dashboard/app.py file should have the following sections:

  - imports (at the top)
  - define a reactive calc to fake new data points and/or filter a data frame
  - define the Shiny Express UI
### The overall page options
  - A sidebar
  - The main section with ui cards, value boxes, and space for grids and charts
  - Your app should have a data source and sketched out the basic functionality before you begin.

## Before Beginning
If working in the browser, open the playground to the plotly example at: https://shinylive.io/py/examples/#plotly

Paste in the contents of your app.py as stored in your GitHub project repo cintel-06-custom.

If working in locally, follow the recommended steps to create, activate, and install your requirements into your local project virtual environment. Remember to activate the environment rerun your app when you open a new terminal window. 

Customize your requirements.txt
PyShiny Playground already includes most of the packages you're likely to use. Please do not add these packages to a requirements.txt running in the Playground - but include them in your requirements.txt that you would use for local development. 

Implement Your Custom App
Create your interactive input. Define the reactive function to update based on user input and / or a regular interval. Display interesting outputs based on the interaction or interval. Include a data table or grid and at least one chart. 

