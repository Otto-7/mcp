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
    SAST[SAST] --> A["Pattern-based<br/>Поиск опасных паттернов"]
    SAST --> B["Data-flow<br/>Анализ значений переменных"]
    SAST --> C["Taint<br/>Путь данных от источника к приёмнику"]
```
