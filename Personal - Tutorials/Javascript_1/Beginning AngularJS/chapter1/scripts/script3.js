function test(){
    var1 = 30;
    console.log(var1);
    let var2 = 30;
    console.log(var2);
    console.log(var3);
}

let var1 = 10; //improvement to var declarations, can be updated but not re-declared.
var var2 = 20; //globally scoped, can be re-declared and updated (mutable).
const var3 = 30; // immutable

test();

console.log(var1);