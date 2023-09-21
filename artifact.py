import os
import requests
import base64
# Retrieve values from environment variables
organization = "$(organizationid)"
project = "$(System.TeamProjectId)"
buildId = "$(build_id)"
token = "$(system.token)"


pat_token_b64 = base64.b64encode(bytes(f':{token}', 'ascii')).decode('ascii')
# Set the headers for the HTTP POST request
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {pat_token_b64}'
}


# Define release URL
artifact_url = f"https://dev.azure.com/{organization}/{project}/_apis/build/builds/{buildId}/artifacts?api-version=7.0"


print(artifact_url)
# Get current release
response = requests.get(artifact_url, headers=headers)
print(response)

if response.status_code == 200:
    artifacts_data  = response.json()

    # Loop through the release artifacts
    for artifact in artifacts_data.get('value', []):
        downloadurl = artifact.get('resource').get('downloadUrl')
        artifact_name = artifact.get('name')
        print(downloadurl)

        local_path = os.path.join(os.getcwd(), f"{artifact_name}.zip")
        response = requests.get(downloadurl, headers=headers)

        if response.status_code == 200:
            with open(local_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded {artifact_name}.zip to {local_path}")
        else:
            print(f"Failed to download {artifact_name}.zip")
else:
    print(f"Failed to fetch artifact information. Status Code: {response.status_code}")
