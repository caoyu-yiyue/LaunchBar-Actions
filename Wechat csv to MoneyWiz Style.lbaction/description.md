# Wechat Red Envelope Record to MoneywWiz Style

This action accepts a CSV file from Wechat Pay record and finds all trades about red envelope (微信红包), export a file consistent with money MoneyWiz import style.

The script dependencies or settings:

1. Python module `Pandas`.
2. You can change the account name for the Wechat pay in the script.
3. If LaunchBar can't find your custom Python version even if you have changed the `$PATH` variable, you could modify the Shebang line to your Python path. run `where python` to find your Python.
