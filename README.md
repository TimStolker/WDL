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
  * [filter](https://github.com/TimStolker/WDL/blob/c329f224a4f9f83bb4af550fa7d4126e747a59f8/src/Lexer.py#L175)

## Interpreter-functionaliteiten must-haves:
* De interpreter ondersteunt meerdere functies in dezelfde file
* Functie parameters worden meegegeven bij het aanroepen van een functie
* Functies kunnen andere functies aanroepen [voorbeeld](https://github.com/TimStolker/WDL/blob/6cb2b4505c7c52cead0f4b143d1d473af5c9f122/src/codeInput.txt#L7)
* Functie resultaten kunnen worden weergegeven door deze te koppelen aan een variabele en de variabele te printen door ''variabele'+0 ENDE'

## Interpreter-functionaliteiten (should/could-haves)
* Advanced language features:
 * Rekensommen op de correcte manier uitrekenen volgens de wiskundige volgorde (eerste haakjes, dan * en /, dan + en -)
 * Printen door in de globale scope '+0 ENDE' toe te voegen aan een variabele
* Eigen taal

## Hoe te gebruiken
* Variabelen kunnen worden aangemaakt met: ```VAR 'var naam' = 'waarde' ```
* If/else statements kunnen gebruikt worden met: 
```
ALS 'conditie' DANN
'body (1 regel/statement)'
SLA

ALS 'conditie' DANN
'body'
ANDERS
'body'
SLA
```
* While loops kunnen gebruikt worden met:
```
WAHREND 'conditie' WIEDERHOLEN
'body (1 regel/statement)'
NELOHREDEIW
```
* Functies kunnen aagemaakt worden met:
```
FUNKTION 'functie naam' ('var', 'var'){
'body (moet een RETURN 'var' hebben, mag meerdere lijnen zijn)'
}
```
