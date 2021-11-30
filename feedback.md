Hej Johan and Simon, 

you ask about what would happen if your repository was public, but it is public already.
Please make it private again as soon as possible, and add me (harisont), William (wakvist) and your examiner (aarneranta). It is strange that you encountered problems in adding us.
I would not say that, strictly speaking, sharing your solution is cheating, and especially not so when you and your classmates are working on the same lab in parallel and there's no known "correct solution". However, making your solutions available to everyone means that future students will be able to find them after they have been graded and perfected, making the assignement too easy to cheat on and making it necessary to create new assignments and tests every single year, which is a lot of work.
If you still diragree with this rule, you can certainly discuss it with your course representatives or directly with Aarne.

With that being said, and moving on to the assignment, your code looks good and it's always nice to see someone try using `re`, but I found the following issues:

- it seems to me that you misunderstood how the time dictionary should look like. It should only store times between _adjacent_ stops (i.e. what would/will become the edges of your tram network grap in lab 3), and it should _not_ be redundant, in the sense that
  - you only store the time it takes to go from A to B, and not also that from B to A
  - you need not store the time it takes from A to A 
- when it comes to queries:
  - some times are wrong. For example, going from Kviberg to Chalmers should take a different amount of time depending on what line you use (I speak for experience too ;)
  - the dialogue should properly distinguish between invalid queries and valid queries with invalid arguments. So, for example
  ```
  > time with 
  Unknown arguments.
  ```
  should instead yield `Sorry, try again.`
- the `distance` query seems to always returns `None`. This will probably be easy to fix.
