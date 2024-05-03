# Lightweight GitHub Stats
Lightweight GitHub stats for your profile using python and GitHub actions. 

All you need to do is fork the repository, do some setup and its usable.

# Example with Light theme
![Example GitHub Stats in Light mode](https://i.imgur.com/JQnOXbX.png)

# Steps To Use
To use stats yourself, you'll need to do a little work:

1. Fork the Lightweight-GitHub-Stats repository.
2. Enable Actions in your new forked repo.
3. If needed, run the "Lightweight GitHub Stats" action once initially.
4. Once the action has run once, your should be able to access the GitHub page it creates. The url for this should be https://yourusernamehere.GitHub.io/Lightweight-GitHub-Stats/.
5. Take the provided img tag the page provides and add it to your profile (or anywhere really).
6. Celebrate (maybe?)

# Letting Stats Access Private Data
By default, stats will use your profile and public data. You can change who it gets data for inside of settings.py.

If you want to allow stats to access and display private data, you can provide it was an API key.
1. Go to your GitHub developer settings and create a new API key/token. It should have read repo access at the least.
2. In your forked repo, go to settings.
3. Navigate to "Secrets and variables" and click actions.
4. Create a new Repository secret with the key of "API_KEY" and the value of your newly created key.
5. Re-run the repos action and the data should update with your private data.

# Settings
By default if you provide it with an api key it will display everything it can. You can change this behaviour inside of settings.py.

Settings.py contains all the settings used by the program. Want to only display your username and stars? Set most of the variables to false. Wish to change the text size and spacing? Its in there.

It's fiddly and takes some trial and error but it works.

# Themes
Stats has a number of themes (and you can extend this) that you can display your stats with. Change them with the IMAGE_THEME setting in settings.py.

See Themes.py for the themes the program has but the best ones are:
1. light -> Models the stats off of GitHub's light mode.
2. dark -> The same but for dark mode.
3. transparent -> Tries for a middleground that has a transparent background.

# Other things
By default, the stats action is run once a week. Personally, I'm happy with that and I think its fair.

Running it often (such as every few minutes) could run into api limits and fair use issues that aren't worthwhile in my opinion.

However that can be changed easily. In the action file you can modify the cron parameters to change how often the stats are updated. 
In theory the lowest update time would be about 10 minutes, that being about the length of time that GitHub caches the image in your profiles readme before checking for an update.
