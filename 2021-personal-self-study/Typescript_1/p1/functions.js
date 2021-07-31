function getSum(n1, n2) {
    return n1 + n2;
}
//console.log(getSum(1,4))
var mySum = function (n1, n2) {
    if (typeof n1 == 'string') {
        n1 = parseInt(n1);
    }
    if (typeof n2 == 'string') {
        n2 = parseInt(n2);
    }
    return n1 + n2;
};
//console.log(mySum('5',5));
function getName(firstName, lastName) {
    if (lastName == undefined) {
        return firstName;
    }
    return firstName + ' ' + lastName;
}
//console.log(getName('John', 'Doe'));
function myVoid() {
    return;
}
