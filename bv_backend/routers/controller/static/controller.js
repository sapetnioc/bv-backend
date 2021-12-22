function inputTimeout() {
    ws.send(JSON.stringify({"id": this.id, "value": this.value}))
    this.timer = undefined;
}

for (input of document.querySelectorAll("input.controller")) {
    input.addEventListener("keypress",
        function (event) {
            let input = event.target;
            if (input.timer !== undefined) {
                clearTimeout(input.timer);
            }
            input.timer = setTimeout(inputTimeout.bind(input), 3000)
        }
    );

    input.addEventListener("focusout",
        function inputFocusOut(event) {
            let input = event.target;
            if (input.timer !== undefined) {
                clearTimeout(input.timer);
                inputTimeout.call(input);
                }
        }
    );
}


for(btn of document.querySelectorAll(".collapsible > button")) {
    btn.addEventListener("click", function(event) {
      this.parentElement.classList.toggle("closed");
      event.preventDefault();
    });
  }
  