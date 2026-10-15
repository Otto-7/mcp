SARIF (Static Analysis Results Interchange Format) - это формат на основе JSON для вывода результатов статического анализа.

Документация
- https://docs.oasis-open.org/sarif/sarif/v2.1.0/os/sarif-v2.1.0-os.html
- https://svacer.ispras.ru/mediawiki/index.php?title=Svacer

- Структура SARIF 2.1.0
- Значимые поля
- Нормализация
- Дедупликация
- Группировка

## Logs and runs

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
## Property bag — объект `properties` 
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

## Results 
Результаты представляют собой проблемы — условия, которые могут снизить качество кода. Некоторые результаты могут быть чисто информационными.
```json
{
          "ruleId": "SvEng.CXX.BUFFER_OVERLAP/SvEng.BO.65",
          "ruleIndex": 0,
          "kind": "notApplicable",
          "level": "error",
          "message": {
            "text": "Memory areas of 'memcpy' function arguments '(*s-\u003ewindow)[s-\u003ew_size]' and 's-\u003ewindow' are overlapping at deflate.c:1774. Consider using 'memmove' function instead."
          },
          "locations": [
            {
              "physicalLocation": {
                "artifactLocation": {
                  "uri": "/.build/deflate.c",
                  "index": 0
                },
                "region": {
                  "startLine": 1774,
                  "sourceLanguage": "CXX"
                }
              },
              "logicalLocations": [
                {
                  "fullyQualifiedName": "deflate_stored",
                  "kind": "function"
                }
              ]
            }
          ],
          "fingerprints": {
            "invariant": "eo3cL51uYoT3HC29ExoP3A"
          },
          "partialFingerprints": {
            "details": "44f65d349fca4d2d47ec144ff5fd25682b9ffba1"
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
                            "startLine": 1774,
                            "startColumn": 17
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
                "text": "buffer overlap не происходит, так как реализация zmemcpy(dest, src, size), принимает size = s-\u003estrstart - s-\u003ew_size и копирует побайтно во внтуренней реализации. Таким образом, хоть это и один буфер, но ни в какой момент при сохранении внутреннего инварианта не происходит пересечения.",
                "createdBy": "p.gubanov",
                "createTs": "2026-03-05T15:44:35.941077Z"
              }
            ],
            "details": "44f65d349fca4d2d47ec144ff5fd25682b9ffba1",
            "invariant": "eo3cL51uYoT3HC29ExoP3A",
            "lang": "CXX",
            "mtid": "SvEng.BO.65",
            "origFunc": "deflate_stored",
            "review_ts": "2026-03-05T15:41:52Z",
            "reviewed_by": "p.gubanov",
            "severity": "Unspecified",
            "status": "False Positive",
            "tags": null,
            "tool": "SvEng",
            "warnClass": "BUFFER_OVERLAP"
          }
        }
```
## Message
Сообщения SARIF представлены отдельным объектом — message. 
```json
 "message": {
            "text": "Memory areas of 'memcpy' function arguments '(*s-\u003ewindow)[s-\u003ew_size]' and 's-\u003ewindow' are overlapping at deflate.c:1774. Consider using 'memmove' function instead."
          }
```

## Rule identifier
Идентификатор — это код, а не человекочитаемая строка. У такого кода два преимущества. Во-первых, его легко искать в интернете: короткий код даёт точечный результат, а не тысячи совпадений. Во-вторых, он не привязан к языку: не нужно переводить название правила на разные языки.
```json
{
          "ruleId": "SvEng.CXX.BUFFER_OVERLAP/SvEng.BO.65"
}
```
## Level
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

## Locations
Место в коде, где инструмент обнаружил результат, называется result location. SARIF представляет местоположения результатов с помощью необязательного свойства `result.locations` — массива объектов location, который почти всегда содержит ровно один элемент.

### Physical and logical locations
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

## Artifacts
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
### Linking results to artifacts
SARIF связывает finding с артефактом через artifactLocation.index:
```json
"artifactLocation": {
  "uri": "/.build/deflate.c",
  "index": 0
}
```
"index": 0 означает: «Чтобы найти больше информации об артефакте в этом месте, посмотрите объект artifact под индексом 0 в массиве run.artifacts».
