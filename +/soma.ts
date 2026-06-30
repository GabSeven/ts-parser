var x = 0

function x_att(y) {
    x = y
}

function x1() {
    x_att(1)
}

function x2() {
    x_att(2)
}

function x3() {
    x_att(3)
}

x1()
console.log(x)
x3()
console.log(x)
x1()
console.log(x)