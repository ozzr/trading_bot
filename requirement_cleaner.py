import re

# Read the requirements.txt file
with open('requirements.txt', 'r') as file:
    lines = file.readlines()

# Remove version specifications
lines = [re.split('==|>=|<=|>|<', line)[0] + '\n' for line in lines]

# Write the modified requirements to a new file
with open('requirements_no_versions.txt', 'w') as file:
    file.writelines(lines)

print("requirements_no_versions.txt file has been created")
