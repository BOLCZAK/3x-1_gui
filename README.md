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
9 --x3+1--> 28 --/2--> 14 --/2--> 7 --x3+1--> 22 --/2--> 11 --> 34 --> 17 --> 52 --> 26 --> 13 --> 40 --> 20 --> 10 --> 5 --> 16 --> 8 --> 4 --> 2 --> 1 --> 4 🔁

Eventually we always end up with 4->2->1 loop. Mathematicians are searching for number that will not fall into that loop

As for now on the bruteforced $2^{68}$ numbers (that's a lot)

[^wiki]: See on Wiki: https://en.wikipedia.org/wiki/Collatz_conjecture | Zobacz na Wikipedii https://pl.wikipedia.org/wiki/Problem_Collatza