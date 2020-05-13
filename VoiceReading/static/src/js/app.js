
$( document ).ready(function() {

});

var voice_info = [];
var current_recording = 0;

var text_panel = $('.text-panel');
var main_text = $('.main_text');

var isFirefox = typeof InstallTrigger !== 'undefined';

text_panel.click(function () {
    $('#main_text').focus();
});

main_text.on('keyup', function (e) {
    add_controls();
});

function add_controls() {
    if (main_text.text().trim() === '') {
        text_panel.children('.side-controls').remove();
        return;
    }

    // for first sentence
    if (!isFirefox && $('.side-controls[data-index=0]').length <= 0) {
        var side_controls = $($('.control-template').html()).clone();
        side_controls.attr('data-index', 0);
        text_panel.append(side_controls);
    }

    // for next sentences
    var sentence_panel = main_text.children('div');
    var n_sentence = sentence_panel.length;
    for (var i=0; i<n_sentence; i++) {
        if ($(sentence_panel[i]).text().trim() === '')
            continue;

        var idx = i;
        if (!isFirefox)
            idx = idx + 1;

        if ($('.side-controls[data-index=' + idx + ']').length <= 0) {
            side_controls = $($('.control-template').html()).clone();
            side_controls.attr('data-index', idx).css('top', ($(sentence_panel[i]).position().top + 8) + 'px');
            text_panel.append(side_controls);
        }
    }

    // remove remain controls
    var n_controls = $('.text-panel').children('.side-controls').last().data('index') + 1;
    if (!isFirefox)
        n_sentence++;

    if (n_controls > n_sentence) {
        for (var j=n_sentence; j<=n_controls; j++) {
            $('.side-controls[data-index=' + j + ']').remove();
        }
    }
}

//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;
var gumStream;
//stream from getUserMedia()
var rec;
//Recorder.js object
var input;
//MediaStreamAudioSourceNode we'll be recording
// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext = new AudioContext;

var btn_record = $('.btn-record');
var voice_name = $('#voice_name');

btn_record.click(function () {
    if (voice_name.val().trim() === '') {
        alert('Please enter voice name.');
        return;
    }
    if ($(this).data('recording') === 'false' || $(this).data('recording') === false) {
        $(this).data('recording', 'true');
        $(this).children('img').attr('src', '/static/dist/img/recording.png');

        btn_record.addClass('disabled');
        $(this).removeClass('disabled');

        startRecording();
    } else {
        $(this).data('recording', 'false');
        $(this).children('img').attr('src', '/static/dist/img/mic.png');
        btn_record.removeClass('disabled');

        stopRecording(parseInt($(this).data('index')));
    }
});

function startRecording() {
    var constraints = {
        audio: true,
        video: false
    };

    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        /* assign to gumStream for later use */
        gumStream = stream;
        /* use the stream */
        input = audioContext.createMediaStreamSource(stream);
        /* Create the Recorder object and configure to record mono sound (1 channel) Recording 2 channels will double the file size */
        rec = new Recorder(input, {
            numChannels: 1
        });
        //start the recording process
        rec.record();
    }).catch(function(err) {
    });
}

function stopRecording(idx) {
    //tell the recorder to stop the recording
    rec.stop(); //stop microphone access
    gumStream.getAudioTracks()[0].stop();
    //create the wav blob and pass it on to createDownloadLink
    current_recording = idx;
    rec.exportWAV(upload_record);
}

function upload_record(data) {
    var form = document.form_create;
    form.record1.value = current_recording;
    if (current_recording === 1)
        form.record1.value = current_recording;
    if (current_recording === 2)
        form.record2.value = current_recording;
    if (current_recording === 3)
        form.record3.value = current_recording;

    var xhr = new XMLHttpRequest();
    xhr.onload = function(e) {
        if (this.readyState === 4) {
            console.log("Server returned: ", e.target.responseText);
        }
    };
    var fd = new FormData();
    fd.append("audio_data", data, voice_name.val());
    fd.append("index", current_recording);
    xhr.open("POST", "/upload_record", true);
    xhr.send(fd);
}

$('#form-text').on('submit', function (e) {
    e.preventDefault();
    e.stopPropagation();

    var voice = $('#voice').val();
    if (voice === 0 || voice === "0") {
        alert('Select a voice.');
        return;
    }

    var count_content = main_text.children('div').length;
    if (!isFirefox)
        count_content++;
    var content_info = [];
    for (var i=0; i<count_content; i++) {
        var sentence_voice = voice_info[i] ? voice_info[i] : voice;
        var sentence = get_nth_sentence(i);

        content_info.push({
            voice: sentence_voice,
            sentence: sentence
        });
    }

    this.sentence_data.value = JSON.stringify(content_info);
    this.submit();
});

text_panel.on('click', '.dropdown-item', function () {
    var voice_name = $(this).html();
    var sentence_index = parseInt($(this).parent().parent().data('index'));
    voice_info[sentence_index] = voice_name;
});

text_panel.on('click', '.play-sentence', function () {
    var voice = $('#voice').val();
    var sentence_index = parseInt($(this).parent().data('index'));

    var sentence_voice = voice_info[sentence_index] ? voice_info[sentence_index] : voice;
    if (sentence_voice === 0 || sentence_voice === "0") {
        alert('Select a voice.');
        return;
    }
    var sentence = get_nth_sentence(sentence_index);

    var content_info = [{
        voice: sentence_voice,
        sentence: sentence
    }];

    $.ajax({
        method: "POST",
        url: "/speech_sentence",
        data: { sentence_data: JSON.stringify(content_info) }
    }).done(function( data ) {
        var audio_obj = $('#sentence-audio');
        audio_obj.attr('src', '/' + data);
        audio_obj[0].play();
    });
});

function get_nth_sentence(n) {
    var text_content = main_text.html();
    var split_content = text_content.split('<div>');

    var sentence = main_text.children('div:nth-child(' + (n + 1) + ')').text().trim();
    if (!isFirefox) {
        if (n === 0)
            sentence = split_content[0];
        else
            sentence = main_text.children('div:nth-child(' + n + ')').text().trim();
    }

    return sentence;
}

$('#form_create').on('submit', function (e) {
    e.preventDefault();
    e.stopPropagation();

    if (this.audio1.value === ''
    && this.audio2.value === ''
    && this.audio3.value === ''
    && this.record1.value === ''
    && this.record2.value === ''
    && this.record3.value === '') {
        alert('Please select the upload file or record your voice');
        return;
    }

    this.submit();
});

text_panel.on('mouseover', '.dropdown', function () {
    text_panel.find('.dropdown').dropdown('hide');
    $(this).dropdown('show');
});