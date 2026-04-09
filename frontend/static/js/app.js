// ===== API Configuration =====
const API_BASE = window.location.origin;

// ===== State =====
let currentUserId = null;

// ===== Utility Functions =====
function showLoading(text = "Processing...") {
    document.getElementById('loading-text').textContent = text;
    document.getElementById('loading-overlay').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading-overlay').classList.add('hidden');
}

function showMessage(elementId, message, type = 'success') {
    const el = document.getElementById(elementId);
    el.textContent = message;
    el.className = `message ${type}`;
    el.classList.remove('hidden');
    setTimeout(() => el.classList.add('hidden'), 5000);
}

async function apiRequest(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        },
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    const response = await fetch(`${API_BASE}${endpoint}`, options);

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Request failed' }));
        throw new Error(error.detail || 'Request failed');
    }

    // Handle 204 No Content
    if (response.status === 204) {
        return null;
    }

    return response.json();
}

// ===== Dynamic Form Builders =====

// Skills
let skillCount = 0;

function addSkill(name = '', level = '', category = 'Technical') {
    skillCount++;
    const container = document.getElementById('skills-container');
    const skillDiv = document.createElement('div');
    skillDiv.className = 'dynamic-item';
    skillDiv.id = `skill-${skillCount}`;
    skillDiv.innerHTML = `
        <div class="dynamic-item-header">
            <span class="dynamic-item-title">Skill #${skillCount}</span>
            <button type="button" class="btn-remove" onclick="removeSkill(${skillCount})">&times;</button>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label>Skill Name *</label>
                <input type="text" class="skill-name" placeholder="e.g., Python" value="${name}">
            </div>
            <div class="form-group">
                <label>Level</label>
                <select class="skill-level">
                    <option value="">Select level</option>
                    <option value="Beginner" ${level === 'Beginner' ? 'selected' : ''}>Beginner</option>
                    <option value="Intermediate" ${level === 'Intermediate' ? 'selected' : ''}>Intermediate</option>
                    <option value="Advanced" ${level === 'Advanced' ? 'selected' : ''}>Advanced</option>
                    <option value="Expert" ${level === 'Expert' ? 'selected' : ''}>Expert</option>
                </select>
            </div>
        </div>
        <div class="form-group">
            <label>Category</label>
            <select class="skill-category">
                <option value="Technical" ${category === 'Technical' ? 'selected' : ''}>Technical</option>
                <option value="Soft Skills" ${category === 'Soft Skills' ? 'selected' : ''}>Soft Skills</option>
                <option value="Languages" ${category === 'Languages' ? 'selected' : ''}>Languages</option>
                <option value="Tools" ${category === 'Tools' ? 'selected' : ''}>Tools</option>
                <option value="Other" ${category === 'Other' ? 'selected' : ''}>Other</option>
            </select>
        </div>
    `;
    container.appendChild(skillDiv);
}

function removeSkill(id) {
    const el = document.getElementById(`skill-${id}`);
    if (el) el.remove();
}

function getSkills() {
    const skills = [];
    document.querySelectorAll('#skills-container .dynamic-item').forEach(item => {
        const name = item.querySelector('.skill-name').value.trim();
        if (name) {
            skills.push({
                name,
                level: item.querySelector('.skill-level').value || null,
                category: item.querySelector('.skill-category').value || null,
            });
        }
    });
    return skills;
}

// Experience
let expCount = 0;

function addExperience(data = {}) {
    expCount++;
    const container = document.getElementById('experience-container');
    const expDiv = document.createElement('div');
    expDiv.className = 'dynamic-item';
    expDiv.id = `experience-${expCount}`;
    expDiv.innerHTML = `
        <div class="dynamic-item-header">
            <span class="dynamic-item-title">Experience #${expCount}</span>
            <button type="button" class="btn-remove" onclick="removeExperience(${expCount})">&times;</button>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label>Company *</label>
                <input type="text" class="exp-company" placeholder="e.g., Google" value="${data.company || ''}">
            </div>
            <div class="form-group">
                <label>Position *</label>
                <input type="text" class="exp-position" placeholder="e.g., Software Engineer" value="${data.position || ''}">
            </div>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label>Start Date</label>
                <input type="text" class="exp-start" placeholder="e.g., Jan 2020" value="${data.start_date || ''}">
            </div>
            <div class="form-group">
                <label>End Date</label>
                <input type="text" class="exp-end" placeholder="e.g., Present" value="${data.end_date || ''}">
            </div>
        </div>
        <div class="form-group">
            <label>Location</label>
            <input type="text" class="exp-location" placeholder="e.g., Mountain View, CA" value="${data.location || ''}">
        </div>
        <div class="form-group">
            <label>Description</label>
            <textarea class="exp-description" rows="3" placeholder="Describe your responsibilities...">${data.description || ''}</textarea>
        </div>
        <div class="form-group">
            <label>Achievements (one per line)</label>
            <textarea class="exp-achievements" rows="3" placeholder="• Increased performance by 40%&#10;• Led team of 5 developers">${data.achievements || ''}</textarea>
        </div>
    `;
    container.appendChild(expDiv);
}

