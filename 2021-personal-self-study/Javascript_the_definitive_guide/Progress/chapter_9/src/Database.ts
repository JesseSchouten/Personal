import { Table } from "./Table";

export class Database {
    serverName: string;
    table: Array<Table>;

    constructor(serverName){
        this.serverName = serverName;
        this.table = new Array;
    }

    createTable (name:string, columns: Array<string>, dataType: Map<string,string>){
        const newtable = new Table(this.serverName, name, columns, dataType);
        this.table.push(newtable);
    }

    printdbInfo(){
        console.log(`Servername: ${this.serverName}`);
        const numberOfTables = this.table.length ?? 0;
        console.log(`Number of tables: ${numberOfTables}`);
    }
}