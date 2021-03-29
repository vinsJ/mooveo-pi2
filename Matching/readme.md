# Matching 👨‍❤️‍👨👨‍❤️‍💋‍👨👩‍❤️‍💋‍👩

This is the macthing part, here you'll find : 

- 📁 DB :
    - passport-index-matrix.csv : Visa type between countries
    - db_loader : Script to gather the data from Mooveo's databse
    - 📁 model :
        -  offer : offer class
        -  user : user class

- 📁 Heursitics : 
    - skills
    - languages 
    - distance
    - disponibility ***empty file***
    - \_\_init__  : compute all the heuristics, to be called in lambda_function

- 📃 lambda_function : main script where the data is loaded and where the endpoint is.

- 💽 .env.example : example of .env | **You must have a .env in the project, with the same name as the example.**

- 🐳 Dockerfile and requirements.txt are used to build a Docker Image (used to be deploy on AWS Lambda ☁).

## Distance 

In the distance script 📃🌍, you'll find coefficient applied on the distance. These are based on the Visa type required to travel from a country to another one 🛫.

Here is their meaning : 

- VR : Visa Required
- ETA : Visa required, but can be done online (not meaningful, same as VR)
- VOA : Visa On Arrival
- VF : Visa free
- integers : number of days you can stay on the territory without Visa


### Want to try the code 💻? 

Add this line in lambda_function.py : 

    print(main('4ca5be7c-7673-424c-93ae-2fb94c2b4c25'))

**Be careful, some IDs in offers_skills are not in offers. And some offers in offers are not in offers_skills. Don't be alarmed 🚨 if you've got skills at 0 : this is a databse's content issue, not our API**

[Go back to the main readme !](../readme.md) 