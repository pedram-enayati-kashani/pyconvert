jQuery(document).ready(function($){
    AskDelete(".Delete-Form");

    getInfoModel();
});

function AskDelete(form) {
    $(form).on('submit', function (e) {
        e.preventDefault();
        let result = confirm('آیا مطمئن هستید؟');
        if (result) {
            this.submit();
        }
    });
}

function getInfoModel(){
    const configEl = document.getElementById('editor-config');
    if (configEl) {
        const model = configEl.getAttribute('data-model');
        const oid = configEl.getAttribute('data-id');
        const address = configEl.getAttribute('data-url');
        setTimeout(() => {
            reInitializeCKEditor(model, oid,address);
        }, 500);
    }
}

async function reInitializeCKEditor(modelName, objectId,dynamicUrl) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const uploadUrl = dynamicUrl;
    const container = document.querySelector('.django_ckeditor_5');
    if (container && window.ClassicEditor) {
        const existingEditor = container.nextSibling;
        if (existingEditor && existingEditor.classList && existingEditor.classList.contains('ck-editor')) {
            existingEditor.remove();
        }
        container.style.display = 'block';
        window.ClassicEditor.create(container, {
            licenseKey: 'GPL',
            simpleUpload: {
                uploadUrl: uploadUrl,
                headers: {
                    'X-CSRFToken': csrftoken,
                    'X-Model-Name': modelName,
                    'X-Object-Id': objectId
                }
            },

            language: {
                ui: 'fa',
                content: 'fa'
            },

            toolbar: {
                items: [
                    'heading', '|',
                    'alignment', '|',
                    'bold', 'italic', 'link', 'bulletedList', 'numberedList', '|',
                    'imageUpload', '|',
                    'fontColor', 'fontBackgroundColor', '|',
                    'insertTable', '|',
                    'sourceEditing', '|',
                    'undo', 'redo', 'removeFormat'
                ]
            },

            alignment: {
                options: [ 'left', 'center', 'right', 'justify' ]
            },

            image: {
                toolbar: [
                    'imageTextAlternative', '|',
                    'imageStyle:alignLeft', 'imageStyle:full', 'imageStyle:alignRight'
                ]
            },

            link: {
                addTargetToExternalLinks: true,

                decorators: {

                    // ✅ nofollow دستی
                    addNofollow: {
                        mode: 'manual',
                        label: 'Nofollow',
                        attributes: {
                            rel: 'nofollow'
                        }
                    },

                    // ✅ sponsored دستی
                    addSponsored: {
                        mode: 'manual',
                        label: 'Sponsored',
                        attributes: {
                            rel: 'sponsored'
                        }
                    },

                    // ✅ noopener + noreferrer خودکار برای لینک خارجی
                    externalLink: {
                        mode: 'automatic',
                        callback: url => /^(https?:)?\/\//.test(url),
                        attributes: {
                            target: '_blank',
                            rel: 'noopener noreferrer'
                        }
                    }

                }
            },

            fontColor: {
                colors: [
                    { color: '#000000', label: 'Black' },
                    { color: '#FF0000', label: 'Red' },
                    { color: '#0000FF', label: 'Blue' },
                    { color: '#008000', label: 'Green' },
                    { color: '#FFFF00', label: 'Yellow' }
                ]
            },

            table: {
                contentToolbar: [
                    'tableColumn', 'tableRow', 'mergeTableCells',
                    'tableProperties', 'tableCellProperties'
                ]
            }
        })
        .then(editor => {
            console.log("CKEditor 5 initialized successfully!");
            const wordCountApi = editor.plugins.get('WordCount');
            wordCountApi.on('update', (evt, stats) => {
                const wordCountDiv = document.querySelector('.word-count');
                if (wordCountDiv) {
                    wordCountDiv.innerHTML = `تعداد لغات: ${stats.words} | تعداد حروف: ${stats.characters}`;
                }
            });
            const extraCounter = document.querySelector('.ck-word-count');
            if (extraCounter) {
                extraCounter.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Initialization error:', error);
        });
    }
}