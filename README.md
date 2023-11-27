## This app is only in Polish for now (sadly)

------------

# $3x+1$ problem (Collatz conjecture)[^wiki]

Inspierd by video on youtube channel Veritasium:

[<img src="https://img.youtube.com/vi/094y1Z2wpJg/sddefault.jpg" width="50%">](https://www.youtube.com/watch?v=094y1Z2wpJg)

[//]: # (https://www.youtube.com/watch?v=094y1Z2wpJg)

I decided to write simple GUI program just for fun tackling the conjecture defined above.

## Explanation

In summary the $3x+1$ conjecture works as follows:
1. Pick any positive integer ($\mathbb{Z}$) number
2. If the number is odd multiply it by 3 and add 1
3. Else divide it by 2
4. Repeat

So for example 9

The steps will be:
`9` --x3+1--> `28` --/2--> `14` --/2--> `7` --x3+1--> `22` --/2--> `11` --> `34` --> `17` --> `52` --> `26` --> `13` --> `40` --> `20` --> `10` --> `5` --> `16` --> `8` --> `4` --> `2` --> `1` --> `4` 🔁

Eventually we always end up with 4->2->1 loop. Mathematicians are searching for number that will not fall into that loop

As for now they bruteforced $2^{68}$ numbers (that's a lot)

-------------------

# Application

My application just calculates those steps and plots them onto graph.

Home page looks like this:

<img src="img\home.png">

It contains few options<br>On the left you can see openable menu that contains (from top to bottom):
1. Home page
2. Single value
3. Range of values
4. Help (not implemented yet)

In the right upper corner there are also some default control buttons

## Single value page
This page looks like so:

<img src="img\single.png">

In the top section we define our selected starting value, and if we want to we can check that plot should be a scatter plot or plotted in a logarithmic scale.<br>

### To start calculation we need to press the big <span stylesheet="color: #00FF00">green</span> button near control buttons

After calculation is done in the bottom section we have our plot that is interactive, and on the right side we have some statistics like max value reached, amount of steps and time it took to calculate


## Range of numbers page
This page looks like so:

<img src="img\range.png">

Similarly, in the top section we define our selected starting value, but we also define end of range, and if we also want to, we can check that plot should be a scatter plot or plotted in a logarithmic scale. Moreovver there are two more options that controls time the program waits between calculations and if we want to clear graph after specified amount of plots we also can check it here. We can also define stop condition here, that will halt the execution of a program until we press the small green button next to stop condition. I implemented here two stop conditions: by value exceeded and by steps exceeded - they can work simultaneously.<br>

### To start calculation we need to press the big <span stylesheet="color: #00FF00">green</span> button near control buttons

The calculation will start and the progress bar will appear showing the overall progress of calculations. Plots will be plotted onto the graph and cleared if we specified to

After calculation is done in the bottom section we have our last plot that is interactive, and on the right side we have some statistics like max value reached, amount of steps and time it took to calculate the last plot and time it took to test whole range that we specified

[^wiki]: See on Wiki: https://en.wikipedia.org/wiki/Collatz_conjecture | Zobacz na Wikipedii https://pl.wikipedia.org/wiki/Problem_Collatza