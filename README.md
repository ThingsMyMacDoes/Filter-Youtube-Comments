How it works

Step 1


You need to get your own Youtube Data API key and insert it in the Dataloader script.


Run the script and it will ask for a video url


It will fetch associated comments and download them to a json file

Step 2

Run the BadWordsFinder script by using streamlit run BadWordsFinder.py

It will open a browser window

In this browser window you can upload the json file with comments you've generated in step 1 and the text file with your keywords

Load and Display comments will then do exactly that. You will also get a count of found keywords/keyphrases
and 2 html files you can download

The API key will let you fetch about 10k comments and replies on a daily basis for free.






