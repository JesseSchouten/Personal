---
title: 'Java-Script: The Definitive Guide'
created: '2021-05-28T19:39:30.039Z'
modified: '2021-06-13T08:28:06.339Z'
---

# Java-Script: The Definitive Guide
Start: 2021-5-28
End:?
Description: This is a summary of my learnings from reading and working through the book 'Java-Script: The Definitive Guide' by D. Flanagan. This was done for educative purposes and improve my javascript skills. 

### Flanagan, D.(2020). Java-Script: The Definitive Guide (seventh edition).

* Interesting chapters: 1 (Introduction), 2 (Lexical structure), 3 (Types, Values and variables), 6 (Objects), 9 (Classes), 10 (Modules), 11 (The javascript standard library), 12 (Iterators and generators), 13 (Asynchronous javascript), 15 (Javascript in webbrowsers), 16 (Server side Javascript with node), [17 (Javascript tools and extensions)]

## Chapter 1: 

* Install node -> open terminal -> [COMMAND] node -> [COMMAND] .help
* generate package.json: npm init
* generate tsconfig: tsc --init
* For ES11, download the nodejs version v14.2 or later
* Expressions, operators, booleans, arrays, functions; all know
* Arrow functions ; kind of new

## Chapter 2:

* Comments in VScode -> CTRL + /
* A javascript identifier must begin with a dollar sign ($), underscore (_) or letters/digits.
* Reserved words: as, export, yield, static, set, etc....
* from, set and target are OK to use as identifiers.
* Unicode escape characters using ASCII characters for trema's/special characters.

## Chapter 3:

* Primitive types - immutable: numbers, strings, booleans, null (primitive value), undefined (primitive value).
* Object types - mutable: All others types, e.g. arrays.
* Automatic garbage collection performed by javascript interpreter.
* Arithmetic with Math.{} (e.g. abs, floor, sqrt, E, PI, log, sin)
* Javascript does not return errors for Overflow or ZeroDivision, it will return Infinity, negative infinity, negative zero.
* Null vs. undefined: Null is a special object that indicates 'no object', undefined indicates values of variables that are not initialized.
* strict equality (===) vs. is equal (==). e.g. null == undefined is true, whilst null === undefined isnt. "0" == 0 also is true.
* let vs. const: they work the same, but for const you MUST initialize the variable, while for let it is okay to say let x; -> x is now undefined.
* const: use for values that are fundamentally unchanging, e.g. physical constants.
* var vs let: multiple differences, e.g. use var outside of function body means a global declaration. for var it is okay to declare the same variable multiple times. Hoisting, before arriving at the var declaration, the definition is moved to the top, meaning the var variable is undefined before arriving at the line where the value is defined -> source of bugs!

## Chapter 4+5 (briefly):

* First defined synthax: ??. a ?? b means pick a, unless it is undefined pick b.
* break statement terminates a for loop.
* continue statement goes to the next iteration in the loop.
* yield statement is similar to return, used for generator functions.
* Generator function are most commonly used to create iterators.  
* throw statement is used when an error occurs that is not handled.
* try/catch/finally statements is used when when exceptions are caught/handled.
* finally is the part that is always executed when handling an exception.
* with is typically handy/clean when working with nested object hierarchies.

## Chapter 6:

* Object: unordered collection of properties.
* Everything in javascript except: strings, numbers, symbols, true, false, null, undefined is an object.
* a = new Array() is the same as a = [].
* Prototypes: object associated with another object. The other object inherits from the prototype.
* Almost all objects have a prototype, but only a relatively small number have a prototype property.
* Object serialization is the process of converting an object's state to a string from which it can later be restored -> JSON.stringify() and JSON.parse().
* Function, RegExp, and Error objects and the undefined value cannot be serialized or restored.
* If a property value cannot be serialized, that property is simply omitted from the stringified output.
* ... is called the spread operator. It is used to copy properties of an existing object into a new object.

## Chapter 7+8:
* The spread operator ('...') is a convenient way to create a shallow copy of an array.
* The spread operator works on any iterable object, including strings.
* a.length = 0 empties an array, getting rid of all present elements.
* Array iterator methods: forEach, map (;passed each element, performs operation and returns new array), filter (;returns subset of the array on which it got invoked), find and findIndex (like index, but stops at first instance found), every and some (return a boolean based on some condition of the array), reduce and reduceRight.
* Arrays can be flattened with flat and flatMap. flat takes a parameter x, with x the number of levels.
* JS functions are hoisted (;declared in a block of JS code and will be defined before the JS interpreter begins to execute any of that code block).
* Arrow function are of the form: const funcName = (x1, x2) => {}, it is a relatively compact synthax.
* In ES2020 you can insert ?. after a function expression and before the open parenthesis in a function invocation in order to invoke the function only of it is not null or undefined. This means f?.(x) is equivalent to (f !== null && f !== undefined) ? f(x) : undefined
* The code that makes up the body of a function is not executed when defined, but rather it is *invoked*.
* When a function is invoked with fewer arguments then declared parameters, the missing parameters are set to their default value, normally `undefined`. Adding a default value manually is done as follows in the book: if(x2 === undefined) a=[];. However, they mention that after ES6 you can define the default value in the function parameters: function f(o,a=[]){}.
* Rest parameters (e.g. -> function f(x,...y)){}) allow us to pass MORE arguments then parameters. It MUST be the last parameters of the declaration. It should not be confused with spread operators for function calls, which works as explaned earlier.
* Javascript using lexical scoping -> use the variable scope of everything that is **defined**, not **invoked**.
* A higher order function is a function that operates on function, taking one or more functions as arguments and returning a new function.


