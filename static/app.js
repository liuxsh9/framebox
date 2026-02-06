// API base URL
const API_BASE = window.location.origin;

// State
let projects = [];
let currentUploadProject = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    loadProjects();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    document.getElementById('createBtn').addEventListener('click', openCreateModal);
    document.getElementById('createForm').addEventListener('submit', handleCreateProject);
    document.getElementById('searchInput').addEventListener('input', handleSearch);

    // Modal close on background click
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        });
    });

    // File input
    document.getElementById('fileInput').addEventListener('change', handleFileSelect);
}

// API Functions
async function loadProjects() {
    showLoading(true);
    try {
        const response = await fetch(`${API_BASE}/api/projects`);
        if (!response.ok) throw new Error('Failed to load projects');

        const data = await response.json();
        projects = data.projects;
        renderProjects(projects);
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

async function createProject(formData) {
    const response = await fetch(`${API_BASE}/api/projects`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to create project');
    }

    return await response.json();
}

async function deleteProject(projectId) {
    const response = await fetch(`${API_BASE}/api/projects/${projectId}`, {
        method: 'DELETE'
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to delete project');
    }
}

async function uploadFiles(projectId, files) {
    const formData = new FormData();
    Array.from(files).forEach(file => {
        formData.append('files', file);
    });

    const response = await fetch(`${API_BASE}/api/projects/${projectId}/files`, {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to upload files');
    }

    return await response.json();
}

async function loadProjectFiles(projectId) {
    const response = await fetch(`${API_BASE}/api/projects/${projectId}/files`);
    if (!response.ok) throw new Error('Failed to load files');
    return await response.json();
}

// UI Functions
function renderProjects(projectList) {
    const container = document.getElementById('projectList');
    const emptyState = document.getElementById('emptyState');

    if (projectList.length === 0) {
        container.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }

    container.style.display = 'grid';
    emptyState.style.display = 'none';

    container.innerHTML = projectList.map(project => `
        <div class="project-card" data-id="${project.id}">
            <div class="project-card-header">
                <div>
                    <h3>${escapeHtml(project.name)}</h3>
                    <div class="project-id">ID: ${project.id}</div>
                </div>
            </div>
            <div class="project-meta">
                Created: ${formatDate(project.created_at)}<br>
                Entry: ${escapeHtml(project.entry_file)}
            </div>
            <div class="project-actions">
                <button class="btn btn-primary btn-small" onclick="openUploadDialog('${project.id}')">
                    Upload
                </button>
                <button class="btn btn-secondary btn-small" onclick="showPreview('${project.id}', '${escapeHtml(project.name)}')">
                    Preview
                </button>
                <button class="btn btn-secondary btn-small" onclick="showEmbedCode('${project.id}', '${escapeHtml(project.name)}')">
                    Embed
                </button>
                <button class="btn btn-danger btn-small" onclick="confirmDelete('${project.id}', '${escapeHtml(project.name)}')">
                    Delete
                </button>
            </div>
        </div>
    `).join('');
}

function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} active`;

    setTimeout(() => {
        toast.classList.remove('active');
    }, 3000);
}

// Modal Functions
function openCreateModal() {
    document.getElementById('createModal').classList.add('active');
    document.getElementById('projectName').focus();
}

function closeCreateModal() {
    document.getElementById('createModal').classList.remove('active');
    document.getElementById('createForm').reset();
}

async function handleCreateProject(e) {
    e.preventDefault();

    const formData = {
        name: document.getElementById('projectName').value,
        entry_file: document.getElementById('entryFile').value || 'index.html'
    };

    try {
        await createProject(formData);
        showToast('Project created successfully!');
        closeCreateModal();
        await loadProjects();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function confirmDelete(projectId, projectName) {
    if (!confirm(`Are you sure you want to delete project "${projectName}"? This cannot be undone.`)) {
        return;
    }

    try {
        await deleteProject(projectId);
        showToast('Project deleted successfully!');
        await loadProjects();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

// File Upload Functions
function openUploadDialog(projectId) {
    currentUploadProject = projectId;
    const fileInput = document.getElementById('fileInput');
    fileInput.click();
}

async function handleFileSelect(e) {
    const files = e.target.files;
    if (!files.length || !currentUploadProject) return;

    await uploadFilesToProject(currentUploadProject, files);
    e.target.value = ''; // Reset file input
}

async function uploadFilesToProject(projectId, files) {
    showLoading(true);
    try {
        const result = await uploadFiles(projectId, files);
        showToast(`Uploaded ${result.uploaded.length} file(s) successfully!`);
        await loadProjects();
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Drag and Drop
document.addEventListener('dragover', (e) => {
    e.preventDefault();
    const uploadZone = document.getElementById('uploadZone');
    uploadZone.style.display = 'flex';
});

document.addEventListener('dragleave', (e) => {
    if (e.target === document.getElementById('uploadZone')) {
        e.target.style.display = 'none';
    }
});

document.addEventListener('drop', async (e) => {
    e.preventDefault();
    const uploadZone = document.getElementById('uploadZone');
    uploadZone.style.display = 'none';

    // Find which project card the files were dropped on
    const projectCard = e.target.closest('.project-card');
    if (!projectCard) {
        showToast('Please drop files on a project card', 'error');
        return;
    }

    const projectId = projectCard.dataset.id;
    const files = Array.from(e.dataTransfer.files);

    if (files.length > 0) {
        await uploadFilesToProject(projectId, files);
    }
});

// Search
function handleSearch(e) {
    const query = e.target.value.toLowerCase();
    const filtered = projects.filter(p =>
        p.name.toLowerCase().includes(query) ||
        p.id.toLowerCase().includes(query)
    );
    renderProjects(filtered);
}

// Preview
function showPreview(projectId, projectName) {
    const modal = document.getElementById('previewModal');
    const frame = document.getElementById('previewFrame');
    const title = document.getElementById('previewTitle');

    title.textContent = `Preview: ${projectName}`;
    frame.src = `${API_BASE}/view/${projectId}/`;
    modal.classList.add('active');
}

function closePreview() {
    const modal = document.getElementById('previewModal');
    const frame = document.getElementById('previewFrame');
    modal.classList.remove('active');
    frame.src = '';
}

// Embed Code
async function showEmbedCode(projectId, projectName) {
    const modal = document.getElementById('embedModal');
    const code = document.getElementById('embedCode');
    const serverUrl = document.getElementById('currentServerUrl');

    // Get server info to check for suggested URL
    let embedBaseUrl = API_BASE;
    try {
        const response = await fetch(`${API_BASE}/api/server-info`);
        if (response.ok) {
            const serverInfo = await response.json();
            // If user is on localhost but server has a suggested URL, use it
            const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
            if (isLocalhost && serverInfo.suggested_url) {
                embedBaseUrl = serverInfo.suggested_url;
            }
        }
    } catch (error) {
        // Fallback to current origin if API fails
        console.warn('Failed to fetch server info:', error);
    }

    const embedHtml = `<iframe src="${embedBaseUrl}/view/${projectName}/" width="100%" height="600" frameborder="0"></iframe>`;

    code.textContent = embedHtml;
    serverUrl.textContent = embedBaseUrl;
    modal.classList.add('active');
}

function closeEmbedModal() {
    document.getElementById('embedModal').classList.remove('active');
}

async function copyEmbedCode() {
    const code = document.getElementById('embedCode').textContent;
    try {
        await navigator.clipboard.writeText(code);
        showToast('Embed code copied to clipboard!');
    } catch (error) {
        showToast('Failed to copy to clipboard', 'error');
    }
}

// Utility Functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(isoString) {
    const date = new Date(isoString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}
