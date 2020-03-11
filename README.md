# Pyrite

Pyrite is a personal spending tracker. Every purchase is placed in a category, with running totals to show you where your money is going each week.

![pyrite](https://i.imgur.com/w0Zz9PV.png)


## Usage
Install dependencies with `pip3 install -r requirements.txt` and run with `python3 pyrite.py`. 
- Press UP and DOWN to choose a category
- Type to enter a price, and press ENTER to submit. 
- Press LEFT and RIGHT to view previous weeks.
- Press Q to quit.

## Why

Pyrite was created to make entering spending data as easy as possible. I found that using a spreadsheet to keep track of individual purchases took too much effort. What I wanted was a program where all I had to do was choose a category and type a price, without having to click anything. Recording a purchase now takes only six seconds instead of twenty or thirty, which makes recording spending much easier to keep on top of.

## Data format

Pyrite uses CSV files to hold program data because they're human-readable and extremely portable. It's easy to take your spending data and use it with another tool, such as a spreadsheet program. 

## User interface library

Pyrite was built using the [Silica terminal user interface library](https://github.com/benbridle/swm).