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

const CKEDITOR_COLOR_CONFIG = [

    /* ---------- سطر ۱: سایه 50 ---------- */
    { color: '#FFEBEE', label: 'Red 50' },
    { color: '#F3E5F5', label: 'Purple 50' },
    { color: '#E8EAF6', label: 'Indigo 50' },
    { color: '#E3F2FD', label: 'Blue 50' },
    { color: '#E0F7FA', label: 'Cyan 50' },
    { color: '#E0F2F1', label: 'Teal 50' },
    { color: '#F1F8E9', label: 'Light green 50' },
    { color: '#F9FBE7', label: 'Lime 50' },
    { color: '#FFF8E1', label: 'Amber 50' },
    { color: '#FFF3E0', label: 'Orange 50' },
    { color: '#FAFAFA', label: 'Grey 50' },
    { color: '#ECEFF1', label: 'Blue grey 50' },

    /* ---------- سطر ۲: سایه 100 ---------- */
    { color: '#FFCDD2', label: 'Red 100' },
    { color: '#E1BEE7', label: 'Purple 100' },
    { color: '#C5CAE9', label: 'Indigo 100' },
    { color: '#BBDEFB', label: 'Blue 100' },
    { color: '#B2EBF2', label: 'Cyan 100' },
    { color: '#B2DFDB', label: 'Teal 100' },
    { color: '#DCEDC8', label: 'Light green 100' },
    { color: '#F0F4C3', label: 'Lime 100' },
    { color: '#FFECB3', label: 'Amber 100' },
    { color: '#FFE0B2', label: 'Orange 100' },
    { color: '#F5F5F5', label: 'Grey 100' },
    { color: '#CFD8DC', label: 'Blue grey 100' },

    /* ---------- سطر ۳: سایه 200 ---------- */
    { color: '#EF9A9A', label: 'Red 200' },
    { color: '#CE93D8', label: 'Purple 200' },
    { color: '#9FA8DA', label: 'Indigo 200' },
    { color: '#90CAF9', label: 'Blue 200' },
    { color: '#80DEEA', label: 'Cyan 200' },
    { color: '#80CBC4', label: 'Teal 200' },
    { color: '#C5E1A5', label: 'Light green 200' },
    { color: '#E6EE9C', label: 'Lime 200' },
    { color: '#FFE082', label: 'Amber 200' },
    { color: '#FFCC80', label: 'Orange 200' },
    { color: '#EEEEEE', label: 'Grey 200' },
    { color: '#B0BEC5', label: 'Blue grey 200' },

    /* ---------- سطر ۴: سایه 300 ---------- */
    { color: '#E57373', label: 'Red 300' },
    { color: '#BA68C8', label: 'Purple 300' },
    { color: '#7986CB', label: 'Indigo 300' },
    { color: '#64B5F6', label: 'Blue 300' },
    { color: '#4DD0E1', label: 'Cyan 300' },
    { color: '#4DB6AC', label: 'Teal 300' },
    { color: '#AED581', label: 'Light green 300' },
    { color: '#DCE775', label: 'Lime 300' },
    { color: '#FFD54F', label: 'Amber 300' },
    { color: '#FFB74D', label: 'Orange 300' },
    { color: '#E0E0E0', label: 'Grey 300' },
    { color: '#90A4AE', label: 'Blue grey 300' },

    /* ---------- سطر ۵: سایه 400 ---------- */
    { color: '#EF5350', label: 'Red 400' },
    { color: '#AB47BC', label: 'Purple 400' },
    { color: '#5C6BC0', label: 'Indigo 400' },
    { color: '#42A5F5', label: 'Blue 400' },
    { color: '#26C6DA', label: 'Cyan 400' },
    { color: '#26A69A', label: 'Teal 400' },
    { color: '#9CCC65', label: 'Light green 400' },
    { color: '#D4E157', label: 'Lime 400' },
    { color: '#FFCA28', label: 'Amber 400' },
    { color: '#FFA726', label: 'Orange 400' },
    { color: '#BDBDBD', label: 'Grey 400' },
    { color: '#78909C', label: 'Blue grey 400' },

    /* ---------- سطر ۶: سایه 500 ---------- */
    { color: '#F44336', label: 'Red 500' },
    { color: '#9C27B0', label: 'Purple 500' },
    { color: '#3F51B5', label: 'Indigo 500' },
    { color: '#2196F3', label: 'Blue 500' },
    { color: '#00BCD4', label: 'Cyan 500' },
    { color: '#009688', label: 'Teal 500' },
    { color: '#8BC34A', label: 'Light green 500' },
    { color: '#CDDC39', label: 'Lime 500' },
    { color: '#FFC107', label: 'Amber 500' },
    { color: '#FF9800', label: 'Orange 500' },
    { color: '#9E9E9E', label: 'Grey 500' },
    { color: '#607D8B', label: 'Blue grey 500' },

    /* ---------- سطر ۷: سایه 600 ---------- */
    { color: '#E53935', label: 'Red 600' },
    { color: '#8E24AA', label: 'Purple 600' },
    { color: '#3949AB', label: 'Indigo 600' },
    { color: '#1E88E5', label: 'Blue 600' },
    { color: '#00ACC1', label: 'Cyan 600' },
    { color: '#00897B', label: 'Teal 600' },
    { color: '#7CB342', label: 'Light green 600' },
    { color: '#C0CA33', label: 'Lime 600' },
    { color: '#FFB300', label: 'Amber 600' },
    { color: '#FB8C00', label: 'Orange 600' },
    { color: '#757575', label: 'Grey 600' },
    { color: '#546E7A', label: 'Blue grey 600' },

    /* ---------- سطر ۸: سایه 700 ---------- */
    { color: '#D32F2F', label: 'Red 700' },
    { color: '#7B1FA2', label: 'Purple 700' },
    { color: '#303F9F', label: 'Indigo 700' },
    { color: '#1976D2', label: 'Blue 700' },
    { color: '#0097A7', label: 'Cyan 700' },
    { color: '#00796B', label: 'Teal 700' },
    { color: '#689F38', label: 'Light green 700' },
    { color: '#AFB42B', label: 'Lime 700' },
    { color: '#FFA000', label: 'Amber 700' },
    { color: '#F57C00', label: 'Orange 700' },
    { color: '#616161', label: 'Grey 700' },
    { color: '#455A64', label: 'Blue grey 700' },

    /* ---------- سطر ۹: سایه 800 ---------- */
    { color: '#C62828', label: 'Red 800' },
    { color: '#6A1B9A', label: 'Purple 800' },
    { color: '#283593', label: 'Indigo 800' },
    { color: '#1565C0', label: 'Blue 800' },
    { color: '#00838F', label: 'Cyan 800' },
    { color: '#00695C', label: 'Teal 800' },
    { color: '#558B2F', label: 'Light green 800' },
    { color: '#9E9D24', label: 'Lime 800' },
    { color: '#FF8F00', label: 'Amber 800' },
    { color: '#EF6C00', label: 'Orange 800' },
    { color: '#424242', label: 'Grey 800' },
    { color: '#37474F', label: 'Blue grey 800' },

    /* ---------- سطر ۱۰: سایه 900 ---------- */
    { color: '#B71C1C', label: 'Red 900' },
    { color: '#4A148C', label: 'Purple 900' },
    { color: '#1A237E', label: 'Indigo 900' },
    { color: '#0D47A1', label: 'Blue 900' },
    { color: '#006064', label: 'Cyan 900' },
    { color: '#004D40', label: 'Teal 900' },
    { color: '#33691E', label: 'Light green 900' },
    { color: '#827717', label: 'Lime 900' },
    { color: '#FF6F00', label: 'Amber 900' },
    { color: '#E65100', label: 'Orange 900' },
    { color: '#212121', label: 'Grey 900' },
    { color: '#263238', label: 'Blue grey 900' },

    /* ---------- سطر ۱۱: رنگ‌های پایه ---------- */
    { color: '#000000', label: 'Black' },
    { color: '#FFFFFF', label: 'White' },
];

function detectEditorLanguage() {
    const segments = window.location.pathname
        .split('/')
        .filter(Boolean);
    const langSegment = segments.find(seg => seg === 'en' || seg === 'fa');
    return langSegment || 'fa';
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

        const editorLang = detectEditorLanguage();

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
                ui: editorLang,
                content: editorLang,
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
                colors: CKEDITOR_COLOR_CONFIG,
                columns: 12,
                colorPicker: {
                    format: 'hex',
                    allowAny: true,
                },
                documentColors: 12,
            },


            fontBackgroundColor: {
                colors: CKEDITOR_COLOR_CONFIG,
                columns: 12,
                colorPicker: {
                    format: 'hex',
                    allowAny: true,
                },
                documentColors: 12,
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
