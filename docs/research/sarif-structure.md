# SARIF (Static Analysis Results Interchange Format) - это формат на основе JSON для вывода результатов статического анализа.

## План:
- [Структура SARIF 2.1.0](#структура-sarif-210)
- [Значимые поля](#значимые-поля)
- [Нормализация](#нормализация)
- [Дедупликация](#дедупликация)
- [Группировка](#группировка)
 
## Структура SARIF 2.1.0

### Logs and runs

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
### Property bag — объект `properties` 
Если в спецификации SARIF нет подходящего элемента, данные помещаются в раздел properties.
Поля для Svace: severity, cwe, reliability, lang, mtid, origin, svacer_checker_id, tool, warnClass. Для анализа LLM нужно только правило severity.
```json
{
  "version": "2.1.0",
  "$schema": "https://docs.oasis-open.org/sarif/sarif/v2.1.0/errata01/os/schemas/sarif-schema-2.1.0.json",
  "runs": [
    {
      "tool": {
        "driver": {
          "informationUri": "https://svacer.ispras.ru/mediawiki",
          "name": "Svacer",
          "rules": [
            {
              "id": "SvEng.CXX.BUFFER_OVERLAP/SvEng.BO.65",
              "name": "BUFFER_OVERLAP",
              "shortDescription": {
                "text": "BUFFER_OVERLAP"
              },
              "properties": {
                "cwe": [
                  {
                    "description": "A stack-based buffer overflow condition...",
                    "name": "121"
                  }
                ],
                "lang": "CXX",
                "mtid": "SvEng.BO.65",
                "origin": "builtin",
                "reliability": "Low",
                "severity": "Critical",
                "svacer_checker_id": "BUFFER_OVERLAP",
                "tool": "SvEng",
                "warnClass": "BUFFER_OVERLAP"
              }
            }
          ]
        }
      }
    }
  ]
}
```

### Results 
Результаты (findings) представляют собой проблемы — условия, которые могут снизить качество кода. Некоторые результаты могут быть чисто информационными.
```json
"results": [
        {
          "ruleId": "SvEng.CXX.BUFFER_OVERLAP/SvEng.BO.65",
          "ruleIndex": 0,
          "kind": "notApplicable",
          "level": "error",
          "message": {
            "text": "Memory areas of 'memcpy' function arguments '(*s-\u003ewindow)[wsize]' and 's-\u003ewindow' are overlapping at deflate.c:287. Consider using 'memmove' function instead."
          },
          "locations": [
            {
              "physicalLocation": {
                "artifactLocation": {
                  "uri": "/.build/deflate.c",
                  "index": 0
                },
                "region": {
                  "startLine": 287,
                  "sourceLanguage": "CXX"
                }
              },
              "logicalLocations": [
                {
                  "fullyQualifiedName": "fill_window",
                  "kind": "function"
                }
              ]
            }
          ],
          "fingerprints": {
            "invariant": "7P6Pei16cq9IlDbvpqZ5WQ"
          },
          "partialFingerprints": {
            "details": "b17829f46421a9bd763acfc31fb7f63ae45768b3"
          },
          "codeFlows": [
            {
              "message": {
                "text": "function call"
              },
              "threadFlows": [
                {
                  "locations": [
                    {
                      "location": {
                        "physicalLocation": {
                          "artifactLocation": {
                            "uri": "/.build/deflate.c"
                          },
                          "region": {
                            "startLine": 287,
                            "startColumn": 13
                          }
                        },
                        "message": {
                          "text": "function call"
                        }
                      }
                    }
                  ],
                  "message": {
                    "text": "function call"
                  }
                }
              ]
            }
          ],
          "properties": {
            "action": "Undecided",
            "checker_reliability": "Low",
            "checker_severity": "Critical",
            "comments": [
              {
                "text": "Перекрытия не происходит - память копируется со сдвигом wsize в количестве (wsize - more) байтов, где more \u003e= 0.",
                "createdBy": "d.kaluh",
                "createTs": "2026-02-02T10:26:10.39938Z"
              }
            ],
            "details": "b17829f46421a9bd763acfc31fb7f63ae45768b3",
            "invariant": "7P6Pei16cq9IlDbvpqZ5WQ",
            "lang": "CXX",
            "mtid": "SvEng.BO.65",
            "origFunc": "fill_window",
            "review_ts": "2026-02-02T10:25:06Z",
            "reviewed_by": "d.kaluh",
            "severity": "Unspecified",
            "status": "False Positive",
            "tags": null,
            "tool": "SvEng",
            "warnClass": "BUFFER_OVERLAP"
          }
        }
```
### Message
Сообщения SARIF представлены отдельным объектом — message. 
```json
 "message": {
            "text": "Memory areas of 'memcpy' function arguments '(*s-\u003ewindow)[s-\u003ew_size]' and 's-\u003ewindow' are overlapping at deflate.c:1774. Consider using 'memmove' function instead."
          }
```

### Rule identifier
Идентификатор — это код, а не человекочитаемая строка. У такого кода два преимущества. Во-первых, его легко искать в интернете: короткий код даёт точечный результат, а не тысячи совпадений. Во-вторых, он не привязан к языку: не нужно переводить название правила на разные языки.
```json
{
          "ruleId": "SvEng.CXX.BUFFER_OVERLAP/SvEng.BO.65"
}
```
### Level
Свойство `result.level` указывает, насколько серьёзна проблема:

- **`"error"`** — серьёзная проблема;
- **`"warning"`** — проблема;
- **`"note"`** — незначительная проблема или возможность улучшить код.
```json
{
          "ruleId": "SvEng.CXX.BUFFER_OVERLAP/SvEng.BO.65",
          "level": "error"
}
```

### Locations
Место в коде, где инструмент обнаружил результат, называется result location. SARIF представляет местоположения результатов с помощью необязательного свойства `result.locations` — массива объектов location, который почти всегда содержит ровно один элемент.

#### Physical and logical locations
SARIF поддерживает два вида местоположений: физические и логические. Физическое местоположение описывает место относительно некоторого программного артефакта — например, диапазон строк в исходном файле или диапазон байтов в исполняемом файле. Логическое местоположение описывает место по имени, без привязки к программному артефакту, — например, имя метода внутри класса внутри пространства имён.

SARIF поддерживает логические местоположения по двум причинам:
1. Самое важное: инструменты анализа бинарных файлов не всегда располагают информацией о физическом местоположении (хотя она может быть доступна, например, если есть файл символов). Такие инструменты вынуждены сообщать, скажем, имя метода; они не могут сказать, в каком файле метод был определён.
2. Даже если физическое местоположение доступно, инструменту бывает полезно сообщить, что проблема на строке 287 внутри функции fill_window.
```json
"locations": [
            {
              "physicalLocation": {
                "artifactLocation": {
                  "uri": "/.build/deflate.c",
                  "index": 0
                },
                "region": {
                  "startLine": 287,
                  "sourceLanguage": "CXX"
                }
              },
              "logicalLocations": [
                {
                  "fullyQualifiedName": "fill_window",
                  "kind": "function"
                }
              ]
            }
          ]
```

### Artifacts
Артефакт - последовательность байтов, адресуемая через URI. Примеры: физический файл в файловой системе, исходный файл.
Почти каждый результат указывает местоположение, и эти местоположения часто являются физическими, которые, в свою очередь, содержат объекты artifactLocation:
```json
 "locations": [
            {
              "physicalLocation": {
                "artifactLocation": {
                  "uri": "/.build/deflate.c",
                  "index": 0
                },
                "region": {
                  "startLine": 287,
                  "sourceLanguage": "CXX"
                }
              },
              "logicalLocations": [
                {
                  "fullyQualifiedName": "fill_window",
                  "kind": "function"
                }
              ]
            }
          ]
```
SARIF позволяет предоставить дополнительную информацию о каждом артефакте с помощью свойства run.artifacts, значение которого представляет собой массив объектов artifact:
```json
{
  "runs": [
    {
      "artifacts": [
        {
          "location": {
            "uri": "/.build/deflate.c"
          },
          "length": 0,
          "contents": {
            "text": ""
          }
        }
      ]
    }
  ]
}
```
Также есть возможность встроить содержимое каждого артефакта в файл SARIF, что позволит пользователям просматривать результаты в контексте, даже если они не входят в состав анализируемой кодовой базы:
```json
"contents": {
            "text": ""
          }
```
#### Linking results to artifacts
SARIF связывает finding с артефактом через artifactLocation.index:
```json
"artifactLocation": {
  "uri": "/.build/deflate.c",
  "index": 0
}
```
"index": 0 означает: «Чтобы найти больше информации об артефакте в этом месте, посмотрите объект artifact под индексом 0 в массиве run.artifacts».

## Значимые поля
Критерии:
1. Идентификация проблемы
2. Контекст и локация
3. Трасса

Поля:
- `ruleId` — тип ошибки
- `level` — уровень критичности
- `message.text` — описание
- `locations[0].physicalLocation.artifactLocation.uri` — файл
- `locations[0].physicalLocation.region.startLine` — строка
- `codeFlows` — трасса
   
## Нормализация
Это значит вложенную структуру преобразовать в словарь.
```
import json
json = json.loads('{ "A": { "B": { "C": {"D": "yes"} } } }')

if 'A' in json:
    if 'B' in json['A']:
        if 'C' in json['A']['B']:
            print(json['A']['B']['C'])
```

Реализовано в парсере, но достаточно ли этого или надо выделить в отдельный файл? 

## Дедупликация
Дедупликация - это процесс устранения дубликатов записей об одних и тех же ошибках.

Причины:
- Использование нескольких анализаторов
- При дублировании кода
- Повторные запуски накапливают результаты

В данном проекте дубликаты - это ошибки с одновременно одинаковыми: ruleId, file, line. 

Решение:
1) Создать отдельный файл deduplicator.py ИЛИ добавить в parser.py
2) Применить set() для ф-ции deduplicate_errors()

## Группировка
[Группировка списков](https://labex.io/ru/tutorials/python-how-to-efficiently-group-a-python-list-based-on-a-given-function-417802) – это процесс организации элементов списка в категории на основе определенной характеристики или функции.
(Понадобится на этапе создания mcp-инструментов) 
## Источники
- [Спецификация SARIF 2.1.0 — OASIS](https://docs.oasis-open.org/sarif/sarif/v2.1.0/os/sarif-v2.1.0-os.html)
- [Документация Svacer](https://svacer.ispras.ru/mediawiki/index.php?title=Svacer)
- [Microsoft SARIF Tutorials](https://github.com/microsoft/sarif-tutorials/blob/main/README.md#contents)
