"use strict";
// Linhas com e sem ; no final
// declaracao de var sem definir
var a1;
let b = 12;
// print de variavel declarada mas nao definida (undefined)
console.log(a1);
{
    // declaracao de mais de uma variavel na mesma linha
    // var pode ser redeclarado sem receber valor
    var a1, a2 = 12;
    var a3 = 1, a4 = 5, a5, a6 = 12;
    // redeclaracao de let em bloco de escopo
    let b = 200;
    {
        b = 1;
    }
    console.log(b); // 1
}
console.log(b); // 12
// atribuição
a1 = 200;
function f1() {
    function f1_1() {
    }
    // call de funcao interna
    f1_1();
    function f1_2() {
        // acesso de variável em escopo maior
        a1 = 1;
        var v1 = 12;
    }
    f1_2();
    {
        function f1_3() {
            let a2 = 12;
            console.log(a2);
        }
        f1_3();
    }
}
f1();
console.log(a1); // 1
{
    var lol = 1500;
}
console.log(lol);
