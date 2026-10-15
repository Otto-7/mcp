flowchart LR
    subgraph System["MCP-сервер"]
        Parser --> Normalizer --> Server
    end
    Svace --> Parser
    Server --> LLM
