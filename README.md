# RandEmailAlias_v3.0-beta

Generate an email with random first and last name alias. Also create random email using a base alias. Generate 10 emails using the base alias. Override random alias with a timestamp or company name. Load and save alias history as a .csv file.

Windows app no longer runs via system tool bar. This function was dropped for code refactor, it will return in a future release.

## v3.0-beta New Features:
Alias Customization: Added Alias options to adjust alias output
- 'Timestamp Alias' will generate an email with a timestamp alias
- 'Company Alias' will generate an email with a company name alilas
- Default generation will output first and last name alias

Info Button: Added button to display general info about the app.

Minor UI and Bug Fixes

### Installation:
Navigate to the [lastest release in repo](https://github.com/JakeOrona/RandEmailAlias/releases), find the macOS or Windows .zip, download file and unzip. Launch application from unziped folder.

Mac users may receive warning when opening app for first time. This app is not signed with a developer certificate. I built the app using py2app. You may need to right click on application -> open. A warning error will display. Click ok to close warning. Right click on app again -> open. Receive a warning label again, this time clicking open should proceed into app. This should clear the warning. You may need to repeat this if you move the application or if you download a new version. (Im not paying apple yet. When I get to swift, I get to swift).

Windows users may need to run as administrator and click "more info" -> "run anyway" to bypass warning.

If you wish to run from source:

Download the .py for your OS from master branch. You may need adjust your PATH to include Python 3 and the .py file location.

See required libraries in source code.

Install the libraries using pip in terminal: pip install <library_name>

To run, download the source .py and use terminal to launch the python program:

python <filename.py> OR python3 <filename.py>