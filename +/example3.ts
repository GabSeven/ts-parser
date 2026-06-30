function f1() {
    function f1_1() {
        
    }
    // call de funcao interna
    f1_1()

    function f1_2() {
        // acesso de variável em escopo maior
        a1 = 1;
        var v1 = 4;
    } 

    f1_2()
    {
        function f1_3() {
            let a2 = 30;
            console.log(a2)
            
        }
        f1_3()
    }
}

f1()