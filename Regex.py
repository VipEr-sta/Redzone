import re

myString = " let x = 5; print(Hello World 3 amd 57)"

pattern = r"^\d+$"
keyword_pattern = r"let"

answer = re.findall(pattern, myString)
#answer = re.search(pattern, myString)

keywords = re.findall(keyword_pattern, myString)

print(answer, keywords)

if answer:
    print("")

