from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext

# Step 1: Install the library using pip install Office365-REST-Python-Client

# Step 2: Set up your SharePoint and authentication details
site_url = "https://yourtenant.sharepoint.com/sites/yoursite"
client_id = "your_client_id"
client_secret = "your_client_secret"

# Step 3: Authenticate and connect to SharePoint
credentials = ClientCredential(client_id, client_secret)
ctx = ClientContext(site_url).with_credentials(credentials)

# Step 4: Specify the repository (document library) path
library_title = "Documents"  # Example library title
library = ctx.web.lists.get_by_title(library_title)

# Step 5: Retrieve all files in the specified repository
ctx.load(library)
ctx.execute_query()
all_items = library.get_items()
ctx.load(all_items)
ctx.execute_query()

# Step 6: Download each file and save it to a local folder
import os

local_path = "path/to/local/folder"  # Specify your local folder path here

for item in all_items:
	if item.properties["FileSystemObjectType"] == 0:  # Object is a file
		file_ref = item.properties["FileRef"]
		file_name = os.path.basename(file_ref)
		download_path = os.path.join(local_path, file_name)
		
		# Download the file
		file = ctx.web.get_file_by_server_relative_url(file_ref)
		file_content = file.read()
		ctx.execute_query()
		
		# Save the file locally
		with open(download_path, "wb") as local_file:
			local_file.write(file_content)
			print(f"Downloaded {file_name} to {download_path}")