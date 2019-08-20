
function do_login(form) {
    var login = form.elements["login"].value;
    var password = form.elements["password"].value;
        
    return bv_rest('/auth/api_key', 'POST',
            data = {
                'login': login,
                'password': password,
            },
            statusCode = {
                401: (function() {do_logout(this)})
            },
            context = form)
        .done(store_api_key)
        .fail(function(error) {alert(JSON.stringify(error));});
}

function bv_rest(route, method='GET', data=null, statusCode=null) {
    var settings = {
        'method': method,
        'url': 'http://localhost:8080' + route,
        'contentType': 'application/json',
        'dataType': 'json',
        'processData': false,
    };
    if (data != null) {
        settings['data'] = JSON.stringify(data);
    }
    if (statusCode != null) {
        settings['statusCode'] = statusCode;
    }
    if (context != null) {
        settings['context'] = context;
    }
    return $.ajax(settings);
}

function store_api_key(data) {
    window.localStorage.setItem("bv_api_key", data)
    reset_login_element(this.parentElement);
}

function do_logout(form) {    
    window.localStorage.removeItem("bv_api_key")
    reset_login_element(form.parentElement);
}

function reset_login_element(login_div) {
    var api_key = window.localStorage.getItem("bv_api_key");
    
    $(login_div.children.login_form).hide();
    $(login_div.children.logout_form).hide();
    var btn = login_div.children.menu_button;
    $(btn).show();
//     var icon = btn.children[0];
    if ( api_key == null ) {
//         icon.setAttribute('style', 'color:#C06363')
//         icon.innerHTML = 'person_outline';
        btn.innerHTML = '👻';
        $(btn).one("click", function() {
            $(this).hide();
            $(this.parentElement.children.login_form).show();
        });
    } else {
//         icon.setAttribute('style', 'color:green')
//         icon.innerHTML = 'person';
        btn.innerHTML = '😀';
        $(btn).one("click", function() {
            $(this).hide();
            $(this.parentElement.children.logout_form).show();
        });
    }
}

function init_login_element() {
    $(this.children.login_form.children.cancel).click(function () {
        reset_login_element(this.parentElement.parentElement);
    });
    $(this.children.login_form).on('submit', function () {
        do_login(this);
        return false;
    });
    $(this.children.logout_form.children.cancel).click(function () {
        reset_login_element(this.parentElement.parentElement);
    });
    $(this.children.logout_form).on('submit', function () {
        do_logout(this);
        return false;
    });
    reset_login_element(this);
}

function set_document_login_element() {
    $("#login").each(init_login_element);
}

$(set_document_login_element)
