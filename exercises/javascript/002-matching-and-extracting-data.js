const regex = /[0-9]+/g;

const text = "My 2 favorite numbers are 19 and 42";

// match() con flag g (global, toda la cadena)
const result = text.match(regex);

console.log(result)

// matchAll() - más moderno y potente
const text2 = "precio: 100, precio: 200";

const result2 = [...text2.matchAll(regex)];
console.log(result2.map(m => m[0]));
