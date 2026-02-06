## ADDED Requirements

### Requirement: Create project
The system SHALL allow users to create a new HTML project with a unique name.

#### Scenario: Successful project creation
- **WHEN** user submits POST /api/projects with a unique name
- **THEN** system creates a new project with generated ID and returns project details

#### Scenario: Duplicate name rejection
- **WHEN** user submits POST /api/projects with an existing name
- **THEN** system returns 409 Conflict error

#### Scenario: Invalid name rejection
- **WHEN** user submits POST /api/projects with empty or invalid name
- **THEN** system returns 400 Bad Request error

### Requirement: List projects
The system SHALL allow users to retrieve a list of all projects with optional filtering.

#### Scenario: List all projects
- **WHEN** user requests GET /api/projects without parameters
- **THEN** system returns array of all projects with metadata

#### Scenario: Search projects by name
- **WHEN** user requests GET /api/projects?search=chart
- **THEN** system returns projects whose names contain "chart"

#### Scenario: Limit results
- **WHEN** user requests GET /api/projects?limit=10
- **THEN** system returns at most 10 projects

### Requirement: Get project by identifier
The system SHALL allow users to retrieve a specific project by ID or name.

#### Scenario: Get project by ID
- **WHEN** user requests GET /api/projects/k3x9p2
- **THEN** system returns the project with ID "k3x9p2"

#### Scenario: Get project by name
- **WHEN** user requests GET /api/projects/my-chart
- **THEN** system returns the project with name "my-chart"

#### Scenario: Project not found
- **WHEN** user requests GET /api/projects/nonexistent
- **THEN** system returns 404 Not Found error

### Requirement: Update project metadata
The system SHALL allow users to update project name and entry file.

#### Scenario: Update project name
- **WHEN** user submits PUT /api/projects/k3x9p2 with new name
- **THEN** system updates the project name and returns updated project

#### Scenario: Update entry file
- **WHEN** user submits PUT /api/projects/k3x9p2 with new entry_file
- **THEN** system updates the entry file and returns updated project

#### Scenario: Update to duplicate name
- **WHEN** user submits PUT /api/projects/k3x9p2 with name of another project
- **THEN** system returns 409 Conflict error

### Requirement: Delete project
The system SHALL allow users to delete a project and all its files.

#### Scenario: Successful deletion
- **WHEN** user requests DELETE /api/projects/k3x9p2
- **THEN** system deletes the project, all associated files, and returns 204 No Content

#### Scenario: Delete nonexistent project
- **WHEN** user requests DELETE /api/projects/nonexistent
- **THEN** system returns 404 Not Found error

### Requirement: Generate unique project IDs
The system SHALL generate short, unique, URL-safe identifiers for new projects.

#### Scenario: ID generation
- **WHEN** system creates a new project
- **THEN** system generates a 6-character ID using nanoid with URL-safe characters

#### Scenario: ID collision handling
- **WHEN** generated ID collides with existing ID
- **THEN** system regenerates until unique ID is found
