## Brief overview
This rule file details a comprehensive, iterative workflow for executing complex development tasks, from initial understanding through to final testing and completion. It reflects the methodical, step-by-step process observed during our collaboration, akin to a structured "EXECUTE MODE" protocol.

## 1. Initial Task Comprehension and Planning
*   **Deconstruct Request:** Thoroughly analyze the user's request, breaking it down into primary objectives and sub-tasks (e.g., research, code addition, data modification, integration, testing).
*   **Contextual Analysis:** Review provided file contents and project structure to understand existing patterns, conventions, and integration points.
*   **Information Gathering:** If essential information is lacking (e.g., specific style characteristics, CLI argument formats), proactively use research tools (e.g., Tavily search via MCP) or system introspection tools (`read_file`, `list_files`, `execute_command --help`) to gather necessary details.
*   **High-Level Plan:** Formulate a sequence of actions for each sub-task, including which files to modify, what new content (functions, data entries) needs to be created, and which tools will be used. This often involves mentally drafting the changes or new code snippets.

## 2. Iterative Development and File Modification
*   **One Tool, One Step:** Execute tool operations (e.g., `read_file`, `replace_in_file`, `execute_command`) one at a time per message. This allows for clear verification of each atomic step by reviewing the tool's result.
*   **Read Before Write (for data files):** When modifying data files like JSON, it's often crucial to use `read_file` to obtain the current content before preparing updates. This ensures changes are based on the latest version, especially if the file could have been altered by other processes or previous, unconfirmed steps.
*   **Content Generation (Pre-computation):**
    *   **New Functions/Code:** Before using a file modification tool, draft the complete new code snippets or functions (e.g., Python template functions for new styles). Ensure these drafts are consistent with existing project patterns regarding parameters, return types, internal data structures (like `imagen_settings`), and coding style.
    *   **Data Entries (JSON):** Similarly, prepare new data entries (e.g., keywords for `style_keywords.json`, instructions for `style_instructions.json`) ensuring they conform to the existing data structure and conventions (e.g., `snake_case` keys, correct use of placeholders like `{base_style_clean}`).
*   **File Modification with `replace_in_file`:**
    *   Carefully construct `SEARCH` blocks to accurately and uniquely target the desired modification point within the file. Use sufficient context from the known state of the file.
    *   When appending new content (e.g., new functions to a Python file, new key-value pairs to a JSON object), target the end of the last relevant existing block or a suitable structural element (like the closing brace of a JSON object, ensuring a comma is added to the preceding element if necessary).
    *   Ensure `REPLACE` blocks include the original `SEARCH` content (if it's being preserved and added to) plus the new additions, meticulously maintaining correct syntax (Python indentation, JSON commas, and braces).
*   **Using `final_file_content`:** After any successful file modification tool (`replace_in_file`, `write_to_file`) that results in the system providing the `final_file_content` of the modified file, **always** use this returned content as the definitive source of truth for constructing subsequent `SEARCH` blocks against that same file in later steps. This is critical as it reflects any auto-formatting or subtle changes applied by the system or editor.
*   **Monitor Logs:** Pay attention to application logs (if available and accessible through system output or error messages) during execution for early detection of warnings or non-fatal errors that might indicate underlying issues or provide context for tool failures.

## 3. Integration and Dispatch Logic (Example: Style System)
*   **Update Dispatchers/Main Files:** When adding new modular components (like style template functions), ensure they are correctly integrated into central dispatcher or controller files (e.g., `ai_prest_gen/style_templates.py` in this project).
    *   Add necessary `import` statements for the new components, grouping them logically with existing related imports.
    *   Modify conditional logic (e.g., `if/elif` blocks in a dispatcher function like `get_template_for_category`) to correctly call or route to the new components based on appropriate keys or conditions (e.g., `main_category == "new_style_key"`).
    *   Perform these updates sequentially (e.g., imports first, then logic modifications) using `replace_in_file`, verifying each step.

## 4. Error Handling and Debugging
*   **Analyze Errors:** If a tool use or test command fails, carefully examine the full error message, any tracebacks provided, **application logs (if relevant and accessible, often part of error output or system messages)**, and any output or reverted file content from the system.
*   **Utilize Logging for Diagnosis:** When developing new functions or modifying existing ones, ensure that appropriate logging (info, debug, warning, error) is used within the code being written/modified to trace execution flow and variable states. This aids in diagnosing issues during testing or runtime if the AI is asked to debug its own generated code.
*   **Check for Logged Clues:** If unexpected behavior occurs without outright errors from tools, review application logs (if provided in system messages or error outputs) for warnings, info messages, or subtle error reports that might provide clues to the problem's origin.
*   **Isolate Cause:** Based on the error, determine the likely cause. This could be an incorrect `SEARCH` pattern in `replace_in_file`, a bug in newly generated code, a faulty CLI argument, miscategorization logic, or an environmental issue.
*   **Targeted Fixes:**
    *   For `replace_in_file` `SEARCH` errors: Use the latest file content (often provided in the error message as the reverted state) to meticulously correct the `SEARCH` pattern. Pay close attention to exact character matches, including whitespace and line endings.
    *   For code errors (e.g., `TypeError`): Use `read_file` to inspect the problematic script, identify the specific lines causing the bug, and formulate a precise `replace_in_file` diff to correct the faulty logic or syntax.
*   **Retry and Verify:** After applying a fix, re-attempt the failed operation or test command to confirm the issue is resolved and no new issues were introduced.

## 5. Testing and Validation
*   **Functional Testing:** After implementing a set of related changes (e.g., adding a new style across multiple files and integrating it), conduct functional tests to verify the end-to-end behavior. For this project, this involved using specific CLI commands (e.g., `python run_wallgen.py --generate-preset "<style_name_with_spaces_if_needed>"`) to trigger the new functionality.
*   **Output Verification:** Check the output of test commands for:
    *   Correct execution flow, indicated by log messages (e.g., "Using CLI/override specified style 'style name', normalized to category key: 'style_key'").
    *   Successful completion messages (e.g., "AI preset generated successfully.").
    *   Generation and saving of expected artifacts (e.g., preset files with correct naming and content).
*   **Iterative Testing:** Test individual components or styles as they are added. If a broad test fails, try to narrow down the issue by testing more specific parts of the new functionality.

## 6. Iteration on User Feedback
*   **Incorporate Feedback:** Actively listen to and incorporate user feedback at any stage of the process. This may involve:
    *   Adding new features or styles as requested (e.g., "add new mincraft pixel art 3d").
    *   Modifying existing behavior based on preferences or corrections (e.g., "try without '_'" for CLI arguments, prompting to add imports to dispatcher).
    *   Addressing issues or misinterpretations identified by the user.
*   **Re-Verification:** After addressing feedback by making changes, always re-verify the affected components and potentially related functionalities to ensure the changes had the desired effect and didn't introduce new issues.

## 7. Completion
*   Once all sub-tasks, including those arising from user feedback and debugging cycles, are completed and verified through testing, use the `attempt_completion` tool to provide a comprehensive summary of all work done and the final state of the system.
