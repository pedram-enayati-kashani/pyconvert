jQuery(document).ready(function($){
    
    // search form
    searchForm();

    // navbar menu
    navbar();
    
    // comment
    $('.comments .commentCol .answerButton').click(function() {
        let $comment = $(this).closest('.commentCol');
        let $answerForm = $comment.find('.answerForm');
    
        if ($answerForm.hasClass('active')) {
            $answerForm.removeClass('active');
        } else {
            $answerForm.addClass('active');
        }
    });

    $('.answerForm .cancel').click(function(e){
        $(this).closest('.answerForm').removeClass('active');
    });

    // move button send comment form and contact
    moveButtons('#commentForm .submitComment');
    moveButtons('#contactForm #submitContact');
    successSendComment("#commentForm",'.commentForm > .successFullSend');
    successSendComment("form.subComment",".answerForm > .successFullSend");
    successSendContact("#contactForm",".commentForm .successFullSend");
    imageSlider();

    preloader();

    // related-content
    relatedContent();

    // moveTableInDiv
    moveTableInDiv();

    // swiperSliderMainPage();

    getTitleInSingleForList();

    refreshCaptcha();

    setupAjaxCSRF();

    initVideoPlayers();
    initAudioPlayers();

});

function searchForm(){
    $('#search .searchIcon').click(()=>{
        $('#search form').addClass('active');
    });

    $('#search .elementGroup').click((e)=>{
        e.stopPropagation();
    });

    $('#search form').click(()=>{
        $('#search form').removeClass('active');
    });
}

function navbar(){
    if (this.matchMedia('(max-width: 991px)').matches) {
        $('.humbergerIcon').click(() => {
            $('#headerNav').addClass('active');
        });

        $('.closeIcon span').click(() => {
            $('#headerNav').removeClass('active');
        });

        $('#headerNav div').click((e) => {
            e.stopPropagation();
        });

        $('#headerNav').click(function() {
            $(this).removeClass('active');
        });
    }

    window.addEventListener('resize',function(){
        if (this.matchMedia('(max-width: 991px)').matches) {

            if ($('#headerNav').hasClass("active")){
                $('#headerNav').removeClass("active");
            }

            if ($('.humbergerIcon').hasClass("hidden")){
                $('.humbergerIcon').removeClass("hidden");
            }

            $('.humbergerIcon').click(() => {
                $('#headerNav').addClass('active');
            });
    
            $('.closeIcon span').click(() => {
                $('#headerNav').removeClass('active');
            });
    
            $('#headerNav div').click((e) => {
                e.stopPropagation();
            });
    
            $('#headerNav').click(function() {
                $(this).removeClass('active');
            });
        }
    });
}

function sameHeight(input){
    let col = document.querySelectorAll(input);
    let heightArray = [];
    let result = '';
    let colHeight = 0;
    if (col.length > 0){
        for (let i = 0;i<col.length;i++){
            result = window.getComputedStyle(col[i]).getPropertyValue("height");
            result = result.replace('px',' ');
            result = Number(result);
            if (!isNaN(result)){
                heightArray.push(result);
            }
            else {
                heightArray.push(0);
            }
        }
        colHeight = Math.max(...heightArray);
        for (let i = 0;i<col.length;i++){
            col[i].style.minHeight =colHeight+'px';
        }
        window.addEventListener('resize',()=>{
            col = document.querySelectorAll(input);
            heightArray = [];
            result = '';
            colHeight = 0;
            for (let i = 0;i<col.length;i++){
                col[i].style.minHeight ='0px';
            }
            for (let i = 0;i<col.length;i++){
                result = window.getComputedStyle(col[i]).getPropertyValue("height");
                result = result.replace('px',' ');
                result = Number(result);
                if (!isNaN(result)){
                    heightArray.push(result);
                }
                else {
                    heightArray.push(0);
                }
            }
            colHeight = Math.max(...heightArray);
            for (let i = 0;i<col.length;i++){
                col[i].style.minHeight =colHeight+'px';
            }
        });
    }
}

function addLimitCountShowText(input,count=50) {
    const textElement = document.querySelectorAll(input);   
    if(textElement.length > 0){
        for(let i=0;i<textElement.length;i++){
            if(textElement[i].innerText.length > count){
                textElement[i].textContent =textElement[i].textContent.slice(0,count)+"...";
            }
        }
    }
};

