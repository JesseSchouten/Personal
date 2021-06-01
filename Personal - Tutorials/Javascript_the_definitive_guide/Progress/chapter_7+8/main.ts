let a = [1,2,3];
let b = [0, ...a, 4];

console.log(b);

let c = [1,2,3,4,5,6];
console.log(...c);

let a1 = new Array();
let a2 = new Array(10); // of length 10

console.log(a1);
console.log(a2);

let a3 = Array.of(1);

console.log(a3);

let data = [1,2,3,4,5], sum = 0;
// Compute the sum of the elements of the array
data.forEach(value => { sum += value; }); // sum == 15
console.log(sum);
console.log(c.map(x=>2*x));

data.forEach(value=> value+=value+2);
console.log(data);

// Now increment each array element
data.forEach(function(v, i, a) { a[i] = v + 1; }); // data == [2,3,4,5,6]
console.log(data);

console.log(data.filter(x=>x>4));

console.log([1,2,3,[4,5,6,[7,8,9]]].flat()); // data == [ 1, 2, 3, 4, 5, 6, [ 7, 8, 9 ] ]

console.log([1,2,3,[4,5,6,[7,8,9]]].flat(2)); // data == [ 1, 2, 3, 4, 5, 6, 7, 8, 9  ]

const sumfunc = function fsum(x,y){
    return x + y;
}
console.log(sumfunc(2,4));

const sumfuncArrow = (x,y) => {
    return x + y;
};
console.log(sumfuncArrow(2,4));

let scope = "global scope"; // A global variable
const checkscope = function () {
    let scope = "local scope"; // A local variable
        function f() { return scope; } // Return the value in scope here
    return f;
}
let s = checkscope()(); // What does this return?
console.log(s);