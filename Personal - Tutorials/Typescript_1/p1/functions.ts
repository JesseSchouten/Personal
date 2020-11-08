function getSum(n1:number, n2:number){
    return n1 + n2;
}
//console.log(getSum(1,4))

let mySum = function(n1:any, n2:any):number{
    if(typeof n1 == 'string'){
        n1 = parseInt(n1);
    }
    if(typeof n2 == 'string'){
        n2 = parseInt(n2);
    }

    return n1 + n2
}

//console.log(mySum('5',5));

function getName(firstName: string, lastName?: string): string {
    if (lastName == undefined){
        return firstName
    }
    return firstName + ' ' + lastName;
}

//console.log(getName('John', 'Doe'));

function myVoid():void{
    return ;
}