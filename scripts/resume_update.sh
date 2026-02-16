

# Download a json Gist
resume_json=$(curl -s https://api.github.com/gists/73d9f410033d4168087a69c129eea56d | jq -r '.files["resume.json"].content')

echo $resume_json | tr -d '\000-\037' | jq -r '.' > ./temp/resume.json

work_array=$(echo $resume_json | tr -d '\000-\037' | jq -r '.work[:4]')

# print a json object with the work array at the key "work"
echo "{\"work\": $work_array}" > ./src/data/work.json
