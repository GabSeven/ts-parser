# TypeScript Analyzer
Aluno: Gabriel Rodrigues Gomes - RA139159

## Processo
O analyzer foi desenvolvido focando primeiro na gramática e depois no algoritmo em si.
"Recomecei" algumas vezes o código até que decidi ler a documentação da biblioteca Lark
para tem uma noção melhor de como realizar o trabalho.
Notei que poderia utilizar Classes da própria biblioteca e mudei algumas coisas na
gramática me inspirando na gramática de python que a documentação apresenta de forma
que ela pudesse utilizaro LALR parser.

### Tabela de Símbolos
Um detalhe da forma que o Typescript é compilados, é que a tabela de símbolos é gerada
antes da execução do código (através do .d.ts - declare file), o leva a erros semânticos
como o uso antes da definição mas que no caso de variáveis do tipo var, não são erros
"fatais" que impedem o funcionamento do código.

## Erros 
### ts2300.ts
Dois elementos (de "espécies" diferentes - let, var, function) tentando usar o mesmo
nome da tabela de símbolos

### ts2304.ts
Erro de quando um nome não está na tabela de símbolos (tanto var, let, function, const, ...)

### ts2393.ts
Implementação de duas funções com o mesmo nome

### ts2448.ts
Variável do tipo let usada antes de ser declarada

### ts2451.ts
Variável do tipo let redeclarada no mesmo escopo de bloco

### ts2454.ts
Variável do tipo var usada antes de ser atribuída
**Detalhe Importante:** o erro é por não ser atribuída, diferente do let que é por não ser definida.


### tiposDiferentes
O código tem suporte para mostrar atribuições de tipos diferentes como erro,
mas a gramática não visto que o escopo do trabalho não abrangia diferentes tipos.