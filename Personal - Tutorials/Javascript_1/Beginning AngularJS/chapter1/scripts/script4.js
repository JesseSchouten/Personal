function equality_operator(){
    var v1 = 10;
    var v2 = '10';
    if (v1 == v2){
        console.log("values are the same");
    } else{
        console.log("values are not the same");
    }
    return;
}

function identity_operator(){
    var v1 = 10;
    var v2 = '10';
    if (v1 === v2){
        console.log("values are the same");
    } else{
        console.log("values are not the same");
    }
    return;
}

// == (equality operator) will attempt to make the datatypes the same before proceeding
// === (identity operator) requires both datatypes to be the same.
//

equality_operator();

identity_operator();