var __spreadArray = (this && this.__spreadArray) || function (to, from) {
    for (var i = 0, il = from.length, j = to.length; i < il; i++, j++)
        to[j] = from[i];
    return to;
};
var a = [1, 2, 3];
var b = __spreadArray(__spreadArray([0], a), [4]);
console.log(b);
var c = [1, 2, 3, 4, 5, 6];
console.log.apply(console, c);
var a1 = new Array();
var a2 = new Array(10); // of length 10
console.log(a1);
console.log(a2);
var a3 = Array.of(1);
console.log(a3);
var data = [1, 2, 3, 4, 5], sum = 0;
// Compute the sum of the elements of the array
data.forEach(function (value) { sum += value; }); // sum == 15
console.log(sum);
console.log(c.map(function (x) { return 2 * x; }));
data.forEach(function (value) { return value += value + 2; });
console.log(data);
// Now increment each array element
data.forEach(function (v, i, a) { a[i] = v + 1; }); // data == [2,3,4,5,6]
console.log(data);
console.log(data.filter(function (x) { return x > 4; }));
console.log([1, 2, 3, [4, 5, 6, [7, 8, 9]]].flat()); // data == [ 1, 2, 3, 4, 5, 6, [ 7, 8, 9 ] ]
console.log([1, 2, 3, [4, 5, 6, [7, 8, 9]]].flat(2)); // data == [ 1, 2, 3, 4, 5, 6, [ 7, 8, 9 ] ]
