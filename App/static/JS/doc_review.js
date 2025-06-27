// Document Viewer Functionality
document.addEventListener('DOMContentLoaded', function() {
    const docName = window.userData.doc_name;
    const docType = window.userData.doc_type;
    const docUrl = window.userData.doc_url;
    alert(`Document Name: ${docName}, Type: ${docType}, URL: ${docUrl}`);
    // DOM Elements
    const pdfViewer = document.getElementById('pdf-viewer');
    const docxViewer = document.getElementById('docx-viewer');
    const textViewer = document.getElementById('text-viewer');
    const unsupportedMessage = document.getElementById('unsupported-message');
    const pageControls = document.getElementById('page-controls');

    // Sample document data (in a real app, this would come from your backend)
    const documents = {
        [docName]: {
            name: docName,
            type: docType,
            url: 'http://res.cloudinary.com/djk1yzglo/raw/upload/v1750747802/uezyruormluiv8ezkykh.docx',
        },
    };

    // Function to load a document
    function loadDocument(docName) {
        const doc = documents[docName];
        if (!doc) return;

        // Hide all viewers first
        pdfViewer.style.display = 'none';
        docxViewer.style.display = 'none';
        textViewer.style.display = 'none';
        unsupportedMessage.style.display = 'none';
        pageControls.style.display = 'none';

        // Load appropriate viewer
        if (doc.type === 'pdf') {
            // PDF viewer using browser's built-in PDF viewer
            pdfViewer.style.display = 'block';
            pdfViewer.src = doc.url;
            //pageControls.style.display = 'flex';
        }
        else if (doc.type === 'docx' || doc.type === 'doc') {
            // DOCX viewer using Microsoft Office Online Viewer
            docxViewer.style.display = 'block';
            docxViewer.src = doc.url;
        }
        else if (doc.type === 'txt') {
            // Plain text viewer
            textViewer.style.display = 'block';
            textViewer.textContent = doc.file.url;
        }
        else {
            // Unsupported file type
            unsupportedMessage.style.display = 'block';
        }


    }

    // Initialize with first document
    loadDocument([docName]);

    // Zoom functionality
    let zoomLevel = 100;
    const zoomLevelDisplay = document.getElementById('zoom-level');

    document.getElementById('zoom-in-btn').addEventListener('click', function() {
        if (zoomLevel < 200) {
            zoomLevel += 10;
            zoomLevelDisplay.textContent = `${zoomLevel}%`;
            pdfViewer.style.zoom = `${zoomLevel}%`;
        }
    });

    document.getElementById('zoom-out-btn').addEventListener('click', function() {
        if (zoomLevel > 50) {
            zoomLevel -= 10;
            zoomLevelDisplay.textContent = `${zoomLevel}%`;
            pdfViewer.style.zoom = `${zoomLevel}%`;
        }
    });

    // Page navigation (for PDF)
    let currentPage = 1;
    const totalPages = 12;
    const pageInfo = document.getElementById('page-info');

    function updatePageInfo() {
        pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
    }

    document.getElementById('prev-page-control-btn').addEventListener('click', function() {
        if (currentPage > 1) {
            currentPage--;
            updatePageInfo();
            // In a real app, you would navigate to the previous page in the PDF
        }
    });

    document.getElementById('next-page-control-btn').addEventListener('click', function() {
        if (currentPage < totalPages) {
            currentPage++;
            updatePageInfo();
            // In a real app, you would navigate to the next page in the PDF
        }
    });

    document.getElementById('first-page-btn').addEventListener('click', function() {
        currentPage = 1;
        updatePageInfo();
    });

    document.getElementById('last-page-btn').addEventListener('click', function() {
        currentPage = totalPages;
        updatePageInfo();
    });

    // Fullscreen functionality
    const fullscreenBtn = document.getElementById('fullscreen-btn');
    fullscreenBtn.addEventListener('click', function() {
        const container = document.querySelector('.document-content-container');

        if (!document.fullscreenElement) {
            container.requestFullscreen().catch(err => {
                console.error(`Error attempting to enable fullscreen: ${err.message}`);
            });
            this.innerHTML = '<i class="fas fa-compress"></i>';
            this.title = 'Exit Fullscreen';
        } else {
            document.exitFullscreen();
            this.innerHTML = '<i class="fas fa-expand"></i>';
            this.title = 'Fullscreen';
        }
    });

    // Print functionality
    document.getElementById('print-btn').addEventListener('click', function() {
        window.print();
    });

    // Share functionality (simplified)
    document.getElementById('share-btn').addEventListener('click', function() {
        alert('Share functionality would be implemented here\nIn a real app, this would use the Web Share API');
    });
});
