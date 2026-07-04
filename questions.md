## Thoughts before writing any code

### Questions before coding
1.) Save the results in a json or csv file?

2.) What are some general expense categories that you can come up with?

3.) Should I save the budget file seperately? This could act like a normalized table which only has budget while the dim table could be the json or csv file I will keep saving for a user

4.) Do I need to store the expenses data in a text file? Or can I just do it in a json or csv file?

### Thought 1:
One expense or record in the expenses file could like this

id, date, description, amount, category, created_at, updated_at

### Thought 2:
add, list, summary, delete --id, summary --month, update, export are methods that i can perform on the expenses table

### Thought 3:
Also since I am going ahead with a json, I will need to have a dictionary of expenses where each key is the expense_id and the value is another dictionary which holds other information

#### Conclusion 3:
This design is fine but since most apis return a list which holds a dictionary, let me mimick the same behaviour.

### Thought 4:
In case of deleting a records from the expense json, should i take care of non continuous id numbers? Is this even needed? Can it cause confusion? Let's say I deleted expense_id = 2, if I end up making these ids continuous, will the user get confused seeing the expense_id = 2 just after deleting it?

#### Conclusion 4:
Do not make the ids continuous as it is not a good practice

### Thought 5:
Finally if i use a csv file, I can very easily mimick sql like behaviour using pandas whereas if I use json my code will be more verbose than necessary.

#### Conclusion 5:
Let me not use pandas as I am good at it and let me instead learn how to use json(although json is not very different from python dictionaries).

### Thought 6:
add: Create a new entry in the expenses json file

list: List the json file in a tabular format

summary: Add all the expense and display to user

summary --month: Add all the expenses for a given month and display it to user

delete --id: Delete an entry in the expenses json file

update: Update an entry in the expense josn file

export: Export the expenses data into csv file and download it for the user

### Thought 7:
Different functions that I can have
1.) Parse the arguments from the cli tool
2.) Validate the arguments
3.) Fetch expenses json (if exists or else create a new json file)
4.) Perform necessary action (CRUD operations)
5.) Save results to existing json
6.) Export json file to a csv file and let the user download it
