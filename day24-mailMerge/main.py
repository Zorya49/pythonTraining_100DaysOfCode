#TODO: Create a letter using starting_letter.txt 
#for each name in invited_names.txt
#Replace the [name] placeholder with the actual name.
#Save the letters in the folder "ReadyToSend".
    
#Hint1: This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp
    #Hint2: This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp
        #Hint3: THis method will help you: https://www.w3schools.com/python/ref_string_strip.asp

names_file = open("./Input/Names/invited_names.txt")
names = names_file.readlines()

invitation = open("./Input/Letters/starting_letter.txt")
invitation_text = invitation.read()

for name in names:
    name = name.strip()
    print(name)
    adjusted_invitation = invitation_text.replace("[name]", name)
    tmp_file = open(f"./Output/ReadyToSend/invitation_for_{name}.txt", mode="w")
    tmp_file.write(adjusted_invitation)
    tmp_file.close()
