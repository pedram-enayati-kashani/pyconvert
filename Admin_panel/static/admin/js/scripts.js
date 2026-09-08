jQuery(document).ready(function($){

    changeTypeInput('#eyeSolid','#eyeSlash','#choseTypeInput','#id_password');
    checkIsStaffField();
    AskDelete(".Delete-Form");

    $('#id_field_type').on('change', toggleOptionsDiv);
    toggleOptionsDiv();

    addFromField();

    getInfoModel();

    galleryVali();

    addGallery();

    initMenuTargetAutoFill({
        endpoint: "/admin/module/menu-builder/json/resolve-menu-target/",
    });

    setup_slug_generator();

    initVideoPlayers();
    initAudioPlayers();

    mediaKeyCopy();
});

function changeTypeInput(iconActive,iconInactive,containerIcon,element){
    let active = $(iconActive);
    let inactive = $(iconInactive);
    let container = $(containerIcon);
    let input = $(element)

    container.click(function(){
        if ($(this).hasClass('active') && input.attr('type') === 'text'){
            $(this).removeClass('active');
            active.show();
            inactive.hide();
            $(element).attr('type', 'password');
        } else {
            $(this).addClass('active')
            active.hide();
            inactive.show();
            $(element).attr('type', 'text');
        }
    })
}

function checkIsStaffField(){
    if ($("#id_is_staff").is(":checked")) {
        $("#GroupField").show();
    } else {
        $("#GroupField").hide();
    }

    $("#id_is_staff").on("change", function () {
        if ($(this).is(":checked")) {
            $("#GroupField").show();
        } else {
            $("#GroupField").hide();
        }
    });
}

function AskDelete(form) {
    $(form).on('submit', function (e) {
        e.preventDefault();
        let result = confirm('آیا مطمئن هستید؟');
        if (result) {
            this.submit();
        }
    });
}

