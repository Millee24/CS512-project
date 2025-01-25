import requests
import json
import pandas as pd
from datetime import datetime

def main():
    #range of years of SCOTUS data to get
    start_year = 2019
    end_year = 2020
    #variable to store dates for SCOTUS trials
    scotus_dates = []

    #API endpoint url for SCOTUS cases
    api_base_url = 'https://api.oyez.org/cases?per_page=0&filter=term:'

    #SCOTUS Cases are organized by Year, so iterate over the range of years
    for i in range(start_year, end_year+1):
        #Create the API URL from the base URL (api_base_url) plus the year
        api_url = api_base_url + str(i)
        # send GET request to the Oyez API
        Oyez_API = requests.get(api_url)
        #
        scotus_data = Oyez_API.json()

        # status code check
        print(str(i) + ": " + f"status code: {Oyez_API.status_code}")


        # ==== DATA FOR ANALYSIS =====
        #iterate over each case in scotus_data list
        for row in scotus_data:
            #temporary list for dates
            line = [str(i)]
            #get name of case
            #line.append(f'"{row.get("name",[])}"')
            #line.append(row.get("name",[]))
            txt = row.get("name", [])
            txt = txt.replace(",","")
            line.append(txt)
            #first, get the timeline data as a list
            timeline = row.get("timeline", [])
            #print(timeline) #debug
            #now get each "event" (Granted, Argued, Decided)
            for item in timeline:
                if item is None:
                    # do something
                    line.append('" "')
                else:
                    #convert epoch time to YYYY-MM-DD, solution provided by "FloLie" at https://stackoverflow.com/questions/65063058/convert-unix-timestamp-to-date-string-with-format-yyyy-mm-dd
                    dt = datetime.fromtimestamp(item["dates"][0])
                    line.append(dt.strftime("%Y-%m-%d"))
            scotus_dates.append(line)

    #Write cleaned data to CSV file
    write_csv(scotus_dates, "scotus_dates.csv")

    #Convert CSV file to JSON file
    # csv_to_json("scotus_dates.csv", "scotus_dates_converted.json")

    #Convert JSON file to CSV file
    # json_to_csv("test.json", "scotus_dates_converted.csv")
    #json_to_csv("scotus_dates_converted.json", "scotus_dates_converted.csv")

def write_csv(data_list, outfile):
    """This function takes a list of lists and writes a CSV file."""
    print("Saving file to CSV: " + outfile)
    with open (outfile, "w") as outfile:
        #write header row
        outfile.write("Year, Title, Date_Granted, Date_Argued, Date_Decided\n")
        #iterate through each row of the data, join with a comma, and write to file
        for row in data_list:
            #add quote marks to title
            row[1] = f'"{row[1]}"'
            line = ", ".join(row)
            outfile.write(line + "\n")

def csv_to_json(infile, outfile):
    """This function converts a CSV-formatted file into a JSON-formatted file."""
    #TO DO
    df = pd.read_csv(infile, quotechar='\"')  ### Changed by Emma
    outfile = df.to_json(infile)        ### Changed by Emma
    print("Converted CSV file (" + infile + ") to JSON (" + outfile + ")")


def write_json(data_list, outfile):
    """This function takes a list of lists(?) and writes a JSON-formatted file."""
    print("Saving file to JSON")
    # TO DO
    # Save data to a JSON file
    outfile = "scotus_data_" + str(i) + ".json" 
    with open (outfile, "w") as outfile:
        json.dump(scotus_data, outfile)


def json_to_csv(infile, outfile):
    """This function converts a JSON-formatted file into a CSV-formatted file."""
    #Converting the json file to csv using pandas
    df = pd.read_json(infile)
    #convert values to strings
    df = df.astype(str)
    date_list = df.values.tolist()
    write_csv(date_list, outfile)
    print("Converted JSON file (" + infile + ") to CSV (" + outfile + ")")

if __name__ == '__main__':
    main()



