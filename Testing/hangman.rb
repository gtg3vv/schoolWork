guesses = 6
print "Enter a word: "
word = gets.chomp.upcase
display = ("-," * word.length).split(",")

loop do
    print "[" + display.join("") + "] You have #{guesses} left, enter a letter: "
    letter = gets.chomp.downcase
    if !word.include? letter.upcase
        guesses -=1
        if guesses == 0
            puts "You lose! The word was \"#{word}\""
            break
        else
             puts "Incorrect!"
        end
       
    else
        for x in 0...word.length
            if word[x].downcase == letter.downcase
                display[x] = letter.upcase
            end
        end
        if !display.include? "-"
            puts "You win! The word was \"#{word}\""
            break
        else
            puts "Correct!"
        end
    end
end