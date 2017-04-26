var urls;
var is_authenticated;
get_cookie = function(k, default_) {
    var cookie = document.cookie.split(';');
    for (var i = 0; i < cookie.length; i++) {
        var tmp = cookie[i].trim().split('=');
        if (k === tmp[0]) {
            return tmp[1];
        }
    }
    return default_;
};
get = function(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.addEventListener('load', function() {
        if (xhr.status === 200) {
            callback(JSON.parse(this.responseText));
        }
    });
    xhr.open('GET', url, true);
    xhr.send();
};
post = function(url, form, cs, ce) {
    var xhr = new XMLHttpRequest();
    xhr.addEventListener('load', function() {
        if (xhr.status === 200) {
            if (this.responseText) {
                cs(JSON.parse(this.responseText));
            } else {
                cs();
            }
        } else if (ce) {
            ce(xhr.status);
        }
    });
    xhr.open('POST', url, true);
    xhr.send(new FormData(form));
};
delete_ = function(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.addEventListener('load', function() {
        if (xhr.status === 204) {
            callback();
        }
    });
    xhr.open('DELETE', url, true);
    xhr.setRequestHeader('X-CSRFToken', get_cookie('csrftoken'));
    xhr.send();
};
list_element_pattern = `<a href="{{ url }}">{{ name }}</a>
<a data-id="{{ id }}" class="delete">delete</a>`;

document.addEventListener('DOMContentLoaded', function() {
    var login_form = document.getElementById('login_form');

    var upload_form = document.getElementById('upload_form');
    upload_form.show_hide = function(total) {
        if (total >= 5) {
            upload_form.classList.add('dn');
        } else {
            upload_form.classList.remove('dn');
        }
    };

    var list = document.getElementById('list');
    list.refresh = function(data) {
        list.innerHTML = '';

        for (var i = 0; i < data.length; i++) {
            var div = document.createElement('div');
            div.innerHTML = list_element_pattern.
                replace('{{ url }}', data[i]['url']).
                replace('{{ name }}', data[i]['name']).
                replace('{{ id }}', data[i]['id']);

            div.getElementsByClassName('delete')[0].addEventListener('click', function() {
                var element = this;

                delete_(urls['file'].replace(0, element.getAttribute('data-id')), function() {
                    list.removeChild(element.parentElement);
                    list.total -= 1;
                    upload_form.show_hide(list.total);
                });
            });

            list.appendChild(div);
        }

        list.total = data.length;
        upload_form.show_hide(list.total);
    };

    login_form.addEventListener('submit', function(e) {
        post(window.location.href, login_form, function() {
            location.reload();
        }, function(status_code) {
            if (status_code === 400) {
                alert('Неправильный пароль.');
            } else if (status_code === 404 && confirm('register?')) {
                login_form.children[5].value = 1;
                post(window.location.href, login_form, function() {
                    location.reload();
                });
            }
        });
        e.preventDefault();
    });

    upload_form.addEventListener('submit', function(e) {
        post(urls['files'], upload_form, function(data) {
            if (data) {
                var text = [];
                for (var i = 0; i < data.length; i++) {
                    text.push(data[i][0] + ', ' + data[i][1]);
                }
                alert(text.join('\n'));
            }

            get(urls['files'], list.refresh);
        });
        e.preventDefault();
    });

    if (is_authenticated) {
        list.classList.remove('dn');
        get(urls['files'], list.refresh);
    } else {
        login_form.classList.remove('dn');
    }
});
