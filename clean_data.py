import sys
import datetime


def clean_data(data):
  print(f"Cleaning data: {data}")

  # open and read file
  with open(data, "r") as f:
    lines = f.readlines()

    # remove bad headers
    lines = lines[3:]

    # Add corrected header
    output = ['"Timestamp","Station","AirTemperatureMax","AirTemperatureMin","RelativeHumidity","Precipitation","WindSpeed2mAvg","WindSpeed2mMax","SoilTemperature5cmMax","SoilTemperature5cmMin","SoilTemperature10cmMax","SoilTemperature10cmMin","SolarRadiation"']

    # process lines
    for line in lines:
      line = line.strip()

      # split line by comma
      if line:
        splits = line.split(",")

        # convert first item to day of year
        try:
          # remove quotes from date string
          splits[0] = splits[0].replace('"', '')
          date = datetime.datetime.strptime(splits[0], "%Y-%m-%d")
          day_of_year = date.timetuple().tm_yday
          splits[0] = str(day_of_year)
        except ValueError:
          print(f"Skipping line with invalid date: {line}")
          continue

        # remove last two items
        splits = splits[:-2]

        # remove bad data
        # splits = [item if item != "M" else "0" for item in splits]

        # join splits back into a line
        output.append(",".join(splits))

  # write output to file
  data = data.replace(".csv", "")
  with open(f"{data}_cleaned.csv", "w") as f:
    f.write("\n".join(output))


# Main Guard
if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: python clean_data.py <data> [<data> ...]")
    sys.exit(1)
  for data in sys.argv[1:]:
    clean_data(data)