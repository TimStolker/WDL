# WDL

# Interpreter checklist
## Gekozen taal
Eigen taal (Wütender Deutscher Language)

## Turing-compleet omdat
* Ondersteunt if/else statements waarbinnen je andere functies kan aanroepen
* Ondersteunt while-loops met condities
* Ondersteunt meerdere functies per file
* Ondersteunt recursieve functies

## Bevat:
* Class met inheritance [TokensEnum](https://github.com/TimStolker/WDL/blob/27fe3f530ccaa7b728086572317585c9ccc169dc/src/classtoken.py#L8)
* Object-printing voor elke class
  * [Token class](https://github.com/TimStolker/WDL/blob/27fe3f530ccaa7b728086572317585c9ccc169dc/src/classtoken.py#L53)
  * [Alle node classes](https://github.com/TimStolker/WDL/blob/27fe3f530ccaa7b728086572317585c9ccc169dc/src/classparser.py#L4)
* Decorator [smart_divide](https://github.com/TimStolker/WDL/blob/9f0d0e977541fd81cff48cb0825f3eeb894042e6/src/classinterpreter.py#L8)
* Type-annotatie Haskell-style: ja
* Type-annotatie Python-stijl: ja
* Minstens drie toepassingen van hogere-orde functies:
  * [binary_operation](https://github.com/TimStolker/WDL/blob/27fe3f530ccaa7b728086572317585c9ccc169dc/src/classparser.py#L361)
  * [smart_divide](https://github.com/TimStolker/WDL/blob/9f0d0e977541fd81cff48cb0825f3eeb894042e6/src/classinterpreter.py#L8)
  * TODO

## Interpreter-functionaliteiten must-haves:
TODO

## Interpreter-functionaliteiten (should/could-haves)
TODO