## Chapter 9:
* A factory function is any function which is not a class or constructor that returns a (presumably new) object.
* Add methods to existing classes: Complex.prototype.conj = function() { return new Complex(this.r, -this.i); };
* Inheritance: class EZArray extends Array.
* One of the most common uses of interfaces is that of explicitly enforcing that a class meets a particular contract.
* Interfaces describe the public side of the class, rather than both the public and private side. This prohibits you from using them to check that a class also has particular types for the private side of the class instance.
* For inheritance, use 'extends', for working with interfaces in classes, use 'implements': export class Table extends Database implements ITable.

## Chapter 10:
* Priorly: modularity in JS was based on require(), from ES6 import and export have been the way to define modules.
* In Node, each file is an independent module with a private namespace. Constants, variables, functions, and classes defined in one file are private to that file unless the file exports them.
* Export single object/class/function from file: export Class Database. Alternatively, you can put a single statement at the bottom of the file exporting multiple classes at once: export { Class1, Class2 }  
* Rename imports: import { TestClass as NewName } from "../importfile.js"
* Because code has to be transferred over a typically slow filesystem over the web, static modules are typically not the way to go. We want to dynamically load the code, which is made easy by web browsers using the DOM API to inject a new <script> tag. Rather then using import * as stats from "./stats.js"; you can us: import("./stats.js").then(stats => {let average = stats.mean(data);})

## Chapter 11:
* A Set is an unordered collection of values, create one with 'new Set()'. Though, for javascript this is not entirely true, as the order in which numbers where inserted IS remembered, though it is not index (don't ask for the first number).
* A Set checks based on strict equality (===). This causes different behavior for objects for example (compared to Python). 
`Python sets compare members for equality, not identity, but the trade-off is that Python sets only allow immutable members, like tuples, and do not allow lists and dicts to be added to sets.`
* Sets are optimized for membership testing; checking whether the set contains some values (using .has()).
* Maps can be used for key value pairs.
* ...x.entries() can be used to iterate over all key value pairs in a Map.
* Garbage collection is the process by which the JavaScript interpreter reclaims the memory of objects that are no longer 'reachable' and cannot be used by the program.
* WeakMap and WeakSet do not prevent the key values from being garbage collected.
* Types arrays are all numbers, and allow you to specify the type unlike other JS numbers. Examples include Int8Array(), BigInt64Array(),...
* JSON.stringify() -> create string from JSON. JSON.parse() -> Create JSON from string.

## Chapter 12:
* There are three seperate types to understand iterables in JS: iterable objects (array,maps,sets), the iterator object itself (x[Symbol.iterator]()) and the iteration result that holds the result of each step.
* Generator functions are defined as function*.
* When a generator function is invoked, it does NOT actually execute the function body, but instead returns a generator object.
* Generator object is an iterator.
* Calling next() runs the body of the generator function from the start to the next *yield*. 
* The most common use of generator functions is to create iterators, but the fundamental feature of generators is that they allow for pause of computation, yield intermediate results and resume computation later on.
* The only real practical usecase for generator function has been for handling asyncronous code. However, since JS now has the await and async keywords, there is no practical use case to 'abuse generators in this way'. 


## Chapter 13:
* Examples of asynchronous situations: Timers, (browser) events and network requests.
* Callback function example: setTimeout(checkForUpdates, 60000), checkForUpdates is the callback function, setTimeout is the function that you invoke to register the callback.
* Client side javascript is event driven: the browser waits for some event and then responds to the user's action. 
* Callback functions responding to user actions in browsers are called event handlers or event listeners. They are registered with addEventListener().
* A callback is a function that you write and then pass to some other function. The other function then invokes your function when some (asynchronous) event occurs or when some condition is met.
* Promise.all is used instead of unnecassary sequential promises. 
  let value1 = await getJSON(url1);
  let value2 = await getJSON(url2);
  to 
  let [value1, value2] = await Promise.all([getJSON(url1), getJSON(url2)]);

