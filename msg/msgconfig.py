import sys, os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path.removesuffix("msg"))

import browser_config
CURRENTVERSION="1.3"
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
class InternalPageContent():
    aboutText = ["About This Program", f"Poly Browser version {CURRENTVERSION}\nDeveloped by Matt Fichter with the help of AI"]
    buttonsEnabled = {
        "Back": browser_config.Config.showBackButton,
        "Forward": browser_config.Config.showForwardButton,
        "Refresh": browser_config.Config.showRefreshButton,
        "Home": browser_config.Config.showHomeButton
    }
    pbUrlsEnabled = {
        "pb:exit": browser_config.Config.exitURLEnabled,
        "pb:about": browser_config.Config.aboutURLEnabled,
        "pb:policy": browser_config.Config.policyURLEnabled
    }
    policyText = f"""
    Browser Configuration:

    URL Allowlist: {str(browser_config.Config.url_allowlist)}

    URL Blocklist: {str(browser_config.Config.url_blocklist)}

    Homepage: {str(browser_config.Config.homepage)}

    Starting page: {str(browser_config.Config.startingpage)}

    Run Mode: {str(browser_config.Config.runMode)}

    Window Dimensions: {str(browser_config.Config.windowDimensions)}

    URL Bar Disabled: {str(browser_config.Config.urlBarDisabled)}

    Browser Buttons Enabled: {str(buttonsEnabled)}
    
    pb: URLs Enabled: {str(browser_config.Config.pbUrlsEnabled)}

    Allowed pb: URLs: {str(pbUrlsEnabled)}
"""