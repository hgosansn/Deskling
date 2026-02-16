

git rm -r --cached .
git add .


echo "Committing the changes..."
git add .

message=$(echo "Refactor the code, make it more spaghetti-like.
Added more bugs to confuse future developers.
Changed something, hope it doesn’t break.
Fixed the bug causing happiness.
This commit has no message. It’s a mystery.
Added a comment, because that’s what pros do.
Removed useless code. Added more useless code.
Making it up as I go along.
Here be dragons.
Oops, did I do that?
Moved stuff around and broke everything.
Fixed something that wasn’t broken.
Deleted the internet.
Attempted to fix the bug, succeeded in creating $((RANDOM % 10 + 1)) more.
Added a feature that nobody asked for.
Making the world a worse place, one commit at a time.
Code that compiles is just a bonus.
Gave up, let the future handle this.
To be honest, I have no idea what this does.
Please work. Please." | sort -R | head -n 1)

printf "\e[1;32m$message\e[0m"

echo "---"

git commit -am "$message"

echo "Bumping the version..."

npm version patch

git push -u origin main --tags

echo "Done."
