/**
 * Travel Journal Hub - Frontend JavaScript
 * Uses fetch API to communicate with Flask backend
 */

const API_BASE_URL = '/api';
let currentEditId = null;

// DOM Elements
const entryForm = document.getElementById('entryForm');
const entriesContainer = document.getElementById('entriesContainer');
const formTitle = document.getElementById('formTitle');
const submitBtn = document.getElementById('submitBtn');
const cancelBtn = document.getElementById('cancelBtn');
const entryModal = document.getElementById('entryModal');
const modalBody = document.getElementById('modalBody');

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    loadEntries();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    entryForm.addEventListener('submit', handleFormSubmit);
    cancelBtn.addEventListener('click', resetForm);
    
    // Modal close button
    const closeBtn = document.querySelector('.close');
    closeBtn.addEventListener('click', closeModal);
    
    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === entryModal) {
            closeModal();
        }
    });
}

// Load all entries from the backend
async function loadEntries() {
    try {
        const response = await fetch(`${API_BASE_URL}/entries`);
        
        if (!response.ok) {
            throw new Error('Failed to load entries');
        }
        
        const data = await response.json();
        displayEntries(data.entries);
    } catch (error) {
        console.error('Error loading entries:', error);
        entriesContainer.innerHTML = '<p class="error">Failed to load entries. Please try again later.</p>';
    }
}

// Display entries in the grid
function displayEntries(entries) {
    if (entries.length === 0) {
        entriesContainer.innerHTML = '<p class="no-entries">No travel entries yet. Start documenting your adventures!</p>';
        return;
    }
    
    entriesContainer.innerHTML = entries.map(entry => `
        <div class="entry-card" data-id="${entry.id}">
            ${entry.image_url ? `<img src="${entry.image_url}" alt="${entry.title}" class="entry-image">` : ''}
            <div class="entry-content">
                <h3>${escapeHtml(entry.title)}</h3>
                <p class="entry-location">📍 ${escapeHtml(entry.location)}</p>
                <p class="entry-date">📅 ${formatDate(entry.travel_date)}</p>
                <p class="entry-excerpt">${truncateText(escapeHtml(entry.content), 150)}</p>
                <div class="entry-actions">
                    <button class="btn btn-small btn-view" onclick="viewEntry(${entry.id})">View</button>
                    <button class="btn btn-small btn-edit" onclick="editEntry(${entry.id})">Edit</button>
                    <button class="btn btn-small btn-delete" onclick="deleteEntry(${entry.id})">Delete</button>
                </div>
            </div>
        </div>
    `).join('');
}

// Handle form submission (create or update)
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const formData = {
        title: document.getElementById('title').value,
        location: document.getElementById('location').value,
        travel_date: document.getElementById('travel_date').value,
        content: document.getElementById('content').value,
        image_url: document.getElementById('image_url').value
    };
    
    try {
        let response;
        
        if (currentEditId) {
            // Update existing entry
            response = await fetch(`${API_BASE_URL}/entries/${currentEditId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
        } else {
            // Create new entry
            response = await fetch(`${API_BASE_URL}/entries`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
        }
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to save entry');
        }
        
        // Success - reload entries and reset form
        await loadEntries();
        resetForm();
        showNotification(currentEditId ? 'Entry updated successfully!' : 'Entry created successfully!');
    } catch (error) {
        console.error('Error saving entry:', error);
        showNotification('Error: ' + error.message, 'error');
    }
}

// View entry in modal
async function viewEntry(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/entries/${id}`);
        
        if (!response.ok) {
            throw new Error('Failed to load entry');
        }
        
        const entry = await response.json();
        
        modalBody.innerHTML = `
            ${entry.image_url ? `<img src="${entry.image_url}" alt="${entry.title}" class="modal-image">` : ''}
            <h2>${escapeHtml(entry.title)}</h2>
            <p class="modal-location">📍 ${escapeHtml(entry.location)}</p>
            <p class="modal-date">📅 ${formatDate(entry.travel_date)}</p>
            <div class="modal-content-text">${escapeHtml(entry.content).replace(/\n/g, '<br>')}</div>
            <p class="modal-timestamp">Created: ${formatDateTime(entry.created_at)}</p>
            ${entry.updated_at !== entry.created_at ? `<p class="modal-timestamp">Updated: ${formatDateTime(entry.updated_at)}</p>` : ''}
        `;
        
        entryModal.style.display = 'block';
    } catch (error) {
        console.error('Error loading entry:', error);
        showNotification('Failed to load entry details', 'error');
    }
}

// Edit entry
async function editEntry(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/entries/${id}`);
        
        if (!response.ok) {
            throw new Error('Failed to load entry');
        }
        
        const entry = await response.json();
        
        // Populate form with entry data
        document.getElementById('title').value = entry.title;
        document.getElementById('location').value = entry.location;
        document.getElementById('travel_date').value = entry.travel_date;
        document.getElementById('content').value = entry.content;
        document.getElementById('image_url').value = entry.image_url || '';
        
        currentEditId = id;
        formTitle.textContent = 'Edit Entry';
        submitBtn.textContent = 'Update Entry';
        cancelBtn.style.display = 'inline-block';
        
        // Scroll to form
        document.getElementById('formSection').scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        console.error('Error loading entry for edit:', error);
        showNotification('Failed to load entry for editing', 'error');
    }
}

// Delete entry
async function deleteEntry(id) {
    if (!confirm('Are you sure you want to delete this entry? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/entries/${id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete entry');
        }
        
        await loadEntries();
        showNotification('Entry deleted successfully!');
    } catch (error) {
        console.error('Error deleting entry:', error);
        showNotification('Failed to delete entry', 'error');
    }
}

// Reset form to initial state
function resetForm() {
    entryForm.reset();
    currentEditId = null;
    formTitle.textContent = 'Add New Entry';
    submitBtn.textContent = 'Add Entry';
    cancelBtn.style.display = 'none';
}

// Close modal
function closeModal() {
    entryModal.style.display = 'none';
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength) + '...';
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
}

function formatDateTime(dateTimeString) {
    const date = new Date(dateTimeString);
    return date.toLocaleString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function showNotification(message, type = 'success') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Show notification
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Hide and remove notification after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}
