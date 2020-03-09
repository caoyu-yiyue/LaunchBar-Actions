# A LaunchBar Action to Download Videos Using you-get

This is an action for quickly download videos using [you-get](https://github.com/soimort/you-get). All the videos will be saved to ~/Downloads/, and no caption or damaku.

It can accept an url or some text containing av numbers for BiliBili.com. If the video is from BiliBili, the file will be renamed to 'avNumber videoTitle.flv'.

The script dependencies or setting:

1. Python modules `you-get` and `validator_collection`.
2. If LaunchBar can't find your custom Python version even if you have changed the `$PATH` variable, you could modify the Shebang line to your own Python path. run `where python` to find your Python.