function removeExperience(id) {
    const el = document.getElementById(`experience-${id}`);
    if (el) el.remove();
}

function getExperience() {
    const experiences = [];
    document.querySelectorAll('#experience-container .dynamic-item').forEach(item => {
        const company = item.querySelector('.exp-company').value.trim();
        const position = item.querySelector('.exp-position').value.trim();
        if (company && position) {
            experiences.push({
                company,
                position,
                start_date: item.querySelector('.exp-start').value.trim() || null,
                end_date: item.querySelector('.exp-end').value.trim() || null,
                location: item.querySelector('.exp-location').value.trim() || null,
                description: item.querySelector('.exp-description').value.trim() || null,
                achievements: item.querySelector('.exp-achievements').value.trim() || null,
            });
        }
    });
    return experiences;
}

// Education
let eduCount = 0;

function addEducation(data = {}) {
    eduCount++;
    const container = document.getElementById('education-container');
    const eduDiv = document.createElement('div');
    eduDiv.className = 'dynamic-item';
    eduDiv.id = `education-${eduCount}`;
    eduDiv.innerHTML = `
        <div class="dynamic-item-header">
            <span class="dynamic-item-title">Education #${eduCount}</span>
            <button type="button" class="btn-remove" onclick="removeEducation(${eduCount})">&times;</button>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label>Institution *</label>
                <input type="text" class="edu-institution" placeholder="e.g., MIT" value="${data.institution || ''}">
            </div>
            <div class="form-group">
                <label>Degree *</label>
                <input type="text" class="edu-degree" placeholder="e.g., Bachelor of Science" value="${data.degree || ''}">
            </div>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label>Field of Study</label>
                <input type="text" class="edu-field" placeholder="e.g., Computer Science" value="${data.field_of_study || ''}">
            </div>
            <div class="form-group">
                <label>Graduation Date</label>
                <input type="text" class="edu-date" placeholder="e.g., May 2019" value="${data.graduation_date || ''}">
            </div>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label>GPA</label>
                <input type="text" class="edu-gpa" placeholder="e.g., 3.8/4.0" value="${data.gpa || ''}">
            </div>
            <div class="form-group">
                <label>Honors</label>
                <input type="text" class="edu-honors" placeholder="e.g., Magna Cum Laude" value="${data.honors || ''}">
            </div>
        </div>
    `;
    container.appendChild(eduDiv);
}

function removeEducation(id) {
    const el = document.getElementById(`education-${id}`);
    if (el) el.remove();
}

function getEducation() {
    const educations = [];
    document.querySelectorAll('#education-container .dynamic-item').forEach(item => {
        const institution = item.querySelector('.edu-institution').value.trim();
        const degree = item.querySelector('.edu-degree').value.trim();
        if (institution && degree) {
            educations.push({
                institution,
                degree,
                field_of_study: item.querySelector('.edu-field').value.trim() || null,
                graduation_date: item.querySelector('.edu-date').value.trim() || null,
                gpa: item.querySelector('.edu-gpa').value.trim() || null,
                honors: item.querySelector('.edu-honors').value.trim() || null,
            });
        }
    });
    return educations;
}

// ===== User Profile Form =====
document.getElementById('user-profile-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = {
        first_name: document.getElementById('first_name').value.trim(),
        last_name: document.getElementById('last_name').value.trim(),
        email: document.getElementById('email').value.trim(),
        phone: document.getElementById('phone').value.trim() || null,
        location: document.getElementById('location').value.trim() || null,
        professional_title: document.getElementById('professional_title').value.trim() || null,
        linkedin: document.getElementById('linkedin').value.trim() || null,
        github: document.getElementById('github').value.trim() || null,
        portfolio: document.getElementById('portfolio').value.trim() || null,
        summary: document.getElementById('summary').value.trim() || null,
    };

    try {
        showLoading('Saving profile...');

        let result;
        if (currentUserId) {
            result = await apiRequest(`/users/${currentUserId}`, 'PUT', formData);
        } else {
            result = await apiRequest('/users/', 'POST', formData);
            currentUserId = result.id;
            localStorage.setItem('resume_builder_user_id', currentUserId);
        }

        hideLoading();
        showMessage('user-profile-message', 'Profile saved successfully!', 'success');
    } catch (error) {
        hideLoading();
        showMessage('user-profile-message', `Error: ${error.message}`, 'error');
    }
});

