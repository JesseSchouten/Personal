import { Database } from "./Database";

export interface ITable {
    tableName: string;

    printTableInfo(): void;
}
export class Table  implements ITable {
    name: string;
    columns: Array<string>;
    dataType: Map<string, string>;

    constructor(serverName: string, name:string, columns: Array<string>, dataType: Map<string,string>){
        //super(serverName);
        this.name = name;
        this.columns = columns;
        this.dataType = dataType;
    }

    get tableName(){
        return this.tableName;
    }

    printTableInfo(){
        console.log(this.tableName);
    }
}