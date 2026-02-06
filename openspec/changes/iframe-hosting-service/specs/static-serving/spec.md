## ADDED Requirements

### Requirement: Serve entry file by project identifier
The system SHALL serve the project's entry file when accessing /view/{id_or_name}/.

#### Scenario: Serve entry file by ID
- **WHEN** user requests GET /view/k3x9p2/
- **THEN** system returns the project's entry file (default: index.html)

#### Scenario: Serve entry file by name
- **WHEN** user requests GET /view/my-chart/
- **THEN** system resolves project by name and returns entry file

#### Scenario: Custom entry file
- **WHEN** project has entry_file set to "main.html" and user requests GET /view/k3x9p2/
- **THEN** system returns main.html instead of index.html

### Requirement: Serve project files by path
The system SHALL serve any file within a project via /view/{id_or_name}/{filepath}.

#### Scenario: Serve root-level file
- **WHEN** user requests GET /view/k3x9p2/data.json
- **THEN** system returns the data.json file from project root

#### Scenario: Serve nested file
- **WHEN** user requests GET /view/k3x9p2/assets/style.css
- **THEN** system returns the file from assets/ subdirectory

#### Scenario: Serve nonexistent file
- **WHEN** user requests GET /view/k3x9p2/missing.txt
- **THEN** system returns 404 Not Found error

### Requirement: Support dual identifier resolution
The system SHALL resolve project identifiers as either ID or name in static serving routes.

#### Scenario: Resolve by ID
- **WHEN** identifier matches 6-character ID format and ID exists
- **THEN** system uses ID lookup

#### Scenario: Resolve by name
- **WHEN** identifier does not match ID format
- **THEN** system treats it as name and performs name lookup

#### Scenario: Name not found
- **WHEN** identifier is treated as name but no project exists with that name
- **THEN** system returns 404 Not Found error

### Requirement: Set CORS headers for iframe embedding
The system SHALL include permissive CORS headers on all static serving responses.

#### Scenario: CORS headers present
- **WHEN** user requests any /view/* resource
- **THEN** response includes Access-Control-Allow-Origin: * header

#### Scenario: OPTIONS preflight support
- **WHEN** browser sends OPTIONS request to /view/* endpoint
- **THEN** system responds with appropriate CORS headers

### Requirement: Serve correct content types
The system SHALL set appropriate Content-Type headers based on file extensions.

#### Scenario: HTML content type
- **WHEN** serving .html file
- **THEN** response includes Content-Type: text/html

#### Scenario: JSON content type
- **WHEN** serving .json file
- **THEN** response includes Content-Type: application/json

#### Scenario: CSS content type
- **WHEN** serving .css file
- **THEN** response includes Content-Type: text/css

#### Scenario: JavaScript content type
- **WHEN** serving .js file
- **THEN** response includes Content-Type: application/javascript

### Requirement: Handle relative path resolution
The system SHALL allow HTML files to reference project assets using relative paths.

#### Scenario: Relative path from HTML
- **WHEN** index.html contains fetch('./data.json')
- **THEN** browser resolves to /view/k3x9p2/data.json and system serves it

#### Scenario: Relative path with subdirectories
- **WHEN** index.html contains <link href="assets/style.css">
- **THEN** browser resolves to /view/k3x9p2/assets/style.css and system serves it
