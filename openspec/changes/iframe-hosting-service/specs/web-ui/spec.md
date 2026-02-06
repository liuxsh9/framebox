## ADDED Requirements

### Requirement: Display project list
The web UI SHALL display a list of all projects with key metadata.

#### Scenario: Show project list
- **WHEN** user opens the web UI
- **THEN** system displays all projects with name, ID, created date, and file count

#### Scenario: Empty state
- **WHEN** no projects exist
- **THEN** system displays empty state message with guidance to create first project

### Requirement: Create project via UI
The web UI SHALL provide a form to create new projects.

#### Scenario: Create project form
- **WHEN** user clicks "Create Project" button
- **THEN** system displays modal/form with name and entry file fields

#### Scenario: Submit project creation
- **WHEN** user fills form and submits
- **THEN** system calls POST /api/projects and adds new project to list

#### Scenario: Show creation error
- **WHEN** project creation fails (e.g., duplicate name)
- **THEN** system displays error message to user

### Requirement: Upload files via UI
The web UI SHALL support file uploads through drag-drop and file picker.

#### Scenario: Drag-drop file upload
- **WHEN** user drags files onto project card
- **THEN** system uploads files to that project via POST /api/projects/{id}/files

#### Scenario: File picker upload
- **WHEN** user clicks "Upload Files" and selects files
- **THEN** system uploads selected files to project

#### Scenario: Show upload progress
- **WHEN** files are being uploaded
- **THEN** system displays progress indicator

#### Scenario: Show upload completion
- **WHEN** upload completes successfully
- **THEN** system displays success message and updates file list

### Requirement: Delete project via UI
The web UI SHALL allow users to delete projects with confirmation.

#### Scenario: Delete button
- **WHEN** user clicks delete button on project
- **THEN** system shows confirmation dialog

#### Scenario: Confirm deletion
- **WHEN** user confirms deletion
- **THEN** system calls DELETE /api/projects/{id} and removes project from list

#### Scenario: Cancel deletion
- **WHEN** user cancels deletion
- **THEN** system closes dialog without deleting project

### Requirement: Copy embed code
The web UI SHALL provide one-click copying of iframe embed code.

#### Scenario: Show embed code
- **WHEN** user clicks "Embed" button on project
- **THEN** system displays iframe code with project URL

#### Scenario: Copy to clipboard
- **WHEN** user clicks "Copy" button
- **THEN** system copies embed code to clipboard and shows confirmation

#### Scenario: Embed code format
- **WHEN** displaying embed code
- **THEN** code includes both ID and name-based URLs as options

### Requirement: Search and filter projects
The web UI SHALL allow users to search projects by name.

#### Scenario: Search projects
- **WHEN** user types in search box
- **THEN** system filters project list to show only matching names

#### Scenario: Clear search
- **WHEN** user clears search box
- **THEN** system shows all projects again

### Requirement: Preview project in iframe
The web UI SHALL provide in-page preview of project content.

#### Scenario: Show preview
- **WHEN** user clicks "Preview" button on project
- **THEN** system displays project in embedded iframe within UI

#### Scenario: Close preview
- **WHEN** user closes preview
- **THEN** system removes iframe and returns to project list

### Requirement: Display file list for project
The web UI SHALL show all files belonging to each project.

#### Scenario: Expand file list
- **WHEN** user clicks on project card
- **THEN** system expands card to show all files with sizes and upload dates

#### Scenario: Collapse file list
- **WHEN** user clicks on expanded project
- **THEN** system collapses the file list

### Requirement: Responsive layout
The web UI SHALL be usable on desktop and tablet screen sizes.

#### Scenario: Desktop layout
- **WHEN** viewed on desktop (>1024px width)
- **THEN** system displays multi-column grid of projects

#### Scenario: Tablet layout
- **WHEN** viewed on tablet (768px-1024px width)
- **THEN** system displays single or two-column layout with readable text
