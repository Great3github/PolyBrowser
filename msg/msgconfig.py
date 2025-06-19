# title, msg
openBrowserConfirmation = ["", "Are you sure you want to start the browser?"]
# error msgs
class ErrorMsg():
    defaultError = "An internal error occurred while performing this command."
    invalidParamError = "One or more parameters entered in the brower configuration file are incorrect or have been removed."
    def importErrorMsg(e:Exception):
        return f"An error occurred while attempting to install or import necessary Python libraries. Check your internet connection and retry later.\nFull details: {str(e)}"
    siteBlockedError = ["Error", "This website is not allowed!"]
# button text
class ButtonText():
    homeButton = "Home"
    backButton = "Back"
    forwardButton = "Forward"
    refreshButton = "Refresh"