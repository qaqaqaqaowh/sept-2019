import peewee as pw
# Importing peewee and renaming it as pw

# We will not talk about all the database connection stuff over here.

# -------------------------
# | todo                  |
# -------------------------
# | id | task | completed |
# -------------------------
# | 1  | Eat  | false     |
# -------------------------

class Todo(pw.Model):
	# task is a column that will contain a string
	# it is required by default
	task = pw.CharField()

	# completed is a column that will contain a boolean
	# it contains false by default
	completed = pw.BooleanField(default=False)

# The values in the columns can be restricted so that all of it must be unique by doing
# task = pw.CharField(unique=True)
# This is useful when you have a user table and you need the email to be unique

# To create
Todo.create(task="Buy Milk")
# OR
todo = Todo(task="Buy Milk")
todo.save()

# To read

# Multiple
todos = Todo.select()

# With criteria
todos = Todo.select().where(Todo.completed == True)
todos = Todo.select().where((Todo.task == "Buy Milk") & (Todo.completed == False))
# the "&" in the code above means AND
# can be switched to "|" to signify OR

# The results can then be iterated
todos[0] # This gives you the first item from the rows that you retrieved
for todo in todos:
	print(todo.task)

# Only one
todo = Todo[1] # Gets the todo with id == 1
todo = Todo.get_by_id(1)
todo = Todo.get(Todo.id == 1) # Raises error when nothing was found
todo = Todo.get_or_none(Todo.id == 9999999) # Gives None when nothing was found
# Both 'get' and 'get_or_none' uses criteria

# Editing / Updating

# Get ONE row
todo = Todo[1]
todo.task = "Buy something else" # Update the columns that you want
todo.completed = True
todo.save() # Saves the current record

# Deleting

# Get ONE row
todo = Todo[1]
todo.delete_instance()