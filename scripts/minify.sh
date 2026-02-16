

# Save currnet directory
current_dir=$(pwd)
echo "Current directory: $current_dir"
    cd ./src/assets/news/
    for file in *.png; do
        sips --resampleWidth 180 "$file" --out "$file";
    done
# go back to the original directory
cd $current_dir
