import single_game
import modifying_data
import pandas as pd
import json

temp_page=single_game.getting_page("20181010","KTLT1")

import json
with open('test.json', 'w') as outfile:
    json.dump(temp_page, outfile)