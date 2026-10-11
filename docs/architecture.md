```mermaid
flowchart LR
    subgraph External1["Входные данные"]
        A[SARIF]
    end
        B[Обработка данных]
        C[Интерфейс для LLM]
    end
    D[LLM]
    A --> B
    B --> C
    C --> D
```
