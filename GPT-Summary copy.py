from openai import OpenAI # Communication with OpenAI servers
import sys 
from pydrive.auth import GoogleAuth  # PyDrive allows to communicate with GoogleDisk
from pydrive.drive import GoogleDrive
import time  # Import for timestamp generation

if __name__ == "__main__":
    # Get the arguments from the shell command line
    arg1 = sys.argv[1]  # First argument


##### Part: Summary via OpenAI 

client = OpenAI(
    api_key="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",
) #OpenAI API key (used for authorization)

# Constructions to OpenAI assigned to a (str) variable
user_message = "Ci-dessous, je te fournis un extrait de cours de notre grande école. Dans le résultat, je ne veux voir que le résumé de cet extrait, rends ce texte compatible avec le format .txt. Pour faire ce résumé, tu dois considerer que les idées ou terminologies principales. De plus, je souhaite que tu divises cet extrait en plusieurs parties et que tu nommes chacune. Tu ne dois rien changer au contenu ni corriger les fautes contextuelles. Tu dois cependant utiliser un niveau de vocabulaire proche de celui d'un enseignant tout en restant grammaticalement correct. ATTENTION: il est inacceptable de rater l'information pertinente, tu peux être moins laconique mais couvrir tous les aspects."

# Assign transcribed recording's text (after -> TRT) to a (str) variable
with open(f"{arg1}.txt", 'r') as file:
    lesson_extract = file.read()

# Send request to OpenAI
completion = client.chat.completions.create(
  model="gpt-4o-mini",
  max_completion_tokens=2000,
  messages=[
    {"role": "developer", "content": "Tu es un correcteur des cours dans une grande école, précis et structuré"},
    {"role": "user", "content": f"{user_message} Voici l'extrait: {lesson_extract}"}
  ]
)

#print(completion.choices[0].message.content) # Read OpenAI's server response (summarized TRT)
content = f"{completion.choices[0].message.content}" # Assign OpenAI's response to a (str) variable

# Store content at file path below
file_path = "/Users/nightfallsoul/Desktop/Programming/NoteHear/WhisperCPP/whisper.cpp/Outputs/resume.md"

# Write content to the Markdown file (for better visual understanding)
with open(file_path, "w") as md_file:
    md_file.write(content)


######

# gauth = GoogleAuth() 
# gauth.LoadCredentialsFile("/Users/nightfallsoul/Desktop/Programming/NoteHear/Summarizer/credentials.json")

# # If credentials don't exist or are invalid, prompt for authentication
# if gauth.credentials is None:
#     gauth.LocalWebserverAuth()  # This will open a web page for login and authorization
# elif gauth.access_token_expired:
#     gauth.Refresh()  # Refresh the access token if expired
# else:
#     gauth.Authorize()

# # Save the credentials for the next run
# gauth.SaveCredentialsFile("/Users/nightfallsoul/Desktop/Programming/NoteHear/Summarizer/credentials.json")
# #Load the client secrets file
# gauth.LoadClientConfigFile("/Users/nightfallsoul/Desktop/Programming/NoteHear/Summarizer/client_secrets.json")

# drive = GoogleDrive(gauth) 

# #files to upload
# upload_file_list = ["/Users/nightfallsoul/Desktop/Programming/NoteHear/WhisperCPP/whisper.cpp/Outputs/resume.md"] 


# for upload_file in upload_file_list:
#     gfile = drive.CreateFile({'title': "SigmaSigmaster"}) # No parent folder ID specified
#     gfile.SetContentFile(upload_file)  # Set the content of the file to upload
#     gfile.Upload()  # Upload the file to Google Drive (it will go to the root)

# PART: Upload summarized content to GoogleDisk
gauth = GoogleAuth() 
gauth.LoadCredentialsFile("/Users/nightfallsoul/Desktop/Programming/NoteHear/Summarizer/credentials.json")

# If credentials don't exist or are invalid, prompt for authentication
if gauth.credentials is None:
    gauth.LocalWebserverAuth()  # This will open a web page for login and authorization
elif gauth.access_token_expired:
    gauth.Refresh()  # Refresh the access token if expired
else:
    gauth.Authorize()

# Save the credentials for the next run
gauth.SaveCredentialsFile("/Users/nightfallsoul/Desktop/Programming/NoteHear/Summarizer/credentials.json")
# Load the client secrets file
gauth.LoadClientConfigFile("/Users/nightfallsoul/Desktop/Programming/NoteHear/Summarizer/client_secrets.json")

drive = GoogleDrive(gauth) 

# Files to upload
upload_file_list = ["/Users/nightfallsoul/Desktop/Programming/NoteHear/WhisperCPP/whisper.cpp/Outputs/resume.md"] 



# Create a unique folder with a timestamp
timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")  # e.g., 20250102_120045
folder_name = f"NoteHear_Upload_{timestamp}"  # Unique folder name
folder_metadata = {
    "title": folder_name,
    "mimeType": "application/vnd.google-apps.folder",
    "parents": [{"id": "1TBmR7fSonknB4JhSH0hOfGdRMfdP2dY1"}] # Save all new unique folders to general folder (named: NoteHear_All_Files)
}
folder = drive.CreateFile(folder_metadata)  # Create folder object
folder.Upload()  # Upload folder to Google Drive
folder_id = folder["id"]  # Get the unique folder ID




# Upload Files into the Unique Folder 
for upload_file in upload_file_list:
    gfile = drive.CreateFile({
        'title': f"Resume_{timestamp}",  # File name to appear in Drive
        'parents': [{"id": folder_id}]  # Specify the unique folder ID
    })
    gfile.SetContentFile(upload_file)  # Set the content of the file to upload
    gfile.Upload()  # Upload the file to the unique folder
    #print(f"File '{upload_file}' uploaded successfully to '{folder_name}'!")


print(folder_name)