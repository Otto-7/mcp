```mermaid
flowchart LR
    subgraph External1["Входные данные"]
        A[SARIF]
    end
    subgraph Core["MCP"]
        B[Обработка данных]
        C[Интерфейс для LLM]
    end
    subgraph 
        D[LLM]
    end
    A --> B
    B --> C
    C --> D
```
