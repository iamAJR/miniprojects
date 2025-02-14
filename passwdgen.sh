#!/bin/bash

# Characters for password generation
LOWERCASE="abcdefghijklmnopqrstuvwxyz"
UPPERCASE="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBERS="0123456789"
SPECIAL="!@#$%^&*()-_=+[]{};:,.<>?"

# Function to generate a password
generate_passwd(){
    local length=$1
    local char_types="$2"
    
    # Use /dev/urandom and tr to filter and generate a password
    password=$(cat /dev/urandom | tr -dc "$char_types" | head -c "$length")
    echo "$password"
}

# Read the desired password length
read -p "Enter the desired password length: " input_length

# Automatically assign "weak" if length is less than 6
if [ "$input_length" -lt 6 ]; then
    echo "Password length is less than 6, setting strength to 'weak'."
    char_types="$LOWERCASE$UPPERCASE"
else
    # Ask the user for the strength level of the password
    echo "Select password strength:"
    echo "weak   - Only lowercase and uppercase alphabets"
    echo "good   - Alphabets and numbers"
    echo "strong - Alphabets, numbers, and special characters"
    read -p "Choose a strength (weak/good/strong): " strength

    # Set the character types based on the user's choice
    case $strength in
        weak)
            char_types="$LOWERCASE$UPPERCASE"
            ;;
        good)
            char_types="$LOWERCASE$UPPERCASE$NUMBERS"
            ;;
        strong)
            char_types="$LOWERCASE$UPPERCASE$NUMBERS$SPECIAL"
            ;;
        *)
            echo "Invalid option. Defaulting to 'good' strength."
            char_types="$LOWERCASE$UPPERCASE$NUMBERS"
            ;;
    esac
fi

# Optionally suggest ways to strengthen the password
echo "For a stronger password:"
echo "- Use at least 12 characters."
echo "- Include numbers, special characters, and both uppercase and lowercase letters."

# Generate and display multiple passwords
echo
echo "Generated passwords:"
echo
for (( i=1; i<=5; i++ ))
do
    password=$(generate_passwd $input_length "$char_types")
    echo "[$i] $password"
    echo
done 

#understanding how passwd is generated 
#cat /dev/urandom

#    /dev/urandom is a special file in Unix-like systems that provides an infinite stream of random bytes.
#    cat /dev/urandom reads these random bytes and outputs them.

#However, the raw bytes from /dev/urandom contain all sorts of characters (including non-printable ones), which are not useful for generating a password, so we filter them in the next step.
#2. tr -dc "$chars"

 #   tr is a command used to translate or delete characters from the input.
  #  The option -d tells tr to delete characters.
   # The option -c negates the character set (inverts it), meaning it will delete everything except the characters specified.
    #$chars is a variable that contains the valid set of characters you want in the password, such as letters, numbers, and possibly special characters.

#This part ensures that only characters from the $chars set are kept (e.g., letters, numbers, and special symbols you define), and all other characters are removed.
#3. head -c "$length"

 #   head is a command that outputs the first part of a file or stream.
  #  The option -c "$length" tells head to output only the first $length bytes (or characters) from the input stream.

