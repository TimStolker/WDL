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
* Decorator //TODO
* Type-annotatie Haskell-style //TODO
* Type-annotatie Python-stijl: Ja
* Minstens drie toepassingen van hogere-orde functies:
  * [binary_operation](https://github.com/TimStolker/WDL/blob/27fe3f530ccaa7b728086572317585c9ccc169dc/src/classparser.py#L361)
  * TODO
  * TODO

## Interpreter-functionaliteiten must-haves:
TODO

## Interpreter-functionaliteiten (should/could-haves)
TODO
