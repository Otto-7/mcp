SARIF (Static Analysis Results Interchange Format) - это формат на основе JSON для вывода результатов статического анализа.

Документация
- https://docs.oasis-open.org/sarif/sarif/v2.1.0/os/sarif-v2.1.0-os.html
- https://svacer.ispras.ru/mediawiki/index.php?title=Svacer

- Структура SARIF 2.1.0
- Значимые поля
- Нормализация
- Дедупликация
- Группировка

## Логи и прогоны

Свойство $schema содержит URI схемы SARIF. Это позволяет средам разработки выполнять проверку схемы (например, подчеркивать неправильно написанные названия свойств). 
```json
{
  "version": "2.1.0",
  "$schema": "https://docs.oasis-open.org/sarif/sarif/v2.1.0/errata01/os/schemas/sarif-schema-2.1.0.json"
}
```

Файл журнала содержит массив из одного или нескольких запусков. Каждый прогон представляет собой отдельный вызов одного инструмента анализа, и в описании прогона должен быть указан инструмент, с помощью которого он был выполнен.

```json
{
  "version": "2.1.0",
  "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0-rtm.4.json",
  "runs": [
    {
      "tool": {
        "driver": {
          "informationUri": "https://svacer.ispras.ru/mediawiki",
          "name": "Svacer"
        }
      }
    }
  ]
}
```
