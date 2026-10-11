SAST — анализ исходного кода без запуска. Ищет уязвимости и ошибки по таким признакам как: паттерн, структура, поток данных.
```mermaid
%%{init: {'theme':'base', 'themeVariables': {
  'primaryColor': '#f0f0f0',
  'primaryTextColor': '#333333',
  'primaryBorderColor': '#999999',
  'lineColor': '#999999',
  'fontSize': '14px'
}}}%%
flowchart TD
    subgraph Methods["<b>Методы анализа</b>"]
        direction LR
        P["<b>Pattern-based</b><br/>поиск паттернов"]
        D["<b>Data-flow</b><br/>значения переменных"]
        T["<b>Taint</b><br/>поток данных"]
        P ~~~ D ~~~ T
    end

    subgraph Basis["<b>Basis</b>"]
        direction LR
        S["<b>Syntax</b><br/>структура кода, AST"]
        SI["<b>Semantic info</b><br/>типы, связи"]
        AN["<b>Annotations</b><br/>о функциях и переменных"]
        S ~~~ SI ~~~ AN
    end

    Methods --> Basis
```
Анализатор имеет встроенные правила
Используемый в проекте стат анализатор - Svace.
Svacer − это комплексный пользовательский интерфейс просмотра предупреждений, сервер хранения и управления результатами анализа. Поддерживает многопользовательский режим и различные фильтры данных

## Правило анализа

Правило — инструкция анализатору: что искать и как назвать проблему.
Содержит id, описание, критичность, помощь по исправлению.

Finding — это одно срабатывание правила. Основная единица данных, с которой работает сервер.

1) Анализатор читает код.
2) Строит AST.
3) Сопоставляет AST с паттернами из правил.
4) Если паттерн совпал — создаёт finding.
5) Записывает его в SARIF в массив results.

Поля у finding:
ruleId
message.text
level
locations
codeFlows
fingerprints
properties

## Уровни критичности 
Critical 
Major 
Minor 
Normal 

У Svace находятся в разделе properties.severity

## Типы findings по истинности

