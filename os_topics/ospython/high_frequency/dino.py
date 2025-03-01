import math
import csv

g = 9.8
def read_data(file1,file2):
    dictionarydata={}


    with open(file1,mode= 'r') as f1:
        reader = csv.DictReader(f1)
        for row in reader:
            name = row["NAME"]
            leg_length = float(row["LEG_LENGTH"])
            diet = row["DIET"]
            dictionarydata[name]= {
            "name":name,
            "leg_length":leg_length,
            "diet": diet,
            "stride_length":None,
            "stance":None
            }
# speed = ((STRIDE_LENGTH / LEG_LENGTH) - 1) * SQRT(LEG_LENGTH * g)

    with open(file2,mode = "r") as f2:
        reader = csv.DictReader(f2)
        for row in reader:
            name = row["NAME"]
            stride_length= float(row["STRIDE_LENGTH"])
            stance = row["STANCE"]
            if name in dictionarydata: # and stance == "bipedal":
                print("dictionarydata",dictionarydata[name],stance,stride_length)
                dictionarydata[name]['stride_length']=stride_length
                dictionarydata[name]['stance']=stance # here its comming as None only
    return dictionarydata



def calculate_speeds(dictionarydata):
    speedarr = []
    dinospeed = 0
    for key in dictionarydata:
        dino = dictionarydata[key]
        print(f"dino:{dino}")
        if dino["stance"] == "bipedal":
            dinospeed = ((dino["stride_length"]/dino["leg_length"])-1) * math.sqrt(dino["leg_length"] * g)

        if dinospeed > 0:
            speedarr.append((dino["name"],dinospeed))
    return speedarr


def sort_the_speed(speedarr):
    speedarr.sort(key=lambda x: x[1],reverse=True)
    for name, speed in speedarr:
        print(f"Name:{name}|Speed:{speed}")
    return

def write_sorted_speeds_to_file(speedarr, output_file):
    speedarr.sort(key=lambda x: x[1], reverse=True)
    with open(output_file, 'w') as f:
        for name, speed in speedarr:
            f.write(f"Name: {name} | Speed: {speed:.2f} m/s\n")
    print(f"Sorted speeds written to {output_file}")



def main():

    file1 = "dataset1.csv"
    file2 = "dataset2.csv"
    data = read_data(file1,file2)
    print("data",data)
    calculated_data = calculate_speeds(data)
    sort_the_speed(calculated_data)
    # print("calculated_data",calculated_data)


if __name__ == "__main__":
    main()





## if you want to add the ouput to the file or read manually not with csv dictionary

import math

g = 9.8

def read_data_from_csv(file1, file2):
    dictionarydata = {}

    # Read dataset1.csv without csv.DictReader
    with open(file1, mode='r') as f1:
        lines = f1.readlines()
        headers = lines[0].strip().split(",")  # Get headers
        for line in lines[1:]:
            values = line.strip().split(",")
            name = values[0]
            leg_length = float(values[1])
            diet = values[2]
            dictionarydata[name] = {
                "name": name,
                "leg_length": leg_length,
                "diet": diet,
                "stride_length": None,
                "stance": None
            }

    # Read dataset2.csv without csv.DictReader
    with open(file2, mode='r') as f2:
        lines = f2.readlines()
        for line in lines[1:]:  # Skip the header
            values = line.strip().split(",")
            name = values[0]
            stride_length = float(values[1])
            stance = values[2]
            if name in dictionarydata:
                dictionarydata[name]['stride_length'] = stride_length
                dictionarydata[name]['stance'] = stance  # Set stance
    return dictionarydata

def calculate_speeds(dictionarydata):
    speedarr = []
    for key in dictionarydata:
        dino = dictionarydata[key]
        if dino["stance"] == "bipedal":
            dinospeed = ((dino["stride_length"] / dino["leg_length"]) - 1) * math.sqrt(dino["leg_length"] * g)
            if dinospeed > 0:
                speedarr.append((dino["name"], dinospeed))
    return speedarr

def write_sorted_speeds_to_file(speedarr, output_file):
    speedarr.sort(key=lambda x: x[1], reverse=True)
    with open(output_file, 'w') as f:
        for name, speed in speedarr:
            f.write(f"Name: {name} | Speed: {speed:.2f} m/s\n")
    print(f"Sorted speeds written to {output_file}")

def main():
    file1 = "dataset1.csv"
    file2 = "dataset2.csv"
    output_file = "sorted_speeds.txt"

    # Read data from CSV files
    data = read_data_from_csv(file1, file2)
    # Calculate speeds
    calculated_data = calculate_speeds(data)
    # Write sorted speeds to file
    write_sorted_speeds_to_file(calculated_data, output_file)

if __name__ == "__main__":
    main()
