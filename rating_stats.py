"""
File: rating_stats.py
----------------------
This file defines a program that allows a user to calculate
baseline summary statistics about a datafile of professor review
data. 
"""

def calculate_rating_stats(filename):
    """
    This function analyzes the professor review data in the given
    file to calculate the percentage of reviews for both men and
    women that fall in the "high rating" bucket, which is a numerical
    rating that is greater than 3.5.

    The resulting information is printed to the console.
    """
    male = 0
    male_high = 0
    female = 0
    female_high = 0

    with open(filename) as f:
        next(f)
        for line in f:
            key_val = line.split(',')
            if key_val[1] == 'M':
                male += 1
            if float(key_val[0]) > 3.5 and key_val[1] == 'M':
                male_high += 1
            if key_val[1] == 'W':
                female += 1
            if float(key_val[0]) > 3.5 and key_val[1] == 'W':
                female_high += 1

    female_percent = round((female_high / female * 100))
    male_percent = round((male_high / male * 100))
    print(str(female_percent) + '%', 'of reviews for women in the data set are high')
    print(str(male_percent) + '%', 'of reviews for men in the data set are high')


def main():
    # Ask the user to input the name of a file
    filename = input("Which data file would you like to load? ")

    # Calculate review distribution statistics by gender for
    # that file. This function should print out the results of
    # the analysis to the console.
    calculate_rating_stats(filename)

if __name__ == '__main__':
    main()