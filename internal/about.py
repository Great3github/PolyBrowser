from dialog import CustomDialog
from msg import msgconfig
def ShowAbout():
    CustomDialog.NewOkDialog(msgconfig.InternalPageContent.aboutText[0], msgconfig.InternalPageContent.aboutText[1])