By using these two scripts you can search comments on YT videos for words or phrases of your choice. These can be 'bad' words or 'good' words or anything in between. This can be useful for identifying spammers but also to find other useful information. As an example you could create a list of brands or game titles and then find any mentions of those brands or game titles in he comments.

Here's a short video on what it looks like : https://youtu.be/_yJt7siSMEk?si=eE6H4GUrf4ZHQuzz

How it works

Step 1

create a .txt file with all the words or phrases you want to find in the comments. Put each word or phrase on a new line.


You need to get your own Youtube Data API key and insert it in the Dataloader script. If necessary consult YT on how to get an API key

The API key will let you fetch about 10k comments and replies on a daily basis for free.


Run the Dataloader script and it will ask for a video url


It will fetch associated comments and download them to a json file

The json file with all the comments and the txt file with your keywords will be used in the next step

Step 2

Run the BadWordsFinder script by using streamlit run BadWordsFinder.py

It will open a browser window

In this browser window you can upload the json file with comments you've generated in step 1 and the text file with your keywords

Load and Display comments will then do exactly that. You will also get a count of found keywords/keyphrases
and 2 html files you can download

The image below shows the output of the BadWordsFinder script



![20240802_11h09m37s_grim](https://github.com/user-attachments/assets/e9cff923-c3e5-434b-8f9c-bfdf84741da8)