function imageSlider(){
    if($('.imageSlider').length > 0){
        let imageSlider = new Swiper(".imageSlider", {
            loop: true,
            speed: 1500,
            spaceBetween: 20,
            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev",
            },
        });
        const galleryItems = document.querySelectorAll('.imageDetails .imageCol .item');
        galleryItems.forEach((item,index)=>{
            item.addEventListener('click', () => {
                imageSlider.slideToLoop(index);
            });
        });
    }
    
}

function relatedContent(){
    if($('.related-content').length > 0){
        let imageSlider = new Swiper(".related-content", {
            loop: true,
            speed: 1500,
            spaceBetween: 20,
            autoplay: {
                delay: 3000,
                pauseOnMouseEnter: true
            },
            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev",
            },
               breakpoints: {
                320: {
                    slidesPerView: 1.2,
                },
                479:{
                    slidesPerView: 2.2,
                },
                768: {
                    slidesPerView: 3.3,
                },
                1024: {
                    slidesPerView: 3.5,
                },
            }
        });
    }
}

function moveButtons(buttonSelector) {
    const button = document.querySelector(buttonSelector);

    if (!button) {
        return;
    }

    const form = button.closest('form');

    if (!form) {
        return;
    }

    const textarea = form.querySelector(':scope > .textarea');
    const cacheInput = form.querySelector('.colRightForm .cacheInput');
    const colRightForm = form.querySelector('.colRightForm');

    if (!textarea || !cacheInput || !colRightForm) {
        console.warn('moveButtons: target elements not found', {
            formId: form.id,
            textareaFound: Boolean(textarea),
            cacheInputFound: Boolean(cacheInput),
            colRightFormFound: Boolean(colRightForm),
        });
        return;
    }

    function moveButton() {
        const isMobile = window.matchMedia('(max-width: 991px)').matches;

        if (isMobile) {
            textarea.insertAdjacentElement('afterend', button);
        } else {
            cacheInput.insertAdjacentElement('afterend', button);
        }
    }

    moveButton();

    let resizeTimer;

    window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);

        resizeTimer = setTimeout(function () {
            moveButton();
        }, 150);
    });
}

function successSendComment(form, messageDiv){
    $(form).on("submit", function(e){
        e.preventDefault();
        let form = $(this);
        let button = form.find("button[type=submit]");
        button.prop("disabled", true);
        let div = $(messageDiv);

        $.ajax({
            type: "POST",
            url: form.attr("action"),
            data: form.serialize(),

            success: function(response){
                if(response.success){
                    form.trigger("reset");
                    div.addClass('active').text(response.message);
                    setTimeout(()=>{
                        div.removeClass('active').text('');
                    }, 5000);
                }
            },

            error: function(xhr) {
                let message = "خطایی در ارسال رخ داد";
                let hasHtmlErrors = false;

                if (xhr.responseJSON && xhr.responseJSON.errors) {
                    let errors = xhr.responseJSON.errors;

                    let listItems = Object.keys(errors).map(label => {
                        return `<li><strong>${label}:</strong> ${errors[label]}</li>`;
                    });

                    message = `<ul class="comment-error-list" style="margin: 0; padding-right: 20px; list-style-type: disc;">${listItems.join('')}</ul>`;
                    hasHtmlErrors = true;
                } else if (xhr.status === 500) {
                    message = "خطای سرور (500)";
                }
                if (hasHtmlErrors) {
                    div.addClass('error').html(message);
                } else {
                    div.addClass('error').text(message);
                }

                setTimeout(() => {
                    div.removeClass('error').html('');
                }, 8000);

                reloadCaptcha(form);
                button.prop("disabled", false);
            }
        });
    });
}


