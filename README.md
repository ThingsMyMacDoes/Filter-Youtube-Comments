How it works

Step 1

create a .txt file with all the words or phrases you want to find in the comments. Put each word or phrase on a new line.


You need to get your own Youtube Data API key and insert it in the Dataloader script. If necessary consult YT on how to get an API key

The API key will let you fetch about 10k comments and replies on a daily basis for free.


Run the script and it will ask for a video url


It will fetch associated comments and download them to a json file

The json file with all the comments and the txt file with your keywords will be used in the next step

Step 2

Run the BadWordsFinder script by using streamlit run BadWordsFinder.py

It will open a browser window

In this browser window you can upload the json file with comments you've generated in step 1 and the text file with your keywords

Load and Display comments will then do exactly that. You will also get a count of found keywords/keyphrases
and 2 html files you can download








