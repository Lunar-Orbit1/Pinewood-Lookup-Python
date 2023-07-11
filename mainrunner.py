#Claym1x, 2023

#GITHUB: https://github.com/Lunar-Orbit1/Pinewood-Lookup-Python

#Import modules and define some tables/classes
import requests, json, os
class cc:
    hea = '\033[95m'
    blu = '\033[94m'
    cyn = '\033[96m'
    grn = '\033[92m'
    warn = '\033[93m'
    fail = '\033[91m'
    end = '\033[0m'
    bold = '\033[1m'
    und = '\033[4m'
groups = {
    159511: "Pinewood",
    645836: "PBST",
    2593707: "PET",
    4890641: "TMS",
    4543796: "PBQA",
    4032816: "PBM",
    670202: "PIA",
    1179443: "Xylem",
}

#Main functions
def getGroupranks(uid):
    #Noblox.js does this better, but thats javascript :/
    requesturl = f"https://groups.roblox.com/v2/users/{str(uid)}/groups/roles" 
    res = requests.get(requesturl)


    if res.status_code == 200:
        #This is the list that is looped through and printed
        #If the user is in the group, it changes N/A to their rank

        #This basically gets all the groups the user is in, and loops through to see if they are in any pb groups
        #I swear there used to be an api for this..
        table = {
            "Pinewood": "N/A",
            "PBST": "N/A",
            "PET": "N/A",
            "TMS": "N/A",
            "PBQA": "N/A",
            "PBM": "N/A",
            "PIA": "N/A",
            "Xylem": "N/A"
        }
        resjson = res.json()['data']
        for x in resjson:
            try: #If the selected group matches with any pinewood group, set it to their rank
                if groups[x['group']['id']]:
                    table[groups[x['group']['id']]] = x['role']['name']
            except:
                pass
        
        return table

    else:
        print(f"{cc.fail}Error:{cc.end}")
        print(res.json())
        return None

def getUId(name):
    #Roblox depricated their username/id api
    #At least I think so, it returns 404 iirc
    #So I have to do this :/

    rl = 'https://users.roblox.com/v1/usernames/users'
    request_body = {
        'usernames': [name],
        'excludeBannedUsers': True
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    json_data = json.dumps(request_body)
    response = requests.post(rl, headers=headers, data=json_data)
    #Return json
    user_data = json.loads(response.text)
    if len(user_data['data']) > 0:
        user_id = user_data['data'][0]['id']
        return user_id
    else:
        return None
    #Basically searches for a user like normal players would
    #And grabs the first result

#If it finishes, or an error occurs, ask user to start again
def startAgainQuestion():
    startagain = input(f"Would you like to start again? (y/n): ")
    if startagain =="y":
        os.system("cls")
        mainFunc()
    elif startagain != "y" and startagain !="n":
        print(f"{startagain} is not valid")
        startAgainQuestion()

#Main function
def mainFunc():
    in1=input(f"{cc.bold}Enter the username you want to search: {cc.end}")
    print(f"{cc.hea}Searching user..{cc.end}")
    uid = getUId(in1)
    if uid != None:
        print(f"{cc.hea}Found user {str(uid)}.. indexing groups {cc.end}")
        groups = getGroupranks(int(uid))
        if groups!=None:
            print(f"{cc.grn}Success, found user's groups{cc.end}")
            print(f"{cc.bold}============================================================={cc.end}")
            for x in groups:
                to_prnt = ""

                #This is messy and jenky and dumb bad code
                #TODO: Fix
                if groups[x] != "N/A":
                    to_prnt = f"{cc.bold}{cc.grn}{x}{cc.end}{cc.grn}: {groups[x]}{cc.end}"
                else:
                    to_prnt = f"{cc.bold}{cc.fail}{x}{cc.end}{cc.fail}: {groups[x]}{cc.end}"
                print(to_prnt)

            #If they are in xylem or pia, add special modifiers that stand out
            if groups['PIA'] !="N/A":
                print(f"{cc.bold}{cc.cyn}~~~~====USER IS PIA====~~~~{cc.end}")

            if groups['Xylem'] !="N/A":
                print(f"{cc.bold}{cc.cyn}~~~~====USER IS XYLEM====~~~~{cc.end}")
            print(f"{cc.bold}============================================================={cc.end}")
            startAgainQuestion()
        else:
            #if for some reason an error occured while getting groups
            print(f"{cc.fail}An error occured and the user's groups were not found{cc.end}")
            startAgainQuestion()

    else:
        #if the user was not found
        print(f"{cc.fail}Could not find user{cc.end}")
        startAgainQuestion()


#Clear the console and start it
os.system("cls")
mainFunc()