function toggleOptionsDiv() {
    const selectedValue = $('#id_field_type').val();
    const optionsDiv = $('#option');
    const showDivValues = ['checkbox', 'select', 'radio'];

    if (showDivValues.includes(selectedValue)) {
        optionsDiv.show();
    } else {
        optionsDiv.hide();
    }
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
async function reInitializeCKEditor(modelName, objectId, dynamicUrl) {
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
                    addNofollow: {
                        mode: 'manual',
                        label: 'Nofollow',
                        attributes: {
                            rel: 'nofollow'
                        }
                    },
                    addSponsored: {
                        mode: 'manual',
                        label: 'Sponsored',
                        attributes: {
                            rel: 'sponsored'
                        }
                    },
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

function addFromField(){
    $('#form-selector').change(function() {
        let formId = $(this).val();
        let urlTemplate = $(this).attr('data-url');

        if (formId && urlTemplate) {
            let finalUrl = urlTemplate.replace('0', formId);
            $.get(finalUrl, function(data) {
                $('#dynamic-fields-container').html(data.html);
            })
            .fail(function() {
                console.error("خطا در بارگذاری فیلدها");
            });
        } else {
            $('#dynamic-fields-container').empty();
        }
    });
}

function galleryVali(){
    $('#gallery-wrapper').on('change', 'input[type="file"]', function() {
        const file = this.files[0];
        const $input = $(this);

        if (!file) return;

        const maxSize = parseInt($input.data('max-size')) || 10 * 1024 * 1024;
        if (file.size > maxSize) {
            alert(`حجم فایل "${file.name}" بیشتر از ۱۰ مگابایت است.`);
            $input.val('');
            return;
        }

        if (!file.type.startsWith('image/')) {
            alert(`فایل "${file.name}" یک تصویر معتبر نیست.`);
            $input.val('');
            return;
        }
    });
}

function addGallery(){
    $('#add-gallery-item').on('click', function() {
        const totalForms = $('#id_gallery_items-TOTAL_FORMS');
        const container = $('#gallery-wrapper');
        const emptyFormHtml = $('#empty-form').html();

        const formNum = parseInt(totalForms.val());
        const newFormHtml = emptyFormHtml.replace(/__prefix__/g, formNum);
        container.append(newFormHtml);
        totalForms.val(formNum + 1);
    });
    $('#gallery-wrapper').on('click', '.remove-form-row', function() {
        $(this).closest('.gallery-row').remove();
    });
}
function initMenuTargetAutoFill(options = {}) {
    const $config = $("#config_info");
    const endpoint = ($config.attr("data-url") || "").trim();

    if (!endpoint) return;

    const settings = {
        targetSelector: "#id_address_list",
        urlSelector: "#id_url",
        onlyIfUrlEmpty: false,
        clearUrlWhenEmptyTarget: true,
        ...options,
        endpoint, // باید آخر باشد تا override نشود
    };

    const $target = $(settings.targetSelector);
    const $url = $(settings.urlSelector);

    if (!$target.length || !$url.length) return;

    async function fetchAndFill() {
        const target = String($target.val() || "").trim();

        if (!target) {
            if (settings.clearUrlWhenEmptyTarget) $url.val("");
            return;
        }

        if (settings.onlyIfUrlEmpty && String($url.val() || "").trim()) {
            return;
        }

        const requestUrl = new URL(settings.endpoint, window.location.origin);
        requestUrl.searchParams.set("address-list", target);

        try {
            const response = await fetch(requestUrl, {
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    Accept: "application/json",
                },
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            $url.val(data.ok && data.url ? data.url : "");

        } catch (error) {
            console.error("resolve-menu-target error:", error);
            $url.val("");
        }
    }

    // جلوگیری از ثبت چندباره event در صورت اجرای مجدد اسکریپت
    $target
        .off("change.menuTargetAutoFill")
        .on("change.menuTargetAutoFill", fetchAndFill);
}


function setup_slug_generator() {
    const $config = $('#slug-config');
    if (!$config.length) return;
    const modelKey = $config.data('model-key');
    const instanceId = $config.data('instance');
    const url = $config.data('url');

    let timeout = null;

    $(document).off('input.sluggen', '#id_title');

    $(document).on('input.sluggen', '#id_title', function () {
        const $titleInput = $(this);
        const $slugInput = $('#id_slug');

        if ($slugInput.prop('disabled') || $slugInput.prop('readonly')) return;

        const text = ($titleInput.val() || '').trim();

        clearTimeout(timeout);
        timeout = setTimeout(function () {
            if (!text) {
                $slugInput.val('');
                return;
            }

            // برای دیباگ
            console.log('sending slug request:', { text, modelKey, instanceId });

            $.ajax({
                url: url,
                method: "GET",
                data: {
                    text: text,
                    model_key: modelKey,
                    instance_id: instanceId
                },
                success: function (res) {
                    if (res && res.ok) {
                        $slugInput.val(res.slug);
                    }
                },
                error: function (xhr) {
                    console.error('slug ajax error:', xhr.status, xhr.responseText);
                }
            });

        }, 400);
    });
}


function initVideoPlayers() {
    $('.js-video-player').each(function() {
        let $video = $(this);

        if ($video.hasClass('vjs-initialized') || $video.parent().hasClass('video-js')) {
            return;
        }

        let playerId = $video.attr('id');
        if (!playerId) {
            playerId = 'vjs-player-' + Math.random().toString(36).substr(2, 9);
            $video.attr('id', playerId);
        }

        videojs(playerId, {
            responsive: true,
            fluid: true,
            aspectRatio: '16:9',
            playbackRates: [0.5, 1, 1.5, 2],
            controlBar: {
                skipButtons: {
                    forward: 10,
                    backward: 10
                }
            }
        });

        $video.addClass('vjs-initialized');
    });
}

function initAudioPlayers() {
    $('.js-audio-player').each(function () {
        if (this.classList.contains('vjs-tech')) {
            return;
        }

        const audioPlayer = videojs(this, {
            controls: true,
            autoplay: false,
            preload: 'auto',
            fluid: false,
            controlBar: {
                pictureInPictureToggle: false,
                chaptersButton: false,
                descriptionsButton: false,
                subsCapsButton: false,
                audioTrackButton: false
            }
        });

        audioPlayer.on('play', function() {
            console.log('پخش صدا شروع شد');
        });
    });
}

function mediaKeyCopy() {
    $(document)
        .off("click.mediaKeyCopy", ".mediaPage .mediaKey")
        .on("click.mediaKeyCopy", ".mediaPage .mediaKey", async function () {
            const mediaKey = $(this).text().trim();
            const valueToCopy = `[${mediaKey}]`;

            if (!mediaKey) {
                showMediaCopyMessage(
                    "error",
                    "کلید رسانه معتبر نیست."
                );
                return;
            }

            try {
                await copyToClipboard(valueToCopy);

                showMediaCopyMessage(
                    "success",
                    `${valueToCopy} با موفقیت کپی شد.`
                );
            } catch (error) {
                console.error("Clipboard error:", error);

                showMediaCopyMessage(
                    "error",
                    "کپی‌کردن کلید رسانه انجام نشد."
                );
            }
        });
}

async function copyToClipboard(value) {
    // Clipboard API فقط در HTTPS یا localhost در دسترس است.
    if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(value);
        return;
    }

    // روش جایگزین برای HTTP و بعضی مرورگرهای قدیمی
    const textarea = document.createElement("textarea");

    textarea.value = value;
    textarea.setAttribute("readonly", "");
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    textarea.style.pointerEvents = "none";

    document.body.appendChild(textarea);

    textarea.select();
    textarea.setSelectionRange(0, textarea.value.length);

    const copied = document.execCommand("copy");

    textarea.remove();

    if (!copied) {
        throw new Error("Copy command failed");
    }
}

function showMediaCopyMessage(type, message) {
    const $container = $(".errorMedia");
    const $successAlert = $container.find(".alert.success");
    const $errorAlert = $container.find(".alert.error");

    $successAlert.addClass("d-none");
    $errorAlert.addClass("d-none");

    const $selectedAlert =
        type === "success" ? $successAlert : $errorAlert;

    $selectedAlert
        .find(".message")
        .text(message);

    $selectedAlert.removeClass("d-none");

    clearTimeout(window.mediaCopyMessageTimer);

    window.mediaCopyMessageTimer = setTimeout(function () {
        $selectedAlert.addClass("d-none");
    }, 3000);
}
