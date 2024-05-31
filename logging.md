```mermaid
graph TD;
    siteLogger((siteLogger \n from get_and_parse)) -->|Logs to| mainLogger((mainLogger));
    parserLogger((parserLogger \n from create_listing)) -->|Logs to| mainLogger((mainLogger));

```