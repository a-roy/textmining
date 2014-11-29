from full_recommender import *



#### Please change the values below as needed ##################################

# Please provide the directory below (use '.' for current working directory)
grade_dir = r"mac/testing.xls"

# Please provide a name for the recommender
recommender_name = r"First Recommender"




################################################################################
#### Creating recommender, importing & anonymizing & saving data ###############

# Initialize the recommender with the name specified in recommender_name
recom = Recommender(recommender_name)

# Import the grades from all Excel and CSV files in the provided directory
recom.import_grades(grade_dir)

# Check first entry of the imported grade data
print recom.grade_data[0]

#### Testing ###################################################################

# Create a new Recommender object with the same name
test = Recommender(recommender_name)

# Load the grade data from the previous instance into test
test.import_grades()

# Check first entry of the loaded grade data
print test.grade_data[0]

#### If everything worked out, there will be a file ending in .grade_data ######
#### This file contains the anonymized recommender data, without duplicates ####
#### There will also be a file ending in .grade_seeds ##########################
#### This file contains the key to revert the anonymization of the data ########
################################################################################
