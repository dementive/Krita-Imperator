# Krita-Imperator
 Krita plugin for drawing provinces in Imperator: Rome

## Setting up the plugin
 
 1. Install to the `pykrita` directory, make sure the `imperator.desktop` file is next to the `imperator` folder and they are both in the `pykrita` directory.

 2. Set the paths to your province setup, default.map, and definitions.csv at the top of `imperator.py`


## Usage

 In the `Tools` tab in the Krita menu 4 entries to create new land, river, sea, or impassable provinces will be available. 

 Click on the type of province you want to draw. The current foreground color for drawing will be set to an appropriate color that is not already defined in the definitions.csv (blue for rivers, black for impassables, any color for land). Additionally, your province setup, default.map, and definitions.csv will all be automatically updated with the new province ID, color, and data depending on what province type you are drawing.