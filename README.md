# Make My Day: Planner
Check your upcoming day in a given google calendar and fill it up from the command line

## Project status

Work in progress...

### Inspiration
I was reading [Deep Work](https://www.amazon.com/Cal-Newport/e/B001IGNR0U) (a book by Cal Newport). He stresses that in order to stay away for shallow and unproductive work it is important to plan your day in advance. The idea is to give yourself a reason to not prioritize low-prio work. The plans you make should *NOT*
- discourage incidentals: It happens, we should get used to it. Its work not a hermitage.
- make you rigid: When your day is disrupted, it should be easy to re-plan your day at the earliest and in the most seamless manner.

On the 2nd point this project seeks to make life easier. The author suggests
that we should keep and update a paper based plan that is easy to cross out and replan.
If you are reading this, I hope this can be a better solution than pen and paper.


# How to get the client ready

* Install the python client for google and oauth
  * Anaconda users : `conda install --channel “conda-forge” --file requirements.txt`
  * Normal pip users : `pip install -r requirements.txt`
* Intialize and create a secrets json
  * Create project in https://console.developers.google.com/
  * Enable the calendar API in `Library`
  * Go to the `Credentials` and make a oauth client ID (gives the option to download in the form of json
  * Download and name it `client_secret.json`
  * an example of this file is present in the root as `example_client_secret.json`
* Run the `create_credentials.py` to create a pickle file that will be used for further runs of the day planner.
  * Once the pickle file `calendar_access_credential.p` is created it will skip the credential creation.

  NOTE: Please run on python versions 3.7 or higher. I have tested the application to the best of my abilities in Ubuntu/Manjaro based systems. Your mileage may vary. Please log an issue if you ecounter bugs or an inability to run the application