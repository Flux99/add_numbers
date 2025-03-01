import csv
import math

# Constants
g = 9.8  # gravitational constant in m/s^2

# Function to read the dinosaur data from CSV files
def read_data(file1, file2):
    dinosaurs = {}

    # Read dataset1.csv
    with open(file1, mode='r') as f1:
        reader = csv.DictReader(f1)
        for row in reader:
            name = row['NAME']
            leg_length = float(row['LEG_LENGTH'])
            diet = row['DIET']
            dinosaurs[name] = {
                'leg_length': leg_length,
                'diet': diet,
                'stride_length': None,  # Initialize with None
                'stance': None           # Initialize stance with None
            }

    # Read dataset2.csv
    with open(file2, mode='r') as f2:
        reader = csv.DictReader(f2)
        for row in reader:
            name = row['NAME']
            stride_length = float(row['STRIDE_LENGTH'])
            stance = row['STANCE']
            if name in dinosaurs:
                dinosaurs[name]['stride_length'] = stride_length
                dinosaurs[name]['stance'] = stance  # Add this line to set the stance

    return dinosaurs

# Function to calculate speed for bipedal dinosaurs
def calculate_speeds(dinosaurs):
    speeds = []
    for name, data in dinosaurs.items():
        if data['stride_length'] is not None and data['stance'] == 'bipedal':
            leg_length = data['leg_length']
            stride_length = data['stride_length']
            speed = ((stride_length / leg_length) - 1) * math.sqrt(leg_length * g)
            if speed > 0:  # Only include positive speeds
                speeds.append((name, speed))
    return speeds



# Function to sort and print the results
def print_sorted_bipedal_speeds(speeds):
    # Sort speeds from fastest to slowest
    speeds.sort(key=lambda x: x[1], reverse=True)
    print("Bipedal Dinosaurs (from fastest to slowest):")
    for name, speed in speeds:
        print(f"{name}: {speed:.2f} m/s")

# Main function
def main():
    dataset1 = 'dataset1.csv'
    dataset2 = 'dataset2.csv'

    # Read data from CSV files
    dinosaurs = read_data(dataset1, dataset2)
    # Calculate speeds for bipedal dinosaurs
    bipedal_speeds = calculate_speeds(dinosaurs)
    # Print sorted speeds
    print_sorted_bipedal_speeds(bipedal_speeds)

if __name__ == '__main__':
    main()
