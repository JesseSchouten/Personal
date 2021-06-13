const url = 'https://jsonplaceholder.typicode.com/todos/1';

const url2 = 'https://jsonplaceholder.typicode.com/posts';


const testFunc = async () => {
    return "this is a test func!";
}


console.log(setTimeout(testFunc, 1000));//mimic asynchronous code

const cb = (response, input) => {
    console.log(response);
    console.log(input);
    if(response === null){
        return input;
    } else if(input === null){
        return response;
    } 

    return undefined;
}
//using callbacks
const getUrlData = (cb, url) => {
    var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest; 
    let request = new XMLHttpRequest();
    request.open("GET", url);
    request.send();

    request.onload = () => {
        if (request.status === 200){
            cb(null, request.responseText);
        } else {
            cb(request.statusText, null);
        }
    };

    request.onerror = request.ontimeout = function(e){
        cb(e.type,null);
    }
};

//Now a promise based example:



const getData2 = async () => {
    const fetch = require('node-fetch');
    const result = await fetch(url2)
    .then(x => x.json())
    .catch(error => error);
    //console.log(result);
    return result
};
const resultGetData2 = getData2();


const processGetData2 = async (data) => {
    const result = await data;
    console.log(result[0]);
    return result[0];
}
const finalResult = processGetData2(resultGetData2);
