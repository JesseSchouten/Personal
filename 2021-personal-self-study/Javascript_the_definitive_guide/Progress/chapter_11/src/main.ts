const testSet = new Set([2,3,4,52,3,4,5]);
testSet.add(10);
testSet.delete(2);
console.log(testSet);
console.log(`testSet is of size: ${testSet.size}`);

const testSetArray = new Set([[1,2,3]]);
testSetArray.delete([1,2,3]);
console.log(testSetArray);


const testMap = new Map([['1',2],['3',4]]);

const testMap2 = new Map(Object.entries({'1':2,'3':4})); // is the same as testMap

console.log(testMap);
console.log(testMap2);
console.log(testMap.get('1'));
testMap2.set('4',4);
console.log(testMap2);

console.log(...testMap2.entries());


const json = {
    'name':'jesse',
    'age':25
}
const jsonString = JSON.stringify(json);
const jsonStringBack = JSON.parse(jsonString);
console.log(json);
console.log(jsonString);
console.log(jsonStringBack);

let euros = Intl.NumberFormat("nl", {style: "currency", currency:"EUR"});
console.log(euros.format(10));

