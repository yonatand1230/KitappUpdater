import json, requests, base64, os
from requests.auth import HTTPBasicAuth


def upload_file(file_path, repository, username, msg, token, branch="main", folder=""):
    # Define the API URL to create or update a file in the repository
    url = f"https://api.github.com/repos/{username}/{repository}/contents/{file_path}"
    
    if folder != "":
        url = f"https://api.github.com/repos/{username}/{repository}/contents/{folder}/{file_path}"

    # Read the contents of the file
    with open(file_path, 'rb') as file:
        file_content = file.read()

    # Encode the file content as Base64
    encoded_content = base64.b64encode(file_content).decode('utf-8')

    # Define the request headers
    headers = {
        'Authorization': f"token {token}",
        'Content-Type': 'application/json'
    }

    # Make a GET request to retrieve the existing file details
    sha = None
    response = requests.get(url, auth=HTTPBasicAuth(username, token), headers=headers)
    if response.status_code == 200:
        file_info = response.json()
        sha = file_info.get('sha')


    # Define the request payload
    payload = {
        'message': msg,
        'committer': {
            'name': username,
            'email': f"{username}@users.noreply.github.com"
        },
        'content': encoded_content,
        'branch': branch,
    }
    
    if sha != None:
        payload.update({
            'sha':sha
        })

    # Make the API request to update the file
    response = requests.put(url, auth=HTTPBasicAuth(username, token), json=payload, headers=headers)

    if response.status_code == 200 or response.status_code == 201:
        return response
    else:
        raise Exception(f"Failed to update file. \nResponse: {response.text}\nCode: {response.status_code}")

def upload_json(obj, file_path, repository, username, msg, token, branch="main", encoding='utf-8', indent=4, ensure_ascii=False, folder=""):
    with open(file_path, 'w', encoding=encoding) as f:
        f.write(json.dumps(obj, indent=indent, ensure_ascii=ensure_ascii))

    response = upload_file(file_path, repository, username, msg, token, branch, folder=folder)
    
    os.remove(file_path)
    
    return response