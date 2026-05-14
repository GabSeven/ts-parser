// Cannot redeclare block-scoped variable 'x'.
let x = 12
let x = 1

// Curiosamente enquanto o analisador estático mostra esse erro semântico
// quando o node roda, o erro aparece como Sintático:
// let x = 1
//     ^
// SyntaxError: Identifier 'x' has already been declared

var y = 12
var y = 123