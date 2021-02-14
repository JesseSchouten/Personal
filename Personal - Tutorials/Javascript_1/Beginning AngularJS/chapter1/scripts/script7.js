var Array = [];

Array[0] = 0;

console.log(Array);

//Callbacks
var myFunctionReference = function(){
    console.log("Message");
};

myFunctionReference();
myFunctionReference;
myFunctionReference();
console.log(myFunctionReference);

var actionsToTakeWhenServerResponds = function(){
    console.log("Server responded, take action");
}

function communicateWithServer(callback){
    callback();
}

communicateWithServer(actionsToTakeWhenServerResponds);


