
const a1 = Object.create([]);
a1.push(1);
console.log(a1);

const a2 = [];
a2.push(1);
console.log(a2);

let o = new Object();
let a = new Array();
let d = new Date();
let r = new Map();
r['test'] = 2;
console.log(o);
console.log(a);
console.log(d);
console.log(r);

let o2 = Object.create(null);
let o3 = Object.create(Object.prototype);
console.log(o);
console.log(o2);
console.log(o3); //is the same as regularly defining the object

let o4 = {'test' : "dont change this value"};
let o5 = Object.create(o4);
console.log(o5);
o5['test2']= 'yeah';
console.log(o5);
console.log(o5.test); //inherited from o4
console.log(o5?.test3); //optional element test3 for object, does not exist => undefined 

let o6 = { x: 1 };
"x" in o6 // => true: o has an own property "x"
"y" in o6 // => false: o doesn't have a property "y"
"toString" in o6 // => true: o inherits a toString property

let o7 = { x: 1 };
o7.hasOwnProperty("x") // => true: o has an own property x
o7.hasOwnProperty("y") // => false: o doesn't have a property y
o7.hasOwnProperty("toString") // => false: toString is an inherited property

let o8 = {x: 1, y: 2, z: 3}; // Three enumerable own properties
o8.propertyIsEnumerable("toString") // => false: not enumerable
for(let p in o8) { // Loop through the properties
    console.log(p); // Prints x, y, and z, but not toString
}

for(let p in o8) {
    if (!o.hasOwnProperty(p)) continue; // Skip inherited properties
};

let o9 = {x: 1, y: {z: [false, null, ""]}}; // Define a test object
let s = JSON.stringify(o9); // s == '{"x":1,"y":{"z":[false,null,""]}}'
let p = JSON.parse(s); // p == {x: 1, y: {z: [false, null, ""]}}

let o10 = {"item1": 1,
        "item2":2      
};
let o11 = {"item3": 1,
        "item4":2      
};
let o12 = {"item3": 1,
        "item4":2      
};

let spreadOperatorTest = {...o10, ...o11, ...012};
console.log(o10);
console.log(spreadOperatorTest);
