people <- list("Vaishnav", "Sri", "Harsha", "Vaishali", "Abc")
j <- 1

for(i in 1:length(people)) {
  if(nchar(people[i]) > 5) {
    result[j] <- people[i]
    j = j+1
  }
}

library(dplyr)
result <- mutate_all(result, funs=toupper)
print(result)
