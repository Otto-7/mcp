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
    SAST["<span style='font-size:18px'><b>SAST</b></span>"] --> A["<span style='font-size:16px'><b>Pattern-based</b></span><br/><br/>Поиск опасных паттернов"]
    SAST --> B["<span style='font-size:16px'><b>Data-flow</b></span><br/><br/>Анализ значений переменных"]
    SAST --> C["<span style='font-size:16px'><b>Taint</b></span><br/><br/>Путь данных от источника к приёмнику"]
```
Все три метода опираются на основу (Basis), которая включает:
```mermaid
%%{init: {'theme':'base', 'themeVariables': {
  'primaryColor': '#f0f0f0',
  'primaryTextColor': '#333333',
  'primaryBorderColor': '#999999',
  'lineColor': '#999999',
  'fontSize': '14px'
}}}%%
flowchart TD
    B["<b>Basis (основа)</b>"]
    B --> S["<b>Syntax</b><br/><br/>структура кода, AST"]
    B --> SI["<b>Semantic info</b><br/><br/>типы, связи"]
    B --> AN["<b>Annotations</b><br/><br/>информация о функциях и переменных"]

    S --> M["<b>Три метода анализа</b>"]
    SI --> M
    AN --> M

    M --> P["<b>Pattern-based</b><br/><br/>поиск опасных паттернов"]
    M --> D["<b>Data-flow</b><br/><br/>значения переменных"]
    M --> T["<b>Taint</b><br/><br/>поток данных"]
```
