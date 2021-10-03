var locked = false;

function disable(styleChange) {
    const styles = document.querySelectorAll('.style')
    Array.from(styles).map(
        function (el) {
            el.classList.add('disabled');
            if (styleChange) el.classList.remove('active');
        }
    )
}

function enable() {
    const styles = document.querySelectorAll('.style')
    Array.from(styles).map(
        function (el) {
            el.classList.remove('disabled')
        }
    )
}

function request(url, options, callback) {
    console.log(`Starting Web request on url=${url}`);
    fetch(url, options).then(
        _ => {
            console.log('Done');
            callback(_);
        }
    );
}

function update_style(element, style, part) {
    if (locked) return
    locked = true;
    disable(true);

    request(
        url = '/style',
        options = {
            method: 'POST',
            body: JSON.stringify({style: style, part: part})
        },
        callback = _ => {
            locked = false;
            enable();
            element.classList.add('active')
        }

    );
}

function toggle_background(element) {
    if (locked) return;
    locked = true;
    disable(false);
    request(
        url = '/background',
        options = {
            method: 'POST',
            body: element.checked
        },
        callback = _ => {
            locked = false;
            enable();
        }
    )
}

function stop_app() {
    request(
        url = '/exit',
        options = {
            method: 'POST'
        },
        callback = _ => {
            close('', '_parent', '');
        }
    )
}


function update_res(select) {
    request(
        url = '/resolution',
        options = {
            method: 'POST',
            body: select.value
        },
        callback = _ => {}
    )
}

function update_bg_type(select) {
    request(
        url = '/bg_type',
        options = {
            method: 'POST',
            body: select.value
        },
        callback = _ => {}
    )
}