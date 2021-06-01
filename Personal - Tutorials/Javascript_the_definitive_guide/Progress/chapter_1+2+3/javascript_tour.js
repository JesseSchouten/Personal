// Values can be assigned to variables with an = sign
x = 0; // Now the variable x has the value 0
x // => 0: A variable evaluates to its value.

// JavaScript supports several types of values
x = 1; // Numbers.
x = 0.01; // Numbers can be integers or reals.
x = "hello world"; // Strings of text in quotation marks.

x = 'JavaScript'; // Single quote marks also delimit strings.
x = true; // A Boolean value.
x = false; // The other Boolean value.
x = null; // Null is a special value that means "no value."
x = undefined; // Undefined is another special value like null.

const y1 = x ? 3 : 5; // Undefined check
console.log(y1);

const y2 = x ?? 5; // nullish coalescing, available from ES11 (earlier available in typescript) 
console.log(y2);

let book = {
    topic: "Javascript",
    pages: 700,
    edition: 7
};

console.log(`This is a book about ${book.topic}`);

console.log(book.contents?.ch01?.sect1); // => undefined: contents is not part of the book object.

x = 10;
y = 9;
console.log(!(x===y));

function testFunc(x){
    return x+10;
};
console.log(testFunc(20));  

function plusOne(x){
    return x + 1;
};
console.log(plusOne(1));

const plusOneArrowFunction = x => x + 1;
console.log(plusOneArrowFunction(1)); 

$testvar = 10;
console.log($testvar);

console.log("caf\u00e9");

console.log(Math.abs(-10));

console.log(-1000000000000000000000000000); // => -e+27
console.log(10000000000000000000000000000); // => -1e+28
console.log(100/0); // => Infinity
console.log(Number.MAX_VALUE*2); //=> Infinity; overflow

const x2 = Number.NaN;
if (Number.isNaN(x2)){ // do NOT do x === NaN
    console.log("x is a NaN value");
};

// Date build-in
let timestamp = Date.now();
let now = new Date();
let ms = now.getTime();
let iso = now.toISOString();
console.log(`timestamp: ${timestamp}, now: ${now}, ms:${ms}, iso:${iso}`);

//Regexp
let text = 'testing: 1,2,3';
let pattern = /\d+/g;
console.log(pattern.test(text));
console.log(text.search(pattern)); //position of the first match.

console.log([100].toString());
