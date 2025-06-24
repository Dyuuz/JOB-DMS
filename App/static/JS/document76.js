function deleteDoc(id) {
        const csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        const docdelete = document.querySelector(`.doc-name[data-id='${id}']`);
        alert(docdelete.value);

}

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const docGrid = document.querySelector('.doc-grid');
    const docCategories = document.querySelectorAll('.doc-category');
    const docModal = document.getElementById('docModal');
    const closeModalBtn = document.querySelector('.doc-close-modal');
    const uploadForm = document.getElementById('docUploadForm');
    const fileInput = document.getElementById('docFileInput');
    const docNameInput = document.getElementById('docName');
    const docTypeSelect = document.getElementById('docType');

    // Get all existing document cards from the HTML
    const initialDocCards = Array.from(document.querySelectorAll('.doc-card'));

    // Extract document data from existing HTML cards
    const documents = initialDocCards.map(card => {
        return {
            element: card,
            type: card.querySelector('.doc-icon i').className.includes('file-pdf') ?
                  (card.querySelector('.Resume')?.getAttribute('data-type') === 'Resume' ? 'resume' :
                   card.querySelector('.CV')?.getAttribute('data-type') === 'CV' ? 'CV' :
                   card.querySelector('.Certification')?.getAttribute('data-type') === 'Certification' ? 'certificate' : 'other') :
                  card.querySelector('.doc-icon i').className.includes('file-word') ? 'cover-letter' :
                  card.querySelector('.doc-icon i').className.includes('file-certificate') ? 'certificate' :
                  card.querySelector('.doc-icon i').className.includes('file-image') ? 'portfolio' : 'other',
            name: card.querySelector('.doc-name').textContent,
            uploaded: card.querySelector('.doc-meta div:first-child').textContent.replace('Uploaded: ', ''),
            size: card.querySelector('.doc-meta div:last-child').textContent.replace('Size: ', '')
        };
    });

    // Filter documents by type
    function filterDocuments(type) {
        docGrid.innerHTML = '';

        if (type === 'All Documents') {
            // Show all documents
            documents.forEach(doc => {
                docGrid.appendChild(doc.element);
            });
        } else {
            // Filter by type
            const filteredDocs = documents.filter(doc => {
                if (type === 'Resumes') return doc.type === 'resume';
                if (type === 'Cover Letters') return doc.type === 'CV';
                if (type === 'Certificates') return doc.type === 'certificate';
                if (type === 'Pdfs') return doc.type === 'pdf';
                if (type === 'Text Files') return doc.type === 'reference';
                // if (type === 'Portfolio') return doc.type === 'portfolio';
                // if (type === 'References') return doc.type === 'reference';
                return true;
            });

            if (filteredDocs.length === 0) {
                showEmptyState();
            } else {
                filteredDocs.forEach(doc => {
                    docGrid.appendChild(doc.element);
                });
            }
        }
    }

    // Show empty state
    function showEmptyState() {
        docGrid.innerHTML = `
            <div class="doc-empty-state">
                <div class="doc-empty-icon">
                    <i class="fas fa-folder-open"></i>
                </div>
                <h3>No Documents Found</h3>
                <p class="doc-empty-text">No documents match the selected filter</p>
            </div>
        `;
    }

    // Category filtering
    docCategories.forEach(category => {
        category.addEventListener('click', function() {
            docCategories.forEach(c => c.classList.remove('active'));
            this.classList.add('active');
            filterDocuments(this.textContent);
        });
    });

    // Modal functions (defined globally for onclick attributes in HTML)
    window.docOpenModal = function() {
        docModal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    };

    window.docCloseModal = function() {
        docModal.style.display = 'none';
        document.body.style.overflow = 'auto';
    };

    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === docModal) {
            docCloseModal();
        }
    });

    // File input change handler
    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            const fileName = e.target.files[0].name;
            docNameInput.value = fileName.split('.')[0];

            // Auto-detect document type based on file name
            if (fileName.toLowerCase().includes('m')) {
                docTypeSelect.value = 'm';
            } else if (fileName.toLowerCase().includes('cover')) {
                docTypeSelect.value = 'cover-letter';
            } else if (fileName.toLowerCase().includes('certif') || fileName.toLowerCase().includes('diploma')) {
                docTypeSelect.value = 'certificate';
            } else if (fileName.toLowerCase().includes('portfolio')) {
                docTypeSelect.value = 'portfolio';
            }
        }
    });

    // Form submission
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();

        if (!fileInput.files.length) {
            alert('Please select a file to upload.');
            return;
        }

        const file = fileInput.files[0];
        const fileName = docNameInput.value || file.name.split('.')[0];
        const fileType = docTypeSelect.value;
        const fileSize = (file.size / (1024 * 1024)).toFixed(1) + ' MB';
        const uploadDate = new Date().toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        });

        // Determine icon based on file type
        let iconClass;
        if (file.type.includes('pdf')) {
            iconClass = 'fas fa-file-pdf';
        } else if (file.type.includes('word') || file.type.includes('document')) {
            iconClass = 'fas fa-file-word';
        } else if (file.type.includes('image')) {
            iconClass = 'fas fa-file-image';
        } else {
            iconClass = 'fas fa-file-alt';
        }

        // Create new document card
        const newDocCard = document.createElement('div');
        newDocCard.className = 'doc-card';
        newDocCard.innerHTML = `
            <div class="doc-icon">
                <i class="${iconClass}"></i>
            </div>
            <h3 class="doc-name">${fileName}.${file.name.split('.').pop()}</h3>
            <div class="doc-meta">
                <div>Uploaded: ${uploadDate}</div>
                <div>Size: ${fileSize}</div>
            </div>
            <div class="doc-actions">
                <button class="doc-action-btn doc-view" title="View">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="doc-action-btn doc-download" title="Download">
                    <i class="fas fa-download"></i>
                </button>
                <button class="doc-action-btn doc-delete" title="Delete">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;

        // Add to documents array
        documents.push({
            element: newDocCard,
            type: fileType,
            name: `${fileName}.${file.name.split('.').pop()}`,
            uploaded: uploadDate,
            size: fileSize
        });

        // Add to DOM
        docGrid.appendChild(newDocCard);

        // Add event listeners to new card's action buttons
        addCardEventListeners(newDocCard);

        // Reset form and close modal
        uploadForm.reset();
        docCloseModal();

        // Show success message
        alert('Document uploaded successfully!');
    });

    // Add event listeners to all document cards
    function addCardEventListeners(card) {
        card.querySelector('.doc-view').addEventListener('click', function() {
            const docName = card.querySelector('.doc-name').textContent;
            alert(`Viewing document: ${docName}`);
        });

        card.querySelector('.doc-download').addEventListener('click', function() {
            const docName = card.querySelector('.doc-name').textContent;
            alert(`Initiating download for: ${docName}`);
        });

        card.querySelector('.doc-delete').addEventListener('click', function() {
            if (confirm('Are you sure you want to delete this document?')) {
                // Remove from documents array
                const docIndex = documents.findIndex(doc => doc.element === card);
                if (docIndex !== -1) {
                    documents.splice(docIndex, 1);
                }

                // Remove from DOM
                card.remove();

                // Check if we need to show empty state
                const activeFilter = document.querySelector('.doc-category.active').textContent;
                if (documents.filter(doc => {
                    if (activeFilter === 'All Documents') return true;
                    if (activeFilter === 'Resumes') return doc.type === 'resume';
                    if (activeFilter === 'Cover Letters') return doc.type === 'cover-letter';
                    if (activeFilter === 'Certificates') return doc.type === 'certificate';
                    if (activeFilter === 'Portfolio') return doc.type === 'portfolio';
                    if (activeFilter === 'References') return doc.type === 'reference';
                    return true;
                }).length === 0) {
                    showEmptyState();
                }
            }
        });
    }

    // Initialize event listeners for existing cards
    initialDocCards.forEach(card => {
        addCardEventListeners(card);
    });
});