function successSendContact(formSelector, messageDiv) {
    $(document).on("submit", formSelector, function(e) {
        e.preventDefault();

        let $form = $(this);
        let button = $form.find("button[type=submit]");
        let div = $(messageDiv);

        button.prop("disabled", true);
        $form.find('small.text-danger').text('');
        div.removeClass('active').text('');

        let formData = $form.find("input, textarea, select").serialize();
        let targetUrl = $form.attr("action") || window.location.href;

        $.ajax({
            type: "POST",
            url: targetUrl,
            data: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(response) {
                if (response.status === 'success') {
                    let successMsg = response.messages && response.messages[0]
                                     ? response.messages[0].message
                                     : 'پیام شما با موفقیت ارسال شد';

                    div.addClass('active').text(successMsg);
                    $form[0].reset();

                    setTimeout(() => {
                        div.removeClass('active').text('');
                    }, 5000);
                }
                button.prop("disabled", false);
            },
            error: function(xhr) {
                let errors = xhr.responseJSON ? xhr.responseJSON.errors : null;

                if (errors) {
                    $.each(errors, function(field, messages) {
                        if (field !== '__all__') {
                            let small = $form.find('small.text-danger[data-field="' + field + '"]');
                            if (small.length > 0) {
                                // استخراج هوشمند پیام متنی خطا بدون توجه به فرمت ارسالی جنگو
                                let errorText = '';
                                if (typeof messages === 'string') {
                                    errorText = messages;
                                } else if (Array.isArray(messages)) {
                                    errorText = messages.map(function(msg) {
                                        if (typeof msg === 'string') return msg;
                                        if (msg && typeof msg === 'object') {
                                            return msg.message || JSON.stringify(msg);
                                        }
                                        return String(msg);
                                    }).join(' ');
                                } else if (messages && typeof messages === 'object') {
                                    errorText = messages.message || JSON.stringify(messages);
                                } else {
                                    errorText = String(messages);
                                }

                                small.text(errorText);
                            }
                        }
                    });
                }
                if (typeof reloadCaptcha === 'function') {
                    reloadCaptcha($form);
                }
                button.prop("disabled", false);
            }
        });
    });
}


function preloader(){
    window.addEventListener("load", function () {
        const preloader = document.getElementById("preloader");
        if (preloader) {
            setTimeout(() => {
                preloader.style.transition = 'opacity 0.5s ease';
                preloader.style.opacity = '0';
                preloader.style.display = 'none';
            }, 500);
        }
    });

    setTimeout(() => {
        const preloader = document.getElementById("preloader");
        if (preloader) {
            setTimeout(() => {
                preloader.style.transition = 'opacity 0.5s ease';
                preloader.style.opacity = '0';
                preloader.style.display = 'none';
            }, 500);
        }
    }, 3000);
}

// move table in div
function moveTableInDiv(){
    $(".singlePage .content figure.table").each(function() {
        $(this).wrap('<div class="table-wrapper"></div>');
    });
}

function swiperSliderMainPage(){
    let swiper = new Swiper("#projectSliderContent", {
        effect: "coverflow",
        slidesPerView: 3,
        loop: true,
        pauseOnMouseEnter: true,
        autoplay: {
            delay: 2500,
            disableOnInteraction: false
        },
        grabCursor: true,
        centeredSlides: true,
        coverflowEffect: {
            rotate: 50,
            stretch: 0,
            depth: 100,
            modifier: 1,
            slideShadows: true,
        },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },
            breakpoints: {
            0: {
                slidesPerView: 1,
            },
            575: {
                slidesPerView: 2,
            },
            768: {
                slidesPerView: 2,
            },
            1024: {
                slidesPerView: 3,
            },
        }
    });
}

function getTitleInSingleForList() {
    let counter = 0;
    let list = [];
    const $listContainer = $(".singlePage .singleList").hide();
    const $content = $listContainer.find(".content");

    $content.empty();

    $(".singlePage .description .content")
        .find("h2, h3, h4, h5, h6")
        .filter(function() {
            return $(this).text().trim();
        })
        .each(function() {
            const linkId = "titleLink" + counter;
            list.push(linkId);
            $(this).attr("id", linkId);
            counter++;
        });

    if (list.length > 0) {
        let html = "<ul>";

        list.forEach(linkId => {
            const text = $("#" + linkId).text().trim();
            html += `<li><a href="#${linkId}">${text}</a></li>`;
        });

        html += "</ul>";
        $content.html(html);
        $listContainer.show();
    }
}

function reloadCaptcha(formElement) {
    let url = window.location.origin + "/captcha/refresh/";
    $.getJSON(url, {}, function (json) {
        formElement.find('img.captcha').attr('src', json.image_url);
        formElement.find('input[name="captcha_0"]').val(json.key);
    });
}

function refreshCaptcha(){
    $('.js-captcha-refresh').click(function (e) {
        e.preventDefault();
        let form = $(this).parents('form');
        reloadCaptcha(form);
    });
}

function setupAjaxCSRF() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
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

function initLanguageSwitcher() {
    const $form = $("#language-form");
    const $languageInput = $("#language-input");

    if (!$form.length || !$languageInput.length) {
        console.warn("Language form or language input was not found.");
        return;
    }

    $(".language-switcher")
        .off("click.languageSwitcher")
        .on("click.languageSwitcher", function (event) {
            event.preventDefault();

            const language = $(this).attr("data-language");

            if (!language) {
                return;
            }

            console.log("Changing language to:", language);

            $languageInput.val(language);
            $form[0].submit();
        });
}
