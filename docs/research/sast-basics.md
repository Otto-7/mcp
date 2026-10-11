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

### Примеры из SARIF

| id | Описание | Уровень |
|---|---|---|
| B608 | Possible SQL injection | error |
| B101 | Use of assert detected | note |
| ... | ... | ... |

### Где в SARIF

Правила лежат в `runs[0].tool.driver.rules`.
Findings ссылаются на правила через поле `ruleId` в `results`.
