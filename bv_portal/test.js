function show_login_form() {
    var content = $(this).parent();
        
    content.html(`<form onsubmit="do_login(this); return false;">
    <div class="form-group">
    <label for="login"><b>Username</b></label>
    <input type="text" placeholder="Enter Username" name="login" required>
    </div>
    <div class="form-group">
    <label for="password"><b>Password</b></label>
    <input type="password" placeholder="Enter Password" name="password" required>
    </div>
    <button type="submit" name="ok"><i class="material-icons" style="color:green">check</i></button>
    <button type="submit" name="cancel"><i class="material-icons" style="color:red">cancel</i></button>
</form>`);
        content.find("[name=\"cancel\"]").click(function () {$(this).parent().parent().each(reset_login_element)});        
}

function show_logout_form() {
    var content = $(this).parent();
        
    content.html(`<form onsubmit="do_logout(this); return false;">
    <label>Logout ?</label>
    <button type="submit" name="ok"><i class="material-icons" style="color:green">check</i></button>
    <button type="submit" name="cancel"><i class="material-icons" style="color:red">cancel</i></button>
</form>`);
        content.find("[name=\"cancel\"]").click(function () {$(this).parent().parent().each(reset_login_element)});        
}

function do_login(form) {
    var login = form.elements["login"].value;
    var password = form.elements["password"].value;
    
    window.localStorage.setItem("bv_api_key", login)
    $(form).parent().each(reset_login_element);
}


function do_logout(form) {    
    window.localStorage.removeItem("bv_api_key")
    $(form).parent().each(reset_login_element);
}

function reset_login_element() {
    var api_key = window.localStorage.getItem("bv_api_key");

    if ( api_key == null ) {
        $(this).html('<button><i class="material-icons" style="color:#C06363">person_outline</i></button>');
        $(this).find("button").one("click", show_login_form);
    } else {
        $(this).html('<button><i class="material-icons" style="color:green">person</i></button>');
        $(this).find("button").one("click", show_logout_form);
    }
}

function set_login_elements() {
    $("#login").each(reset_login_element);
}

$(set_login_elements)
