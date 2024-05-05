from .imperator import Imperator

# And add the extension to Krita's list of extensions:
app = Krita.instance()
# Instantiate your class:
extension = Imperator(parent = app)
app.addExtension(extension)
