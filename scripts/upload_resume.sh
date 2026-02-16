



# Get the json file
resume_json=$(cat ./temp/resume.json)

# Upload to an existing gist using gh
# https://cli.github.com/manual/gh_gist_edit
# Current version
# https://gist.github.com/hgosansn/73d9f410033d4168087a69c129eea56d
gh gist edit 73d9f410033d4168087a69c129eea56d ./temp/resume.json