// ===== Resume Generation =====
async function generateResume() {
    if (!currentUserId) {
        showMessage('resume-message', 'Please save your profile first!', 'error');
        return;
    }

    const skills = getSkills();
    const experience = getExperience();
    const education = getEducation();

    if (skills.length === 0 && experience.length === 0 && education.length === 0) {
        showMessage('resume-message', 'Please add at least one skill, experience, or education entry!', 'error');
        return;
    }

    const payload = {
        user_id: currentUserId,
        title: document.getElementById('resume_title').value.trim() || null,
        summary: document.getElementById('summary').value.trim() || null,
        skills,
        experience,
        education,
        job_description: document.getElementById('job_description').value.trim() || null,
    };

    try {
        showLoading('AI is polishing your resume...');
        const result = await apiRequest('/resumes/generate', 'POST', payload);
        hideLoading();

        // Show download link
        document.getElementById('download-link').href = result.pdf_url;
        document.getElementById('resume-result').classList.remove('hidden');
        showMessage('resume-message', result.message, 'success');

        // Load history
        loadResumeHistory();
    } catch (error) {
        hideLoading();
        showMessage('resume-message', `Error: ${error.message}`, 'error');
    }
}

// ===== Resume Optimization =====
async function optimizeResume() {
    if (!currentUserId) {
        showMessage('resume-message', 'Please save your profile first!', 'error');
        return;
    }

    const jobDescription = document.getElementById('job_description').value.trim();
    if (!jobDescription) {
        showMessage('resume-message', 'Please paste a job description to optimize against!', 'error');
        return;
    }

    const payload = {
        user_id: currentUserId,
        job_description: jobDescription,
    };

    try {
        showLoading('AI is optimizing your resume for the job...');
        const result = await apiRequest('/resumes/optimize', 'POST', payload);
        hideLoading();

        // Show download link
        document.getElementById('download-link').href = result.pdf_url;
        document.getElementById('resume-result').classList.remove('hidden');
        showMessage('resume-message', `Optimized! Keyword match score: ${result.keyword_match_score}%`, 'success');

        loadResumeHistory();
    } catch (error) {
        hideLoading();
        showMessage('resume-message', `Error: ${error.message}`, 'error');
    }
}

// ===== Resume History =====
async function loadResumeHistory() {
    if (!currentUserId) return;

    try {
        const history = await apiRequest(`/resumes/history/${currentUserId}`);

        if (history && history.length > 0) {
            const section = document.getElementById('resume-history-section');
            const list = document.getElementById('history-list');
            list.innerHTML = '';

            history.forEach(item => {
                const div = document.createElement('div');
                div.className = 'history-item';
                const date = new Date(item.created_at).toLocaleString();
                div.innerHTML = `
                    <div class="history-item-info">
                        <h4>${item.title || 'Untitled Resume'}</h4>
                        <p>${date}</p>
                    </div>
                    <div class="history-item-actions">
                        <a href="${item.pdf_url}" class="btn btn-success btn-sm" download>Download</a>
                    </div>
                `;
                list.appendChild(div);
            });

            section.classList.remove('hidden');
        }
    } catch (error) {
        console.error('Failed to load history:', error);
    }
}

// ===== Show optimize button when job description is entered =====
document.getElementById('job_description').addEventListener('input', (e) => {
    const optimizeBtn = document.getElementById('optimize-btn');
    if (e.target.value.trim().length > 50) {
        optimizeBtn.style.display = 'inline-block';
    } else {
        optimizeBtn.style.display = 'none';
    }
});

// ===== Initialize on Page Load =====
document.addEventListener('DOMContentLoaded', () => {
    // Load saved user ID
    const savedUserId = localStorage.getItem('resume_builder_user_id');
    if (savedUserId) {
        currentUserId = parseInt(savedUserId);
        // Optionally load user profile data
    }

    // Add one empty entry for each section to get started
    addSkill();
    addExperience();
    addEducation();
});
