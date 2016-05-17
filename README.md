# kudospy
Python script for retrieving Kudos info from OJS

# usage

- setup a virtualenv and install requirements.txt (you're welcome to install them globally if you don't use virtualenv but this may cause issues_
- copy and/or rename example_settings.py as settings.py
- complete the settings using your own mysql variables
- run ```python main.py```

kudospy uses dict cursor, so results are returned as a {'key': 'value'} pair for easy use.
