import { Range2 } from "./RangeOldSkool";

// Here are example uses of this new Range class
let r = new Range2(1,3); // Create a Range object; note the use of new
r.includes(2); // => true: 2 is in the range
r.toString(); // => "(1...3)"
console.log(r.includes(2));

import { Database } from "./Database";

const columns = ['col1','col2'];
const datatypes = new Map([["col1","int"],["col2",'string']])
const db = new Database("server1");

db.printdbInfo();
db.createTable("table1", columns, datatypes);
db.printdbInfo();