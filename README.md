
# GameParams2Json  
  
**Converts GameParams to JSON**  
  
**GameParams2Json.py** arguments:

 - --path: GameParams.data file path
 - --filter: Filter the data. (Optional)
 - --pts: Extracts the entities to `pts` directory. Omitting this argument will extract the entities to `live` directory instead.
  
It will create **entities** folder which has all the entities separated by types (with their respective folders.)  

# Localization

**mo2json.py** arguments:
- --filter: The filter. A csv file. Each line is the used keys. (Required)
- --mofile: WoWS localization file. (Required)
- --missing: Outputs the not found indexes to a text file. (Optional)
- --out: Output file (optional) (default: strings.json)

### DEPENDENCIES:  
  
 For GameParams2Json, nothing. Everything it needs is already in Python's buitins.  
 For localization, please install `lxml` and `polib`. Just do `pip install -r requirements.txt`.  