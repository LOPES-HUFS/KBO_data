import get_data
import pandas as pd
import json

if __name__ == "__main__":
    temp_page = get_data.getting_page("20181010", "KTLT1")
    # print(temp_page)

    with open("test.json", "w") as outfile:
        json.dump(temp_page, outfile)
