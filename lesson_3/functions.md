# Functions

You sometimes have pieces of code which you need multiple times (often with small variations).
It is often wise to put these pieces of code in a function.

A function has the following structure:

```Python
def my_function(argument1, argument2):
    # Function logic
    result = argument1 + argument2
    return result
```

The function starts of with a name. It can optionally also have one or more arguments.
The arguments are input for the function. The results of the function are given back
to the function caller by using the **return** statement. All variables which are
declared in the function can only be used within the function.

The following example demonstrates how to use a function:

```Python
def my_function(argument1, argument2):
    # Function logic
    result = argument1 + argument2
    return result

first_number = 5
second_number = 10

sum = my_function(first_number, second_number)
print("The sum of {} and {} is {}".format(first_number, second_number, sum))
```

## Documentation

It is best practice to document your functions so others will know
how to use them:

```Python
def my_function(argument1, argument2):
    '''
    This is my function. It takes two arguments
    and return the sum of those arguments.
    '''
    result = argument1 + argument2
    return result
```

## Builtin functions

Python has a lot of builtin functions which you can use.
The `print` function is the best known one. It can be used to
display text on your screen.
