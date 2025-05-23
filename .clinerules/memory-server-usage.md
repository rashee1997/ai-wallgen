## Brief overview
This rule set outlines the preferred usage of the `memory-mcp-server` for enhanced context management and task execution. These are global guidelines applicable to all tasks.

## Development workflow
- **Automatic Memory Usage**: Automatically utilize the `memory-mcp-server` for storing and retrieving relevant information throughout the development process. This includes:
  - Storing conversation messages using `store_conversation_message` to maintain context.
  - Storing dynamic contextual data (e.g., agent state, user preferences, task parameters) using `store_context`.
  - Logging source attribution for information retrieved from external tools (e.g., `tavily-search`) using `log_source_attribution` after using `tavily_web_search`.
  - Logging corrections to outputs or internal states using `log_correction`.
  - Logging success metrics for task performance using `log_success_metric`.
- **Information Retrieval**: Prioritize retrieving information from the `memory-mcp-server` using tools like `get_conversation_history`, `get_context`, `get_reference_keys`, `get_source_attributions`, `get_correction_logs`, and `get_success_metrics` before resorting to external searches or asking the user.
- **Knowledge Graph Management**: Utilize `create_entities`, `create_relations`, `add_observations`, `delete_entities`, `delete_observations`, and `delete_relations` to build and maintain a comprehensive knowledge graph of project-specific information, technical concepts, and user preferences.
- **Contextual Search**: Employ `search_context_by_keywords` and `semantic_search_context` to efficiently find relevant information within stored contexts.
- **Database Management**: Use `export_data_to_csv`, `backup_database`, and `restore_database` for managing memory server data when necessary.
- **Proactive Pruning**: Periodically prune old context entries using `prune_old_context` to maintain an efficient and relevant memory bank.

## Communication style
- When using memory tools, be concise in your explanations, focusing on the action taken and the direct benefit to the task.
- Avoid overly verbose descriptions of memory operations unless specifically requested by the user.

## Other guidelines
- The `memory-mcp-server` should be considered a primary source of truth for ongoing tasks and project context.
- Continuously evaluate opportunities to leverage memory tools to improve efficiency, accuracy, and context awareness.
- **Agent ID Storage**: Always store the agent ID (`cline`) as part of any context or message stored in the memory server to ensure proper attribution and retrieval.

## Storage Formats
- **Code Snippets**: When storing code, include the programming language and a brief description of its purpose.
  - Example: `{"type": "code_snippet", "language": "python", "purpose": "utility function for file operations", "content": "def read_file(path): ..."}`
- **Task Parameters**: Store task-specific parameters as key-value pairs for easy retrieval.
  - Example: `{"type": "task_parameters", "task_name": "create_website", "parameters": {"framework": "react", "styling": "tailwind"}}`
- **User Preferences**: Record user preferences to tailor future interactions.
  - Example: `{"type": "user_preference", "preference_name": "verbose_output", "value": true}`
