# medibot
Serverless Machine Learning Classifier SlackBot

Medibot is a Slack bot running serverlessly in AWS via Chalice. Questions are passed to a machine learning classifier running in sci-kit learn. The SVM model is loaded on demand from S3 allowing it to be updated without redeploying or bloating the bot.
 
![Screen shot from Slack](https://4.bp.blogspot.com/-736_Xo3gl5Y/W52Jiik2egI/AAAAAAABWuk/AI10Tearcdcp_28wg8Rfg6j0A6d29Vf_ACLcBGAs/s1600/Bot-smudged.png "Screen shot from Slack")

More info here: http://jeremyblythe.blogspot.com/
