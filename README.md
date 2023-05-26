# RandEmailAlias_v2.4.4-beta

Generate an email with random alias. Also create random email using a base alias. Generate 10 emails using the base alias. Override random alias with a timestamp (YY-MM-DD-HH.MM.SS).

Windows app runs via system tool bar. User must right click and select open to launch instance of program. 
User can close window and toolbar icon instance runs in background. Right click and quit to close toolbar
System Toolbar only working on windows.

MacOS users will need to wait until solution is found to run in system tool bar. May require rewriting in swift...

## v2.4.4-beta New Features:
Alias History: Generated emails are saved with a timestamp. Click 'View Alias History' to view alias history.

- Aliases are saved in the following format: "Email | Timestamp: YY-MM-DD-HH.MM.SS"

- If email was generated via 'feeling lucky' button alias history will have "(FL)" flag

### v2.4.3 Misc Updates:
- Button click confirmation updated. Buttons now flash blue when clicked and valid output is generated.
- Updated copy to clipboard confirmation due to auto-copy. Copy confirmation message is clearer.
- Copy to Clipboard function checks for valid email to avoid copying error message.

### Installation:
Navigate to the [lastest release in repo](https://github.com/JakeOrona/RandEmailAlias/releases), find the macOS or Windows .zip, download file and unzip. Launch application from unziped folder.

Mac users may receive warning when opening app for first time. This app is not signed with a developer certificate. I built the app using py2app. You may need to right click on application -> open. A warning error will display. Click ok to close warning. Right click on app again -> open. Receive a warning label again, this time clicking open should proceed into app. This should clear the warning. You may need to repeat this if you move the application or if you download a new version. (Im not paying apple yet. When I get to swift, I get to swift).

Windows users may need to run as administrator and click "more info" -> "run anyway" to bypass warning.

If you wish to run from source:

Download the .py for your OS from master branch. You may need adjust your PATH to include Python 3 and the .py file location.

See required libraries in source code.

Install the libraries using pip in terminal: pip install <library_name>

To run, download the source .py and use terminal to launch the python program with the following command (you may need to move the file to correct directory/change directory/adjust your PATH to include Python 3 and the file location. (Google is your friend or ask me for help):

python <filename.py> OR python3 <filename.py>
