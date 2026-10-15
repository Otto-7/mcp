flowchart TB
    Svace["Svace"]
    LLM["LLM"]

    subgraph System["MCP-сервер"]
        Parser
        Normalizer
        Server
    end

    Svace --> Parser
    Server --> LLM
