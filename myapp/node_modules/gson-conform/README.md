# json-conform

`npm install gson-conform --save`


```js
const gc = require("gson-conform");

const array = gc.asArray(anything);
// [anything]

gc.forEach(arrayOrObject, callback(value, key, parent) {});

const keyInData = gc.keyOf(arrayOrObject, valueToFind);
// *

const allKeys = gc.keys(anything);
// []

const allValues = gc.values(anything);
// []
```